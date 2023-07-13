import sys
from argparse import ArgumentParser
from app.config import DEFAULT_PORT, DEFAULT_HOST
from log.server_log_config import logger


def parse_params():
    parser = ArgumentParser()
    parser.add_argument('-p', type=int, default=DEFAULT_PORT, help='TCP-port')
    parser.add_argument('-a', default=DEFAULT_HOST, type=str, help='IP-address')
    namespace = parser.parse_args(sys.argv[1:])
    host = namespace.a
    port = namespace.p
    logger.info(
        f"IP-address: {host if host else DEFAULT_PORT}, TCP-port: {port if port else DEFAULT_HOST}"
    )
    return host, port
