DEFAULT_PORT = 7777
DEFAULT_HOST = 'localhost'

ENCODING = 'utf-8'

MAX_CONNECTIONS = 10
TIMEOUT = 1.0
MAX_PACKAGE_LENGTH = 2048

SERVER_DATABASE = 'sqlite+pysqlite:///server_base.db3'
CLIENT_DATABASE = 'sqlite+pysqlite:///client_base.db3'

VERIFICATION_PARAMS = ("accept", "listen", "connect", "AF_INET", "SOCK_STREAM")
