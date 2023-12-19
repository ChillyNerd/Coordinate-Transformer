import datetime
import logging.handlers
import os

current_date = str(datetime.datetime.now().date())
logs_path = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(logs_path):
    os.mkdir(logs_path)
log = logging.getLogger('coordinate_transformer')
handler = logging.handlers.RotatingFileHandler(os.path.join(logs_path, f'{current_date}.log'), mode='a',
                                               maxBytes=5_000_000, backupCount=1000)
logger_handlers = [handler, logging.StreamHandler()]
logging.basicConfig(format='%(asctime)s - %(name)s %(module)s %(levelname)s [%(threadName)s]: %(message)s',
                    handlers=logger_handlers, level=logging.getLevelName('DEBUG'))
logging.getLogger('werkzeug').setLevel(logging.ERROR)
