#!/usr/bin/env python
#coding:utf8


from flask import Flask, request
from flask_restful import Resource, Api
import subprocess
import logging
import os
import ansible

app = Flask(__name__)
api = Api(app)


class monitor(Resource):
    def get(self):
        #CMD = "ansible -i {0}/inventory/hosts all -m shell -a 'supervisorctl status'".format(os.getcwd())
        current_path = os.getcwd()
        CMD = "ansible-playbook -i {0}/inventory/hosts {1}/playbook/web.yml".format(current_path, current_path)
        child = subprocess.Popen([CMD], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        child.wait()
        
        if child.returncode == 0:
            msg = child.stdout.read().decode("utf-8")
        else:
            msg = child.stderr.read().decode("utf-8")

        res = {
            "code": child.returncode,
            "msg": msg
        }
        return res
    
    def post(self):
        pass
        


api.add_resource(monitor, "/monitor")

if __name__ == '__main__':
    app.run(debug=True)
