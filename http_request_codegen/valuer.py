'''Parameter value formatter factory.'''

import importlib
import random
import uuid
from collections.abc import Iterable
from functools import lru_cache

from faker import Faker
from faker.providers import lorem as faker_lorem_provider

from http_request_codegen.meta import CallableTypes
from http_request_codegen.string import lazy_string


@lru_cache(maxsize=32)
def _instanciate_faker(seed=None, locale=None):
    if seed is not None:
        Faker.seed(seed)
    faker = Faker(locale)
    return faker


def lazy_name_by_parameter(parameter_data, seed=None):
    '''Given a dictionary of parameter options, returns the corresponding name
    built following the rules listed in ``parameters`` argument of
    :py:func:`http_request_codegen.api.generate_http_request_code` function
    documentation.

    The strategy of name building is to check next attributes in given order:

    - ``name``
    - ``names``

    Args:
        parameter_data (dict): Parameter specification data. It's defined at
            **name** and **names** sections of ``parameters`` argument of
            ``http_request_codegen.api.generate_http_request_code`` function
            documentation.
        seed (int): Seed using randomizing names.

    Returns:
        str: Parameter name.
    '''
    if 'name' in parameter_data:
        return lazy_string(parameter_data['name'], seed=seed)
    elif 'names' in parameter_data:
        try:
            return lazy_string(parameter_data['names'],
                               seed=seed,
                               string_func_path=True)
        except (ModuleNotFoundError, ImportError):
            raise ValueError(
                ('\'names\' \'%s\' attribute of parameter is pointing to an'
                 ' inexistent Python callable object') % (
                     parameter_data['names']))

        return lazy_string(parameter_data['names'],
                           seed=seed, string_func_path=True)
    raise ValueError(('Parameter must contain \'name\' or \'names\''
                      ' attribute, got "%s"') % str(parameter_data))


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

    Args:
        parameter_data (dict): Parameter specification data. It's defined at
            **type**, **value**, **values** and **faker** sections of
            ``parameters`` argument of
            ``http_request_codegen.api.generate_http_request_code`` function
            documentation.
        seed (int): Seed using randomizing values.
        locale (str): Locale used for ``faker`` providers.

    Returns:
        str: Parameter value.
    '''
    if 'value' in parameter_data:
        return lazy_string(parameter_data['value'], seed=seed)
    elif 'values' in parameter_data:
        try:
            return lazy_string(parameter_data['values'],
                               seed=seed,
                               string_func_path=True)
        except (ModuleNotFoundError, ImportError):
            raise ImportError(
                ('\'values\' \'%s\' attribute of parameter \'%s\' is'
                 ' pointing to an inexistent Python callable object') % (
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
             ' instance of \'str\' or \'function\'') % (
                 str(parameter_data['faker']), parameter_data['name']))
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
            seed=seed, locale=locale).uuid4(cast_to=None).hex
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
            if not isinstance(parameter_data['types'], Iterable):
                raise TypeError(
                    ('\'types\' attribute specifying random type must be'
                     ' an iterable, got type %s') % (
                        str(type((parameter_data['types'])))))
            _possible = list(parameter_data['types'])
        else:
            _possible = [
                'str', 'int', 'float', 'bool', 'uuid', 'id', 'file']
        parameter_data['type'] = random.choice(_possible)
        return lazy_value_by_parameter(parameter_data['type'], seed=seed)
    raise TypeError(
        ('Data type \'%s\' of parameter \'%s\' not supported') % (
            parameter_data['type'], parameter_data['name']))
