#!/usr/bin/env python
#coding: utf-8


import paramiko
from fabric.api import run, env, roles, execute, hosts, task


#IP="172.28.32.50"
#PORT=22
#USERNAME="root"
#PASSWORD="123.com"
#CMD="supervisorctl status"
#
#ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.connect(IP, PORT, USERNAME, PASSWORD, timeout=5)
#stdin, stdout, stderr = ssh.exec_command(CMD)
#print stdout.readlines()
#ssh.close()

supervisorctl_status_cmd = "supervisorctl status"
keepalived_status_cmd = "systemctl status keepalived"

#env.password = "123.com"
env.passwords = {
    'root@172.28.32.32:22': '123.com',
    'root@172.28.32.51:22': '123.com',
    'root@172.28.32.52:22': '123.com',
    'root@172.28.32.49:22': '123.com',
    'root@172.28.32.50:22': '123.com',
    'root@172.28.26.199:22': '123.com',
    'root@172.28.26.200:22': '123.com',
    'root@172.28.26.217:22': '123.com',
    'root@172.28.26.222:22': '123.com',
} 

env.roledefs = {   
    'dev_crp' : ['172.28.32.32'],  
    'test_lb' : ['172.28.32.51', '172.28.32.53'], 
    'test_app' : ['172.28.32.49', '172.28.32.50'],  
    'dasha_lb': ["172.28.26.199", "172.28.26.200"],
    'dasha_app': ["172.28.26.217", "172.28.26.222"],
}  
  

@roles("dev_crp")
def dev_crp_status():
    run(supervisorctl_status_cmd)

@roles("test_lb")
def test_lb_status():
    try:
        run(keepalived_status_cmd)
    except Exception as e:
        print("error:", e)

@roles("test_app")
def test_app_status():
    run(supervisorctl_status_cmd)

@roles("dasha_lb")
def dasha_lb_status():
    run(keepalived_status_cmd)

@roles("dasha_app")
def dasha_app_status():
    run(supervisorctl_status_cmd)

def main():
    execute(dev_crp_status)
    execute(test_lb_status)
    execute(test_app_status)
    execute(dasha_lb_status)
    execute(dasha_app_status)

