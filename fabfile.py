import copy
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


def _mergedicts(base, *extras):
    merged = copy.deepcopy(base)
    for e in extras:
        merged.update(e)
    return merged


# =======
# CONFIGS
# =======

# source repository
REPO = 'https://github.com/kuc2477/anchor-backend'

# vhost
VHOST = 'anchor'
REDIS = 'redis'
ROUTER = 'router'
SCHEDULER = 'scheduler'
NOTIFIER = 'notifier'
CELERY = 'celery'

# application paths
HOME_DIR = '/home/ubuntu'
VIRTUALENV = _join(HOME_DIR, '.pyenv/versions/{}'.format(VHOST))
VIRTUALENV_UWSGI = _join(VIRTUALENV, 'bin/uwsgi')
VIRTUALENV_PYTHON = _join(VIRTUALENV, 'bin/python')
VIRTUALENV_CROSSBAR = _join(VIRTUALENV, 'bin/crossbar')
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

# extension paths
REDIS_LOGFILE = _join(APP_DIR, 'redis.log')
CELERY_LOGFILE = _join(APP_DIR, 'celery.log')
ROUTER_LOGFILE = _join(APP_DIR, 'router.log')
SCHEDULER_LOGFILE = _join(APP_DIR, 'scheduler.log')
NOTIFIER_LOGFILE = _join(APP_DIR, 'notifier.log')

# static paths
STATIC = 'static'


# ===============
# FABRIC SETTINGS
# ===============

EC2_INSTANCES = ['ubuntu@ec2-54-218-75-14.us-west-2.compute.amazonaws.com']
EC2 = EC2_INSTANCES[0]

APP_SERVERS = [EC2]
REDIS_SERVER = EC2
WORKER_SERVERS = [EC2]
SCHEDULER_SERVER = EC2
NOTIFIER_SERVER = EC2
CROSSBAR_ROUTER = EC2

env.shell = '/bin/bash -l -i -c'
env.roledefs = {
    'app': APP_SERVERS,
    'redis': [REDIS_SERVER],
    'worker': WORKER_SERVERS,
    'scheduler': [SCHEDULER_SERVER],
    'notifier': [NOTIFIER_SERVER],
    'router': [CROSSBAR_ROUTER],
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

    # template contexts for supervisorctl configuration file
    base_context = {'root': APP_DIR}
    app_context = {
        'vhost': VHOST,
        'uwsgi': VIRTUALENV_UWSGI,
        'module': APP_MODULE,
        'callable': APP_CALLABLE,
        'virtualenv': VIRTUALENV,
        'uwsgi_logfile': UWSGI_LOGFILE,
    }
    redis_context = {
        'redis': REDIS,
        'runredis': '{} manage.py runredis'.format(VIRTUALENV_PYTHON),
        'redis_logfile': REDIS_LOGFILE,
    }
    celery_context = {
        'celery': CELERY,
        'runcelery': '{} manage.py runcelery'.format(VIRTUALENV_PYTHON),
        'celery_logfile': CELERY_LOGFILE,
    }
    router_context = {
        'router': ROUTER,
        'runrouter': '{} start'.format(VIRTUALENV_CROSSBAR),
        'router_logfile': ROUTER_LOGFILE
    }
    scheduler_context = {
        'scheduler': SCHEDULER,
        'runscheduler': '{} manage.py runscheduler'.format(VIRTUALENV_PYTHON),
        'scheduler_logfile': SCHEDULER_LOGFILE,
    }
    notifier_context = {
        'notifier': NOTIFIER,
        'runnotifier': '{} manage.py runnotifier'.format(VIRTUALENV_PYTHON),
        'notifier_logfile': NOTIFIER_LOGFILE,
    }

    # install supervisorctl configuration file
    context = _mergedicts(
        base_context, app_context, redis_context, celery_context,
        router_context, scheduler_context, notifier_context,
    )
    with open('./templates/conf/supervisor.tpl') as f:
        template = f.read()
    interpolated = StringIO.StringIO()
    interpolated.write(_render(template, context))
    put(interpolated, '{}.conf'.format(_join(SUPERVISOR_DIR, VHOST)),
        use_sudo=True)

    # create empty logfiles
    sudo('touch {}'.format(UWSGI_LOGFILE))
    sudo('touch {}'.format(REDIS_LOGFILE))
    sudo('touch {}'.format(CELERY_LOGFILE))
    sudo('touch {}'.format(ROUTER_LOGFILE))
    sudo('touch {}'.format(SCHEDULER_LOGFILE))
    sudo('touch {}'.format(NOTIFIER_LOGFILE))
    sudo('mkdir -p {}'.format(SUPERVISOR_DIR))


# ===================
# SERVICE (WEBSERVER)
# ===================

def _start_webserver():
    sudo('/etc/init.d/nginx start')


def _reload_webserver():
    sudo('/etc/init.d/nginx reload')


def _stop_webserver():
    sudo('/etc/init.d/nginx stop')


# =====================
# SERVICE (SUPERVISORD)
# =====================

def _start_supervisord():
    sudo('supervisord')


def _reload_supervisor():
    sudo('supervisorctl update')


# =============
# SERVICE (APP)
# =============

def _start_app():
    sudo('supervisorctl start {}'.format(VHOST))


def _reload_app():
    sudo('supervisorctl restart {}'.format(VHOST))


def _stop_app():
    sudo('supervisorctl stop {}'.format(VHOST))


# ===============
# SERVICE (REDIS)
# ===============

def _start_redis():
    sudo('supervisorctl start {}'.format(REDIS))


def _reload_redis():
    sudo('supervisorctl restart {}'.format(REDIS))


def _stop_redis():
    sudo('supervisorctl stop {}'.format(REDIS))


# ================
# SERVICE (CELERY)
# ================

def _start_worker():
    sudo('supervisorctl start {}'.format(CELERY))


def _reload_worker():
    sudo('supervisorctl restart {}'.format(CELERY))


def _stop_worker():
    sudo('supervisorctl stop {}'.format(CELERY))


# ================
# SERVICE (ROUTER)
# ================

def _start_router():
    sudo('supervisorctl start {}'.format(ROUTER))


def _reload_router():
    sudo('supervisorctl restart {}'.format(ROUTER))


def _stop_router():
    sudo('supervisorctl stop {}'.format(ROUTER))


# ===================
# SERVICE (SCHEDULER)
# ===================

def _start_scheduler():
    sudo('supervisorctl start {}'.format(SCHEDULER))


def _reload_scheduler():
    sudo('supervisorctl restart {}'.format(SCHEDULER))


def _stop_scheduler():
    sudo('supervisorctl stop {}'.format(SCHEDULER))


# ==================
# SERVICE (NOTIFIER)
# ==================

def _start_notifier():
    sudo('supervisorctl start {}'.format(NOTIFIER))


def _reload_notifier():
    sudo('supervisorctl restart {}'.format(NOTIFIER))


def _stop_notifier():
    sudo('supervisorctl stop {}'.format(NOTIFIER))


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

@roles('app', 'redis', 'worker', 'router', 'scheduler', 'notifier')
def install():
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


def destroy():
    sudo('rm -rf {}'.format(APPS_DIR))
    _stop_webserver()
    _stop_app()
    _stop_redis()
    _stop_worker()
    _stop_router()
    _stop_scheduler()
    _stop_notifier()


@roles('app')
def init():
    install()
    # kick off webserver, supervisord and app server
    _reload_webserver()
    _reload_supervisor()
    _start_app()


@roles('app')
def deploy():
    _update_repo()
    _reload_app()


@roles('app')
def upload_secret():
    _upload_secret()


@roles('redis')
def run_redis():
    _reload_redis()


@roles('worker')
def run_workers():
    _reload_worker()


@roles('scheduler')
def run_scheduler():
    _reload_scheduler()


@roles('notifier')
def run_notifier():
    _reload_notifier()


@roles('router')
def run_router():
    _reload_router()
