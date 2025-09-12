from os import getenv

import uvicorn

from src.app import app
from src.utils.logger import logger


def main():
    logger.info("DAL service starting up..")
    uvicorn.run(app=app, host='0.0.0.0', port=int(getenv("DAL_PORT", default=8000)))


if __name__ == '__main__':
    main()
    
