import os
import logging
import traceback

import uvicorn as uvicorn
from fastapi import FastAPI

from app.core.exception.exception_handlers import sodaflow_soda_reponse_exception_handler, \
    sodaflow_default_exception_handler, default_exception_handler
from app.core.exception.exceptions import SodaflowResponseError, SodaflowError
from app.db.init_db import init_db

from main_init import app_path
from app.api.root_router import root_router
from app.core.app_meta import AppState
from app.core.config.config import FileConfig
from app.common.env import Settings, get_env_type
from app.core.sqlalchemy.database import db_connector, create_db_and_tables

def set_state_app(app : FastAPI, settings, config):
    appState = AppState()
    app.state = appState

    # setting initialize app info
    appState.APP_DIR = os.path.dirname(os.path.realpath(__file__))
    appState.settings = settings
    #application configuration
    appState.config = config

def load_env(app_path: str):
    env_type = get_env_type()
    logger.info('| env_type : ' + env_type)
    path = os.path.join(app_path, 'app', 'conf')
    full_path = os.path.join(path, f'{env_type}.env')
    logger.info('| env file path : ' + full_path)
    settings = Settings(_env_file=full_path)
    return settings

def load_config(app_path: str):
    path = os.path.join(app_path, 'app', 'conf')
    file_config = FileConfig()
    config = file_config.load_config(path)
    return config

def create_app(settings, config) -> FastAPI:
    app = FastAPI(title=config['COMMON']['NAME'],
                  # dependencies=[Depends(my_context_dependency)]
                  )
    # db setting
    #connect_args = {"check_same_thread": False}         #sqlite 전용
    db_connector.init_app(DB_URL=settings.DATABASE_URL,DB_ECHO=False)

    # router
    app.include_router(root_router, prefix="")

    # exception handler
    app.add_exception_handler(SodaflowResponseError, sodaflow_soda_reponse_exception_handler)
    app.add_exception_handler(SodaflowError, sodaflow_default_exception_handler)
    app.add_exception_handler(Exception, default_exception_handler)

    return app


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('===================================================================')
logger.info('  Start Application V2')
logger.info('===================================================================')

# environment 설정 로드
logger.info('| App path : ' + app_path)
settings: Settings = load_env(app_path)
# configuration 설정 로드
config = load_config(app_path)

# app 생성
app = create_app(settings, config)
set_state_app(app, settings, config)

#session middleware
# app.add_middleware(SessionMiddleware, secret_key="some-random-string")
logger.info("| PORT :%s", app.state.settings.PORT)
logger.info("| DB URL :%s", app.state.settings.DATABASE_URL)

@app.on_event("startup")
async def startup():
    try:
        await create_db_and_tables()
        session = db_connector.get_async_session()
        await init_db(await session.__anext__())
        logger.info("create db and tables")
    except Exception:
        logging.exception("error startup ")

@app.on_event("shutdown")
async def shutdown():
    # await async_scoped_session.close_all()
    # db_connector._scoped_session.close_all()
    await db_connector._engine.dispose()
    logging.info("DB disconnected")

#https://www.starlette.io/middleware/
# @app.middleware("http")
# async def session_middleware(request: Request, call_next):
#     response = await call_next(request)
#     session = request.cookies.get('session')
#     if session:
#         logger.debug(f'session ={session[len(session) - 100:-1]}')
#         response.set_cookie(key='session', value=request.cookies.get('session'), httponly=True)
#     return response

# 실행시 ENV_TYPE = "dev" 혹은 "local"로 설정
if __name__ == '__main__':
    try:
        logger.info('===================================================================')
        logger.info('  Start ')
        logger.info('===================================================================')
        uvicorn.run("main:app", port=int(app.state.settings.PORT), host='0.0.0.0',  #workers=5)
                    # reload=True,reload_includes=['*.py'],reload_excludes=['*.log', '*.pyc']
                    #reload_dirs=['/Users/add/product/metrix/survey_studio_app/app'], reload_excludes=['.log', '.pyc'])

        )
    except:
        logger.critical(traceback.format_exc())



# 참고)
# 1. 실제 실행 script 작성시 uvicorn main:app --host 0.0.0.0 --port 80 --workers 5 형태로 실행 해야 함
# 2. main 실행시 main.py의 실행이 3번 된다.??
#   https://stackoverflow.com/questions/70300675/fastapi-uvicorn-run-always-create-3-instances-but-i-want-it-1-instance
#   >> 별도의 파일로 uvicorn.run()하면 되는데..이러면 env를 사용하지 못한다.
# 3.uvicorn.run(app,port....)로 사용하면 "main:app":str 대신 app객체 전달 시 실행 때 종료 된다. (reload및 debug 설정시 )
#   https://www.sysnet.pe.kr/2/0/13087