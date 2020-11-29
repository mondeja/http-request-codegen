"""Test language-implementation-method factory."""

import pytest

from http_request_codegen.factory import get_func_by_lang_impl_method
from http_request_codegen.python.requests import (
    get as requests_get,
    post as requests_post
)


@pytest.mark.parametrize(("language", "impl", "method", "result"), (
    # Default cases
    (None, None, None, requests_get),
    ('python', None, None, requests_get),
    ('python', 'requests', None, requests_get),

    # Explicit valid cases
    ('python', 'requests', 'GET', requests_get),
    ('python', 'requests', 'get', requests_get),
    ('python', 'requests', 'POST', requests_post),
    ('python', 'requests', 'post', requests_post),

    # Define method
    (None, None, 'GET', requests_get),
    (None, None, 'get', requests_get),
    (None, None, 'POST', requests_post),
    (None, None, 'post', requests_post),
    (None, None, 'qwerty', ValueError),

    # Define implementation (language autodiscover)
    (None, 'requests', None, requests_get),
    (None, 'requests', 'GET', requests_get),
    (None, 'requests', 'foo', ValueError),

    # Invalid implementation
    (None, 'jbfdjksabfashfbd', 'GET', ValueError),
    (None, 'fdjsfjsdfsdfvvbsd', None, ValueError),

    # Invalid language
    ('flklfsdngklsnhfd', None, None, ValueError),
    ('flklfsdngklsnhfd', 'requests', None, ValueError),
    ('flklfsdngklsnhfd', 'requests', 'GET', ValueError),
))
def test_language_impl_method_factory(language, impl, method, result):
    if hasattr(result, '__traceback__'):
        with pytest.raises(result):
            get_func_by_lang_impl_method(
                language=language, impl=impl, method=method)
    else:
        assert get_func_by_lang_impl_method(
            language=language, impl=impl, method=method) == result
