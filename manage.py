#!/usr/bin/env python
import click

from app import (
    create_app,
    setup_db
)


@click.group(help='anchor backend management cli')
def main():
    pass


@click.command('run', help='run anchor backend server')
@click.option(
    '-c', '--config',
    default='dev', type=click.Choice(['dev', 'test', 'prod'])
)
def run(config):
    create_app(config.title()).run(debug=True)


@click.command('setup', help='initialize database')
@click.option(
    '-c', '--config',
    default='prod', type=click.Choice(['dev', 'test', 'prod'])
)
def setup(config):
    app = create_app(config.title())
    setup_db(app)


main.add_command(run)
main.add_command(setup)


if __name__ == "__main__":
    main()
