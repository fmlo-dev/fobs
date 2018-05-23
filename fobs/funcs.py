# coding: utf-8

__all__ = ['multiline',
           'replace',
           'insert',
           'delete',
           'swap']

# standard library
import re
from functools import wraps
from itertools import chain
from logging import getLogger

# module logging
logger = getLogger(__name__)


# decorators
def multiline(func):
    """Decorator that makes single line function compatible with multiple lines.

    The first parameter of function must be a line (str), and the returned value
    must be modified line (str). Then the wrapped function will accept multiple
    lines (str containing multiple '\n') and apply the original function to each
    line. In addition to parameters of the original function, the wrapped one
    has special parameters that controls range wherein the function is applied:

    first (str): Regular expression for the first line of range.
        Default is '.*' (it matches everything and thus means no range).
    last (str):  Regular expression for the last line of range.
        Default is '$.' (it matches nothing and thus means no range).
    line (str): Regular expression for lines to which the function is applied.
        Default is '.*' (it matches everything and thus means no selection).
    nmatch (int): Number of matchings of `first` from which the function is
        applied, i.e., 1st, ..., `nmatch`-1 th matchings of `first` are ignored.
        Default is 1 (1st matching of `first` is used).
    nskip (int): Number of lines to which the function is not applied after
        matching of `first`. Default is 0 (not skipping lines).
    exlast (bool): Whether the function is applied to the last line.
        Default is False (the last line is included within a range).

    Args:
        func (function): Function to be wrapped.

    Returns
        wrapper (function): Wrapped function compatible with multiple lines.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        lines = iter(args[0].split('\n'))
        args  = args[1:]

        # special parameters
        first  = kwargs.pop('first', '.*')
        last   = kwargs.pop('last', '$.')
        line_  = kwargs.pop('line', '.*')
        nmatch = kwargs.pop('nmatch', 1)
        nskip  = kwargs.pop('nskip', 0)
        exlast = kwargs.pop('exlast', False)

        # not applying func before first line is matched
        newlines = []
        counter = 1

        for line in lines:
            if not re.search(first, line):
                newlines.append(line)
                continue

            if not counter == nmatch:
                newlines.append(line)
                counter += 1
                continue

            # undo an iteration
            lines = chain([line], lines)
            break

        # skip line nskip times
        for i in range(nskip):
            line = next(lines, None)

            if line is not None:
                newlines.append(line)

        # applying func until last line is matched
        for line in lines:
            if not re.search(last, line):
                if not re.search(line_, line):
                    newlines.append(line)
                    continue

                newlines.append(func(line, *args, **kwargs))
                continue

            if exlast:
                # undo an iteration
                lines = chain([line], lines)
                break

            newlines.append(func(line, *args, **kwargs))
            break

        return '\n'.join(newlines + list(lines))

    return wrapper


# functions
@multiline
def replace(line, old, new):
    """Replace all of old keyword with new one in line.

    Args:
        line (str): Line to be processed.
        old (str): Regular expression for old keyword.
        new (Str): String with which old keyword is replaced.

    Returns:
        line (str): Processed line.

    """
    return re.sub(old, new, line)


@multiline
def insert(line, string, position='below'):
    """Insert string below or above line (joined with '\n').

    Args:
        line (str): Line to be processed.
        string (str): String to be inserted below/above line.
        position (str): Insertion position. Must be either 'below' or 'above'.

    Returns:
        line (str): Processed line.

    """
    if position == 'below':
        return f'{line}\n{string}'
    elif position == 'above':
        return f'{string}\n{line}'
    else:
        return line


@multiline
def delete(line, mode='comment out', mark='#'):
    """Comment out line.

    Args:
        line (str): Line to be processed.
        mode (str): Deletion mode. Must be either 'remove' (cut whole line) or
            'comment out' (insert mark to line head). Default is 'comment out'.
        mark (str): Comment mark used in the comment out mode. Default is '#'.

    Returns:
        line (str): Processed line.

    """
    if mode == 'remove':
        return ''
    elif mode == 'comment out':
        if re.search(f'^{mark}', line):
            return line
        else:
            return f'{mark} {line}'
    else:
        return line


def swap(lines, line1, line2, separator='='):
    """Swap values of two lines.

    Args:
        lines (str): Lines to be processed.
        line1 (str): Regular expression for line of parameter 1.
        line2 (str): Regular expression for line of parameter 2.
        separator (str): Character that separates parameter and value
            in lines, e.g., <parameter><separator><value>. Default is '='.

    Returns:
        lines (str): Processed line.

    """
    m1 = re.search(f'^.*{line1}.*$', lines, re.M)
    m2 = re.search(f'^.*{line2}.*$', lines, re.M)

    if not (m1 and m2):
        return lines

    l1 = m1.group()
    l2 = m2.group()
    p1, v1 = l1.split(separator)
    p2, v2 = l2.split(separator)
    s1 = separator.join([p1, v2])
    s2 = separator.join([p2, v1])
    return re.sub(l2, s2, re.sub(l1, s1, lines))
