#!/usr/bin/env python
import os
from distutils.util import strtobool
from getpass import getpass


DEFAULT_DB_NAME = 'anchor'
DEFAULT_DB_USERNAME = 'postgres'
DEFAULT_MAIL_SERVER = 'smtp.gmail.com'


def ask_boolean(prompt):
    while True:
        try:
            return strtobool(raw_input('{0} [y/n]: '.format(prompt)).lower())
        except ValueError:
            print('Please answer with y or n')


def run():
    try:
        import secret
    except ImportError:
        secret = None
        print('secret.py not found. Following process will create new secret.py')

    prompt = 'Enter database name [{0}]: '.format(DEFAULT_DB_NAME)
    db_name = raw_input(prompt) or DEFAULT_DB_NAME

    prompt = 'Enter database username [{0}]: '.format(DEFAULT_DB_USERNAME)
    db_username = raw_input(prompt) or DEFAULT_DB_USERNAME
    db_password = getpass('Enter database password: ')

    if secret is None or 'SECRET_KEY' not in secret.__dict__:
        print('Secret key not found. Generating...')
        secret_key_changed = True
        secret_key = os.urandom(24).encode('hex')
        print('Secret key generated: {0}'.format(secret_key))
    else:
        secret_key_changed = False
        secret_key = secret.SECRET_KEY

    prompt = 'Enter mail server [{0}]: '.format(DEFAULT_MAIL_SERVER)
    mail_server = raw_input(prompt) or DEFAULT_MAIL_SERVER
    mail_username = raw_input('Enter mail username: ')
    mail_password = getpass('Enter mail password: ')

    secrets = {
        'db_name': db_name,
        'db_username': db_username,
        'db_password': db_password,
        'secret_key': secret_key,
        'changed': 'CHANGED' if secret_key_changed else 'UNCHANGED',
        'mail_server': mail_server,
        'mail_username': mail_username,
        'mail_password': mail_password
    }

    prompt = '\n'.join([
        '\n',
        'Generated secrets are:\n',
        'db_name: {db_name}',
        'db username: {db_username}',
        'db password: {db_password}',
        'secret_key: {secret_key} ({changed})',
        'mail_server: {mail_server}',
        'mail_username: {mail_username}',
        'mail_password: {mail_password}\n',
        'Are you sure to overwrite current secrets?',
    ]).format(**secrets)

    template = '\n'.join([
        "DB_NAME = '{db_name}'",
        "DB_USERNAME = '{db_username}'",
        "DB_PASSWORD = '{db_password}'",
        "SECRET_KEY = '{secret_key}'",
        "MAIL_SERVER = '{mail_server}'",
        "MAIL_USERNAME = '{mail_username}'",
        "MAIL_PASSWORD = '{mail_password}'"
    ]).format(**secrets)

    if ask_boolean(prompt):
        print('\n')
        print('secret.py generated: \n')
        print(template + '\n\n')
        with open('secret.py', 'w') as f:
            f.write(template)
        print('All secrets updated!')
    else:
        print('Secrets not updated!')


if __name__ == '__main__':
    run()
