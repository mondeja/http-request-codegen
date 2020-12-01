'''Parameter value formatter factory.'''

import importlib
import random
import uuid
from collections.abc import Iterable
from functools import lru_cache
from types import FunctionType, GeneratorType, LambdaType, MethodType

from faker import Faker
from faker.providers import (
    file as faker_file_provider,
    lorem as faker_lorem_provider
)


CallableTypes = (FunctionType, MethodType, LambdaType)


@lru_cache(maxsize=32)
def _instanciate_faker(seed=None, locale=None):
    if seed is not None:
        Faker.seed(seed)
    faker = Faker(locale)
    return faker


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

    Returns:
        str: A string resulted from one of the strategies, depends on the input
            data type.
    """
    if isinstance(string, str):
        if not string_func_path:
            return string
        try:
            module_path, resolver_name = string.split("::")
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
                    resolver_name, module_path))
        return lazy_string(resolved,
                           seed=seed,
                           string_func_path=string_func_path)
    elif isinstance(string, Iterable):
        if not string:
            # Prevent IndexError in ``random.choice``
            raise ValueError(('The iterable used to build a lazy string can'
                              ' not be empty.'))

        if isinstance(string, (set, GeneratorType)):
            string = list(string)
        if seed is not None:
            random.seed(seed)
        return lazy_string(random.choice(string),
                           seed=seed,
                           string_func_path=string_func_path)
    elif isinstance(string, CallableTypes):
        if seed is not None:
            random.seed(seed)
        return lazy_string(string(),
                           seed=seed,
                           string_func_path=string_func_path)
    elif hasattr(string, '__name__'):
        return string.__name__
    return str(string)


def lazy_value_by_parameter(parameter_data, seed=None, locale=None):
    '''Given a dictionary of parameter options, returns the corresponding value
    built following the rules listed in ``parameters`` argument of
    :py:func:`http_request_codegen.api.generate_http_request_code` function
    documentation.

    The strategy of value building is to check next attributes in given order:

    - ``value``
    - ``values``
    - ``faker``
    - ``type``

    TODO: Document arguments.
    '''
    if 'value' in parameter_data:
        return str(parameter_data['value'])
    elif 'values' in parameter_data:
        try:
            return lazy_string(parameter_data['values'],
                               seed=seed,
                               string_func_path=True)
        except (ModuleNotFoundError, ImportError):
            raise ValueError(
                ('\'values\' \'%s\' attribute of parameter \'%s\' is'
                 ' pointing to an inexistent Python function.') % (
                     parameter_data['values'], parameter_data['name']))
    elif 'faker' in parameter_data:
        if isinstance(parameter_data['faker'], str):
            # Search provider by string
            provider_mod_name, func_name = parameter_data['faker'].split("::")
            mod = importlib.import_module(provider_mod_name)
            faker = _instanciate_faker(seed=seed, locale=locale)
            faker.add_provider(mod)
            return getattr(faker, func_name)()
        elif isinstance(parameter_data['faker'], CallableTypes):
            faker = _instanciate_faker(seed=seed, locale=locale)
            faker.add_provider(parameter_data['faker'].__module__)
            return getattr(faker, parameter_data['faker'].__name__)()
        raise TypeError(
            ('\'faker\' \'%s\' attribute of parameter \'%s\' must be an'
             ' instance of \'str\' or \'function\'.') % (
                 str(parameter_data['faker']), parameter_data['name']))
    else:
        if 'type' not in parameter_data:
            _type = 'str'
        else:
            # TODO: Document that type can be a function, a list...
            _type = lazy_string(parameter_data['type'])
            if isinstance(_type, str):
                _type = _type.lower()
        if _type in ('str', 'string', str):
            faker = _instanciate_faker(seed=seed, locale=locale)
            faker.add_provider(faker_lorem_provider)
            return faker.word()
        elif _type in ('int', 'integer', int):
            if seed is not None:
                random.seed(seed)
            # Document max and min in public API
            _max = 65536 if 'max' not in parameter_data \
                else parameter_data['max']
            _min = -65536 if 'min' not in parameter_data \
                else parameter_data['min']
            return str(random.randint(_min, _max))
        elif _type in ('float', 'number', float):
            if seed is not None:
                random.seed(seed)
            # Document step in public API
            _max = 65536 if 'max' not in parameter_data \
                else parameter_data['max']
            _min = -65536 if 'min' not in parameter_data \
                else parameter_data['min']
            _round = 2 if 'round' not in parameter_data \
                else parameter_data['round']
            return str(round(random.uniform(_min, _max), _round))
        elif _type in ('bool', 'boolean', bool):
            if seed is not None:
                random.seed(seed)
            # TODO: Add support for nullable values
            return random.choice(['true', 'false'])
        elif _type in ('uuid', 'uuid4', uuid.UUID):
            return _instanciate_faker(
                seed=seed, locale=locale).uuid4(cast_to=None).hex
        elif _type in ('id', 'identifier'):
            # TODO: Document id type
            if seed is not None:
                random.seed(seed)
            _max = 65536 if 'max' not in parameter_data \
                else parameter_data['max']
            return str(random.randint(1, _max))
        elif _type == 'file':
            # TODO: Document file type
            faker = _instanciate_faker(seed=seed, locale=locale)
            faker.add_provider(faker_file_provider)
            return faker.file_path()
        elif _type == 'random':
            # TODO: Document 'random' type
            if seed is not None:
                random.seed(seed)

            parameter_data['type'] = random.choice([
                'str', 'int', 'float', 'bool', 'uuid', 'id', 'file'])
            return lazy_value_by_parameter(parameter_data['type'], seed=seed)
        raise TypeError(
            ('Data type \'%s\' of parameter \'%s\' not supported.') % (
                parameter_data['type'], parameter_data['name']))
