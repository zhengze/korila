#!/usr/bin/python env
#coding: utf8

# AUTHOR: zhanghai
# DATE: 2018.05.24
# FILENAME: yanlian_update.py


from fabric.api import run, env, roles, execute, local, cd, task


env.executable = '/bin/bash'

env.roledefs = {
    'yanlian_lb': {'hosts':['172.28.50.116', '172.28.50.117']},
    'yanlian_uop': {'hosts':['172.28.50.125', '172.28.50.161']},
    'yanlian_crp': {'hosts':['172.28.50.125', '172.28.50.161']}
}

env.users = {
    'yanlian_lb': 'root',
    'yanlian_uop': 'root',
    'yanlian_crp': 'root'
}
env.passwords = {
    'yanlian_lb': '123456',
    'yanlian_uop': '123456',
    'yanlian_crp': '123456'
}

uop_frontend_update_cmd = "git pull;npm run build;nginx -t;nginx -s reload"
uop_backend_update_cmd = "git pull;supervisorctl reload uop"
crp_backend_update_cmd = "git pull;supervisorctl reload crp"


@task
@roles("yanlian_lb")
def update_uop_frontend(
    code_path="/opt/uop-frontend",
    cmd=uop_frontend_update_cmd
):
    with cd(code_path):
        run(cmd)


@task
@roles("yanlian_uop")
def update_uop_backend(
    code_path="/opt/uop-backend",
    cmd=uop_backend_update_cmd
):
    with cd(code_path):
        run(cmd)


@task
@roles("yanlian_crp")
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
