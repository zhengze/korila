from flask import Flask, request
from flask_restful import Resource, Api
import subprocess
import logging
import os

app = Flask(__name__)
api = Api(app)


class monitor(Resource):
    def get(self):
        workpath = os.getcwd()
        return {"workpath": workpath}
    
    def post(self):
        #child = subprocess.Popen(["fab -f ./scripts/monitor.py test_app_status"], stdout=subprocess.PIPE)
        #res = child.wait()
        res = os.system("fab -f ./scripts/monitor.py test_app_status")
        logging.info("res:", res)
        return res
        


api.add_resource(monitor, "/monitor")

if __name__ == '__main__':
    app.run(debug=True)
