{%
  include-markdown "../README.md"
  start="<!--start-intro-->"
  end="<!--end-intro-->"
%}

!!! abstract "Remember"

    This is not a greater level API across multiple HTTP request libraries,
    but it is written so that you can generate the most common types of HTTP
    requests regardless of the implementation.

## Installation

<!-- mdpo-disable-next-line -->
=== "pip"

    ```bash
    pip install http-request-codegen
    ```

<!-- mdpo-disable-next-line -->
=== "pipenv"

    ```bash
    pipenv install http-request-codegen
    ```

<!-- mdpo-disable-next-line -->
=== "source"

    ```bash
    git clone https://github.com/mondeja/http-request-codegen.git --depth=1
    cd http-request-codegen
    python setup.py install
    ```

<!-- mdpo-disable-next-line -->
=== "development"

    ```bash
    git clone https://github.com/mondeja/http-request-codegen.git
    cd http-request-codegen
    pip install -e .[dev]
    ```

## Demo

{% for lang, impls in http_request_codegen.supported_methods().items() %}
=== "{{ lang|capitalize }}"

    {% for impl, methods in impls.items() %}
    === "{{impl}}"

        {% for method in methods %}
        === "{{method}}"

            {% if method != 'POST' %}

            === "Input"

                ```python
                import fake_module

                from http_request_codegen import generate_http_request_code

                generate_http_request_code(
                    language='{{lang}}',
                    impl='{{impl}}',
                    method='{{method}}',
                    url='https://github.com/mondeja/http-request-codegen',
                    headers={
                        'Content-Type': 'application/json',
                        'Accept-Language': '*'
                    },
                    seed={{seed}},
                    parameters=[
                        {
                            'name': 'fixed-value',
                            'value': 3
                        },
                        {
                            'name': 'dinamic-value-by-iterable',
                            'value': [1, 2, 3]  # same as 'values': [1, 2, 3]
                        },
                        {
                            'name': 'dinamic-value-by-function',
                            'value': fake_module.integers_from_1_to_10
                        },

                        # Parameter value randomization
                        {
                            'name': 'random-values-by-iterable',
                            'values': ['foo', 'bar', 'baz']
                        },
                        {
                            'name': 'random-values-by-function',
                            'values': fake_module.integers_from_1_to_10
                        },
                        {
                            'name': 'random-values-by-function-path',
                            'values': 'fake_module::integers_from_1_to_10'
                        },
                        {
                            'name': 'random-value-by-faker-provider-function-path',
                            'faker': 'faker.providers.job::job'
                        },
                        {
                            'name': 'random-string',  # by default: random word
                            'type': 'str'
                        },
                        {
                            'name': 'random-integer',
                            'type': 'int',
                        },
                        {
                            'name': 'random-integer-in-range',
                            'type': int,  # You can use Python types also
                            'min': 2,
                            'max': 5,
                        },
                        {
                            'name': 'random-float',
                            'type': 'number',  # You can use some type aliases also
                        },
                        {
                            'name': 'random-rounded-float-in-range',
                            'type': float,
                            'min': 1.555,
                            'max': 2.555,
                            'round': 3
                        },
                        {
                            'name': 'random-boolean',
                            'type': bool
                        },
                        {
                            'name': 'random-boolean-nullable',
                            'type': 'boolean',
                            'null': True
                        },
                        {
                            'name': 'random-type',
                            'type': 'random'  # random type from availables
                        },
                        {
                            'name': 'random-unique-identifier',
                            'type': 'uuid'
                        },
                        {
                            'name': 'random-id',  # positive integer
                            'type': 'id'
                        },

                        # Parameter name randomization
                        {
                            'name': ['random-name-from-iterable',
                                     'random-name-by-iterable'],
                            'type': 'str',
                        },
                        {
                            'name': fake_module.random_name_by_function,
                            'type': 'random',
                        },
                    ]
                )
                ```

                {{get_func_by_lang_impl_method(
                  language=lang,
                  impl=impl,
                  method=method).__doc__|indent(12)}}

            === "Output"

                {{http_request_codegen.generate_http_request_md_fenced_code_block(
                    language=lang,
                    impl=impl,
                    method=method,
                    url='https://github.com/mondeja/http-request-codegen',
                    headers={
                        'Content-Type': 'application/json',
                        'Accept-Language': '*'
                    },
                    seed=seed,
                    parameters=[
                        {
                            'name': 'fixed-value',
                            'value': 3
                        },
                        {
                            'name': 'dinamic-value-by-iterable',
                            'value': [1, 2, 3]
                        },
                        {
                            'name': 'dinamic-value-by-function',
                            'value': fake_module.integers_from_1_to_10
                        },
                        {
                            'name': 'random-values-by-iterable',
                            'values': ['foo', 'bar', 'baz']
                        },
                        {
                            'name': 'random-values-by-function',
                            'values': fake_module.integers_from_1_to_10
                        },
                        {
                            'name': 'random-values-by-function-path',
                            'values': 'fake_module::integers_from_1_to_10'
                        },
                        {
                            'name': 'random-value-by-faker-provider-function-path',
                            'faker': 'faker.providers.job::job'
                        },
                        {
                            'name': 'random-string',
                            'type': 'str'
                        },
                        {
                            'name': 'random-integer',
                            'type': 'int',
                        },
                        {
                            'name': 'random-integer-in-range',
                            'type': int,
                            'min': 2,
                            'max': 5,
                        },
                        {
                            'name': 'random-float',
                            'type': 'number',
                        },
                        {
                            'name': 'random-rounded-float-in-range',
                            'type': float,
                            'min': 1.555,
                            'max': 2.555,
                            'round': 3
                        },
                        {
                            'name': 'random-boolean',
                            'type': bool
                        },
                        {
                            'name': 'random-boolean-nullable',
                            'type': 'boolean',
                            'null': True
                        },
                        {
                            'name': 'random-type',
                            'type': 'random'
                        },
                        {
                            'name': 'random-unique-identifier',
                            'type': 'uuid',
                        },
                        {
                            'name': 'random-id',
                            'type': 'id'
                        },
                        {
                            'name': ['random-name-from-iterable',
                                     'random-name-by-iterable'],
                            'type': 'str',
                        },
                        {
                            'name': fake_module.random_name_by_function,
                            'type': 'random',
                        },
                    ]
                )|indent(16)}}

            {% else %}  {# POST method #}

            === "application/x-www-form-urlencoded"

                === "Input"

                    ```python
                    import fake_module

                    from http_request_codegen import generate_http_request_code

                    generate_http_request_code(
                        language='{{lang}}',
                        impl='{{impl}}',
                        method='{{method}}',
                        url='https://github.com/mondeja/http-request-codegen',
                        headers={
                            'Accept-Language': '*',
                            'Accept-Charset': 'utf-8'
                        },
                        seed={{seed}},
                        parameters=[
                            {
                                'name': 'fixed-value',
                                'value': 3
                            },
                            {
                                'name': 'dinamic-value-by-iterable',
                                'value': [1, 2, 3]  # same as 'values': [1, 2, 3]
                            },
                            {
                                'name': 'dinamic-value-by-function',
                                'value': fake_module.integers_from_1_to_10
                            },

                            # Parameter value randomization
                            {
                                'name': 'random-values-by-iterable',
                                'values': ['foo', 'bar', 'baz']
                            },
                            {
                                'name': 'random-values-by-function',
                                'values': fake_module.integers_from_1_to_10
                            },
                            {
                                'name': 'random-values-by-function-path',
                                'values': 'fake_module::integers_from_1_to_10'
                            },
                            {
                                'name': 'random-value-by-faker-provider-function-path',
                                'faker': 'faker.providers.job::job'
                            },
                            {
                                'name': 'random-string',  # by default: random word
                                'type': 'str'
                            },
                            {
                                'name': 'random-integer',
                                'type': 'int',
                            },
                            {
                                'name': 'random-integer-in-range',
                                'type': int,  # You can use Python types also
                                'min': 2,
                                'max': 5,
                            },
                            {
                                'name': 'random-float',
                                'type': 'number',  # You can use some type aliases also
                            },
                            {
                                'name': 'random-rounded-float-in-range',
                                'type': float,
                                'min': 1.555,
                                'max': 2.555,
                                'round': 3
                            },
                            {
                                'name': 'random-boolean',
                                'type': bool
                            },
                            {
                                'name': 'random-boolean-nullable',
                                'type': 'boolean',
                                'null': True
                            },
                            {
                                'name': 'random-type',
                                'type': 'random'  # random type from availables
                            },
                            {
                                'name': 'random-unique-identifier',
                                'type': 'uuid'
                            },
                            {
                                'name': 'random-id',  # positive integer
                                'type': 'id'
                            },

                            # Parameter name randomization
                            {
                                'name': ['random-name-from-iterable',
                                         'random-name-by-iterable'],
                                'type': 'str',
                            },
                            {
                                'name': fake_module.random_name_by_function,
                                'type': 'random',
                            },
                        ]
                    )
                    ```

                === "Output"

                    {{http_request_codegen.generate_http_request_md_fenced_code_block(
                        language=lang,
                        impl=impl,
                        method=method,
                        url='https://github.com/mondeja/http-request-codegen',
                        headers={
                            'Accept-Language': '*',
                            'Accept-Charset': 'utf-8'
                        },
                        seed=seed,
                        parameters=[
                            {
                                'name': 'fixed-value',
                                'value': 3
                            },
                            {
                                'name': 'dinamic-value-by-iterable',
                                'value': [1, 2, 3]
                            },
                            {
                                'name': 'dinamic-value-by-function',
                                'value': fake_module.integers_from_1_to_10
                            },
                            {
                                'name': 'random-values-by-iterable',
                                'values': ['foo', 'bar', 'baz']
                            },
                            {
                                'name': 'random-values-by-function',
                                'values': fake_module.integers_from_1_to_10
                            },
                            {
                                'name': 'random-values-by-function-path',
                                'values': 'fake_module::integers_from_1_to_10'
                            },
                            {
                                'name': 'random-value-by-faker-provider-function-path',
                                'faker': 'faker.providers.job::job'
                            },
                            {
                                'name': 'random-string',
                                'type': 'str'
                            },
                            {
                                'name': 'random-integer',
                                'type': 'int',
                            },
                            {
                                'name': 'random-integer-in-range',
                                'type': int,
                                'min': 2,
                                'max': 5,
                            },
                            {
                                'name': 'random-float',
                                'type': 'number',
                            },
                            {
                                'name': 'random-rounded-float-in-range',
                                'type': float,
                                'min': 1.555,
                                'max': 2.555,
                                'round': 3
                            },
                            {
                                'name': 'random-boolean',
                                'type': bool
                            },
                            {
                                'name': 'random-boolean-nullable',
                                'type': 'boolean',
                                'null': True
                            },
                            {
                                'name': 'random-type',
                                'type': 'random'
                            },
                            {
                                'name': 'random-unique-identifier',
                                'type': 'uuid',
                            },
                            {
                                'name': 'random-id',
                                'type': 'id'
                            },
                            {
                                'name': ['random-name-from-iterable',
                                         'random-name-by-iterable'],
                                'type': 'str',
                            },
                            {
                                'name': fake_module.random_name_by_function,
                                'type': 'random',
                            },
                        ]
                    )|indent(20)}}

            === "multipart/form-data"

                === "Input"

                    ```python
                    from http_request_codegen import generate_http_request_code

                    generate_http_request_code(
                        language='{{lang}}',
                        impl='{{impl}}',
                        method='{{method}}',
                        url='https://github.com/mondeja/http-request-codegen',
                        headers={
                            'Accept-Language': '*',
                            'Accept-Charset': 'utf-8'
                        },
                        seed={{seed}},
                        files={
                            'fixed-filepath': '/tmp/foo.txt',
                            'random-filepath': None,
                            'fixed-filepath-content-type': (
                                '/tmp/bar.csv',
                                'text/csv'
                            ),
                            'fixed-filepath-ct-header': (
                                '/tmp/bar.json',
                                'application/json',
                                {'Accept-Charset': 'utf-8'}
                            ),
                            'random-filepath-content-type': (
                                None,
                                'text/plain'
                            ),
                            'random-filepath-ct-header': (
                                None,
                                'text/csv',
                                {'Accept-Charset': 'utf-8'}
                            )
                        }
                    )
                    ```

                === "Output"

                    {{http_request_codegen.generate_http_request_md_fenced_code_block(
                        language=lang,
                        impl=impl,
                        method=method,
                        url='https://github.com/mondeja/http-request-codegen',
                        headers={
                            'Accept-Language': '*',
                            'Accept-Charset': 'utf-8'
                        },
                        seed=seed,
                        files={
                            'fixed-filepath': '/tmp/foo.txt',
                            'random-filepath': None,
                            'fixed-filepath-content-type': (
                                '/tmp/bar.csv',
                                'text/csv'
                            ),
                            'fixed-filepath-ct-header': (
                                '/tmp/bar.json',
                                'application/json',
                                {'Accept-Charset': 'utf-8'}
                            ),
                            'random-filepath-content-type': (
                                None,
                                'text/plain'
                            ),
                            'random-filepath-ct-header': (
                                None,
                                'text/csv',
                                {'Accept-Charset': 'utf-8'}
                            )
                        }
                    )|indent(20)}}

            === "application/json"

                === "Input"

                    ```python
                    import fake_module

                    from http_request_codegen import generate_http_request_code

                    generate_http_request_code(
                        language='{{lang}}',
                        impl='{{impl}}',
                        method='{{method}}',
                        url='https://github.com/mondeja/http-request-codegen',
                        headers={
                            'Content-Type': 'application/json'
                        },
                        seed={{seed}},
                        parameters=[
                            {
                                'name': 'fixed-value',
                                'value': 3
                            },
                            {
                                'name': 'dinamic-value-by-iterable',
                                'value': [1, 2, 3]  # same as 'values': [1, 2, 3]
                            },
                            {
                                'name': 'dinamic-value-by-function',
                                'value': fake_module.integers_from_1_to_10
                            },

                            # Parameter value randomization
                            {
                                'name': 'random-values-by-iterable',
                                'values': ['foo', 'bar', 'baz']
                            },
                            {
                                'name': 'random-values-by-function',
                                'values': fake_module.integers_from_1_to_10
                            },
                            {
                                'name': 'random-values-by-function-path',
                                'values': 'fake_module::integers_from_1_to_10'
                            },
                            {
                                'name': 'random-value-by-faker-provider-function-path',
                                'faker': 'faker.providers.job::job'
                            },
                            {
                                'name': 'random-string',  # by default: random word
                                'type': 'str'
                            },
                            {
                                'name': 'random-integer',
                                'type': 'int',
                            },
                            {
                                'name': 'random-integer-in-range',
                                'type': int,  # You can use Python types also
                                'min': 2,
                                'max': 5,
                            },
                            {
                                'name': 'random-float',
                                'type': 'number',  # You can use some type aliases also
                            },
                            {
                                'name': 'random-rounded-float-in-range',
                                'type': float,
                                'min': 1.555,
                                'max': 2.555,
                                'round': 3
                            },
                            {
                                'name': 'random-boolean',
                                'type': bool
                            },
                            {
                                'name': 'random-boolean-nullable',
                                'type': 'boolean',
                                'null': True
                            },
                            {
                                'name': 'random-type',
                                'type': 'random'  # random type from availables
                            },
                            {
                                'name': 'random-unique-identifier',
                                'type': 'uuid'
                            },
                            {
                                'name': 'random-id',  # positive integer
                                'type': 'id'
                            },

                            # Parameter name randomization
                            {
                                'name': ['random-name-from-iterable',
                                         'random-name-by-iterable'],
                                'type': 'str',
                            },
                            {
                                'name': fake_module.random_name_by_function,
                                'type': 'random',
                            },
                        ]
                    )
                    ```

                === "Output"

                    {{http_request_codegen.generate_http_request_md_fenced_code_block(
                        language=lang,
                        impl=impl,
                        method=method,
                        url='https://github.com/mondeja/http-request-codegen',
                        headers={
                            'Content-Type': 'application/json'
                        },
                        seed=seed,
                        parameters=[
                            {
                                'name': 'fixed-value',
                                'value': 3
                            },
                            {
                                'name': 'dinamic-value-by-iterable',
                                'value': [1, 2, 3]
                            },
                            {
                                'name': 'dinamic-value-by-function',
                                'value': fake_module.integers_from_1_to_10
                            },
                            {
                                'name': 'random-values-by-iterable',
                                'values': ['foo', 'bar', 'baz']
                            },
                            {
                                'name': 'random-values-by-function',
                                'values': fake_module.integers_from_1_to_10
                            },
                            {
                                'name': 'random-values-by-function-path',
                                'values': 'fake_module::integers_from_1_to_10'
                            },
                            {
                                'name': 'random-value-by-faker-provider-function-path',
                                'faker': 'faker.providers.job::job'
                            },
                            {
                                'name': 'random-string',
                                'type': 'str'
                            },
                            {
                                'name': 'random-integer',
                                'type': 'int',
                            },
                            {
                                'name': 'random-integer-in-range',
                                'type': int,
                                'min': 2,
                                'max': 5,
                            },
                            {
                                'name': 'random-float',
                                'type': 'number',
                            },
                            {
                                'name': 'random-rounded-float-in-range',
                                'type': float,
                                'min': 1.555,
                                'max': 2.555,
                                'round': 3
                            },
                            {
                                'name': 'random-boolean',
                                'type': bool
                            },
                            {
                                'name': 'random-boolean-nullable',
                                'type': 'boolean',
                                'null': True
                            },
                            {
                                'name': 'random-type',
                                'type': 'random'
                            },
                            {
                                'name': 'random-unique-identifier',
                                'type': 'uuid',
                            },
                            {
                                'name': 'random-id',
                                'type': 'id'
                            },
                            {
                                'name': ['random-name-from-iterable',
                                         'random-name-by-iterable'],
                                'type': 'str',
                            },
                            {
                                'name': fake_module.random_name_by_function,
                                'type': 'random',
                            },
                        ]
                    )|indent(20)}}


            === "text/plain"

                === "Input"

                    ```python
                    from http_request_codegen import generate_http_request_code

                    generate_http_request_code(
                        language='{{lang}}',
                        impl='{{impl}}',
                        method='{{method}}',
                        url='https://github.com/mondeja/http-request-codegen',
                        headers={
                            'Content-Type': 'text/plain'
                        },
                        seed={{seed}},
                        parameters=[
                            {
                                'name': 'random-values-by-iterable',
                                'values': ['foo', 'bar', 'baz']
                            }
                        ]
                    )
                    ```

                === "Output"

                    {{http_request_codegen.generate_http_request_md_fenced_code_block(
                        language=lang,
                        impl=impl,
                        method=method,
                        url='https://github.com/mondeja/http-request-codegen',
                        headers={
                            'Content-Type': 'text/plain'
                        },
                        seed=seed,
                        parameters=[
                            {
                                'name': 'random-values-by-iterable',
                                'values': ['foo', 'bar', 'baz']
                            }
                        ]
                    )|indent(20)}}

            {% endif %}
        {% endfor %}
    {% endfor %}
{% endfor %}

## Support

{% for lang, impls in http_request_codegen.supported_features().items() %}
=== "{{lang|capitalize}}"

    {% for impl, methods in impls.items() %}
    === "{{impl}}"

        {{supported_features_md_table(methods)}}

    {% endfor %}

{% endfor %}
