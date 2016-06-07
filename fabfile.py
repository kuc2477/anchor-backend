import StringIO
import os.path
from jinja2 import Template
from contextlib import contextmanager
from fabric.api import *


# ================
# HELPER FUNCTIONS
# ================

def _join(path, *paths):
    return os.path.join(path, *paths).replace('\\', '/')


def _render(string, context=None):
    return Template(string).render(context or {})


# =======
# CONFIGS
# =======

# source repository
REPO = 'https://github.com/kuc2477/anchor-backend'

# vhost
VHOST = 'anchor'

# application paths
HOME_DIR = '/home/ubuntu'
VIRTUALENV = _join(HOME_DIR, '.pyenv/versions/{}'.format(VHOST))
VIRTUALENV_UWSGI = _join(VIRTUALENV, 'bin/uwsgi')
APPS_DIR = _join(HOME_DIR, 'production')
APP_DIR = _join(APPS_DIR, VHOST)
APP_MODULE = 'wsgi'
APP_CALLABLE = 'app'
UWSGI_LOGFILE = _join(APP_DIR, 'uwsgi.log')

# supervisor paths
SUPERVISOR_DIR = '/etc/supervisor/conf.d'
SUPERVISORD_CONFIG = '/etc/supervisord.conf'
SUPERVISORD_LOG_DIR = '/var/log/supervisord'
SUPERVISORD_SOCKET = '/tmp/supervisor.sock'
SUPERVISORD_PIDFILE = '/var/run/supervisord.pid'

# nginx paths
NGINX_DIR = '/etc/nginx/sites-'
NGINX_AVAILABLE_DIR = '{}available'.format(NGINX_DIR)
NGINX_ENABLED_DIR = '{}enabled'.format(NGINX_DIR)

# static paths
STATIC = 'static'


# ===============
# FABRIC SETTINGS
# ===============

REDIS_SERVERS = [
    'ubuntu@ec2-54-218-75-14.us-west-2.compute.amazonaws.com',
]
APP_SERVERS = [
    'ubuntu@ec2-54-218-75-14.us-west-2.compute.amazonaws.com',
]

env.shell = '/bin/bash -l -i -c'
env.roledefs = {
    'app': {'hosts':  APP_SERVERS},
    'redis': {'hosts': REDIS_SERVERS},
}


# ==========
# EVIRONMENT
# ==========

def _install_production_dir():
    run('mkdir -p {}'.format(APPS_DIR))


def _install_pyenv():
    # pyenv dependencies
    sudo('apt-get update')
    sudo(
        'apt-get install -y make build-essential libssl-dev zlib1g-dev ' +
        'libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm ' +
        'libncurses5-dev'
    )
    if not run('which pyenv'):
        # pyenv
        sudo('curl -L ' +
             'https://raw.githubusercontent.com/yyuu/pyenv-installer/' +
             'master/bin/pyenv-installer | bash')
        # install python
        run('pyenv install 3.5.1')
        run('pyenv shell 3.5.1')
        run('pyenv virtualenv {}'.format(VHOST))


@contextmanager
def _system_python(after=VHOST):
    run('pyenv shell system')
    yield
    run('pyenv shell {}'.format(after))


@contextmanager
def _production_python(after='system'):
    run('pyenv shell {}'.format(VHOST))
    yield
    run('pyenv shell {}'.format(after))


@contextmanager
def _swap_enabled():
    sudo('/bin/dd if=/dev/zero of=/var/swap.1 bs=1M count=1024')
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
        run('rm -rf {}'.format(VHOST))
        run('git clone {} {}'.format(REPO, VHOST))


def _update_repo():
    with cd(APP_DIR), _production_python():
        run('git checkout master')
        run('git pull origin master')
        run('pip install -r requirements/prod.txt')


# =====================
# SYSTEM CONFIGURATIONS
# =====================

def _upload_secret():
    with open('./secret.py') as f:
        secret = f.read()
    interpolated = StringIO.StringIO()
    interpolated.write(secret)
    put(interpolated, _join(APP_DIR, 'secret.py'))


def _make_nginx_conf():
    with open('./templates/conf/nginx.tpl') as f:
        template = f.read()
    interpolated = StringIO.StringIO()
    interpolated.write(_render(template, {
        'domain': VHOST,
        'root': APP_DIR,
        'static': STATIC
    }))

    put(interpolated, _join(NGINX_AVAILABLE_DIR, VHOST), use_sudo=True)
    sudo('rm -f {}'.format(_join(NGINX_ENABLED_DIR, 'default')))
    sudo('ln -sf {} {}'.format(
        _join(NGINX_AVAILABLE_DIR, VHOST),
        _join(NGINX_ENABLED_DIR, VHOST),
    ))
    run('touch {}'.format(_join(APP_DIR, 'access.log')))
    run('touch {}'.format(_join(APP_DIR, 'error.log')))


def _make_supervisor_conf():
    # install default supervisord configuration file
    with open('./templates/conf/supervisord.tpl') as f:
        template = f.read()
    interpolated = StringIO.StringIO()
    interpolated.write(_render(template, {
        'socket': SUPERVISORD_SOCKET,
        'pidfile': SUPERVISORD_PIDFILE,
        'logfile': _join(SUPERVISORD_LOG_DIR, 'supervisord.log'),
        'childlogdir': SUPERVISORD_LOG_DIR,
    }))
    sudo('mkdir -p {}'.format(SUPERVISORD_LOG_DIR))
    put(interpolated, SUPERVISORD_CONFIG, use_sudo=True)

    # install supervisorctl configuration file
    with open('./templates/conf/supervisor.tpl') as f:
        template = f.read()
    interpolated = StringIO.StringIO()
    interpolated.write(_render(template, {
        'program': VHOST,
        'uwsgi': VIRTUALENV_UWSGI,
        'root': APP_DIR,
        'module': APP_MODULE,
        'callable': APP_CALLABLE,
        'virtualenv': VIRTUALENV,
        'uwsgi_logfile': UWSGI_LOGFILE,
    }))
    sudo('touch {}'.format(UWSGI_LOGFILE))
    sudo('mkdir -p {}'.format(SUPERVISOR_DIR))
    put(interpolated, '{}.conf'.format(_join(SUPERVISOR_DIR, VHOST)),
        use_sudo=True)


# =======
# SERVICE
# =======

def _start_webserver():
    sudo('/etc/init.d/nginx start')


def _start_supervisord():
    sudo('supervisord')


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
        run('sudo pip install -r requirements/depl.txt')


def _install_production_dependencies():
    with cd(APP_DIR), _production_python(after=VHOST), _swap_enabled():
            run('pip install -r requirements/prod.txt')


def _install_extensions():
    sudo('apt-get install redis-server')


# =================
# DEPLOYMENT (MAIN)
# =================

def init():
    # install pyenv
    _install_pyenv()

    # install production dir and clone fresh repo from github
    _install_production_dir()
    _clone_repo()

    # install build / system dependencies and pruduction python dependencies
    _install_build_dependencies()
    _install_deployment_dependencies()
    _install_production_dependencies()
    _install_extensions()

    # make vhost and supervisor configurations
    _upload_secret()
    _make_nginx_conf()
    _make_supervisor_conf()

    # kick off webserver and supervisor
    _reload_webserver()
    _reload_supervisor()

    # start app server
    _start_app()


def deploy():
    _update_repo()
    _reload_app()


def destroy():
    sudo('rm -rf {}'.format(APPS_DIR))


def upload_secret():
    _upload_secret()
