"""Utilities for Python HTTP request generators."""

DEFAULT_INDENT = '    '

VALID_QUOTE_CHARS = '"\''
DEFAULT_QUOTE_CHAR = "'"
DEFAULT_WRAP = 80

# TODO: Document all functions.


def validate_python_identifier(value):
    if not value.isidentifier():
        raise ValueError('\'%s\' is not a valid Python identifier' % value)


def validate_quote_character(char):
    if char not in VALID_QUOTE_CHARS:
        raise ValueError(('The character %s is not a valid Python'
                          ' quotation character') % char)


def escape_single_quote(value):
    return value.replace("'", "\\'")


def escape_double_quote(value):
    return value.replace('"', '\\"')


def escape_quote_func_by_quote_char(quote_char):
    return escape_single_quote \
        if quote_char == "'" else escape_double_quote


def escape_quote(value, quote_char):
    return escape_quote_func_by_quote_char(quote_char)(value)


def repr_kwarg(kwarg_name, value, **kwargs):
    """Returns the code of any value passed as Python keyword argument to
    a function.

    Args:
        kwarg_name (str): Name of the argument. Must be a valid Python
            identifier or a `ValueError` will be raised.
        value (object): Value of the argument to be reproduced.

    TODO: Add examples.
    """
    # Invalid Python identifiers can't be defined as keyword arguments
    validate_python_identifier(kwarg_name)

    if isinstance(value, dict):
        return repr_dict_kwarg(kwarg_name, value,
                               _validate_identifier=False,
                               **kwargs)
    elif isinstance(value, str):
        return repr_str_kwarg(kwarg_name, value,
                              _validate_identifier=False,
                              **kwargs)
    return '%(kwarg_name)s=%(value)s' % {
        'kwarg_name': kwarg_name,
        'value': value.__repr__(),
    }


def repr_str_kwarg(kwarg_name, string, quote_char=DEFAULT_QUOTE_CHAR,
                   _validate_identifier=True):
    """Returns the code of a string passed as Python keyword argument to
    a function.

    Args:
        kwarg_name (str): Name of the argument. Must be a valid Python
            identifier or a `ValueError` will be raised.
        dictionary (str): Dictionary of keys-values shown as passed to the
            argument of the function.
        quote_char (str): Quotation mark character used in strings. Must be
            a valid Python quotation character or a `ValueError` will be
            raised.

    TODO: Add examples.
    """
    if _validate_identifier:
        validate_python_identifier(kwarg_name)
    validate_quote_character(quote_char)

    return '%(kwarg_name)s=%(quote_char)s%(value)s%(quote_char)s' % {
        'kwarg_name': kwarg_name,
        'value': escape_quote(string, quote_char),
        'quote_char': quote_char,
    }


def repr_dict_kwarg(kwarg_name, dictionary, quote_char=DEFAULT_QUOTE_CHAR,
                    indent=DEFAULT_INDENT, indent_depth=1, newline='\n',
                    _validate_identifier=True, _validate_quote_char=True,
                    _escape_keys=True, _escape_values=True):
    """Returns the code of a dictionary passed as Python keyword argument
    to a function.

    Args:
        kwarg_name (str): Name of the argument. Must be a valid Python
            identifier or a `ValueError` will be raised.
        dictionary (str): Dictionary of keys-values shown as passed to the
            argument of the function.
        quote_char (str): Quotation mark character used in strings. Must be
            a valid Python quotation character or a `ValueError` will be
            raised.
        indent (str): Indentation string.
        indent_depth (int): First indentation level.
        newline (str): Newline string.

    Examples:
        >>> print(
        ...     repr_dict_kwarg(
        ...         'headers',
        ...         {'Authorization': '__token__',
        ...          'Content-Type': 'application/json'}
        ...     )
        ... )
            headers={
                "Authorization": "__token__",
                "Content-Type": "application/json",
            }

    # TODO: Add more examples.
    """
    # Invalid Python identifiers can't be defined as keyword arguments
    if _validate_identifier:
        validate_python_identifier(kwarg_name)
    if _validate_quote_char:
        validate_quote_character(quote_char)

    escape_quote_func = escape_quote_func_by_quote_char(quote_char)

    response = '%(indent)s%(kwarg_name)s={' % {
        'indent': indent * indent_depth,
        'kwarg_name': kwarg_name,
    }
    if dictionary:
        response += newline
        for i, (key, value) in enumerate(dictionary.items()):
            response += ('%(indents)s%(quote_char)s%(key)s%(quote_char)s:'
                         ' %(quote_char)s%(value)s%(quote_char)s%(comma)s'
                         '%(newline)s') % {
                'indents': indent * (indent_depth + 1),
                'key': key if not _escape_keys else escape_quote_func(key),
                'value': value if not _escape_values else
                escape_quote_func(value),
                'quote_char': quote_char,
                'newline': newline,
                'comma': ',' if i < len(dictionary) - 1 else '',
            }
    response += '%(indent)s}' % {'indent': indent * indent_depth}
    return response


def raw_str_definition(string, indent=DEFAULT_INDENT,
                       quote_char=DEFAULT_QUOTE_CHAR, wrap=DEFAULT_WRAP,
                       _escape=False):
    """Creates a definition of a Python string, multilining it if neccesary.
    Does not handle spaces at all.

    Examples:

        >>> print(raw_str_definition(('Lorem Ipsum es simplemente el texto de'
        ...                           ' relleno de las imprentas y archivos de'
        ...                           ' texto.', wrap=70))
        ('Lorem Ipsum es simplemente el texto de relleno de las imprenta'
         's y archivos de texto.')

        >>> print(raw_str_definition('123', wrap=1, quote_char='"'))
        ("1"
         "2"
         "3")
    """
    _wrap_at = wrap - len(indent) + len(quote_char) * 2
    string_escaped = string if not _escape else \
        escape_quote(string, quote_char)

    if len(string) < _wrap_at:
        return '%(quote_char)s%(value)s%(quote_char)s' % {
            'quote_char': quote_char,
            'value': string_escaped,
        }

    response = '(%(quote_char)s' % {
        'quote_char': quote_char
    }
    _chars_in_current_line = len(response) + len(indent)
    for i, ch in enumerate(string):
        response += ch
        _chars_in_current_line += 1
        if _chars_in_current_line >= _wrap_at:
            if i >= len(string) - 1:
                break
            response += '%(quote_char)s\n%(indent)s %(quote_char)s' % {
                'quote_char': quote_char,
                'indent': indent,
            }
            _chars_in_current_line = 2 + len(indent)  # ' ('
    response += '%(quote_char)s)' % {'quote_char': quote_char}
    return response
