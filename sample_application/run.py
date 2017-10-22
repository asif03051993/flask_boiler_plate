import logging

from flask import request
from app import create_app

app = create_app(config_name = 'server_config')

import sys
file_handler = logging.StreamHandler(sys.stdout)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - {%(pathname)s:%(lineno)d} - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
rootLogger.addHandler(file_handler)

@app.before_request
def pre_request_logging():
    # Logging request details in prod servers
    logging.info('\t'.join([
        request.remote_addr,
        request.method,
        request.path,
        ', '.join([': '.join(x) for x in request.headers])])
    )

app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)