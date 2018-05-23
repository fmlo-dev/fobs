# :globe_with_meridians: fobs
Convert 45m/ASTE obstable to one for FMLO observation

## Installation

```
$ pip install fobs
```

Note that Python 3.6 or higher is required for fobs.

## Command line interface

Command line interface `fobs` is available after installation.

```
$ fobs -h
fobs: convert 45m/ASTE obstable to one for FMLO observation.

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
```

### Actions

#### Replace

#### Insert

#### Delete

#### Swap

### Substitutions
