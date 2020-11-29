"""Test Python generators utilities."""

import pytest

from http_request_codegen.python._utils import (
    DEFAULT_INDENT,
    DEFAULT_QUOTE_CHAR,
    repr_dict_kwarg
)


@pytest.mark.parametrize(
    (
        'kwarg_name',
        'dictionary',
        'quote_char',
        'indent',
        'indent_depth',
        'result',
    ),
    (
        # Basic case
        (
            'headers',
            {'Authorization': '__token__', 'Content-Type': 'application/json'},
            DEFAULT_QUOTE_CHAR,
            DEFAULT_INDENT,
            1,
            '''    headers={
        'Authorization': '__token__',
        'Content-Type': 'application/json'
    }'''
        ),

        # Without indentation depth
        (
            'params',
            {'foo': 'bar'},
            DEFAULT_QUOTE_CHAR,
            DEFAULT_INDENT,
            0,
            '''params={
    'foo': 'bar'
}'''
        ),

        # Indentation of two spaces
        (
            'params',
            {'foo': 'bar'},
            DEFAULT_QUOTE_CHAR,
            '  ',
            3,
            '''      params={
        'foo': 'bar'
      }'''
        ),

        # Empty dictionary
        (
            'params',
            {},
            DEFAULT_QUOTE_CHAR,
            '',
            0,
            'params={}'
        ),

        # Invalid Python identifiers as kwarg name
        (
            '123',
            {},
            DEFAULT_QUOTE_CHAR,
            '',
            0,
            ValueError
        ),

        # " quote character
        (
            'headers',
            {'Authorization': '__token__', 'Content-Type': 'application/json'},
            '"',
            DEFAULT_INDENT,
            1,
            '''    headers={
        "Authorization": "__token__",
        "Content-Type": "application/json"
    }'''
        ),

        # Invalid quote character
        (
            'params',
            {},
            '$',
            '',
            0,
            ValueError
        ),
    )
)
def test_python_repr_dict_kwarg(kwarg_name, dictionary, quote_char,
                                indent, indent_depth, result):
    if hasattr(result, '__traceback__'):
        with pytest.raises(result):
            repr_dict_kwarg(kwarg_name, dictionary, quote_char=quote_char,
                            indent=indent, indent_depth=indent_depth)
    else:
        assert repr_dict_kwarg(
            kwarg_name, dictionary, quote_char=quote_char,
            indent=indent, indent_depth=indent_depth
        ) == result
