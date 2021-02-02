'''Language-implementation-method factory.'''

import importlib
import os
from functools import lru_cache

from http_request_codegen.hrc_http import HTTP_METHODS


DEFAULT_LANGUAGE = 'python'
DEFAULT_IMPLEMENTATION = 'requests'

GENERATORS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'generators'),
)


@lru_cache(maxsize=1)
def get_generators_modules_by_lang_impl():
    response = {}

    for fname in os.listdir(GENERATORS_DIR):
        if fname.startswith('_'):
            continue
        fpath = os.path.join(GENERATORS_DIR, fname)
        if not os.path.isdir(fpath):
            continue
        response[fname] = {}

        for modfname in os.listdir(fpath):
            if modfname.startswith('_'):
                continue
            modname = modfname.rstrip('.py')
            response[fname][modname] = (
                'http_request_codegen.generators.%s.%s'
            ) % (fname, modname)
    return response


@lru_cache(maxsize=32)
def get_func_by_lang_impl_method(language=None, impl=None, method=None):
    generators_by_lang_impl = get_generators_modules_by_lang_impl()

    if language is None:
        if impl is None:
            _language = 'python'
        else:
            _language = None
            for __lang, __imps in generators_by_lang_impl.items():
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
        lang_impls = generators_by_lang_impl[_language]
    except KeyError:
        raise ValueError(
            (
                'The language \'%s\' is not implemented in'
                ' http-request-codegen.'
            ) % language,
        )
    if impl is None:
        _impl = list(lang_impls.keys())[0]
    else:
        _impl = impl

    try:
        impl_modpath = lang_impls[_impl]
    except KeyError:
        raise ValueError(
            (
                'The implementation \'%s\' is not implemented'
                ' for the language \'%s\' in http-request-codegen.'
            ) % (
                impl, _language,
            ),
        )

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
            (
                'The implementation \'%s\' of the language \'%s\' does not'
                ' support HTTP %s methods.'
            ) % (impl, _language, _method.upper()),
        )
    return func
