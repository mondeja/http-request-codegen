'''http-request-codegen public API.'''

from http_request_codegen.hrc_factory import (
    DEFAULT_LANGUAGE,
    get_func_by_lang_impl_method,
)
from http_request_codegen.hrc_string import lazy_string


def generate_http_request_code(
    language=None, impl=None, method='GET',
    url='http://localhost', parameters=[],
    headers={}, files={}, indent=None,
    quote_char='\'', setup=None, teardown=None,
    oneline=False, seed=None, locale=None, wrap=80,
    **kwargs,
):
    '''Generates a code snippet of an HTTP request for a library of a given
    programming language or a CLI of a program, based on a valid HTTP method
    and a specification of parameters.

    There are some peculiarities concerning certain methods:

    ??? info "POST"

        <!-- start-POST-singularities -->
        Most POST methods implementations render their code snippets different,
        depending on *Content-Types* header, including by default some of the
        most used *Content-Types* header related behaviours:

        - The default behavior, even if you don't specify it explicitly in the
            *Content-Type* header is the generation of an
            `application/x-www-form-urlencoded` encoded request.
        - If you want to generate a ``multipart/form-data`` encoded request,
            you need to specify the files to sent using the ``files`` argument.
        - If you specifies the *Content-Type* header `application/json`, the
            parameters sent will be adjusted according to the JSON encoded POST
            request.
        - If you specifies the *Content-Type* header `text/plain`, you can only
            send one parameter and it will be adjusted accordingly following
            the implementation.
        <!-- end-POST-singularities -->

    Args:
        language (str): Programming language or plataform of the resulting code
            snippet. See [Support](/#support) to check the supported platforms
            and programming languages.
        impl (str): Implementation type used for the code snippet. It can be a
            library, a program, or a language API. See [Support](/#support)
            to check the supported implementations by language.
        method (str): HTTP method of the generated request.
        url (str, iterable, callable): URL endpoint of the generated request.

            - Defined as a string, the url will be the string itself.
            - Defined as an iterable, the url will be selected randomly
            from the iterable. Supports recursivity: until a string is not
            selected the recursion will not be stopped.
            - Defined as a callable, the url will be the returned value of
            the callable. Supports recursivity: until a string is returned the
            recursion will not be stopped.
        headers (dict): Mapping of request header names and values.
        parameters (list): List of parameters for the request. Each parameter
            must be a dictionary. This dictionary defines, for each parameter,
            what is the parameter name and how are the parameters values
            generated:

            - **name** (*str*, *list*, *function*): Parameter name. At least
                one of this or ``names`` attributes are required.
                - Defined as a string, the name will be the string itself.
                - Defined as an iterable, the name will be selected
                randomly from the iterable. Supports recursivity: until a
                string is not selected the recursion will not be stopped.
                - Defined as a callable, the name will be the returned
                value of the callable. Supports recursivity: until a string is
                returned the recursion will not be stopped.

            - **names** (*str*, *list*, *function*): Parameter name. At least
                one of this or ``name`` attributes are required.
                - Defined as an iterable, the name will be selected
                randomly from the iterable. Supports recursivity: until a
                string is not selected the recursion will not be stopped.
                - Defined as a string, must be a Python formatted module
                path following the format ``'path.to.module::function'`` and
                the return name will be used as the name for the parameter,
                which is useful if choosing a random value from a list doesn't
                fit your needs.
                - Defined as a callable, the name will be the returned
                value of the callable. Supports recursivity: until a string is
                returned the recursion will not be stopped.

            - **type** (*str*, *iterable*, *callable*): Parameter data type.
                If not defined and ``value``, ``values`` and ``faker`` are not
                defined, will be considered as a string and the value of the
                parameter will be a random word built using [faker](
                https://faker.readthedocs.io) library. For some types, other
                parameter dictionary attributes are supported, documented, if
                so, in each type. The following parameter data types are
                supported as attributes of parameters dictionaries, as well as
                their corresponding names in capital letters:

                - ``'str'``: Basic string type. Can be defined with the Python
                    builtin type ``str`` or the strings ``'str'`` and
                    ``'string'``.
                - ``'int'``: Basic integer type. Can be defined with the Python
                    builtin type ``int``, or the strings ``'int'`` and
                    ``'integer'``. As default will be an integer in the range
                    -65536 to 65536. The minimum and maximum values can be
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

                Defined as an iterable or callable, the type will be selected
                randomly from the iterable, or the returned value from the
                callable will be used. This allows you to select a random
                type from a list of custom predefined types.

            - **value** (*str*, *iterable*, *callable*): Parameter value. If
                not defined and ``type``, ``values`` and ``faker`` are not
                defined, the value of the parameter will be a random word built
                using faker library.
                - Defined as a string, the value will be the string itself.
                - Defined as an iterable, the value will be selected
                randomly from the iterable. Supports recursivity: until a
                string is not selected the recursion will not be stopped.
                - Defined as a callable, the value will be the returned
                value of the callable. Supports recursivity: until a string is
                returned the recursion will not be stopped.

            - **values** (*list*, *iterable*, *callable*): Possible parameter
                values.

                - Defined as an iterable, the value will be selected
                randomly from the iterable. Supports recursivity: until a
                string is not selected the recursion will not be stopped.
                -  Defined as a string, must be a Python formatted module
                path following the format ``'path.to.module::function'`` and
                the return value will be used as the value for the parameter,
                which is useful if choosing a random value from a list doesn't
                fit your needs.
                - Defined as a callable, the value will be the returned
                value of the callable. Supports recursivity: until a string is
                returned the recursion will not be stopped.

            - **faker** (*str*, *function*): Python formatted module path to a
                function of a Faker provider used to build the value
                randomized. Can be a standard, external provider or any
                function, but if is not a provider, ``seed`` and ``locale``
                will not have effect.
                - Defined as a string must follow the format
                ``'path.to.provider.module::function'``.

        files (dict): Mapping of files to send to URL. Only has effect for POST
            methods. If you define this argument, the `Content-Type` header of
            the request will be assumed to be `'multipart/form-data'`, but only
            will be explicitly specified in the code generated if the
            implementation needs it. Each value accepts a string, ``None`` or a
            tuple:

            + Defined as a string, must be the filepath of the file to be sent.
            + Defined as ``None``, the filepath will be randomized using
            ``faker.providers.file::file_path`` function.
            + Defined as a tuple, the first value must be the filepath of the
            file to be sent (if ``None`` will be a randomized filepath), the
            second value the content-type of the file and the third a
            dictionary of custom headers for the file.

        wrap (int): Maximum anchor of the rendered code snippet. If it exceeds
            it, the rendered code will be conveniently formatted on multiple
            lines.
        indent (str): Indentation string used in the generated code. If not
            defined, the indentation string commonly used in the implementation
            will be used.
        quote_char (str): Quotation character for strings used in the generated
            code.
        setup (bool, str): If ``True``, includes the code needed by an
            implementation to perform the request. Could be imports of
            additional modules or intialization of objects, depends on
            implementation. You can customize this snippet passing a string
            with the code snippet that you want to include.
        teardown (str): Code snippet to include after the HTTP request code.
        oneline (bool): Render the code in a single line.
        seed (int): Seed used generating random fake values of parameters.
            Useful if you want to generate the same set of values between
            multiples code snippets.
        locale (str): Locale used by [faker](https://faker.readthedocs.io)
            library to localize the faked random values for parameters.

    Raises:
        ValueError: Value is not a valid value in their context.
        TypeError: Values does not complaint with the types supported for it.
        ImportError: Python module-function path specified can not be imported
            successfully.

    Returns:
        str: HTTP request code snippet.
    '''
    _function_kwargs = {
        'parameters': parameters, 'headers': headers,
        'oneline': oneline, 'seed': seed, 'locale': locale,
        'teardown': teardown, 'wrap': wrap or float('inf'),
    }
    if indent is not None:
        _function_kwargs['indent'] = indent
    if quote_char is not None:
        _function_kwargs['quote_char'] = quote_char
    if method.lower() == 'post':
        _function_kwargs['files'] = files
    if setup is not None:
        _function_kwargs['setup'] = setup
    kwargs.update(_function_kwargs)
    return get_func_by_lang_impl_method(
        language=language.lower() if language else language,
        impl=impl,
        method=method,
    )(lazy_string(url), **kwargs)


def generate_http_request_md_fenced_code_block(
    language=None,
    fence_string='```',
    **kwargs,
):
    """Wraps [``generate_http_request_code``](#generate_http_request_code)
    function result in a Markdown fenced code block.

    Args:
        fence_string (str): Code block fence string used wrapping the code.
            It does not perform any check about if the fenced string is a
            "valid" markdown code block fence string.
        **kwargs: All other optional arguments are passed to
            [``generate_http_request_code``](#generate_http_request_code)
            function.

    Examples:
        >>> generate_http_request_md_fenced_code_block(setup=False)
        "```python\\nreq = requests.get('http://localhost')\\n```"

        >>> generate_http_request_md_fenced_code_block(fence_string='~~~',
        ...                                            setup=False)
        "~~~python\\nreq = requests.get('http://localhost')\\n~~~"

    Returns:
        str: Fenced code block with HTTP request code snippet inside.
    """
    return '{fence_string}{language}\n{render}\n{fence_string}'.format(
        language=language if language else DEFAULT_LANGUAGE,
        render=generate_http_request_code(language=language, **kwargs),
        fence_string=fence_string,
    )
