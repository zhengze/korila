#!/usr/bin/env python
#coding: utf-8

from fabric.api import run, env, roles, execute, hosts, task, local, put

env.gateway = '600408@172.31.2.185:60022'

env.passwords = {
    '600408@172.31.2.185:60022': 'syswin#2018',
    'root@10.252.38.132:22': '123.com',
    'root@10.252.38.134:22': '123.com',
}

env.roledefs = {
    'daxing_bastion_host': ["172.31.2.185"],
    'daxing_crp': ['10.252.38.132', '10.252.38.134'],
}

def get_command(command):
    
    commands = dict(supervisorctl_status_cmd = "supervisorctl status",
        keepalived_status_cmd = "systemctl status keepalived",
        df_cmd = "df -h",
    )
    return commands.get(command)


@roles("daxing_crp")
def daxing_crp_status(cmd):
    cmd = get_command(cmd)
    run(cmd)
    #local(cmd)


@roles("daxing_crp")
def daxing_crp_uploadfile():
    put("monitor.py", "/root")
    
    
