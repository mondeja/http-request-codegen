[![PyPI version][pypi-version-image]][pypi-link]
[![Test][test-image]][test-link]
[![Documentation][docs-image]][docs-link]
[![Coverage status][coverage-image]][coverage-link]

!!! warning
    This library is currently under development, only supporting a few
    methods and implementations (see [Support](#support)). Please wait before
    use it and [help me][pull-requests-link] with implementations if you are
    interested.

**http-request-codegen** generates HTTP request code snippets for different
implementations. It's perfect if you want to include examples documenting APIs.
Supports the following features:

- Request parameters values randomization using multiples strategies:
    - Random values from lists and functions.
    - Random values from data types.
    - Random values from [Faker providers][faker-providers-doc].
    - Randomization seeds.
    - Localization.
- Request headers customization.
- Request optional arguments.
- Custom line wrapping.
- Custom indentation.
- Custom quotation character.
- Rendering in one line.

## Installation

=== "pip"

    ```bash
    pip install http-request-codegen
    ```

=== "pipenv"

    ```bash
    pipenv install http-request-codegen
    ```

=== "source"

    ```bash
    git clone https://github.com/mondeja/http-request-codegen.git --depth=1
    cd http-request-codegen
    python setup.py install
    ```

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
                                'name': 'fixed-value',
                                'value': 3
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
                            'Content-Type': 'text/plain'
                        },
                        seed=seed,
                        parameters=[
                            {
                                'name': 'fixed-value',
                                'value': 3
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

## **Public API**

### **`generate_http_request_code`**

```python
from http_request_codegen import generate_http_request_code
```

::: http_request_codegen.generate_http_request_code

### **`generate_http_request_md_fenced_code_block`**

```python
from http_request_codegen import generate_http_request_md_fenced_code_block
```

::: http_request_codegen.generate_http_request_md_fenced_code_block

[pypi-version-image]: https://img.shields.io/pypi/v/http-request-codegen?label=version
[pypi-link]: https://pypi.org/project/http-request-codegen
[test-image]: https://img.shields.io/github/workflow/status/mondeja/http-request-codegen/CI?label=tests&logo=github
[test-link]: https://github.com/mondeja/http-request-codegen/actions?query=workflow%3ACI
[docs-image]: https://img.shields.io/github/workflow/status/mondeja/http-request-codegen/Github%20Pages?label=docs&logo=github
[docs-link]: https://mondeja.github.io/http-request-codegen
[coverage-image]: https://img.shields.io/coveralls/github/mondeja/http-request-codegen?logo=coveralls
[coverage-link]: https://coveralls.io/github/mondeja/http-request-codegen

[pull-requests-link]: https://github.com/mondeja/http-request-codegen/pulls

[faker-doc]: https://faker.readthedocs.io
[faker-providers-doc]: https://faker.readthedocs.io/en/master/providers.html
