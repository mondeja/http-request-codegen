'''Utilities for Javascript HTTP request generators.'''

from http_request_codegen.hrc_string import (
    escape_backtick,
    escape_double_quote,
    escape_single_quote,
    lazy_escape_quote_func_by_quote_char
)


DEFAULT_INDENT = '  '
DEFAULT_QUOTE_CHAR = "'"
DEFAULT_WRAP = 80


def escape_by_quote(string, char):
    '''Escapes the quote characters of a string.

    Args:
        string (str): String whose qutation characters must be escaped.
        char (str): Quotation character to escape.

    Raises:
        ValueError: If the character to escape is an invalid Javascript string
            quotation character.
        TypeError: If the value to escape is not a string.

    Examples:
        >>> print(escape_by_quote("I need single quote ' escape.", "'"))
        I need single quote \\' escape.

        >>> print(escape_by_quote("I need two single quote '' escapes.", "'"))
        I need two single quote \\'\\' escapes.

        >>> print(escape_by_quote('I need double quote " escape.', '"'))
        I need double quote \\" escape.

        >>> print(escape_by_quote('I need two double quote "" escapes.', '"'))
        I need two double quote \\"\\" escapes.

        >>> escape_by_quote(12, '"')
        Traceback (most recent call last):
          ...
        TypeError: The value '12' can not be escaped because is not a string

        >>> escape_by_quote('I need escape of ? character.', '?')
        Traceback (most recent call last):
          ...
        ValueError: '?' is an invalid Javascript quotation character

        >>> escape_by_quote(12, '?')
        Traceback (most recent call last):
          ...
        ValueError: '?' is an invalid Javascript quotation character

    Returns:
        str: The original string with the specified character escaped.
    '''
    return lazy_escape_quote_func_by_quote_char(
        char,
        replacers_funcs={
            '"': escape_double_quote,
            '\'': escape_single_quote,
            '`': escape_backtick
        },
        error_msg_schema=('%(quote_char)s is an invalid Javascript quotation'
                          ' character')
    )(string)


def str_definition(string, indent=DEFAULT_INDENT,
                   quote_char=DEFAULT_QUOTE_CHAR, wrap=DEFAULT_WRAP,
                   _escape=True):
    '''Creates a definition of a Javascript string, multilining it if
    neccesary. Does not handle spaces at all wrapping it, so it's useful to
    efficiently wrap non-spaced strings like URLs.

    Args:
        string (str): String to be reproducted.
        indent (str): Indentation string. This defines the space at the left of
            the string in the code with respect to column 0 of the code.
        quote_char (str): Quotation mark character used in the string. Must be
            a valid Python string quotation character or a `ValueError` will be
            raised.
        wrap (int): Maximum anchor in which the string will be wrapped in
            multiples lines with respect to column 0 of the code.
        _escape (bool): Defines if the reproducted string must be escaped by
            the given ``quote_char`` argument.

    Raises:
        ValueError: if the argument ``quote_char`` is not a valid Javascript
            string quotation character.

    Examples:

        >>> print(str_definition(
        ...           'Lorem Ipsum es simplemente el texto de'
        ...           + ' relleno de las imprentas y archivos de texto. Lorem'
        ...           + ' Ipsum ha sido el texto de relleno estándar de las'
        ...           + ' industrias desde el año 1500.',
        ...           wrap=70, indent=''))
        'Lorem Ipsum es simplemente el texto de relleno de las imprentas y a'
        + 'rchivos de texto. Lorem Ipsum ha sido el texto de relleno estánda'
        + 'r de las industrias desde el año 1500.'

    Returns:
        str: Javascript string definition reproducted.
    '''
    string_escaped = string if not _escape else \
        escape_by_quote(str(string), quote_char)

    if len(str(string)) + len(indent) + len(quote_char) * 2 < wrap:
        return '%(quote_char)s%(value)s%(quote_char)s' % {
            'quote_char': quote_char,
            'value': string_escaped,
        }

    indent_length = len(indent)
    response = '%(quote_char)s' % {
        'quote_char': quote_char
    }
    _chars_in_current_line = len(response) + indent_length
    for i, ch in enumerate(string):
        response += ch
        _chars_in_current_line += 1
        if _chars_in_current_line >= wrap - 2:
            if i >= len(string) - 1:
                break
            response += '%(quote_char)s\n%(indent)s+ %(quote_char)s' % {
                'quote_char': quote_char,
                'indent': indent,
            }
            _chars_in_current_line = 3 + indent_length  # ' ('
    response += '%(quote_char)s%(newline)s%(indent)s' % {
        'newline': '\n' if _chars_in_current_line >= wrap - 1 else '',
        'indent': indent if _chars_in_current_line >= wrap - 1 else '',
        'quote_char': quote_char,
    }
    return response
