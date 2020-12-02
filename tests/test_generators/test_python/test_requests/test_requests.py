"""Tests for Python requests implementation generators."""

import os

import pytest

from http_request_codegen import generate_http_request_code
from tests.conftest import (
    combination_arguments_to_kwargs,
    get_argument_combinations
)


GET_CASES_DIRPATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'GET'))


@pytest.mark.parametrize(
    'args_group',
    get_argument_combinations(dirpath=GET_CASES_DIRPATH),
    ids=lambda args_group: os.path.basename(args_group['filename'])
)
def test_python_requests_get(args_group):
    with open(args_group['filename'], 'r') as f:
        expected_result = f.read()

    result = generate_http_request_code(
        'python', 'requests', 'GET',
        **combination_arguments_to_kwargs(args_group['arguments']))

    assert result == expected_result
