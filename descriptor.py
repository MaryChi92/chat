from app.config import DEFAULT_PORT
from log.server_log_config import logger


class Port:
    def __set__(self, instance, value):
        if not value and value != 0:
            value = DEFAULT_PORT

        if value < 0:
            logger.critical(f'Can not run server on port {value}')
            exit(1)

        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
