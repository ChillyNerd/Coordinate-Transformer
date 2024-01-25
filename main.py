import os
import logging

from src.app import ApplicationServer
from src.config import Config

if __name__ == '__main__':
    config = Config(config_path=os.path.join(os.getcwd(), 'config.yaml'))
    log = logging.getLogger(config.main)
    try:
        server = ApplicationServer(config)
        log.debug("Application initialized")
        log.debug(f"Config host {config.host} and port {config.port}")
        server.app.run_server(host=config.host, port=config.port)
        log.debug("Application stopped")
    except Exception as e:
        log.error("Failed to initialize application")
        log.exception(e)
