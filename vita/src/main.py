import strawberry
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from vita.src.graph_ql.mutation import Mutation
from vita.src.graph_ql.query import Query
from strawberry.fastapi import GraphQLRouter

schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=None)

graphql_app = GraphQLRouter(schema)

app = FastAPI(openapi_url=None)
app.include_router(graphql_app, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        server_header=False,
    )
