import os

from src import app, Config, log

if __name__ == '__main__':
    try:
        config = Config(os.path.join(os.getcwd(), 'config.yaml'))
        log.debug("Application initialized")
        log.debug(f"Config host {config.host} and port {config.port}")
        app.run_server(host=config.host, port=config.port)
        log.debug("Application stopped")
    except Exception as e:
        log.error("Failed to initialize application")
        log.exception(e)

