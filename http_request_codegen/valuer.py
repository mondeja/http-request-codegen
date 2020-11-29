"""Parameter value formatter factory."""

import importlib
import random
import uuid
from functools import lru_cache
from types import FunctionType

from faker import Faker
from faker.providers import (
    file as faker_file_provider,
    lorem as faker_lorem_provider
)


@lru_cache(maxsize=32)
def _instanciate_faker(seed=None, locale=None):
    if seed is not None:
        Faker.seed(seed)
    faker = Faker(locale)
    return faker


def value_by_parameter(parameter_data, seed=None, locale=None):
    """Given a dictionary of parameter options, returns the corresponding value
    built following the rules listed in ``parameters`` argument of
    :py:func:`http_request_codegen.api.generate_http_request_code` function
    documentation.

    The strategy of value building is to check next attributes in given order:

    - ``value``
    - ``values``
    - ``faker``
    - ``type``

    TODO: Document arguments.
    """
    if 'value' in parameter_data:
        return str(parameter_data['value'])
    elif 'values' in parameter_data:
        if isinstance(parameter_data['values'], list):
            if seed is not None:
                random.seed(seed)
            # Can be a list of random functions
            # TODO: Document this in public API
            response = random.choice(parameter_data['values'])
            if isinstance(response, FunctionType):
                return response()
            return response
        elif isinstance(parameter_data['values'], FunctionType):
            response = parameter_data['values']()
            if isinstance(response, list):
                if seed is not None:
                    random.seed(seed)
                return str(random.choice(response))
            return str(response)
        elif isinstance(parameter_data['values'], str):
            module_path, func_name = parameter_data['values'].split("::")
            try:
                # If ``module_path`` is not a valid Python module a
                # ``ModuleNotFoundError`` will be raised
                func = getattr(importlib.import_module(module_path), func_name)
            except AttributeError:
                raise ValueError(
                    ('\'values\' \'%s\' attribute of parameter \'%s\' is'
                     ' pointing to an inexistent Python function.') % (
                         parameter_data['values'], parameter_data['name']))
            response = func()
            if isinstance(response, list):
                if seed is not None:
                    random.seed(seed)
                return str(random.choice(response))
            return str(response)
        raise TypeError(
            ('\'values\' \'%s\' attribute of parameter \'%s\' must be an'
             ' instance of \'str\', \'list\' or \'function\'.') % (
                 str(parameter_data['values']), parameter_data['name']))
    elif 'faker' in parameter_data:
        if isinstance(parameter_data['faker'], str):
            # Search provider by string
            provider_mod_name, func_name = parameter_data['faker'].split("::")
            mod = importlib.import_module(provider_mod_name)
            faker = _instanciate_faker(seed=seed, locale=locale)
            faker.add_provider(mod)
            return getattr(faker, func_name)()
        elif isinstance(parameter_data['faker'], FunctionType):
            faker = _instanciate_faker(seed=seed, locale=locale)
            faker.add_provider(parameter_data['faker'].__module__)
            return getattr(faker, parameter_data['faker'].__name__)()
        # TODO: Add support for random choosing from list of provider-funcs
        raise TypeError(
            ('\'faker\' \'%s\' attribute of parameter \'%s\' must be an'
             ' instance of \'str\' or \'function\'.') % (
                 str(parameter_data['faker']), parameter_data['name']))
    else:
        if 'type' not in parameter_data:
            parameter_data['type'] = 'str'

        # str.lower() raises error
        if isinstance(parameter_data['type'], str):
            _type = parameter_data['type'].lower()
        else:
            _type = parameter_data['type']
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
        raise TypeError(
            ('Data type \'%s\' of parameter \'%s\' not supported.') % (
                parameter_data['type'], parameter_data['name']))
