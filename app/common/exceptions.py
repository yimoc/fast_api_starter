from app.core.exception.exceptions import SodaflowResponseError
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

invalidLoginError = SodaflowResponseError(
    status_code=HTTP_400_BAD_REQUEST,
    code = "InvalidedLogin",
    message = "Invalide id and password"
)

expiredTokenError = SodaflowResponseError(
    status_code=HTTP_401_UNAUTHORIZED,
    code = "ExpiredToken",
    message = "ExpiredTokenError"
)

# login 하기전 : 인증이 필요하고 실패했거나 아직 제공되지 않은 경우에 사용합니다.
unauthorizedError = SodaflowResponseError(
    status_code=HTTP_401_UNAUTHORIZED,
    code = "Unauthorized",
    message = "unauthorized. reqeust a login"
)

# WWW-Authenticate 헤더 필드 챌린지에 응답하여 인증을 제공했지만 서버가 해당 인증을 수락하지 않은 경우
noPermissionError = SodaflowResponseError(
    status_code=HTTP_403_FORBIDDEN,
    code = "NoPermission",
    message = "Not enough permissions"
)
