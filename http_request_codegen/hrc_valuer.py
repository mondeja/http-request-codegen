'''Parameter value formatter factory.'''

import importlib
import random
import uuid
from functools import lru_cache

from faker import Faker
from faker.providers import lorem as faker_lorem_provider

from http_request_codegen.hrc_meta import CallableTypes
from http_request_codegen.hrc_string import lazy_string


@lru_cache(maxsize=32)
def _instanciate_faker(seed=None, locale=None):
    if seed is not None:
        Faker.seed(seed)
    faker = Faker(locale)
    return faker


def lazy_name_by_parameter(parameter_data, seed=None):
    '''Given a dictionary of parameter options, returns the corresponding
    parameter name built following the rules listed in ``parameters`` argument
    of [``generate_http_request_code``](#generate_http_request_code) function
    documentation.

    The strategy of name building is to check next attributes in given order:

    - ``name``
    - ``names``

    You can use this function to build the parameters at lower level. This can
    be used, for example, to append the parameters to an URL generating GET
    method code snippets if an implementation does by building the parameters
    as arguments of a function.

    Args:
        parameter_data (dict): Parameter specification data. It's defined at
            **name** and **names** sections of ``parameters`` argument of
            [``generate_http_request_code``](#generate_http_request_code)
            function documentation.
        seed (int): Seed using randomizing names.

    Raises:
        ValueError: none of the ``name`` or ``names`` attributes are defined
            inside ``parameter_data`` dictionary.

    Examples:
        >>> lazy_name_by_parameter({'name': 'foo'})
        'foo'

        >>> result = lazy_name_by_parameter({'names': ['foo', 'bar', 'baz']})
        >>> result in ['foo', 'bar', 'baz']
        True

    Returns:
        str: Parameter name.
    '''
    if 'name' in parameter_data:
        return lazy_string(parameter_data['name'], seed=seed)
    elif 'names' in parameter_data:
        try:
            return lazy_string(
                parameter_data['names'],
                seed=seed,
                string_func_path=True,
            )
        except (ModuleNotFoundError, ImportError):
            raise ValueError(
                (
                    '\'names\' \'%s\' attribute of parameter is pointing to an'
                    ' inexistent Python callable object'
                ) % (
                    parameter_data['names']
                ),
            )

        return lazy_string(
            parameter_data['names'],
            seed=seed, string_func_path=True,
        )
    raise ValueError((
        'Parameter must contain \'name\' or \'names\''
        ' attribute, got "%s"'
    ) % str(parameter_data))


def lazy_value_by_parameter(parameter_data, seed=None, locale=None):
    '''Given a dictionary of parameter options, returns the corresponding value
    built following the rules listed in ``parameters`` argument of
    [``generate_http_request_code``](#generate_http_request_code) function
    documentation.

    For example, giving ``{\'type\': int}`` as input, the output will be a
    random number as string.

    The strategy of value building is to check next attributes in given order:

    - ``'value'``
    - ``'values'``
    - ``'faker'``
    - ``'type'``

    If none of the previous attributes are passed will be treated as if
    ``{\'type\': str}`` has been passed, returning a random word.

    You can use this function to build the parameters at lower level. This can
    be used, for example, to append the parameters to an URL generating GET
    method code snippets if an implementation does by building the parameters
    as arguments of a function.

    Args:
        parameter_data (dict): Parameter specification data. It's defined at
            **type**, **value**, **values** and **faker** sections of
            ``parameters`` argument as is defined at
            [``generate_http_request_code``](#generate_http_request_code)
            function documentation.
        seed (int): Seed using randomizing values.
        locale (str): Locale used for ``faker`` providers.

    Examples:
        >>> lazy_value_by_parameter({'value': 'foo'})
        'foo'

        >>> result = lazy_value_by_parameter({'values': ['foo', 'bar', 'baz']})
        >>> result in ['foo', 'bar', 'baz']
        True

        >>> result = lazy_value_by_parameter({'type': 'int'})
        >>> result.replace('.', '', 1).lstrip('-').isnumeric() and \\
        ...     isinstance(result, str)
        True

    Raises:
        ImportError: ``'values'`` attribute value points to an inexistent
            Python object.
        TypeError: ``'faker'`` attribute value does not contains a string or
            Python callable object, or if the ``'type'`` attribute value does
            not support the defined type.
        ImportError: ``'faker'`` attribute value, when passed as string,
            points to an inexistent Python object.

    Returns:
        str: Parameter value.
    '''
    if 'value' in parameter_data:
        return lazy_string(parameter_data['value'], seed=seed)
    elif 'values' in parameter_data:
        try:
            return lazy_string(
                parameter_data['values'],
                seed=seed,
                string_func_path=True,
            )
        except (ModuleNotFoundError, ImportError):
            raise ImportError(
                (
                    '\'values\' \'%s\' attribute of parameter \'%s\' is'
                    ' pointing to an inexistent Python callable object'
                ) % (
                    parameter_data['values'], parameter_data['name'],
                ),
            )
    elif 'faker' in parameter_data:
        if isinstance(parameter_data['faker'], str):
            # Search provider by string
            provider_mod_name, func_name = parameter_data['faker'].split('::')
            mod = importlib.import_module(provider_mod_name)
            faker = _instanciate_faker(seed=seed, locale=locale)
            faker.add_provider(mod)
            return getattr(faker, func_name)()
        elif isinstance(parameter_data['faker'], CallableTypes):
            faker = _instanciate_faker(seed=seed, locale=locale)
            faker.add_provider(parameter_data['faker'].__module__)
            return getattr(faker, parameter_data['faker'].__name__)()
        raise TypeError(
            (
                '\'faker\' \'%s\' attribute of parameter \'%s\' must be an'
                ' instance of \'str\' or \'callable\''
            ) % (
                str(parameter_data['faker']), parameter_data['name'],
            ),
        )
    if 'type' not in parameter_data:
        _type = 'str'
    else:
        _type = lazy_string(parameter_data['type'], seed=seed)
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
        response = random.uniform(_min, _max)
        if 'round' in parameter_data:
            response = round(response, parameter_data['round'])
        return str(response)
    elif _type in ('bool', 'boolean', bool):
        _possibles = ['true', 'false']
        if parameter_data.get('null'):
            _possibles.append('null')
        if seed is not None:
            random.seed(seed)
        return random.choice(_possibles)
    elif _type in ('uuid', 'uuid4', uuid.UUID):
        return _instanciate_faker(
            seed=seed, locale=locale,
        ).uuid4(cast_to=None).hex
    elif _type in ('id', 'identifier'):
        if seed is not None:
            random.seed(seed)
        _max = 65536 if 'max' not in parameter_data \
            else parameter_data['max']
        return str(random.randint(1, _max))
    elif _type == 'random':
        if seed is not None:
            random.seed(seed)
        if 'types' in parameter_data:
            _possible = lazy_string(parameter_data['types'], seed=seed)
        else:
            _possible = [
                'str', 'int', 'float', 'bool', 'uuid', 'id', 'file',
            ]
        parameter_data['type'] = random.choice(_possible)
        return lazy_value_by_parameter(parameter_data['type'], seed=seed)
    raise TypeError(
        ('Data type \'%s\' of parameter \'%s\' not supported') % (
            parameter_data['type'], parameter_data['name'],
        ),
    )
