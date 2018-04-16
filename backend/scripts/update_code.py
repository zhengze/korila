from fabric.api import run, env, roles, execute, local
import os


env.shell = True
env.executable = '/bin/bash'

def update_uop():
    root_path = "/home/zhengze/codes"
    uop_backend_path = "/".join([root_path, "uop-backend"])
    crp_backend_path = "/".join([root_path, "uop-crp"])
    uop_frontend_path = "/".join([root_path, "uop-frontend"])
    paths = [uop_backend_path, crp_backend_path, uop_frontend_path]
        
    for path in paths:
        print
        local("cd "+path+";git branch;git pull")


def main():
    execute(update_uop)


if __name__ == "__main__":
    cmd = "fab -f update_code.py main"
    os.system(cmd)
