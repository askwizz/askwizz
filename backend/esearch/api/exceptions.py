from fastapi import HTTPException, status


class NotAuthenticatedException(HTTPException):
    def __init__(self: "NotAuthenticatedException") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )


class DBNotInitializedException(HTTPException):
    def __init__(self: "DBNotInitializedException") -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database not connected",
        )
