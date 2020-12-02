'''Test valuer factories.'''

import builtins
import uuid
from collections.abc import Iterable
from types import LambdaType

import pytest
from faker.providers.lorem import Provider as LoremProvider
from faker.providers.lorem.en_US import Provider as EnUsLoremProvider

from http_request_codegen.valuer import lazy_value_by_parameter
from tests.conftest import (
    value as _value_func,
    values_list as _values_list_func
)


@pytest.mark.parametrize('value', (
    'hello',
    'foo',
    'bar',
    1,
    2,
    True,
    None
))
def test_lazy_value_by_parameter__value(value):
    '''Passing the attribute 'value', will be casted to string.'''
    assert lazy_value_by_parameter({'value': value}) == str(value)


@pytest.mark.parametrize(('values', 'seed', 'result'), (
    # list
    (['foo', 'bar', 'baz'], 1, ['foo', 'bar', 'baz']),
    (['foo', 'bar', 'baz'], 500, ['foo', 'bar', 'baz']),
    ([1, None, True], 1, ['1', 'None', 'True']),
    ([1, None, True], 500, ['1', 'None', 'True']),

    # function
    #   function returning list
    (_values_list_func, 1, [str(val) for val in _values_list_func()]),
    (_values_list_func, 5, [str(val) for val in _values_list_func()]),
    #   function returning value
    (_value_func, None, str(_value_func())),
    (_value_func, 1, str(_value_func())),
    (_value_func, 500, str(_value_func())),

    # str
    #   str to Python module-func path format returning list
    ('tests.conftest::values_list', 1, 'baz'),
    ('tests.conftest::values_list', 5, '-1.5'),

    #   str to Python module-func path format returning value
    ('tests.conftest::value', None, 'foo'),
    ('tests.conftest::value', 1, 'foo'),
    ('tests.conftest::value', 500, 'foo'),

    #   str to non-existent function from module-func path format
    ('tests.conftest::non-existent', None, ImportError),
    ('tests.conftest::non-existent', 5, ImportError),
    #   str to non-existent module from module-func path format
    ('test.non-existent::non-existent', None, ImportError),
    ('test.non-existent::non-existent', 5, ImportError),
))
def test_lazy_value_by_parameter__values(values, seed, result):
    parameter = {'values': values, 'name': 'foo'}
    if hasattr(result, '__traceback__'):
        with pytest.raises(result):
            lazy_value_by_parameter(parameter, seed=seed)
    elif isinstance(result, Iterable):
        assert lazy_value_by_parameter(parameter, seed=seed) in result
    else:
        assert lazy_value_by_parameter(parameter, seed=seed) == result


@pytest.mark.parametrize(('faker', 'seed', 'result'), (
    # Faker provider by Python module-func path
    ('faker.providers.lorem::word', None, EnUsLoremProvider.word_list),
    ('faker.providers.lorem::word', 5, EnUsLoremProvider.word_list),

    # Faker provider by function
    (LoremProvider.word, None, EnUsLoremProvider.word_list),
    (LoremProvider.word, 5, EnUsLoremProvider.word_list),
))
def test_lazy_value_by_parameter__faker(faker, seed, result):
    parameter = {'faker': faker, 'name': 'foo'}
    if isinstance(result, (list, tuple)):
        assert lazy_value_by_parameter(parameter, seed=seed) in result
    else:
        assert lazy_value_by_parameter(parameter, seed=seed) == result


VALID_INT_FROM_TYPE = lambda r: int(r) in range(-2**16, 2**16)
VALID_FLOAT_FROM_TYPE = lambda r: float(r) >= -2**16 and float(r) <= 2**16
VALID_ID_FROM_TYPE = lambda r: int(r) in range(1, 2**16)


def VALID_UUID4_FROM_TYPE(r):
    # https://gist.github.com/ShawnMilo/7777304
    try:
        val = uuid.UUID(r, version=4)
    except ValueError:
        return False
    return val.hex == r


@pytest.mark.parametrize(('type', 'seed', 'result'), (
    # str
    ('str', None, EnUsLoremProvider.word_list),
    ('Str', None, EnUsLoremProvider.word_list),
    ('STR', None, EnUsLoremProvider.word_list),
    ('string', None, EnUsLoremProvider.word_list),
    ('String', None, EnUsLoremProvider.word_list),
    ('STRING', None, EnUsLoremProvider.word_list),
    (str, None, EnUsLoremProvider.word_list),
    (builtins.str, None, EnUsLoremProvider.word_list),

    # TODO: test str seeded

    # int
    ('int', None, VALID_INT_FROM_TYPE),
    ('Int', None, VALID_INT_FROM_TYPE),
    ('INT', None, VALID_INT_FROM_TYPE),
    ('integer', None, VALID_INT_FROM_TYPE),
    ('Integer', None, VALID_INT_FROM_TYPE),
    ('INTEGER', None, VALID_INT_FROM_TYPE),
    (int, None, VALID_INT_FROM_TYPE),
    (builtins.int, None, VALID_INT_FROM_TYPE),

    # int seeded
    ('Int', 4, '-3658'),
    (int, 4, '-3658'),
    ('INTEGER', 5, '1427'),
    (builtins.int, 5, '1427'),

    # float
    ('float', None, VALID_FLOAT_FROM_TYPE),
    ('Float', None, VALID_FLOAT_FROM_TYPE),
    ('FLOAT', None, VALID_FLOAT_FROM_TYPE),
    ('number', None, VALID_FLOAT_FROM_TYPE),
    ('Number', None, VALID_FLOAT_FROM_TYPE),
    ('NUMBER', None, VALID_FLOAT_FROM_TYPE),
    (float, None, VALID_FLOAT_FROM_TYPE),
    (builtins.float, None, VALID_FLOAT_FROM_TYPE),

    # float seeded
    ('Float', 4, '-34596.70478193498'),
    (float, 4, '-34596.70478193498'),
    ('NUMBER', 5, '16108.970952583011'),
    (builtins.float, 5, '16108.970952583011'),

    # bool
    ('bool', None, ['true', 'false']),
    ('Bool', None, ['true', 'false']),
    ('BOOL', None, ['true', 'false']),
    ('boolean', None, ['true', 'false']),
    ('Boolean', None, ['true', 'false']),
    ('BOOLEAN', None, ['true', 'false']),
    (bool, None, ['true', 'false']),
    (builtins.bool, None, ['true', 'false']),

    # bool seeded
    ('Bool', 4, 'true'),
    (bool, 4, 'true'),
    ('BOOLEAN', 5, 'false'),
    (builtins.bool, 5, 'false'),

    # uuid
    ('uuid', None, VALID_UUID4_FROM_TYPE),
    ('Uuid', None, VALID_UUID4_FROM_TYPE),
    ('UUID', None, VALID_UUID4_FROM_TYPE),
    ('uuid4', None, VALID_UUID4_FROM_TYPE),
    ('Uuid4', None, VALID_UUID4_FROM_TYPE),
    ('UUID4', None, VALID_UUID4_FROM_TYPE),
    (uuid.UUID, None, VALID_UUID4_FROM_TYPE),

    # TODO: test uuid seeded

    # id
    ('id', None, VALID_ID_FROM_TYPE),
    ('Id', None, VALID_ID_FROM_TYPE),
    ('ID', None, VALID_ID_FROM_TYPE),
    ('identifier', None, VALID_ID_FROM_TYPE),
    ('Identifier', None, VALID_ID_FROM_TYPE),
    ('IDENTIFIER', None, VALID_ID_FROM_TYPE),
))
def test_lazy_value_by_parameter__type(type, seed, result):
    parameter = {'type': type, 'name': 'foo'}
    if isinstance(result, (list, tuple, range)):
        assert lazy_value_by_parameter(parameter, seed=seed) in result
    elif isinstance(result, LambdaType):
        assert result(lazy_value_by_parameter(parameter, seed=seed))
    else:
        assert lazy_value_by_parameter(parameter, seed=seed) == result
