import os.path
from fabric.api import *
from fabric.operations import get, put


NAME = 'anchor-backend'
APPS_DIR = '/production'
APP_DIR = os.path.join(APPS_DIR, VHOST)

REPO = 'https://github.com/kuc2477/anchor-backend'
SUPERVISOR_DIR = '/etc/supervisor/conf.d/'
NGINX_DIR = '/etc/nginx/sites-'
STATIC = 'static'


# ==========
# EVIRONMENT
# ==========

def _use_python2():
    pass


def _use_python3():
    pass


def _use_production():
    pass


def _turn_on_swap():
    pass


def _turn_off_swap():
    pass


# ==================
# REPOSITORY CONTROL
# ==================

def _clone_repo():
    with cd(APPS_DIR):
        run('git clone {}'.format(REPO))


def _update_repo():
    with cd(APP_DIR):
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
    # TODO: NOT IMPLEMENTED YET
    pass


def _reload_app():
    # TODO: NOT IMPLEMENTED YET
    pass


# ============
# DEPENDENCIES
# ============

def _install_build_dependencies():
    sudo('apt-get install build-essential g++ libatlas-dev gfortran')
    sudo('apt-get install nginx')


def _install_deployment_dependencies():
    with cd(APP_DIR):
        run('pip install -r requirements/depl.txt')


def _install_production_dependencies():
    with cd(APP_DIR):
        _turn_on_swap()
        run('pip install -r requirements/prod.txt')
        _turn_off_swap()


# =================
# DEPLOYMENT (MAIN)
# =================

def init_deploy():
    _clone_repo()

    _install_build_dependencies()
    _install_deployment_dependencies()
    _install_production_dependencies()

    _make_vhost()
    _make_supervisor_conf()
    _reload_webserver()
    _reload_supervisor()
    _start_app()


def deploy():
    _update_repo()
    _reload_app()
