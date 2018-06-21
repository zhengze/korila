#!/usr/bin/python env
# coding: utf8

# AUTHOR: zhanghai
# DATE: 2018.05.24
# FILENAME: gaofang_install.py


from fabric.api import run, env, roles, execute, local, cd, task


env.executable = '/bin/bash'

env.roledefs = {
    'gaofang_lb': {'hosts': ['172.28.50.116', '172.28.50.117']},
    'gaofang_uop': {'hosts': ['172.28.50.125', '172.28.50.161']},
    'gaofang_crp': {'hosts': ['172.28.50.125', '172.28.50.161']},
    # 'all_nodes': ['172.28.50.116', '172.28.50.117', '172.28.50.125', '172.28.50.161']
}

env.users = {
    'gaofang_lb': 'root',
    'gaofang_uop': 'root',
    'gaofang_crp': 'root'
}

env.passwords = {
    'gaofang_lb': '123456',
    'gaofang_uop': '123456',
    'gaofang_crp': '123456'
}


@task
@roles("all_nodes")
def update_hosts_file():
    hosts_mapping = """
{0} app-1 
{1} app-2
{2} lb-1 
{3} lb-2
{4} mongo-1 
{5} mongo-2
{6} mongo-3
{7} uop.syswin.com crp.syswin.com
    """.format("172.28.26.26",
               "172.28.26.27",
               "172.28.26.28",
               "172.28.26.29",
               "172.28.26.30",
               "172.28.26.31",
               "172.28.26.32",
               "172.28.26.33",
               )
    run("echo \""+hosts_mapping+"\">>/etc/hosts")


@task
@roles("all_nodes")
def install_dependent_packages():
    cmd = """yum install –y epel-release && \
yum clean all && \
yum update && \
yum install -y git screen tree psmisc curl wget multitail htop vim && \
yum install readline readline-devel readline-static && \
yum install openssl openssl-devel openssl-static && \
yum install sqlite-devel && \
yum install bzip2-devel bzip2-libs && \
yum install zlib-devel && \
yum install gcc libffi-devel python-devel && \
yum install openldap-devel -y && \
yum install nmap -y && \
yum install openssh-server openssh-clients -y && \
yum install ansible -y 
    """
    run(cmd)


@task
@roles("gaofang_lb")
def nginx_configure():
    run("yum install nginx -y && mkdir -p /var/log/nginx/{uop, crp} && \
setsebool -P httpd_can_network_connect 1 && \
mv /etc/nginx.conf /etc/nginx_back.conf && systemctl enable nginx")
    run("scp 172.28.50.125:/opt/uop-backend/conf.d/prod/nginx/nginx.conf /etc/")
    run("scp 172.28.50.125:/opt/uop-backend/conf.d/prod/nginx/src/uop.conf /etc/nginx/conf.d/")
    run("scp 172.28.50.125:/opt/uop-backend/conf.d/prod/nginx/src/crp.conf /etc/nginx/conf.d/")


@task
@roles("gaofang_lb")
def keepalived_configure():
    run("yum install ipvsadm kernel-devel popt-devel libnl-devel -y && \
yum install keepalived nodejs -y")
    run("scp 172.28.50.125:/etc/keepalived.conf /etc/keepalived_back.conf")
    run("scp 172.28.50.125:/opt/uop-backend/conf.d/prod/keepalived/keepalived.conf /etc/")
    run("scp -r 172.28.50.125:/opt/uop-backend/conf.d/prod/keepalived/scripts /etc/keepalived")
    run("systemctl enable keepalived")


@task
@roles("gaofang_app")
def python_env_configure():
    cmd = """easy_install pip && pip install virtualenvwrapper && \
mkdir $HOME/.virtualenvs && \
echo 'export WORKON_HOME=$HOME/.virtualenvs' >> ~/.bashrc && \
echo 'source `which virtualenvwrapper.sh` ' >> ~/.bashrc && \
source ~/.bashrc && \
git clone git://github.com/yyuu/pyenv.git ~/.pyenv && \
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
exec $SHELL -l && \
pyenv install 2.7.13 -v && \
mkvirtualenv py2.7.13uop -p /root/.pyenv/versions/2.7.13/bin/python --no-site-packages && \
mkvirtualenv py2.7.13crp -p /root/.pyenv/versions/2.7.13/bin/python --no-site-packages
"""
    run(cmd)


@task
@roles("gaofang_uop")
def supervisor_configure():
    cmd = "yum install supervisor -y && \
mkdir -p /var/log/supervisor/{uop,crp} && \
cp /etc/supervisord.conf /etcsupervisord.conf_bak && \
systemctl enable supervisord && \
cp /opt/uop-backend/conf.d/prod/supervisord/src/uop.conf /etc/supervisord.d && \
cp /opt/uop-backend/conf.d/prod/supervisord/src/crp.conf /etc/supervisord.d"
    run(cmd)


@task
@roles("gaofang_crp")
def install_docker():
    cmd = "yum install docker-io -y"
    run(cmd)


@task
@roles("gaofang_lb")
def build_uop_frontend(
    code_path="/opt/uop-frontend"
):
    with cd(code_path):
        cmd = "git checkout -b feature-fuzhou origin/feature-fuzhou && \
npm install -g cnpm --registry=https://registry.npm.taobao.org && \
cnpm install && cnpm run build"
        run(cmd)


@task
@roles("yanlian_uop")
def update_uop_backend(
    code_path="/opt/uop-backend",
):
    with cd(code_path):
        cmd = ""
        run(cmd)


@task
@roles("yanlian_crp")
def update_crp_backend(
    code_path="/opt/crp-backend",
):
    with cd(code_path):
        cmd = ""
        run(cmd)


@task
def main():
    execute(update_hosts_file)
    execute(install_dependent_packages)
    execute(keepalived_configure)
    execute(nginx_configure)
    execute(python_env_configure)
    execute(supervisor_configure)


if __name__ == "__main__":
    main()
