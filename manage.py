#!/usr/bin/env python
import click


@click.group(help='anchor backend management cli')
def main():
    pass


@click.command('run', help='run anchor backend server')
@click.option(
    '-c', '--config',
    default='prod', type=click.Choice(['dev', 'test', 'prod'])
)
def run(config):
    pass


@click.command('dbinit', help='initialize database')
def dbinit():
    pass


main.add_command(run)
main.add_command(dbinit)


if __name__ == "__main__":
    main()
