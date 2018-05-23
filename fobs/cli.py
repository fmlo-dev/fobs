#!/usr/bin/env python
# coding: utf-8

"""fobs: convert 45m/ASTE obstable to one for FMLO observation.

Usage:
  fobs <obstable> <actions> [<substitution>...] [options]
  fobs -h | --help
  fobs -v | --version

Arguments:
  <obstable>         Path of 45/ASTE obstable (*.start)
  <actions>          Path of YAML file that describes actions.
  <substitution>...  String(s) of substitution statement like
                     param=value. This will replace string of
                     <param> with value in the converted obstable.

Options:
  -h --help        Show the help and exit.
  -v --version     Show the version and exit.
  -f --force       Force to overwrite existing obstable.
  -o --out <path>  Path of converted obstable. If not spacified (default),
                   then string of it will be printed to standard output.
  -l --log <path>  Path of log file. If not spacified (default),
                   then log strings will be printed to standard output.

"""

# standard library
import re
import sys
from pathlib import Path
from logging import basicConfig, getLogger

# dependent packages
import fobs
import yaml
from docopt import docopt

# module logger
logger = getLogger(__name__)


# functions
def main(args=None):
    """Main function of fobs command line interface.

    Args:
        args (dict): Dictionary of arguments (i.e., {arg:value}).
            If not spacified (defualt), args parsed by docopt is used.

    Returns:
        this function returns nothing.

    """
    if args is None:
        args = docopt(__doc__, version=fobs.__version__)

    # logging config
    basicConfig(filename=args['--log'], filemode='w',
                datefmt='%Y-%m-%d %H:%M:%S', style='{',
                format='{asctime} | {levelname:7} | {message}')

    # read obstable (*.start) and actions (*.yaml)
    path1 = Path(args['<obstable>']).expanduser()
    path2 = Path(args['<actions>']).expanduser()

    with path1.open() as f1:
        lines = f1.read()

    with path2.open() as f2:
        actions = yaml.load(f2)

    # run actions and replace <param> with value
    for kwargs in actions:
        func = getattr(fobs, kwargs.pop('action'))
        lines = func(lines, **kwargs)

    for state in args['<substitution>']:
        try:
            param, value = state.split('=')
        except ValueError:
            logger.warning(f'Invalid statement: {state}')
            continue

        lines = fobs.replace(lines, f'<{param}>', value)

    # output converted obstable (several options)
    if not args['--out']:
        print(lines)
        sys.exit(0)

    path3 = Path(args['--out']).expanduser()

    if path3.exists() and not args['--force']:
        logger.warning(f'{path3} already exists')
        logger.warning('use -f option to overwrite it')
        sys.exit(0)

    with path3.open('w') as f3:
        f3.write(lines)
        sys.exit(0)


# main
if __name__ == '__main__':
    main()
