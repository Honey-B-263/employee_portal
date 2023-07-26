from flask import Flask
from api.restApi import restApi

app = Flask(__name__)

app.register_blueprint(restApi)

if __name__ == '__main__':

    # logger.debug("Starting Flask Server")
    # from api import *
    app.run(port=5001,debug=True)
