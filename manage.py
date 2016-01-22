#!/usr/bin/env python
import click

from app import create_app
from app.database import init_db


@click.group(help='anchor backend management cli')
def main():
    pass


@click.command('run', help='run anchor backend server')
@click.option(
    '-c', '--config',
    default='prod', type=click.Choice(['dev', 'test', 'prod'])
)
def run(config):
    app = create_app(config.title())
    app.run()


@click.command('initdb', help='initialize database')
@click.option(
    '-c', '--config',
    default='prod', type=click.Choice(['dev', 'test', 'prod'])
)
def initdb(config):
    init_db(config.title())


main.add_command(run)
main.add_command(initdb)


if __name__ == "__main__":
    main()
