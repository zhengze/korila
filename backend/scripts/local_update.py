#!/usr/bin/python env


import os
from fabric.api import run, env, roles, execute, local, cd, lcd, parallel, task

env.executable = '/bin/bash'


@task
@parallel
def update_uop():
    root_path = "/home/zhengze/codes"
    paths = ["uop-frontend", "uop-backend", "uop-crp"]

    def update(source_path):
        path = os.path.join(root_path, source_path)
        with lcd(path):
            local("git fetch origin && git reset --hard HEAD && git pull")

    map(update, paths)


@task
def main():
    execute(update_uop)


if __name__ == "__main__":
    main()
