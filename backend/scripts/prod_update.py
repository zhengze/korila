#!/bin/python env
# coding: utf8

# AUTHOR: zhanghai
# DATE: 2018.05.24
# FILENAME: prod_update.py


from fabric.api import run, env, roles, execute, local, cd, task, parallel
from settings import UserInfo

userinfo = UserInfo()

env.executable = '/bin/bash'

env.roledefs = {
    'dasha_lb': ['172.28.26.199', '172.28.26.200'],
    'dasha_uop': ['172.28.26.212', '172.28.26.217'],
    'dasha_crp': ['172.28.26.212', '172.28.26.217']
}

env.user = 'root'
env.passwords = {
    'dasha_lb': userinfo.get_password(),
    'dasha_uop': userinfo.get_password(),
    'dasha_crp': userinfo.get_password(),
}

uop_frontend_update_cmd = "git pull && npm run build && nginx -t && \
    nginx -s reload"
uop_backend_update_cmd = "git pull && supervisorctl reload uop"
crp_backend_update_cmd = "git pull && supervisorctl reload crp"


@task
@roles("dasha_lb")
def update_uop_frontend(
    code_path="/opt/uop-frontend",
    cmd=uop_frontend_update_cmd
):
    with cd(code_path):
        run(cmd)


@task
@roles("dasha_uop")
def update_uop_backend(
    code_path="/opt/uop-backend",
    cmd=uop_backend_update_cmd
):
    with cd(code_path):
        run(cmd)


@task
@roles("dasha_crp")
def update_crp_backend(
    code_path="/opt/crp-backend",
    cmd=crp_backend_update_cmd
):
    with cd(code_path):
        run(cmd)


@task
def main():
    execute(update_uop_frontend, uop_frontend_update_cmd)
    execute(update_uop_backend, uop_backend_update_cmd)
    execute(update_crp_backend, crp_backend_update_cmd)


if __name__ == "__main__":
    main()
