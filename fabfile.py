import os.path
from contextlib import contextmanager
from fabric.api import *


VHOST = 'anchor'
APPS_DIR = '/production'
APP_DIR = os.path.join(APPS_DIR, VHOST)

REPO = 'https://github.com/kuc2477/anchor-backend'
SUPERVISOR_DIR = '/etc/supervisor/conf.d/'
NGINX_DIR = '/etc/nginx/sites-'
STATIC = 'static'


# ==========
# EVIRONMENT
# ==========

def _install_pyenv():
    # pyenv dependencies
    sudo(' '.join([
        'apt-get install -y make build-essential libssl-dev zlib1g-dev',
        'libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm',
        'libncurses5-dev',
    ]))
    # pyenv
    sudo('curl -L ' +
         'https://raw.githubusercontent.com/yyuu/pyenv-installer/' +
         'master/bin/pyenv-installer | bash')
    # install python
    run('pyenv install 3.5.1')
    run('pyenv shell 3.5.1')
    run('pyenv virtualenv anchor')


@contextmanager
def _system_python(after='anchor'):
    run('pyenv shell system')
    yield
    run('pyenv shell {}'.format(after))


@contextmanager
def _production_python(after='system'):
    run('pyenv shell anchor')
    yield
    run('pyenv shell {}'.format(after))


@contextmanager
def _swap_enabled():
    sudo('/bin/dd if=/dev/zero of=/var/swap.1 bs-1M count=1024')
    sudo('/sbin/mkswap /var/swap.1')
    sudo('/sbin/swapon /var/swap.1')
    yield
    sudo('swapoff /var/swap.1')
    sudo('rm /var/swap.1')


# ==================
# REPOSITORY CONTROL
# ==================

def _clone_repo():
    with cd(APPS_DIR):
        run('git clone {}'.format(REPO))


def _update_repo():
    with cd(APP_DIR), _production_python():
        run('git checkout master')
        run('git pull origin master')
        run('pip install -r requirements/prod.txt')


# =====================
# SYSTEM CONFIGURATIONS
# =====================

def _make_supervisor_conf():
    # TODO: NOT IMPLEMENTED YET
    pass


def _make_vhost():
    # TODO: NOT IMPLEMENTED YET
    pass


# =======
# SERVICE
# =======

def _reload_webserver():
    sudo('/etc/init.d/nginx reload')


def _reload_supervisor():
    sudo('supervisorctl update')


def _start_app():
    sudo('supervisorctl start {}'.format(VHOST))


def _reload_app():
    sudo('supervisorctl restart {}'.format(VHOST))


# ============
# DEPENDENCIES
# ============

def _install_build_dependencies():
    sudo('apt-get install build-essential g++ libatlas-dev gfortran')
    sudo('apt-get install nginx')


def _install_deployment_dependencies():
    with cd(APP_DIR), _system_python(after='system'):
        run('pip install -r requirements/depl.txt')


def _install_production_dependencies():
    with cd(APP_DIR), _production_python(after='anchor'), _swap_enabled():
            run('pip install -r requirements/prod.txt')


# =================
# DEPLOYMENT (MAIN)
# =================

def init_deploy():
    # clone fresh source code from github
    _clone_repo()

    # install build / system dependencies and pruduction python dependencies
    _install_build_dependencies()
    _install_deployment_dependencies()
    _install_production_dependencies()

    # make vhost and supervisor configurations
    _make_vhost()
    _make_supervisor_conf()

    # kick off webserver and supervisor
    _reload_webserver()
    _reload_supervisor()

    # start app server
    _start_app()


def deploy():
    _update_repo()
    _reload_app()
