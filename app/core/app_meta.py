from starlette.datastructures import State

from app.core.defines import EnvironmentType


class AppState(State):
    '''
    Application의 공용값들을 저장하는 클래스이다.
    '''
    def __init__(self):
        super().__init__()
        self.APP_DIR: str =''
        self.ENV_TYPE: EnvironmentType = EnvironmentType.PRODUCT
        self.config =None
        self.settings =None







