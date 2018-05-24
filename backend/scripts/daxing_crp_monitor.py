#!/usr/bin/env python
# coding: utf-8

from fabric.api import run, env, roles, execute, hosts, task

env.gateway = '600408@172.31.2.185:60022'

env.roledefs = {
    'daxing_bastion_host': ["172.31.2.185"],
    'daxing_crp': ['10.252.38.132', '10.252.38.134'],
}

env.passwords = {
    '600408@172.31.2.185:60022': 'syswin#2018',
    'daxing_crp': '123.com',
}

supervisorctl_status_cmd = "supervisorctl status crp"


@roles("daxing_crp")
def daxing_crp_status():
    run(supervisorctl_status_cmd)
