import os

from src.app import ApplicationServer
from src.config import Config
from src.logger import log

if __name__ == '__main__':
    try:
        config = Config(os.path.join(os.getcwd(), 'config.yaml'))
        server = ApplicationServer(config)
        log.debug("Application initialized")
        log.debug(f"Config host {config.host} and port {config.port}")
        server.app.run_server(host=config.host, port=config.port)
        log.debug("Application stopped")
    except Exception as e:
        log.error("Failed to initialize application")
        log.exception(e)
