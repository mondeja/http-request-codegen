"""Tests for Bash curl implementation generators."""

import os

import pytest

from http_request_codegen import generate_http_request_code

from tests.combinations import (
    combination_arguments_to_kwargs,
    get_argument_combinations,
)


CASES_DIRS = {
    method: os.path.abspath(os.path.join(os.path.dirname(__file__), method))
    for method in ['GET', 'POST']
}


@pytest.mark.parametrize(
    'args_group',
    get_argument_combinations(method='GET', dirpath=CASES_DIRS['GET']),
    ids=lambda args_group: os.path.basename(args_group['filename']),
)
def test_bash_curl_get(args_group):
    with open(args_group['filename']) as f:
        expected_result = f.read()

    result = generate_http_request_code(
        'bash', 'curl', 'GET',
        **combination_arguments_to_kwargs(args_group['arguments']),
    )

    assert result == expected_result


@pytest.mark.parametrize(
    'args_group',
    get_argument_combinations(method='POST', dirpath=CASES_DIRS['POST']),
    ids=lambda args_group: os.path.basename(args_group['filename']),
)
def test_bash_curl_post(args_group):
    with open(args_group['filename']) as f:
        expected_result = f.read()

    result = generate_http_request_code(
        'bash', 'curl', 'POST',
        **combination_arguments_to_kwargs(args_group['arguments']),
    )

    assert result == expected_result
