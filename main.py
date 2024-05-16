from start import ModBusProcessManager
from dotenv import load_dotenv
import logging, os
import portalocker
from logging.handlers import RotatingFileHandler

load_dotenv()


class SafeRotatingFileHandler(RotatingFileHandler):

    def doRollover(self):
        with portalocker.Lock(self.baseFilename, timeout=1):
            super().doRollover()


logLevel = os.getenv('LOG_LEVEL')

logLevel = 40 if logLevel is None else int(logLevel)

logger = logging.getLogger('app_logger')
handler = SafeRotatingFileHandler(filename='logs/DCMShiram.log',
                                  maxBytes=1024 * 1024 * 20,
                                  backupCount=10)
logging.basicConfig(level=logging.INFO, handlers=[handler])

handler.setFormatter(logging.Formatter(
    fmt='%(asctime)s %(levelname)s %(threadName)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

logger.addHandler(handler)
logger.setLevel(logLevel)

# Example logging usage
logger.info("This is a log message.")

if __name__ == '__main__':
    ModBusProcessManager()
