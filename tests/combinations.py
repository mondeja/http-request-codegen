'''Test cases arguments combinations.'''

import os
import sys

import inflection


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
if TEST_DIR not in sys.path:
    sys.path.append(TEST_DIR)

from consts import TEMPDIR, TEST_BASE_URL  # noqa: E402

from http_request_codegen.hrc_string import replace_multiple  # noqa: E402


def argument_combination_to_filename(combination_name, index):
    return '{}.{}.expect.txt'.format(
        str(index).zfill(3),
        inflection.parameterize(
            replace_multiple(
                combination_name, replacements={
                    '"': '-double-quote-',
                    '\'': '-single-quote-',
                },
            ),
        ),
    )


def combination_arguments_to_kwargs(arguments):
    kwargs = {}
    for key, value in arguments.items():
        if key == 'kwargs':
            kwargs.update(value)
        else:
            kwargs[key] = value
    return kwargs


def get_argument_combinations(
    method='GET', include_filenames=True,
    dirpath=None,
):
    response = [
        {
            'name': 'URL',
            'arguments': {
                'url': TEST_BASE_URL,
            },
        },
        {
            'name': 'URL wrapping (no wrap)',
            'arguments': {
                'url': TEST_BASE_URL,
                'wrap': 99999,
            },
        },
        {
            'name': 'URL wrapping (wrap 15)',
            'arguments': {
                'url': TEST_BASE_URL,
                'wrap': 15,
            },
        },
        {
            'name': 'Parameter',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                ],
            },
        },
        {
            'name': 'Parameters',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'foo',
                    },
                    {
                        'name': 'param-2',
                        'value': 1,
                    },
                    {
                        'name': 'param-3',
                        'value': .777,
                    },
                    {
                        'name': 'param-4',
                        'value': True,
                    },
                ],
            },
        },
        {
            'name': 'Parameter wrapping value',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'foo-bar-baz' * 50,
                    },
                ],
            },
        },
        {
            'name': 'Parameters, one wrapping value',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'foo-bar-baz' * 50,
                    },
                    {
                        'name': 'param-2',
                        'value': 'value-2',
                    },
                ],
            },
        },
        {
            'name': 'Parameter escaping quotes',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1-with-\'\'-quotes',
                        'value': 'value-1-with-\'\'-quotes',
                    },
                ],
            },
        },
        {
            'name': 'URL + header',
            'arguments': {
                'url': TEST_BASE_URL,
                'headers': {
                    'Content-Type': 'application/json',
                },
            },
        },
        {
            'name': 'URL + headers',
            'arguments': {
                'url': TEST_BASE_URL,
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': 'es',
                },
            },
        },
        {
            'name': 'URL + header wrapping value',
            'arguments': {
                'url': TEST_BASE_URL,
                'headers': {
                    'Content-Type': 'application/json' * 5,
                },
            },
        },
        {
            'name': 'URL + headers, one wrapping value',
            'arguments': {
                'url': TEST_BASE_URL,
                'headers': {
                    'Content-Type': 'application/json' * 5,
                    'Accept-Language': '*',
                },
            },
        },
        {
            'name': 'URL + header escaping quotes',
            'arguments': {
                'url': TEST_BASE_URL,
                'headers': {
                    'Accept-Language': 'Header value with \'\' quotes',
                },
            },
        },
        {
            'name': 'URL + kwarg',
            'arguments': {
                'url': TEST_BASE_URL,
                'kwargs': {
                    'timeout': 5,
                },
            },
        },
        {
            'name': 'URL + kwargs',
            'arguments': {
                'url': TEST_BASE_URL,
                'kwargs': {
                    'timeout': 5,
                    'stream': True,
                },
            },
        },
        {
            'name': 'URL + kwarg escaping quotes',
            'arguments': {
                'url': TEST_BASE_URL,
                'kwargs': {
                    'cookies': {
                        'foo': 'value with \'\' quotes',
                    },
                },
            },
        },
        {
            'name': 'URL + kwarg wrapping value',
            'arguments': {
                'url': TEST_BASE_URL,
                'kwargs': {
                    'cookies': {
                        'bar': 'foo bar baz ' * 50,
                    },
                },
            },
        },
        {
            'name': 'URL + kwargs, one wrapping value',
            'arguments': {
                'url': TEST_BASE_URL,
                'kwargs': {
                    'cookies': {
                        'bar': 'foo bar baz ' * 50,
                    },
                    'stream': True,
                },
            },
        },
        {
            'name': 'Parameter + header',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                ],
                'headers': {
                    'Content-Type': 'application/json',
                },
            },
        },
        {
            'name': 'Parameter + header (oneline)',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                ],
                'headers': {
                    'Content-Type': 'application/json',
                },
                'oneline': True,
            },
        },
        {
            'name': 'Parameters + header',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                    {
                        'name': 'param-2',
                        'value': 'value-2',
                    },
                ],
                'headers': {
                    'Content-Type': 'application/json',
                },
            },
        },
        {
            'name': 'Parameter + headers',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                ],
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': '*',
                },
            },
        },
        {
            'name': 'Parameters + headers',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                    {
                        'name': 'param-2',
                        'value': 'value-2',
                    },
                ],
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': '*',
                },
            },
        },
        {
            'name': 'Parameter + kwarg',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                ],
                'kwargs': {
                    'timeout': 10,
                },
            },
        },
        {
            'name': 'Parameter + kwarg (oneline)',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'a',
                        'value': 'b',
                    },
                ],
                'kwargs': {
                    'timeout': 10,
                },
                'oneline': True,
            },
        },
        {
            'name': 'Parameters + kwarg',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                    {
                        'name': 'param-2',
                        'value': 'value-2',
                    },
                ],
                'kwargs': {
                    'timeout': 10,
                },
            },
        },
        {
            'name': 'Parameter + kwargs',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                ],
                'kwargs': {
                    'timeout': 10,
                    'stream': True,
                },
            },
        },
        {
            'name': 'Parameters + kwargs',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                    {
                        'name': 'param-2',
                        'value': 'value-2',
                    },
                ],
                'kwargs': {
                    'timeout': 10,
                    'stream': True,
                },
            },
        },
        {
            'name': 'URL + header + kwarg',
            'arguments': {
                'url': TEST_BASE_URL,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'kwargs': {
                    'timeout': 5,
                },
            },
        },
        {
            'name': 'URL + header + kwarg (oneline)',
            'arguments': {
                'url': TEST_BASE_URL,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'kwargs': {
                    'timeout': 5,
                },
                'oneline': True,
            },
        },
        {
            'name': 'URL + headers + kwarg',
            'arguments': {
                'url': TEST_BASE_URL,
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': '*',
                },
                'kwargs': {
                    'timeout': 5,
                },
            },
        },
        {
            'name': 'URL + header + kwargs',
            'arguments': {
                'url': TEST_BASE_URL,
                'headers': {
                    'Accept-Language': '*',
                },
                'kwargs': {
                    'timeout': 5,
                    'stream': False,
                },
            },
        },
        {
            'name': 'URL + headers + kwargs',
            'arguments': {
                'url': TEST_BASE_URL,
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': '*',
                },
                'kwargs': {
                    'timeout': 5,
                    'stream': False,
                },
            },
        },
        {
            'name': 'Parameter + header + kwarg',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                ],
                'headers': {
                    'Content-Type': 'application/json',
                },
                'kwargs': {
                    'timeout': 5,
                },
            },
        },
        {
            'name': 'Parameter + header + kwargs',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                ],
                'headers': {
                    'Content-Type': 'application/json',
                },
                'kwargs': {
                    'timeout': 5,
                    'stream': True,
                },
            },
        },
        {
            'name': 'Parameters + header + kwarg',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                    {
                        'name': 'param-2',
                        'value': 7.77,
                    },
                ],
                'headers': {
                    'Content-Type': 'application/json',
                },
                'kwargs': {
                    'timeout': 5,
                },
            },
        },
        {
            'name': 'Parameters + header + kwargs',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                    {
                        'name': 'param-2',
                        'value': 7.77,
                    },
                ],
                'headers': {
                    'Content-Type': 'application/json',
                },
                'kwargs': {
                    'timeout': 5,
                    'stream': False,
                },
            },
        },
        {
            'name': 'Parameters + headers + kwarg',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                    {
                        'name': 'param-2',
                        'value': 7.77,
                    },
                ],
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': 'fr',
                },
                'kwargs': {
                    'timeout': 5,
                },
            },
        },
        {
            'name': 'Parameters + headers + kwargs',
            'arguments': {
                'url': TEST_BASE_URL,
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                    {
                        'name': 'param-2',
                        'value': 7.77,
                    },
                ],
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': 'fr',
                },
                'kwargs': {
                    'timeout': 5,
                    'stream': True,
                },
            },
        },
        {
            'name': 'Setup',
            'arguments': {
                'url': TEST_BASE_URL,
                'setup': True,
            },
        },
        {
            'name': 'No setup',
            'arguments': {
                'url': TEST_BASE_URL,
                'setup': False,
            },
        },
        {
            'name': 'Custom setup',
            'arguments': {
                'url': TEST_BASE_URL,
                'setup': 'custom_setup=1\n\n',
            },
        },
        {
            'name': 'Custom teardown',
            'arguments': {
                'url': TEST_BASE_URL,
                'teardown': '\n\ncustom_teardown=1',
            },
        },
        {
            'name': 'Quote character \'',
            'arguments': {
                'url': TEST_BASE_URL,
                'quote_char': '\'',
            },
        },
        {
            'name': 'Quote character "',
            'arguments': {
                'url': TEST_BASE_URL,
                'quote_char': '"',
            },
        },
        {
            'name': 'Indent 2 spaces',
            'arguments': {
                'url': TEST_BASE_URL,
                'indent': '  ',
                'headers': {
                    'Accept-Language': 'es en fr * ' * 20,
                },
            },
        },
        {
            'name': 'Indent 4 spaces',
            'arguments': {
                'url': TEST_BASE_URL,
                'indent': '    ',
                'headers': {
                    'Accept-Language': 'es en fr * ' * 20,
                },
            },
        },
        {
            'name': 'One line',
            'arguments': {
                'url': TEST_BASE_URL,
                'oneline': True,
            },
        },
        {
            'name': 'One line + no setup',
            'arguments': {
                'url': TEST_BASE_URL,
                'oneline': True,
                'setup': False,
            },
        },
        {
            'name': 'Wrap 0',
            'arguments': {
                'url': TEST_BASE_URL,
                'wrap': 0,
            },
        },
        {
            'name': 'Wrap 1',
            'arguments': {
                'url': TEST_BASE_URL,
                'wrap': 1,
            },
        },
        {
            'name': 'Wrap 10',
            'arguments': {
                'url': TEST_BASE_URL,
                'wrap': 10,
            },
        },
        {
            'name': 'Wrap 20',
            'arguments': {
                'url': TEST_BASE_URL,
                'wrap': 20,
            },
        },
        {
            'name': 'Wrap 25',
            'arguments': {
                'url': TEST_BASE_URL,
                'wrap': 25,
            },
        },
        {
            'name': 'Wrap 30',
            'arguments': {
                'url': TEST_BASE_URL,
                'wrap': 30,
            },
        },
        {
            'name': 'Wrap 35',
            'arguments': {
                'url': TEST_BASE_URL,
                'wrap': 35,
            },
        },
        {
            'name': 'Wrap 40',
            'arguments': {
                'url': TEST_BASE_URL,
                'wrap': 40,
            },
        },
        {
            'name': 'Wrap infinite',
            'arguments': {
                'url': TEST_BASE_URL,
                'wrap': float('inf'),
            },
        },
        {
            'name': 'Wrap null is infinite',
            'arguments': {
                'url': TEST_BASE_URL,
                'wrap': None,
            },
        },
    ]

    if method.lower() == 'post':
        response.extend([
            {
                'name': 'Data by parameter (text/plain)',
                'arguments': {
                    'url': TEST_BASE_URL,
                    'parameters': [
                        {
                            'name': '',
                            'value': 'foo bar baz ' * 3,
                        },
                    ],
                    'headers': {
                        'Content-Type': 'text/plain',
                    },
                },
            },
            {
                'name': 'Data by parameter (text/plain) wrapping value',
                'arguments': {
                    'url': TEST_BASE_URL,
                    'parameters': [
                        {
                            'name': '',
                            'value': 'foo bar baz ' * 30,
                        },
                    ],
                    'headers': {
                        'Content-Type': 'text/plain',
                    },
                },
            },
            {
                'name': 'Data by parameter (application/json)',
                'arguments': {
                    'url': TEST_BASE_URL,
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                    ],
                    'headers': {
                        'Content-Type': 'application/json',
                    },
                },
            },
            {
                'name': 'Data by parameters (application/json)',
                'arguments': {
                    'url': TEST_BASE_URL,
                    'parameters': [
                        {
                            'name': 'param-int',
                            'value': 1,
                        },
                        {
                            'name': 'param-float',
                            'value': .777,
                        },
                        {
                            'name': 'param-bool',
                            'value': True,
                        },
                    ],
                    'headers': {
                        'Content-Type': 'application/json',
                    },
                },
            },
            {
                'name': (
                    'Data by parameter'
                    ' (application/x-www-form-urlencoded)'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                    ],
                    'headers': {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                },
            },
            {
                'name': (
                    'Data by parameters'
                    ' (application/x-www-form-urlencoded)'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'parameters': [
                        {
                            'name': 'param-int',
                            'value': 1,
                        },
                        {
                            'name': 'param-float',
                            'value': .777,
                        },
                        {
                            'name': 'param-bool',
                            'value': True,
                        },
                    ],
                    'headers': {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                },
            },
            {
                'name': 'File by filepath (multipart/form-data)',
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                    },
                },
            },
            {
                'name': 'Files by filepath (multipart/form-data)',
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                },
            },
            {
                'name': 'File by filepath (multipart/form-data) wrapping',
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(
                            TEMPDIR, '%s.ext' % ('foo' * 40),
                        ),
                    },
                },
            },
            {
                'name': (
                    'Files by filepath (multipart/form-data)'
                    ' with Content-Type'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': (
                            os.path.join(TEMPDIR, 'file-1.ext'),
                            'text/plain',
                        ),
                        'param-2': (
                            os.path.join(TEMPDIR, 'file-2.ext'),
                            'text/csv',
                        ),
                    },
                },
            },
            {
                'name': (
                    'File by filepath (multipart/form-data)'
                    ' with Content-Type wrapping'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': (
                            os.path.join(TEMPDIR, 'file-1.ext'),
                            'text/plain ' * 20,
                        ),
                    },
                },
            },
            {
                'name': (
                    'File by filepath (multipart/form-data),'
                    ' Content-Type, header'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': (
                            os.path.join(TEMPDIR, 'file-1.ext'),
                            'text/plain',
                            {'Accept-Language': 'es'},
                        ),
                    },
                },
            },
            {
                'name': (
                    'File by filepath (multipart/form-data),'
                    ' Content-Type, headers'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': (
                            os.path.join(TEMPDIR, 'file-1.ext'),
                            'text/plain',
                            {
                                'Accept-Language': 'es',
                                'Accept-Charset': 'utf-8',
                            },
                        ),
                    },
                },
            },
            {
                'name': 'Files by filepath (multipart/form-data) + parameter',
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                    ],
                },
            },
            {
                'name': 'Files by filepath (multipart/form-data) + parameters',
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                        {
                            'name': 'param-2',
                            'value': 'value-2',
                        },
                    ],
                },
            },
            {
                'name': (
                    'Files by filepath (multipart/form-data) + parameter'
                    ' + header'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                    ],
                    'headers': {
                        'Accept-Language': 'fr',
                    },
                },
            },
            {
                'name': (
                    'Files by filepath (multipart/form-data) + parameter'
                    ' + headers'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                    ],
                    'headers': {
                        'Accept-Language': 'fr',
                        'Accept-Charset': 'utf-8',
                    },
                },
            },
            {
                'name': (
                    'Files by filepath (multipart/form-data) + parameters'
                    ' + header'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                        {
                            'name': 'param-2',
                            'value': 'value-2',
                        },
                    ],
                    'headers': {
                        'Accept-Language': 'es',
                    },
                },
            },
            {
                'name': (
                    'Files by filepath (multipart/form-data) + parameters'
                    ' + headers'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                        {
                            'name': 'param-2',
                            'value': 'value-2',
                        },
                    ],
                    'headers': {
                        'Accept-Language': 'fr',
                        'Accept-Charset': 'utf-8',
                    },
                },
            },
            {
                'name': (
                    'Files by filepath (multipart/form-data) + parameter'
                    ' + header + kwarg'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                    ],
                    'headers': {
                        'Accept-Language': 'fr',
                    },
                    'kwargs': {
                        'timeout': 10,
                    },
                },
            },
            {
                'name': (
                    'Files by filepath (multipart/form-data) + parameter'
                    ' + headers + kwarg'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                    ],
                    'headers': {
                        'Accept-Language': 'fr',
                        'Accept-Charset': 'utf-8',
                    },
                    'kwargs': {
                        'timeout': 10,
                    },
                },
            },
            {
                'name': (
                    'Files by filepath (multipart/form-data) + parameters'
                    ' + header + kwarg'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                        {
                            'name': 'param-2',
                            'value': 'value-2',
                        },
                    ],
                    'headers': {
                        'Accept-Language': 'fr',
                    },
                    'kwargs': {
                        'timeout': 10,
                    },
                },
            },
            {
                'name': (
                    'Files by filepath (multipart/form-data) + parameters'
                    ' + headers + kwarg'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                        {
                            'name': 'param-2',
                            'value': 'value-2',
                        },
                    ],
                    'headers': {
                        'Accept-Language': 'fr',
                        'Accept-Charset': 'utf-8',
                    },
                    'kwargs': {
                        'timeout': 10,
                    },
                },
            },
            {
                'name': (
                    'Files by filepath (multipart/form-data) + parameter'
                    ' + header + kwargs'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                    ],
                    'headers': {
                        'Accept-Language': 'fr',
                    },
                    'kwargs': {
                        'timeout': 10,
                        'cookies': {
                            'hello': 'world',
                        },
                    },
                },
            },
            {
                'name': (
                    'Files by filepath (multipart/form-data) + parameter'
                    ' + headers + kwargs'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                    ],
                    'headers': {
                        'Accept-Language': 'fr',
                        'Accept-Charset': 'utf-8',
                    },
                    'kwargs': {
                        'timeout': 10,
                        'stream': False,
                    },
                },
            },
            {
                'name': (
                    'Files by filepath (multipart/form-data) + parameters'
                    ' + header + kwargs'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                        {
                            'name': 'param-2',
                            'value': 'value-2',
                        },
                    ],
                    'headers': {
                        'Accept-Language': 'fr',
                    },
                    'kwargs': {
                        'timeout': 10,
                        'stream': False,
                    },
                },
            },
            {
                'name': (
                    'Files by filepath (multipart/form-data) + parameters'
                    ' + headers + kwargs'
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                        {
                            'name': 'param-2',
                            'value': 'value-2',
                        },
                    ],
                    'headers': {
                        'Accept-Language': 'fr',
                        'Accept-Charset': 'utf-8',
                    },
                    'kwargs': {
                        'timeout': 10,
                        'stream': False,
                    },
                },
            },
            {
                'name': (
                    'No setup + files by filepath (multipart/form-data)'
                    ' + parameters + headers + kwargs + '
                ),
                'arguments': {
                    'url': TEST_BASE_URL,
                    'setup': False,
                    'files': {
                        'param-1': os.path.join(TEMPDIR, 'file-1.ext'),
                        'param-2': os.path.join(TEMPDIR, 'file-2.ext'),
                    },
                    'parameters': [
                        {
                            'name': 'param-1',
                            'value': 'value-1',
                        },
                        {
                            'name': 'param-2',
                            'value': 'value-2',
                        },
                    ],
                    'headers': {
                        'Accept-Language': 'fr',
                        'Accept-Charset': 'utf-8',
                    },
                    'kwargs': {
                        'timeout': 10,
                        'stream': False,
                    },
                },
            },
        ])

    if include_filenames:
        for index, args_group in enumerate(response):
            fname = argument_combination_to_filename(
                args_group['name'], index,
            )
            if dirpath and os.path.exists(dirpath):
                fname = os.path.join(dirpath, fname)
            args_group['filename'] = fname
    return response
