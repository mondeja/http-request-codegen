"""Test Python requests library generators."""

import re

import pytest

from http_request_codegen.generators.python._utils import (
    DEFAULT_INDENT,
    DEFAULT_QUOTE_CHAR
)
from http_request_codegen.generators.python.requests import get as requests_get


# from faker.providers.lorem.en_US import Provider as EnUsLoremProvider


#   - url
#   - url + parameter
#   - url + parameters
#   - url + header
#   - url + headers
#   - url + kwarg
#   - url + kwargs
#   - url + parameter  + header
#   - url + parameters + header
#   - url + parameter  + headers
#   - url + parameters + headers
#   - url + parameter  + header + kwarg
#   - url + parameter  + header + kwargs
#   - url + parameters + header + kwarg
#   - url + parameters + header + kwargs
#   - url + parameter  + headers + kwargs
#   - url + parameters + headers + kwargs
#   - url + parameter + kwarg
#   - url + parameters + kwarg
#   - url + parameter + kwargs
#   - url + parameters + kwargs
#   - url + header + kwarg
#   - url + headers + kwarg
#   - url + header + kwargs
#   - url + headers + kwargs

# init
# no init
# quote_char '
# quote_char DEFAULT_QUOTE_CHAR
# quote_char "
# indent '  '
# indent '    '
# indent DEFAULT_INDENT
# indent \t
# oneline
# wrap DEFAULT_WRAP
# wrap 1
# wrap DEFAULT_WRAP + 1
# wrap DEFAULT_WRAP + 2
# wrap DEFAULT_WRAP - 1
# wrap DEFAULT_WRAP - 2
# wrap 99999

"""
# Basic complete case
(
    'localhost',
    [
        {
            'name': 'foo',
            'type': 'str',
        }
    ],
    {'Content-Type': 'application/json'},
    DEFAULT_INDENT,
    DEFAULT_QUOTE_CHAR,
    None,
    True,
    False,
    {'stream': True, 'timeout': 2.5},
    re.escape('''import requests

req = requests.get(
'localhost',
params={
'foo': \'''') + '(?P<foo>[^\']+)' + re.escape('''\'
},
headers={
'Content-Type': 'application/json'
},
stream=True,
timeout=2.5
)'''),
    {'foo': EnUsLoremProvider.word_list}
),
"""


@pytest.mark.parametrize(
    (
        'url',
        'parameters',
        'headers',
        'indent',
        'quote_char',
        'seed',
        'init',
        'oneline',
        'kwargs',
        'result_regex',
        'possible_groups',
    ),
    (
        # Basic simple case
        (
            'localhost',
            [],
            {},
            DEFAULT_INDENT,
            DEFAULT_QUOTE_CHAR,
            None,
            True,
            False,
            {},
            '''import requests

req = requests.get('localhost')''',
            {}
        ),


        # Headers
        #   one
        (
            'localhost',
            [],
            {'Content-Type': 'application/json'},
            DEFAULT_INDENT,
            DEFAULT_QUOTE_CHAR,
            None,
            True,
            False,
            {},
            ('import requests\n\n'
             'req = requests.get(\'localhost\', headers={'
             '\'Content-Type\': \'application/json\'})'),
            {}
        ),
        #   two
        (
            'localhost',
            [],
            {
                'Content-Type': 'application/json',
                'Accept-Language': '*',
            },
            DEFAULT_INDENT,
            DEFAULT_QUOTE_CHAR,
            None,
            True,
            False,
            {},
            '''import requests

req = requests.get(
    'localhost',
    headers={
        'Content-Type': 'application/json',
        'Accept-Language': '*'
    }
)''',
            {}
        ),

        # Indentation of two spaces
        (
            'localhost',
            [],
            {
                'Content-Type': 'application/json',
                'Accept-Language': '*',
            },
            '  ',
            DEFAULT_QUOTE_CHAR,
            None,
            True,
            False,
            {},
            '''import requests

req = requests.get(
  'localhost',
  headers={
    'Content-Type': 'application/json',
    'Accept-Language': '*'
  }
)''',
            {},
        ),

        # Double quote character
        (
            'localhost',
            [],
            {
                'Content-Type': 'application/json',
                'Accept-Language': '*',
            },
            DEFAULT_INDENT,
            '"',
            None,
            True,
            False,
            {},
            '''import requests

req = requests.get(
    "localhost",
    headers={
        "Content-Type": "application/json",
        "Accept-Language": "*"
    }
)''',
            {},
        ),

        # One line
        (
            'localhost',
            [],
            {
                'Content-Type': 'application/json',
                'Accept-Language': '*',
            },
            DEFAULT_INDENT,
            DEFAULT_QUOTE_CHAR,
            None,
            True,
            True,
            {'stream': True, 'timeout': 2.5},
            ('import requests;req = requests.get(\'localhost\', headers={'
             '\'Content-Type\': \'application/json\','
             '\'Accept-Language\': \'*\'}, stream=True, timeout=2.5);'),
            {},
        ),

    )
)
def test_python_requests_get(url, parameters, headers, indent, quote_char,
                             seed, init, oneline, kwargs, result_regex,
                             possible_groups):
    result = requests_get(
        url,
        parameters=parameters,
        headers=headers,
        indent=indent,
        quote_char=quote_char,
        init=init,
        seed=seed,
        oneline=oneline,
        **kwargs
    )
    if possible_groups:
        matches = re.search(result_regex, result)
        assert matches
        for group, possible_values in possible_groups.items():
            assert matches.group(group) in possible_values
    else:
        assert result == result_regex
