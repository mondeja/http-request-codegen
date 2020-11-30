"""Utilities for Python HTTP request generators."""

DEFAULT_INDENT = '    '

VALID_QUOTE_CHARS = '"\''
DEFAULT_QUOTE_CHAR = "'"
DEFAULT_WRAP = 80

# TODO: Document all functions.


def validate_python_identifier(value):
    """Validates if a string is a valid Python identifier. If not, raises
    a ValueError.

    Args:
        value (str): Value to validate.

    Raises:
        ValueError: if the string is not a valid Python identifier.

    Examples:
        >>> validate_python_identifier('_hello')
        >>> validate_python_identifier('123')
        Traceback (most recent call last):
          ...
        ValueError: '123' is not a valid Python identifier

        >>> validate_python_identifier(123)
        Traceback (most recent call last):
          ...
        ValueError: '123' is not a valid Python identifier
    """
    try:
        if not value.isidentifier():
            raise ValueError('\'%s\' is not a valid Python identifier' % value)
    except AttributeError:
        raise ValueError(
            '\'%s\' is not a valid Python identifier' % str(value))


def validate_quote_character(char):
    """Validates if a character is a valid Python string quotation character.

    Args:
        char (str): Character to validate.

    Raises:
        ValueError: if the character is not a valid Python string quotation
            character.

    Examples:
        >>> validate_quote_character('"')
        >>> validate_quote_character('1')
        Traceback (most recent call last):
          ...
        ValueError: The character '1' is not a valid Python quotation character
    """
    if char not in VALID_QUOTE_CHARS:
        raise ValueError(('The character \'%s\' is not a valid Python'
                          ' quotation character') % char)


def escape_single_quote(value):
    """Escapes single quotes inside a string.

    Args:
        value (str): String for which single quotes will be escaped.

    Raises:
        TypeError: is the value is not a string.

    Examples:
        >>> print(escape_single_quote("Hello I neeed a ' escape."))
        Hello I neeed a \\' escape.
        >>> print(escape_single_quote(1))
        Traceback (most recent call last):
          ...
        TypeError: The value '1' can not be escaped because is not a string

    Returns:
        str: The string with single quote characters escaped.
    """
    try:
        return value.replace("'", "\\'")
    except AttributeError:
        raise TypeError(('The value \'%s\' can not be escaped because is not'
                         ' a string') % str(value))


def escape_double_quote(value):
    """Escapes double quotes inside a string.

    Args:
        value (str): String for which double quotes will be escaped.

    Raises:
        TypeError: is the value is not a string.

    Examples:
        >>> print(escape_double_quote('Hello I neeed a " escape.'))
        Hello I neeed a \\" escape.
        >>> print(escape_double_quote(1))
        Traceback (most recent call last):
          ...
        TypeError: The value '1' can not be escaped because is not a string

    Returns:
        str: The string with double quote characters escaped.
    """
    try:
        return value.replace('"', '\\"')
    except AttributeError:
        raise TypeError(('The value \'%s\' can not be escaped because is not'
                         ' a string') % str(value))


def escape_quote_func_by_quote_char(char):
    """Get a function that can escape a string quotation character given
    the character. This works as a factory for quotation string characters
    escapes functions.

    Args:
        char (str): Character that the returned function is able to escape.

    Raises:
        ValueError: if the character passed is not a valid Python string
            quotation character.

    Examples:
        >>> func = escape_quote_func_by_quote_char("'")
        >>> print(func("String that must be ' escaped."))
        String that must be \\' escaped.

        >>> escape_quote_func_by_quote_char("?")
        Traceback (most recent call last):
          ...
        ValueError: Character '?' is not a valid Python quotation character

        >>> escape_quote_func_by_quote_char("abc")
        Traceback (most recent call last):
          ...
        ValueError: String 'abc' is not a valid Python quotation character

    Returns:
        function: Function that can escape the character passed as argument.
    """
    try:
        return {
            "'": escape_single_quote,
            '"': escape_double_quote,
        }[char]
    except KeyError:
        raise ValueError(
            ('%s \'%s\' is not a valid Python quotation character') % (
                'Character' if len(char) == 1 else 'String', char))


def escape_by_quote(string, char):
    """Escapes the quote characters of a string.

    Args:
        string (str): String whose qutation characters must be escaped.
        char (str): Quotation character to escape.

    Raises:
        ValueError: If the character to escape is not a valid Python string
            quotation character.
        TypeError: If the value to escape is not a string.

    Examples:
        >>> print(escape_by_quote("I need single quote ' escape.", "'"))
        I need single quote \\' escape.

        >>> print(escape_by_quote('I need double quote " escape.', '"'))
        I need double quote \\" escape.

        >>> escape_by_quote(12, '"')
        Traceback (most recent call last):
          ...
        TypeError: The value '12' can not be escaped because is not a string

        >>> escape_by_quote('I need escape of ? character.', '?')
        Traceback (most recent call last):
          ...
        ValueError: Character '?' is not a valid Python quotation character

        >>> escape_by_quote(12, '?')
        Traceback (most recent call last):
          ...
        ValueError: Character '?' is not a valid Python quotation character

    Returns:
        str: The original string with the specified character escaped.
    """
    return escape_quote_func_by_quote_char(char)(string)


def repr_kwarg(kwarg_name, value, indent=DEFAULT_INDENT, **kwargs):
    """Returns the code of any value passed as Python keyword argument to
    a function. The indentation used before the keyword argument is 4 spaces
    by default.

    Args:
        kwarg_name (str): Name of the argument. Must be a valid Python
            identifier or a `ValueError` will be raised.
        value (object): Value of the argument to be reproduced.
        **kwargs: Arguments passed to the functions ``repr_dict_kwarg`` and
            ``repr_str_kwarg``.

    Raises:
        ValueError: If the argument ``kwarg_name`` is not a valid Python
            identifier.

    Examples:
        >>> print(repr_kwarg('foo', 'bar'))
            foo='bar'
        >>> print(repr_kwarg('foo', 1))
            foo=1
        >>> print(repr_kwarg('foo', dict(bar='baz')))
            foo={
                'bar': 'baz'
            }
        >>> print(repr_kwarg('foo', dict(bar=1, baz=2)))
            foo={
                'bar': 1,
                'baz': 2
            }

        >>> print(repr_kwarg(123, 'a'))
        Traceback (most recent call last):
          ...
        ValueError: '123' is not a valid Python identifier

    Returns:
        str: Code needed to pass an optional keyword argument to a function
            in Python
    """
    # Invalid Python identifiers can't be defined as keyword arguments
    validate_python_identifier(kwarg_name)

    if isinstance(value, dict):
        return repr_dict_kwarg(kwarg_name, value, indent=indent,
                               _validate_identifier=False,
                               **kwargs)
    elif isinstance(value, str):
        return repr_str_kwarg(kwarg_name, value, indent=indent,
                              _validate_identifier=False,
                              **kwargs)
    return '%(indent)s%(kwarg_name)s=%(value)s' % {
        'kwarg_name': kwarg_name,
        'value': value.__repr__(),
        'indent': indent
    }


def repr_str_kwarg(kwarg_name, string, quote_char=DEFAULT_QUOTE_CHAR,
                   indent=DEFAULT_INDENT, _validate_identifier=True):
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

    return '%(indent)s%(kwarg_name)s=%(quote_char)s%(value)s%(quote_char)s' % {
        'kwarg_name': kwarg_name,
        'value': escape_by_quote(string, quote_char),
        'quote_char': quote_char,
        'indent': indent,
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
                'Authorization': '__token__',
                'Content-Type': 'application/json'
            }

        >>> print(repr_dict_kwarg('foo', dict(bar='baz'), quote_char='"'))
            foo={
                "bar": "baz"
            }

        >>> print(repr_dict_kwarg('foo', {'bar': 1}, quote_char="'",
        ...       indent_depth=0))
        foo={
            'bar': 1
        }
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
            if isinstance(value, str):
                _value = '%(quote_char)s%(value)s%(quote_char)s' % {
                    'quote_char': quote_char,
                    'value': value if not _escape_values else
                    escape_quote_func(value)
                }
            else:
                _value = str(value)
            response += ('%(indents)s%(quote_char)s%(key)s%(quote_char)s:'
                         ' %(value)s%(comma)s%(newline)s') % {
                'indents': indent * (indent_depth + 1),
                'key': key if not _escape_keys else escape_quote_func(key),
                'value': _value,
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

        >>> print(raw_str_definition(
        ...           'Lorem Ipsum es simplemente el texto de'
        ...           + ' relleno de las imprentas y archivos de texto.',
        ...           wrap=70, indent=''))
        ('Lorem Ipsum es simplemente el texto de relleno de las imprentas y '
         'archivos de texto.')

        >>> print(raw_str_definition('123', wrap=1, quote_char='"', indent=''))
        ("1"
         "2"
         "3")
    """
    _wrap_at = wrap - len(indent) + len(quote_char) * 2
    string_escaped = string if not _escape else \
        escape_by_quote(string, quote_char)

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
        if _chars_in_current_line >= _wrap_at - 4:
            if i >= len(string) - 1:
                break
            response += '%(quote_char)s\n%(indent)s %(quote_char)s' % {
                'quote_char': quote_char,
                'indent': indent,
            }
            _chars_in_current_line = 2 + len(indent)  # ' ('
    response += '%(quote_char)s)' % {'quote_char': quote_char}
    return response
