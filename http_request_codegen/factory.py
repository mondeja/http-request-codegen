"""Language-implementation-method factory."""

import importlib
from functools import lru_cache

from http_request_codegen.http import HTTP_METHODS


# TODO: Autodiscover languages and implementations
GENERATORS_BY_LANG_IMPL = {
    'python': {
        'requests': 'http_request_codegen.python.requests',
        'urllib': 'http_request_codegen.python.urllib',
    },
    'javascript': {
        'fetch': 'http_request_codegen.javascript.fetch',
    },
    'bash': {
        'curl': 'http_request_codegen.bash.curl',
        'wget': 'http_request_codegen.bash.wget',
    }
}


@lru_cache(maxsize=32)
def get_func_by_lang_impl_method(language=None, impl=None, method=None):
    if language is None:
        if impl is None:
            _language = 'python'
        else:
            _language = None
            for __lang, __imps in GENERATORS_BY_LANG_IMPL.items():
                for __imp in __imps.keys():
                    if __imp == impl:
                        _language = __lang
                        break
                if _language is not None:
                    break
            if _language is None:
                _language = 'python'
    else:
        _language = language
    try:
        lang_impls = GENERATORS_BY_LANG_IMPL[_language]
    except KeyError:
        raise ValueError(('The language \'%s\' is not implemented in'
                          ' http-request-codegen.') % language)
    if impl is None:
        _impl = list(lang_impls.keys())[0]
    else:
        _impl = impl

    try:
        impl_modpath = lang_impls[_impl]
    except KeyError:
        raise ValueError(
            ('The implementation \'%s\' is not implemented'
             ' for the language \'%s\' in http-request-codegen.') % (
                 impl, _language))

    module = importlib.import_module(impl_modpath)

    if method is None:
        _method = 'get'
    else:
        _method = method.lower()
    try:
        func = getattr(module, _method)
    except AttributeError:
        if method.upper() not in HTTP_METHODS:
            raise ValueError('Invalid HTTP method \'%s\'' % method.upper())
        raise ValueError(
            ('The implementation \'%s\' of the language \'%s\' does not'
             ' support HTTP %s methods.') % (impl, _language, _method.upper())
        )
    return func
