"""http-request-codegen string utilities."""

import importlib
import random
from collections.abc import Iterable
from types import GeneratorType

from http_request_codegen.hrc_meta import CallableTypes


def lazy_string(string, seed=None, string_func_path=False):
    """Builds a string given an iterable, a callable or the string itself (in
    this case does not transforms it). Useful to randomize a string following
    multiple strategies. Using ``string_func_path``, takes the string as
    a module-callable/iterable path.

    This function is recursive, so if you passes callables as result of your
    callable, make sure that one of them returns other non callable object
    or a ``RecursionError`` will be raised.

    Args:
        string (str/iterable/callable): String or possibilities of strings that
            can be used to build the output. Any other type like numbers or
            booleans will return the ``__repr__`` method of the object.
        seed (int): Seed used in randomization calls.
        string_func_path (bool): If ``True`` and ``string`` is of type ``str``,
            will try to import an object of a module assuming that the string
            has the form ``'path.to.module::object'``. Will raise a
            ``ModuleNotFoundError`` if the module can't be imported or a
            ``ImportError`` if the object to import does not exists in the
            module.

    Examples:
        >>> # String input
        >>> lazy_string('foo')
        'foo'

        >>> # List input
        >>> result = lazy_string(['foo', 'bar'])
        >>> result in ('foo', 'bar')
        True

        >>> # Set input
        >>> result = lazy_string({'foo', 'bar'})
        >>> result in ('foo', 'bar')
        True

        >>> # Tuple input
        >>> result = lazy_string(('foo', 'bar'))
        >>> result in ('foo', 'bar')
        True

        >>> # Generator input
        >>> result = lazy_string((s for s in ('foo', 'bar')))
        >>> result in ('foo', 'bar')
        True

        >>> # Function input
        >>> def func():
        ...     return ['foo', 'bar']
        >>> result = lazy_string(func)
        >>> result in ('foo', 'bar')
        True

        >>> # Function that returns itself
        >>> def func_returning_itself():
        ...     return func_returning_itself
        >>> result = lazy_string(func_returning_itself)
        Traceback (most recent call last):
        ...
        RecursionError: maximum recursion depth exceeded in comparison

        >>> # Lambda input
        >>> result = lazy_string(lambda: ('foo', 'bar'))
        >>> result in ('foo', 'bar')
        True

        >>> # Method input
        >>> class Foo(object):
        ...     def bar(self):
        ...         return ('foo', 'bar')
        >>> result = lazy_string(Foo().bar)
        >>> result in ('foo', 'bar')
        True

        >>> # Boolean input
        >>> lazy_string(False)
        'False'

        >>> # Integer input
        >>> lazy_string(1)
        '1'

        >>> # Float input
        >>> lazy_string(5.73)
        '5.73'

        >>> # Type input
        >>> lazy_string(str)
        'str'

    Raises:
        ValueError: if the value is an empty iterable (although this not
            applies to string types) or if ``string_func_path`` is ``True`` but
            '::' is not used to define the path to a Python function.
        ModuleNotFoundError: if ``string_func_path`` is ``True`` but the
            provided module can't be imported.

    Returns:
        str: A string resulted from one of the strategies, depends on the input
            data type.
    """
    if isinstance(string, str):
        if not string_func_path:
            return string
        try:
            module_path, resolver_name = string.split('::')
        except ValueError as err:
            if '::' not in string:
                return string
            raise err
        # here raises ``ModuleNotFoundError`` if not module
        mod = importlib.import_module(module_path)
        try:
            resolved = getattr(mod, resolver_name)
        except AttributeError:
            raise ImportError(
                ('Object \'%s\' not found in module \'%s\'') % (
                    resolver_name, module_path,
                ),
            )
        return lazy_string(
            resolved,
            seed=seed,
            string_func_path=string_func_path,
        )
    elif isinstance(string, Iterable):
        if not string:
            # Prevent IndexError in ``random.choice``
            raise ValueError(
                'The iterable used to build a lazy string can'
                ' not be empty.',
            )

        if isinstance(string, (set, GeneratorType)):
            string = list(string)
        if seed is not None:
            random.seed(seed)
        return lazy_string(
            random.choice(string),
            seed=seed,
            string_func_path=string_func_path,
        )
    elif isinstance(string, CallableTypes):
        if seed is not None:
            random.seed(seed)
        return lazy_string(
            string(),
            seed=seed,
            string_func_path=string_func_path,
        )
    elif hasattr(string, '__name__'):
        return string.__name__
    return str(string)


def replace_multiple(string, replacements={}):
    """Replaces multiple strings inside a string.

    Args:
        string (str): String to replace.
        replacements (dict): Custom replacements for the string.

    Examples:
        >>> print(replace_multiple('Replace this ".',
        ...                         replacements={'"': 'double quote'}))
        Replace this double quote.

    Returns:
        str: Input string with multiple replaces performed.
    """
    for replacer, replacement in replacements.items():
        string = string.replace(replacer, replacement)
    return string


def escape_single_quote(value):
    '''Escapes single quotes inside a string.

    Args:
        value (str): String for which single quotes will be escaped.

    Raises:
        TypeError: is the value is not a string.

    Examples:
        >>> print(escape_single_quote("Hello I neeed a ' escape."))
        Hello I neeed a \\' escape.
        >>> print(escape_single_quote("Hello I neeed two '' escapes."))
        Hello I neeed two \\'\\' escapes.
        >>> print(escape_single_quote(1))
        Traceback (most recent call last):
        ...
        TypeError: The value '1' can not be escaped because is not a string

    Returns:
        str: The string with single quote characters escaped.
    '''
    try:
        return value.replace("'", "\\'")
    except AttributeError:
        raise TypeError((
            'The value \'%s\' can not be escaped because is not'
            ' a string'
        ) % str(value))


def escape_double_quote(value):
    '''Escapes double quotes inside a string.

    Args:
        value (str): String for which double quotes will be escaped.

    Raises:
        TypeError: is the value is not a string.

    Examples:
        >>> print(escape_double_quote('Hello I neeed a " escape.'))
        Hello I neeed a \\" escape.
        >>> print(escape_double_quote('Hello I neeed two "" escapes.'))
        Hello I neeed two \\"\\" escapes.
        >>> print(escape_double_quote(1))
        Traceback (most recent call last):
        ...
        TypeError: The value '1' can not be escaped because is not a string

    Returns:
        str: The string with double quote characters escaped.
    '''
    try:
        return value.replace('"', '\\"')
    except AttributeError:
        raise TypeError((
            'The value \'%s\' can not be escaped because is not'
            ' a string'
        ) % str(value))


def escape_backtick(value):
    '''Escapes backticks inside a string.

    Args:
        value (str): String for which backticks will be escaped.

    Raises:
        TypeError: is the value is not a string.

    Examples:
        >>> print(escape_backtick('Hello I neeed a ` escape.'))
        Hello I neeed a \\` escape.
        >>> print(escape_backtick('Hello I neeed two `` escapes.'))
        Hello I neeed two \\`\\` escapes.
        >>> print(escape_backtick(1))
        Traceback (most recent call last):
        ...
        TypeError: The value '1' can not be escaped because is not a string

    Returns:
        str: The string with double quote characters escaped.
    '''
    try:
        return value.replace('`', '\\`')
    except AttributeError:
        raise TypeError((
            'The value \'%s\' can not be escaped because is not'
            ' a string'
        ) % str(value))


def lazy_escape_quote_func_by_quote_char(
    quote_char,
    replacers_funcs={'"': escape_double_quote, '\'': escape_single_quote},
    error_msg_schema='Invalid quotation character %(quote_char)s',
    exception_cls=ValueError,
):
    '''Factory for quote-escaping functions. It is designed to be used in
    languages utilities implementations to make easier to build quotation
    character functions.

    Arguments:
        quote_char (str): Character to escape.
        replacers_funcs (dict): Mapping of quotation characters to escape
            functions.
        error_msg_schema (str): Schema string that will be the error message
            displayed if the quotation character is not handled by
            ``replacers_funcs`` mapping. Takes the optional named sustituion
            ``'quote_char'`` that will be replaced by the quotation character
            passed in ``quote_char`` parameter.
        exception_cls (type): Exception to be raised if the quotation character
            is not handled by ``replacers_funcs`` mapping.

    Returns:
        str: Quotation character escape function for a string.
    '''
    try:
        return replacers_funcs[quote_char]
    except KeyError:
        if '%(quote_char)s' in error_msg_schema:
            _quote_quote_char = '"' if quote_char == '\'' else '\''
            error_msg_schema = error_msg_schema % {
                'quote_char': (
                    _quote_quote_char + str(quote_char) + _quote_quote_char
                ),
            }
        raise exception_cls(error_msg_schema)
