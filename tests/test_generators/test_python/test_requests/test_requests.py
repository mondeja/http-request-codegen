"""Tests for Python requests implementation generators."""

import os

import pytest

from http_request_codegen import generate_http_request_code
from tests.conftest import (
    combination_arguments_to_kwargs,
    get_argument_combinations
)


CASES_DIRS = {
    method: os.path.abspath(os.path.join(os.path.dirname(__file__), method))
    for method in ['GET', 'POST']
}


@pytest.mark.parametrize(
    'args_group',
    get_argument_combinations(method='GET', dirpath=CASES_DIRS['GET']),
    ids=lambda args_group: os.path.basename(args_group['filename'])
)
def test_python_requests_get(args_group):
    with open(args_group['filename'], 'r') as f:
        expected_result = f.read()

    result = generate_http_request_code(
        'python', 'requests', 'GET',
        **combination_arguments_to_kwargs(args_group['arguments']))

    assert result == expected_result


@pytest.mark.parametrize(
    'args_group',
    get_argument_combinations(method='GET', dirpath=CASES_DIRS['GET']),
    ids=lambda args_group: os.path.basename(args_group['filename'])
)
def test_python_requests_get__response(args_group, assert_request_args):
    result = generate_http_request_code(
        'python', 'requests', 'GET',
        **combination_arguments_to_kwargs(args_group['arguments']))

    if 'import requests' not in result:
        result = 'import requests\n\n%s' % result
    namespace = {}
    exec(result, namespace)
    assert_request_args(args_group['arguments'], namespace['req'].json())


@pytest.mark.parametrize(
    'args_group',
    get_argument_combinations(method='POST', dirpath=CASES_DIRS['POST']),
    ids=lambda args_group: os.path.basename(args_group['filename'])
)
def test_python_requests_post(args_group):
    with open(args_group['filename'], 'r') as f:
        expected_result = f.read()

    result = generate_http_request_code(
        'python', 'requests', 'POST',
        **combination_arguments_to_kwargs(args_group['arguments']))

    assert result == expected_result
