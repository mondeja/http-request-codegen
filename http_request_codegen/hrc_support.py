'''Library supported features discovering through code inspection.'''

import importlib
from collections import OrderedDict

from http_request_codegen.hrc_factory import (
    get_func_by_lang_impl_method,
    get_generators_modules_by_lang_impl,
)
from http_request_codegen.hrc_http import HTTP_METHODS
from http_request_codegen.hrc_meta import function_has_kwarg


FEATURES_KWARGS = OrderedDict({
    'Headers': 'headers',
    'Parameters': 'parameters',
    'Parameters localization': 'locale',
    'Parameters seed': 'seed',
    'Custom indentation': 'indent',
    'Quotation character': 'quote_char',
    'One line rendering': 'oneline',
    'Custom initialization': 'setup',
    'Custom teardown': 'teardown',
    'Line wrapping': 'wrap',
})


def _func_has_kwarg_support_factory(kwarg_name):
    def _func_has_kwarg(language, impl, method):
        func = get_func_by_lang_impl_method(
            language=language, impl=impl, method=method,
        )
        return function_has_kwarg(func, kwarg_name)
    return _func_has_kwarg


def _get_supports_parameters_funcs():
    return OrderedDict({
        feature: _func_has_kwarg_support_factory(kwarg) for feature, kwarg in
        FEATURES_KWARGS.items()
    })


def supported_features():
    '''Returns all supported features for each implementation of the library
    by methods, following the next form:

    ```python
    {
        'language/platform': {
            'implementation_A': {
                'GET': {
                    'Feature-A': True,
                    'Feature-B': False,
                    'Feature-C': False,
                },
                'POST': {
                    'Feature-A': False,
                    'Feature-B': True,
                    'Feature-C': False,
                },
            }
        }
    }
    ```

    A feature is supported is a function that reproduces a method in their
    implementation has a certain keyword argument in his definition. The
    mapping of features and keyword arguments are defined in the global
    variable ``FEATURES_KWARGS`` of this module.

    This function is used to build the "Support" section of the documentation.

    Returns:
        dict: Mapping with all features supported by method for each
            implementation.
    '''
    _supports_params_funcs = _get_supports_parameters_funcs()

    response = {}

    for lang, impls in get_generators_modules_by_lang_impl().items():
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
    methods supported for each implementation, in next form:

    ```python
    {
        'language/platform': {
            'implementation_A': ['GET', 'POST', 'PATCH'],
            'implementation_B': ['GET'],
        }
    }
    ```

    A method will be only included if at least one of the required features is
    supported.

    Returns:
        dict: Mapping with all supported methods for each implementation.
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
