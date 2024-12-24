from __future__ import annotations

from datetime import datetime
import json
import logging
from typing import Literal, Self, TypeVar
from uuid import uuid4

from pydantic import ValidationError
from sqlalchemy.engine import URL
from sqlalchemy.orm import Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from util.err import VitaError
from util.dt import VitaDatetime

from .condition import Condition, ConditionType
from .env import get
from .logg import Logg


class Base(SQLModel, table=False):  # type: ignore
    __table_args__ = {"extend_existing": True}
    id: str | None = Field(default=None, primary_key=True)
    create_date: datetime | None = Field(default=None)
    create_object_id: str | None = Field(default=None)
    update_date: datetime | None = Field(default=None)
    update_object_id: str | None = Field(default=None)
    delete_date: datetime | None = Field(default=None, nullable=True)
    delete_object_id: str | None = Field(default=None, nullable=True)

    def add_or_update(self, object_id: str):
        setattr(self, "update_date", VitaDatetime.now())
        setattr(self, "update_object_id", object_id)
        if self.create_date is None:
            setattr(self, "create_date", VitaDatetime.now())
            setattr(self, "create_object_id", object_id)
        if self.id is None:
            setattr(self, "id", str(uuid4()))

    def logical_delete(self, object_id: str):
        setattr(self, "delete_date", VitaDatetime.now())
        setattr(self, "delete_object_id", object_id)

    def copy_only_id(self):
        return Base(id=self.id)

    def copy_poperty(self: Self, copy: Self, properties: list[str]):
        for k in properties:
            v = getattr(copy, k)
            setattr(self, k, v)

    def extract_valid_value(self):
        static_property = ["_sa_instance_state"]
        return {
            k: v
            for k, v in vars(self).items()
            if v is not None and k not in static_property
        }

    def delete_property(self, properties: list[str]):
        for k in properties:
            setattr(self, k, None)

    def is_new(self):
        return self.id is None

    def is_empty(self):
        static_property = ["_sa_instance_state"]
        evv = self.extract_valid_value()
        for k in evv.keys():
            if k not in static_property:
                return False
        return True

    def validate(self):
        self.model_validate(self)


T = TypeVar("T", bound=Base)


class SQLSession:
    session: Session
    logg: Logg

    def __init__(self, logg: Logg, db_type: Literal["mysql", "sqlite"] = "mysql"):
        if db_type == "mysql":
            uri = get("MYSQL_URI")
            user = get("MYSQL_USER")
            pin = get("MYSQL_PASSWORD")
            database = get("MYSQL_DATABASE")
            url = URL.create(
                drivername="mysql+mysqldb",
                username=user,
                password=pin,
                host=uri,
                database=database,
                query={"charset": "utf8mb4", "ssl": "true"},
            )
        else:
            url = "sqlite:///:memory:"

        engine = create_engine(url=url, echo=logg.logger.level <= logging.DEBUG)
        self.session = Session(engine, autoflush=False)
        self.logg = logg

    def close(self):
        self.session.close()

    def _append_where(
        self,
        query: Query,
        model_type: type[T],
        cond: T | None,
        type: ConditionType,
    ) -> Query:
        if not cond:
            return query

        if not cond.is_empty():
            dict_cond = cond.extract_valid_value()
            for k, v in dict_cond.items():
                condition = Condition(getattr(model_type, k), type, v, False)
                query = query.where(condition.to_sqlachemy())
        return query

    def _exec_query(
        self, query: Query, model_type: type[T], isOne: bool
    ) -> list[T] | T | None:
        self.logg.info(
            "execute query.",
            {
                "query": query,
                "type": model_type.__name__,
            },
        )
        try:
            if isOne:
                result = self.session.exec(query).first()
                if result is None:
                    return None
                elif result.is_empty():
                    return None
                else:
                    return result
            else:
                result = self.session.exec(query).all()
                if len(result) == 0:
                    return []
                else:
                    return result
        except Exception as e:
            self.logg.error("execute query error", {"message": str(e)})
            return None

    def execute(
        self, query: Query, model_type: type[T], isOne: bool
    ) -> list[T] | T | None:
        self.logg.info("execute sql", {"type": model_type.__name__})
        return self._exec_query(query, model_type, isOne)

    def _find_base(
        self,
        model_type: type[T],
        cond: T | None = None,
        isOne: bool = True,
    ) -> list[T] | T | None:
        query = select(model_type)
        query = self._append_where(query, model_type, cond, ConditionType.EQUAL)
        return self._exec_query(query, model_type, isOne)

    def find(
        self,
        model_type: type[T],
        conds: dict[ConditionType, T] | None = None,
        isOne: bool = True,
    ) -> list[T] | T | None:
        self.logg.info("find sql", {"type": model_type.__name__})
        query = select(model_type)
        if conds is not None:
            for k, v in conds.items():
                query = self._append_where(query, model_type, v, k)
        return self._exec_query(query, model_type, isOne)

    def _save_base(
        self,
        model_type: type[T],
        model: T,
        object_id: str,
        isnew: bool = False,
    ) -> T | None:
        try:
            is_new = isnew if isnew else model.is_new()
            entity: T = model
            if not is_new:
                entity_from_db = self._find_base(model_type, model.copy_only_id())
                if isinstance(entity_from_db, model_type):
                    entity = entity_from_db

            entity.add_or_update(object_id)
            entity.copy_poperty(model, model.extract_valid_value().keys())
            self.session.add(entity)
            self.session.commit()
            return entity
        except Exception as e:
            self.logg.error("save sql error", {"message": str(e)})
            return None

    def save(self, model_type: type[T], model: T, object_id: str) -> T | None:
        self.logg.info("save sql", {"type": model_type.__name__})
        try:
            model.validate()
        except ValidationError as e:
            e_dicts = json.loads(e.json())
            messages: list[dict] = []
            for e_dict in e_dicts:
                message = {
                    "type": e_dict["type"],
                    "message": e_dict["msg"],
                    "location": e_dict["loc"],
                }
                messages.append(message)
                self.logg.error("validation error", message)
            raise VitaError(400, json.dumps(messages))
        return self._save_base(model_type, model, object_id)

    def bulk_save(self, models: list[T], object_id: str):
        self.logg.info("bulk save sql")
        try:
            for model in models:
                model.add_or_update(object_id)
            self.session.bulk_save_objects(models)
            self.session.commit()
        except Exception as e:
            self.logg.error("buls save sql error", {"message": str(e)})

    def _delete_base(self, model_type: type[T], model: T):
        try:
            entity = self._find_base(model_type, model.copy_only_id())
            self.session.delete(entity)
            self.session.commit()
        except Exception as e:
            self.logg.error("delete sql error", {"message": str(e)})

    def delete(self, model_type: type[T], model: T):
        self.logg.info("delete sql", {"type": model_type.__name__})
        self._delete_base(model_type, model)

    def logical_delete(self, model_type: type[T], model: T, object_id: str) -> T | None:
        self.logg.info("logical delete sql", {"type": model_type.__name__})
        model.logical_delete(object_id)
        try:
            model.validate()
        except ValidationError as e:
            e_dicts = json.loads(e.json())
            messages: list[dict] = []
            for e_dict in e_dicts:
                message = {
                    "type": e_dict["type"],
                    "message": e_dict["msg"],
                    "location": e_dict["loc"],
                }
                messages.append(message)
                self.logg.error("validation error", message)
            raise VitaError(400, json.dumps(messages))
        return self._save_base(model_type, model, object_id)
