#!/usr/bin/env python
#coding: utf-8


from optparse import OptionParser 
import paramiko
from fabric.api import run, env, roles, execute, hosts, task


env.passwords = {
    'root@172.28.32.32:22': '123.com',
    'root@172.28.32.51:22': '123.com',
    'root@172.28.32.53:22': '123.com',
    'root@172.28.32.49:22': '123.com',
    'root@172.28.32.50:22': '123.com',
    'root@172.28.26.199:22': '123.com',
    'root@172.28.26.200:22': '123.com',
    'root@172.28.26.217:22': '123.com',
    'root@172.28.26.212:22': '123.com',
} 

env.roledefs = {   
    'dev_crp' : ['172.28.32.32'],  
    'test_lb' : ['172.28.32.51', '172.28.32.53'], 
    'test_app' : ['172.28.32.49', '172.28.32.50'],  
    'dasha_lb': ["172.28.26.199", "172.28.26.200"],
    'dasha_app': ["172.28.26.217", "172.28.26.212"],
}  
  

def get_command(command):
    
    commands = dict(supervisorctl_status_cmd = "supervisorctl status",
        keepalived_status_cmd = "systemctl status keepalived",
        df_cmd = "df -h"
    )
    return commands.get(command)


@roles("dev_crp")
@task
def dev_crp_status(cmd):
    cmd = get_command(cmd)
    run(cmd)

@roles("test_lb")
@task
def test_lb_status(cmd):
    try:
        cmd = get_command(cmd)
        run(cmd)
    except Exception as e:
        print("error:", e)

@roles("test_app")
@task
def test_app_status(cmd):
    cmd = get_command(cmd)
    run(cmd)

@roles("dasha_lb")
@task
def dasha_lb_status(cmd):
    cmd = get_command(cmd)
    run(cmd)

@roles("dasha_app")
@task
def dasha_app_status(cmd):
    cmd = get_command(cmd)
    run(cmd)


@task
def main(cmd):
    #cmd = get_command(cmd)
    execute(dev_crp_status, cmd)
    execute(test_lb_status, cmd)
    execute(test_app_status, cmd)
    execute(dasha_lb_status, cmd)
    execute(dasha_app_status, cmd)


if __name__ == "__main__":
    parser = OptionParser() 
    parser.add_option("-C", "--command", action="store_true", 
       dest="command", 
       default=False, 
       help="get input command, supervisorctl_status_cmd, keepalived_status_cmd, df_cmd"
    ) 
    (options, args) = parser.parse_args()
    command = get_command(args[0])
    main(command)
