import logging
from flask import request

from app import create_app
application = create_app(config_name = 'server_config')


import sys
file_handler = logging.StreamHandler(sys.stdout)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - {%(pathname)s:%(lineno)d} - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)
rootLogger.addHandler(file_handler)

@application.before_request
def pre_request_logging():
    # Logging request details in prod servers
    logging.info('\t'.join([
        request.remote_addr,
        request.method,
        request.path,
        ', '.join([': '.join(x) for x in request.headers])])
    )

if __name__ == "__main__":
  application.run()

