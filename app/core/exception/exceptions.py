from typing import Any, Dict, Optional, Sequence, Type

from fastapi import HTTPException

class SodaflowError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message


class SodaflowResponseError(SodaflowError, HTTPException):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        SodaflowError.__init__(
            self,
            code=code, message=message
        )
        HTTPException.__init__(
            self,
            status_code=status_code, headers=headers
        )




class SodaflowServiceError(SodaflowError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(code, message)

class SodaflowOrmError(SodaflowError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(code, message)
