'''http-request-codegen public API.'''

from http_request_codegen.factory import (
    DEFAULT_LANGUAGE,
    get_func_by_lang_impl_method
)


def generate_http_request_code(language=None, impl=None, method='GET',
                               url='localhost', parameters=[], headers={},
                               indent=None, quote_char='\'', init=True,
                               oneline=False, seed=None, locale=None,
                               wrap=80, **kwargs):
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
        url (str, iterable, callable): URL endpoint of the generated request.
                + Defined as a string, the url will be the string itself.
                + Defined as an iterable, the url will be selected randomly
            from the iterable. Supports recursivity: until a string is not
            selected the recursion will not be stopped.
                + Defined as a callable, the url will be the returned value of
            the callable. Supports recursivity: until a string is returned the
            recursion will not be stopped.
        headers (dict): Mapping of request header names and values.
        parameters (list): List of parameters for the request. Each parameter
            must be a dictionary. This dictionary defines, for each parameter,
            what is the parameter name and how are the parameters values
            generated:

            - **name** (*str*, *list*, *function*): Parameter name. At least
                one of this or ``names`` attributes are required.
                    + Defined as a string, the name will be the string itself.
                    + Defined as an iterable, the name will be selected
                randomly from the iterable. Supports recursivity: until a
                string is not selected the recursion will not be stopped.
                    + Defined as a callable, the name will be the returned
                value of the callable. Supports recursivity: until a string is
                returned the recursion will not be stopped.
            - **names** (*str*, *list*, *function*): Parameter name. At least
                one of this or ``name`` attributes are required.
                    + Defined as an iterable, the name will be selected
                randomly from the iterable. Supports recursivity: until a
                string is not selected the recursion will not be stopped.
                    + Defined as a string, must be a Python formatted module
                path following the format ``'path.to.module::function'`` and
                the return name will be used as the name for the parameter,
                which is useful if choosing a random value from a list doesn't
                fit your needs.
                    + Defined as a callable, the name will be the returned
                value of the callable. Supports recursivity: until a string is
                returned the recursion will not be stopped.
            - **type** (*str*): Parameter data type. If not defined and
                ``value``, ``values`` and ``faker`` are not defined, will be
                considered as a string and the value of the parameter will be a
                random word built using [faker][faker-doc] library. For some
                types, other parameter dictionary attributes are supported,
                documented, if so, in each type. The following parameter data
                types are supported as attributes of parameters dictionaries,
                as well as their corresponding names in capital letters:

                - ``'str'``: Basic string type. Can be defined with the Python
                    builtin type ``str`` or the strings ``'str'`` and
                    ``'string'``.
                - ``'int'``: Basic integer type. Can be defined with the Python
                    builtin type ``int``, or the strings ``'int'`` and
                    ``'integer'``. As default will be an integer in the range
                    -65536 to -65536. The minimum and maximum values can be
                    defined with ``min`` and ``max`` parameter optional
                    attributes.
                - ``'float'``: Floating point number type. Can be defined
                    with the Python builtin type ``float``, or the strings
                    ``'float'`` and ``number``. As default will be in the range
                    -65536 to 65536. The minimum and maximum values
                    can be defined with ``min`` and ``max`` parameter optional
                    attributes and can be rounded with ``round`` Python builtin
                    function using ``round`` parameter optional attribute.
                - ``'bool'``: Basic boolean type. Can be defined with the
                    Python builtin type ``bool``, or the strings ``'bool'``
                    and ``'boolean'``. Returns as parameter value one of the
                    strings ``'true'`` or ``'false'``. If you pass the optional
                    parameter attribute ``null`` as ``True``, the string
                    ``'null'`` can also be returned.
                - ``'uuid'``: Unique identifier type. Can be defined with the
                    Python type ``uuid.UUID``, or the strings ``'uuid'``
                    and ``'uuid4'``. It's a unique identifier v4 encoded as
                    hexadecimal string.
                - ``'id'``: Basic integer id. It's a positive integer in the
                    range 1 to 65536. The maximum value can be defined by
                    optional ``max`` attribute.
                - ``'random'``: Random type between the available types. You
                    can define a set of possible types passing an iterable
                    to ``types`` optional parameter attribute.
            - **value** (*str*, *iterable*, *callable*): Parameter value. If
                not defined and ``type``, ``values`` and ``faker`` are not
                defined, the value of the parameter will be a random word built
                using faker library.
                    + Defined as a string, the value will be the string itself.
                    + Defined as an iterable, the value will be selected
                randomly from the iterable. Supports recursivity: until a
                string is not selected the recursion will not be stopped.
                    + Defined as a callable, the value will be the returned
                value of the callable. Supports recursivity: until a string is
                returned the recursion will not be stopped.
            - **values** (*list*, *iterable*, *callable*): Possible parameter
                values.
                    + Defined as an iterable, the value will be selected
                randomly from the iterable. Supports recursivity: until a
                string is not selected the recursion will not be stopped.
                    + Defined as a string, must be a Python formatted module
                path following the format ``'path.to.module::function'`` and
                the return value will be used as the value for the parameter,
                which is useful if choosing a random value from a list doesn't
                fit your needs.
                    + Defined as a callable, the value will be the returned
                value of the callable. Supports recursivity: until a string is
                returned the recursion will not be stopped.
            - **faker** (*str*, *function*): Python formatted module path to a
                function of a Faker provider used to build the value
                randomized. Can be a standard, external provider or any
                function, but if is not a provider, ``seed`` and ``locale``
                will not have effect.
                    + Defined as a string must follow the format
                ``'path.to.provider.module::function'``.
        wrap (int): Maximum anchor of the code. If it exceeds it, the output
            code will be conveniently formatted on multiple lines.
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

    Raises:
        ValueError: One of the values is not a valid value in their
            context.
        TypeError: One of the values does not complaint with the types
            supported for it.
        ImportError: One of the Python module-function paths specified can not
            be imported successfully.

    Returns:
        str: HTTP request code snippet.
    '''
    return get_func_by_lang_impl_method(
        language=language, impl=impl, method=method
    )(
        url, parameters=parameters, headers=headers, indent=indent,
        oneline=oneline, seed=seed, locale=locale, init=init,
        wrap=wrap or float('inf'), quote_char=quote_char, **kwargs
    )


def generate_http_request_md_fenced_code_block(language=None,
                                               fence_string='```',
                                               **kwargs):
    """Wraps [``generate_http_request_code``](#generate_http_request_code)
    function result in a Markdown fenced code block.

    Args:
        fence_string (str): Code block fence string used wrapping the code.
            It does not perform any check about if the fenced string is a
            "valid" markdown code block fence string.
        **kwargs: All optional arguments are passed to
            [``generate_http_request_code``](#generate_http_request_code)
            function.

    Examples:
        >>> print(generate_http_request_md_fenced_code_block())
        ```python
        import requests
        <BLANKLINE>
        req = requests.get('localhost')
        ```

        >>> print(
        ...     generate_http_request_md_fenced_code_block(fence_string='~~~'))
        ~~~python
        import requests
        <BLANKLINE>
        req = requests.get('localhost')
        ~~~

    Returns:
        str: Fenced code block with HTTP request code snippet inside.
    """
    return '%(fence_string)s%(language)s\n%(render)s\n%(fence_string)s' % {
        'language': language if language else DEFAULT_LANGUAGE,
        'render': generate_http_request_code(language=language, **kwargs),
        'fence_string': fence_string
    }
