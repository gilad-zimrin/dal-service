import logging
from os import getenv

import uvicorn

from src.app_config import app
from src.core.logger import logger




def main():
    logger.info("DAL service starting up..")
    uvicorn.run(
        app=app,
        host='0.0.0.0',
        port=int(getenv("DAL_PORT", default=8000)),
    )
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_error.disabled = True
    uvicorn_error.propagate = False


if __name__ == '__main__':
    main()

