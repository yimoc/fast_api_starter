import logging
import os

from app.core.log.logging import set_log

'''
제일 먼저 실행할 것으로 main.py에 import 상단에 온다.
'''
app_path = os.path.dirname(os.path.realpath(__file__))

# logger 설정
set_log(app_path)
logger = logging.getLogger(__name__)
logger.info('| Applicaton path : ' + app_path)