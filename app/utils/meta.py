from flask import current_app


def get_project_name():
    return current_app.config['PROJECT_NAME']

def get_service_name():
    return current_app.config['SERVICE_NAME']
