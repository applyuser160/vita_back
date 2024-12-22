import strawberry


@strawberry.type
class VitaError(Exception):

    error_code: int
    message: str

    def __init__(self, error_code: int, message: str):
        self.error_code = error_code
        self.message = message
