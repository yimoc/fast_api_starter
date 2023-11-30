from strenum import StrEnum

class EnvironmentType(StrEnum):
    '''
    환경에 따른 Type
        PRODUCT
    '''
    PRODUCT = 'prod'
    TEST = 'test'
    LOCAL = 'local'
    DEV = 'dev'
