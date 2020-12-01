'''Testinf for inspection functions of http-request-codegen.'''

import pytest

from http_request_codegen.meta import function_has_kwarg


def _func_without_parameters():
    return None


def _func_without_parameters_kwarg(another_param):
    return another_param


def _func_with_parameters_kwarg(parameters=None):
    return parameters


def _func_with_parameters_arg(parameters):
    return parameters


@pytest.mark.parametrize(('func', 'kwarg_name', 'result'), (
    (_func_without_parameters, 'parameters', False),
    (_func_without_parameters_kwarg, 'parameters', False),
    (_func_with_parameters_kwarg, 'parameters', True),
    (_func_with_parameters_arg, 'parameters', False),
))
def test_function_has_kwarg(func, kwarg_name, result):
    assert function_has_kwarg(func, kwarg_name) is result
