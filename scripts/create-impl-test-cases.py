#!/usr/bin/env python

"""Creates implementation test cases."""

import argparse
import os
import shutil
import sys

from http_request_codegen import __version__, generate_http_request_code
from http_request_codegen.hrc_factory import (
    DEFAULT_IMPLEMENTATION,
    DEFAULT_LANGUAGE,
)

from tests.combinations import (
    combination_arguments_to_kwargs,
    get_argument_combinations,
)


DESCRIPTION = (
    'Implementation test cases creator. This script creates a'
    ' directory where are placed all expected outputs of a method'
    ' for one implementation supported in http-request-codegen.'
    ' Is needed for help testing this library.'
)


def build_parser():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '-v', '--version', action='version',
        version='%(prog)s ' + __version__,
        help='Show program version number and exit.',
    )
    parser.add_argument(
        '-l', '--language', dest='language',
        default=DEFAULT_LANGUAGE, required=True,
        help='Language or platform for which the test cases'
             ' will be created.', metavar='LANGUAGE',
    )
    parser.add_argument(
        '-i', '--implementation', dest='implementation',
        default=DEFAULT_IMPLEMENTATION, required=True,
        help='Implementation for which the test cases will be'
             ' created.', metavar='IMPLEMENTATION',
    )
    parser.add_argument(
        '-m', '--method', dest='method', default='GET',
        required=True,
        help='HTTP request method for which the test cases'
             ' will be created.', metavar='METHOD',
    )
    parser.add_argument(
        '-d', '--directory', dest='directory', default=None,
        required=True,
        help='Directory inside which the test cases will be'
             ' placed.', metavar='DIR',
    )
    return parser


def parse_options(args=[]):
    parser = build_parser()
    if '-h' in args or '--help' in args:
        parser.print_help()
        sys.exit(0)
    opts, unknown = parser.parse_known_args(args)

    return opts


def main(args=[]):
    opts = parse_options(args=args)

    if os.path.exists(opts.directory):
        sys.stderr.write('The directory \'%s\' exists.\n' % opts.directory)
    os.makedirs(opts.directory, exist_ok=True)

    try:
        for args_group in get_argument_combinations(method=opts.method):
            result = generate_http_request_code(
                language=opts.language,
                impl=opts.implementation,
                method=opts.method,
                **combination_arguments_to_kwargs(args_group['arguments']),
            )

            fpath = os.path.join(opts.directory, args_group['filename'])
            with open(fpath, 'w') as f:
                f.write(result)
    except Exception as err:
        shutil.rmtree(opts.directory)
        raise err

    return 0


if __name__ == '__main__':
    sys.exit(main(args=sys.argv[1:]))
