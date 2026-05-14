import logging
import sys
from datetime import datetime
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # Standardize timestamp format
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

def setup_logging():
    logger = logging.getLogger("flask_app")
    logger.setLevel(logging.INFO)

    # JSON Formatter
    formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')

    # Console Transport (all logs >= INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Transport: app.log (all logs >= INFO)
    app_log_handler = logging.FileHandler("app.log")
    app_log_handler.setFormatter(formatter)
    app_log_handler.setLevel(logging.INFO)
    logger.addHandler(app_log_handler)

    # File Transport: error.log (only ERROR logs)
    error_log_handler = logging.FileHandler("error.log")
    error_log_handler.setFormatter(formatter)
    error_log_handler.setLevel(logging.ERROR)
    logger.addHandler(error_log_handler)

    return logger

# Initialize logger
logger = setup_logging()
