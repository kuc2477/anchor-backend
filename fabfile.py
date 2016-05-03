from fabric.api import *


VHOST = 'anchor'


def _clone_repo():
    # TODO: NOT IMPLEMENTED YET
    pass


def _update_repo():
    # TODO: NOT IMPLEMENTED YET
    pass


def _reload_webserver():
    # TODO: NOT IMPLEMENTED YET
    pass


def _reload_supervisor():
    # TODO: NOT IMPLEMENTED YET
    pass


def _start_app():
    # TODO: NOT IMPLEMENTED YET
    pass


def _reload_app():
    # TODO: NOT IMPLEMENTED YET
    pass


def init_deployment():
    # TODO: NOT IMPLEMENTED YET
    pass


def deploy():
    _update_repo()
    _reload_app()
