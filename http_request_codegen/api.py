"""http-request-codegen public API."""

from http_request_codegen.factory import get_func_by_lang_impl_method


def generate_http_request_code(language=None, impl=None, method='GET',
                               url='localhost', parameters=[], headers={},
                               indent=None, quote_char='\'', init=True,
                               oneline=False, seed=None, locale=None,
                               **kwargs):
    '''Generates a code snippet of an HTTP request for a library of a given
    programming language or a CLI of a program, based on a valid HTTP method
    and a specification of parameters.

    Args:
        language (str): Programming language or plataform of the resulting code
            snippet. See [Support](#support) to check the supported platforms
            and programming languages.
        impl (str): Implementation type used for the code snippet. It can be a
            library, a program, or a language API. See [Support](#support)
            to check the supported implementations by language.
        method (str): HTTP method of the generated request.
        url (str): URL endpoint of the generated request.
        headers (dict): Request headers.
        parameters (list): List of parameters for the request. Each parameter
            must be a dictionary. This dictionary defines, for each parameter,
            what is the parameter name and how are the parameters values
            generated:

            - **name** (*str*): Parameter name. This attribute is required.
            - **type** (*str*): Parameter data type. If not defined and
                ``value``, ``values`` and ``faker`` are not defined, will be
                considered as a string and the value of the parameter will be a
                random word built using [faker][faker-doc] library. The
                following parameter data types are supported, as well as their
                corresponding names in capital letters:

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
                    + Defined as a list, the value of the parameter will be
                selected from the list using [random.random.choice
                ](https://docs.python.org/library/random.html#random.choice).
                    + Defined as a string, must be a Python formatted module
                path following the format ``'path.to.module::function'`` and
                the return value will be used as the value for the parameter,
                which is useful if choosing a random value from a list doesn't
                fit your needs.
                    + Defined as a function, their return value will be used
                as the value for the parameter, which is useful if choosing a
                random value from a list doesn't fit your needs.
                If not defined and ``type``, ``value`` and ``faker`` are not
                defined, it will be a random word built using faker library.
            - **faker** (*str*/*function*): Python formatted module path to a
                function of a Faker provider used to build the value
                randomized. Can be a standard, external provider or any
                function, but if is not a provider, ``seed`` and ``locale``
                will not have effect.
                    + Defined as a string must follow the format
                ``'path.to.provider.module::function'``.
        indent (str): Indentation string used in the generated code. If not
            defined, the indentation string commonly used in the implementation
            will be used.
        quote_char (str): Quotation character for strings used in the generated
            code.
        init (bool): Includes the code needed by an implementation tp perform
            the request. Could be imports of additional modules or
            intialization of objects, depends on implementation.
        oneline (bool): Render the code in a single line.
        seed (int): Seed used generating random fake values of parameters.
            Useful if you want to generate the same set of values between
            multiples code snippets.
        locale (str): Locale used by [faker](https://faker.readthedocs.io)
            library for localization of the fake random values for parameters.
    '''
    func = get_func_by_lang_impl_method(
        language=language, impl=impl, method=method)
    func_kwargs = kwargs
    return func(url, parameters=parameters, headers=headers, indent=indent,
                oneline=oneline, seed=seed, locale=locale,
                quote_char=quote_char, **func_kwargs)


def generate_http_request_md_code_block(language=None, **kwargs):
    return '```%(language)s\n%(render)s\n```' % {
        'language': language if language else 'python',
        'render': generate_http_request_code(language=language, **kwargs),
    }
