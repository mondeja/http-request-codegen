"""http-request-codegen public API."""

from http_request_codegen.factory import get_func_by_lang_impl_method


def generate_http_request_code(language=None, impl=None, method='GET',
                               url='localhost', parameters=[], headers={},
                               indent=None, quote_char=None, oneline=False,
                               seed=None, locale=None, **kwargs):
    '''Generates a code snippet of an HTTP request for a library of a given
    programming language, based on a valid HTTP method and parameters.

    Args:
        language (str): Programming language of the resulting code snippet.
        impl (str): Implementation type used for the code snippet. It can be a
            library, a program, or a language API.
        method (str): HTTP method of the generated request. Only next methods
            are currently supported:

            - GET
            - POST
        url (str): URL endpoint of the generated request.
        parameters (list): List of parameters for the request. Each parameter
            must be a dictionary. This dictionary defines, for each parameter,
            what is the parameter name and how are the parameters values
            defined:

            - **name** (*str*): Parameter name. This attribute is required.
            - **type** (*str*): Parameter data type. If not defined and
                ``value``, ``values`` and ``faker`` are not defined, will be
                considered as a string and the value of the parameter will be a
                random word built using faker library. The following parameter
                data types are supported, as well as their corresponding names
                in capital letters:

                - ``'str'``: Basic string type. Can be defined with the Python
                    builtin type ``str`` or the strings ``'str'`` and
                    ``'string'``.
                - ``'bool'``: Basic boolean type. Can be defined with the
                    Python builtin type ``bool``, or the strings ``'bool'``
                    and ``'boolean'``.
                - ``'int'``: Basic integer type. Can be defined with the Python
                    builtin type ``int``, or the strings ``'int'`` and
                    ``'integer'``.
                - ``'float'``: Basic integer type. Can be defined with the
                    Python builtin type ``float``, or the strings ``'float'``
                    and ``number``.
            - **value** (*str*): Parameter value. Id not defined and ``type``,
                ``values`` and ``faker`` are not defined, it will be a random
                word built using faker library.
            - **values** (*list*/*str*/*function*): Possible parameter values.
                Defined as a list, the value of the parameter will be selected
                from the list using :py:func:`random.random.choice`.
                Defined as a string, must be a Python formatted module path
                following the format ``path.to.module::function`` and the
                return value will be used as the value for the parameter, which
                is useful if choosing a random value from a list doesn't fit
                your needs.
                Defined as a function, their return value will be used as the
                value for the parameter, which is useful if choosing a random
                value from a list doesn't fit your needs.
                If not defined and ``type``, ``value`` and ``faker`` are not
                defined, it will be a random word built using faker library.
            - **faker** (*str*): Python formatted module path to a function of
                a Faker provider used to build the value randomized. Must
                follow the format ``path.to.provider.module::function`` and can
                be a standard, external provider or any function, but if is not
                a provider, ``seed`` and ``locale`` will not have effect.
        headers (dict): Request headers.
        indent (str): Indentation string used in the generated code.
        quote_char (str): Quotation character used in the generated code. If
            not defined, the default quotation character for the language
            will be used.
        seed (int): Seed used generating random fake values of parameters.
            Useful if you want to generate the same set of values between
            multiples code snippets.
        locale (str): Locale used by Faker library for localization of the
            fake random values for parameters.
    '''
    func = get_func_by_lang_impl_method(
        language=language, impl=impl, method=method)
    func_kwargs = kwargs
    if quote_char is not None:
        func_kwargs["quote_char"] = quote_char
    return func(url, parameters=parameters, headers=headers, indent=indent,
                oneline=oneline, seed=seed, locale=locale, **func_kwargs)


def generate_http_request_md_code_block(language=None, **kwargs):
    return '``` %(language)s\n%(render)s\n```' % {
        'language': language if language else 'python',
        'render': generate_http_request_code(language=language, **kwargs),
    }
