#!/usr/bin/env python
# coding: utf-8


from fabric.api import run, env, roles, execute, hosts, task, parallel, with_settings
from fabric.colors import green
from settings import UserInfo

userinfo = UserInfo()

supervisorctl_status_cmd = "supervisorctl status"
keepalived_status_cmd = "systemctl status keepalived"
nginx_status_cmd = "service nginx status"

env.roledefs = {
    'dev_crp': ['172.28.32.32'],
    'test_lb': ['172.28.32.51', '172.28.32.53'],
    'test_app': ['172.28.32.49', '172.28.32.50'],
    'dasha_lb': ["172.28.26.199", "172.28.26.200"],
    'dasha_app': ["172.28.26.217", "172.28.26.212"],
    'daxing_crp': ['10.252.38.132', '10.252.38.134'],
}

env.passwords = {
    'root@172.28.32.32:22': userinfo.get_password(),
    'root@172.28.32.49:22': userinfo.get_password(),
    'root@172.28.32.50:22': userinfo.get_password(),
    'root@172.28.32.51:22': userinfo.get_password(),
    'root@172.28.32.53:22': userinfo.get_password(),
    'root@172.28.26.199:22': userinfo.get_password(),
    'root@172.28.26.200:22': userinfo.get_password(),
    'root@172.28.26.212:22': userinfo.get_password(),
    'root@172.28.26.217:22': userinfo.get_password(),
    '600408@172.31.2.185:60022': 'syswin#2018',
    'root@10.252.38.132:22': userinfo.get_password(),
    'root@10.252.38.134:22': userinfo.get_password(),
}


@task
@roles("dev_crp")
def dev_crp_status():
    run(supervisorctl_status_cmd)


@task
@roles("test_lb")
def test_lb_status():
    try:
        run(keepalived_status_cmd)
        run(nginx_status_cmd)
    except Exception as e:
        print("error:", e)


@task
@roles("test_app")
def test_app_status():
    run(supervisorctl_status_cmd)


@task
@roles("dasha_lb")
def dasha_lb_status():
    run(keepalived_status_cmd)
    run(nginx_status_cmd)


@task
@roles("dasha_app")
def dasha_app_status():
    run(supervisorctl_status_cmd)


@task
@roles("daxing_crp")
@with_settings(
  gateway="600408@172.31.2.185:60022"
)
def daxing_crp_status():
    run(supervisorctl_status_cmd)


@task
def main():
    execute(dev_crp_status)
    execute(test_lb_status)
    execute(test_app_status)
    execute(dasha_lb_status)
    execute(dasha_app_status)
    execute(daxing_crp_status)
