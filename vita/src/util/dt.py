from datetime import datetime


class VitaDatetime(datetime):

    @classmethod
    def now(cls):
        return super().now()
