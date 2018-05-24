#!/usr/bin/env python
# coding: utf-8


from fabric.api import run, env, roles, execute, hosts, task, parallel
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
}

env.users = {
    'dev_crp': userinfo.get_user(),
    'test_lb': userinfo.get_user(),
    'test_app': userinfo.get_user(),
    'dasha_lb': userinfo.get_user(),
    'dasha_app': userinfo.get_user(),
}
env.passwords = {
    'dev_crp': userinfo.get_password(),
    'test_lb': userinfo.get_password(),
    'test_app': userinfo.get_password(),
    'dasha_lb': userinfo.get_password(),
    'dasha_app': userinfo.get_password(),
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


@task
@roles("dasha_app")
def dasha_app_status():
    run(supervisorctl_status_cmd)


@task
def main():
    execute(dev_crp_status)
    execute(test_lb_status)
    execute(test_app_status)
    execute(dasha_lb_status)
    execute(dasha_app_status)
