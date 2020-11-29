"""Library supported features discovering through code inspection."""

import importlib
from collections import OrderedDict

from http_request_codegen.factory import (
    GENERATORS_BY_LANG_IMPL,
    get_func_by_lang_impl_method
)
from http_request_codegen.http import HTTP_METHODS
from http_request_codegen.inspector import function_has_kwarg


def _func_has_kwarg_support_factory(kwarg_name):
    def _func_has_kwarg(language, impl, method):
        func = get_func_by_lang_impl_method(
            language=language, impl=impl, method=method)
        return function_has_kwarg(func, kwarg_name)
    return _func_has_kwarg


def _get_supports_parameters_funcs():
    return OrderedDict({
        "Headers": _func_has_kwarg_support_factory('headers'),
        "Indentation": _func_has_kwarg_support_factory('indent'),
        "Initialization": _func_has_kwarg_support_factory('init'),
        "One liner": _func_has_kwarg_support_factory('oneline'),
        "Parameters": _func_has_kwarg_support_factory('parameters'),
        "Parameters localization": _func_has_kwarg_support_factory('locale'),
        "Parameters seed": _func_has_kwarg_support_factory('seed'),
        "Quotation character": _func_has_kwarg_support_factory('quote_char'),
        "Wrapping": _func_has_kwarg_support_factory('wrap'),
    })


def supported_features():
    _supports_params_funcs = _get_supports_parameters_funcs()

    response = {}

    for lang, impls in GENERATORS_BY_LANG_IMPL.items():
        response[lang] = {}
        for impl, module_path in impls.items():
            response[lang][impl] = {}
            mod = importlib.import_module(module_path)

            for method in HTTP_METHODS:
                _method_supported = False

                try:
                    getattr(mod, method.lower())
                except AttributeError:
                    continue
                response[lang][impl][method] = OrderedDict({})
                for feature, support_func in _supports_params_funcs.items():
                    supported = support_func(lang, impl, method)
                    response[lang][impl][method][feature] = supported
                    if supported:
                        _method_supported = True
                response[lang][impl][method]['_supported'] = _method_supported

    return response


def supported_methods():
    '''Returns a dictionary with all languages with all implmentations and
    methods supported for each implementation.
    '''
    response = {}
    for lang, impls in supported_features().items():
        response[lang] = {}
        for impl, methods in impls.items():
            _impl_methods = []
            for method, features in methods.items():
                if not features['_supported']:
                    continue
                _impl_methods.append(method)
            if _impl_methods:
                response[lang][impl] = _impl_methods
    return response
