"""Test language-implementation-method factory."""

import importlib
from types import ModuleType

import pytest

from http_request_codegen.factory import (
    get_func_by_lang_impl_method,
    get_generators_modules_by_lang_impl
)
from http_request_codegen.generators.python.requests import (
    get as requests_get,
    post as requests_post
)
from http_request_codegen.generators.python.urllib import (
    get as urllib_get,
    post as urllib_post
)


@pytest.mark.parametrize(("language", "impl", "method", "result"), (
    # Default cases
    (None, None, None, [requests_get, urllib_get]),
    ('python', None, None, [requests_get, urllib_get]),
    ('python', 'requests', None, requests_get),

    # Explicit valid cases
    ('python', 'requests', 'GET', requests_get),
    ('python', 'requests', 'get', requests_get),
    ('python', 'requests', 'POST', requests_post),
    ('python', 'requests', 'post', requests_post),

    # Define method
    (None, None, 'GET', [requests_get, urllib_get]),
    (None, None, 'get', [requests_get, urllib_get]),
    (None, None, 'POST', [requests_post, urllib_post]),
    (None, None, 'post', [requests_post, urllib_post]),
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
def test_get_func_by_lang_impl_method(language, impl, method, result):
    if hasattr(result, '__traceback__'):
        with pytest.raises(result):
            get_func_by_lang_impl_method(
                language=language, impl=impl, method=method)
    elif isinstance(result, (list, tuple)):
        assert get_func_by_lang_impl_method(
            language=language, impl=impl, method=method) in result
    else:
        assert get_func_by_lang_impl_method(
            language=language, impl=impl, method=method) == result


def test_get_generators_modules_by_lang_impl():
    generators_modules_by_lang_impl = get_generators_modules_by_lang_impl()
    assert generators_modules_by_lang_impl
    assert isinstance(generators_modules_by_lang_impl, dict)

    for lang, impls in generators_modules_by_lang_impl.items():
        assert lang
        assert isinstance(lang, str)
        assert isinstance(impls, dict)

        for impl, modpath in impls.items():
            assert impl
            assert isinstance(impl, str)
            assert isinstance(modpath, str)
            assert 'http_request_codegen.generators.' in modpath

            mod = importlib.import_module(modpath)
            assert mod
            assert isinstance(mod, ModuleType)
