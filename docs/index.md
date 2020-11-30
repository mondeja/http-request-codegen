[![PyPI version][pypi-version-image]][pypi-link]
[![Test][test-image]][test-link]
[![Documentation][docs-image]][docs-link]
[![Coverage status][coverage-image]][coverage-link]

**http-request-codegen** generates HTTP request code snippets for different
implementations. It's perfect if you want to include examples documenting APIs.
Supports the following features:

- Parameters values randomization using multiples strategies:
    - Random values from lists and functions.
    - Random values from data types.
    - Random values from [Faker providers][faker-providers-doc].
    - Randomization seeds.
    - Localization.
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
        
            === "Input"
            
                ```python
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
                          'value': 32
                      },
                      {
                          'name': 'random-values-by-list',
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
                          'name': 'boolean',
                          'type': bool
                      },
                      {
                          'name': 'unique-identifier',
                          'type': 'uuid'
                      },
                      {
                          'name': 'id',  # positive integer
                          'type': 'id'
                      },
                      {
                          'name': 'filepath',
                          'type': 'file'  # 'faker.providers.file::file_path'
                      }
                  ]
                )
                ```
                
            
            === "Output"
          
                {{http_request_codegen.generate_http_request_md_code_block(
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
                          'value': 32
                      },
                      {
                          'name': 'random-values-by-list',
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
                          'name': 'boolean',
                          'type': bool
                      },
                      {
                          'name': 'unique-identifier',
                          'type': 'uuid',
                      },
                      {
                          'name': 'id',
                          'type': 'id'
                      },
                      {
                          'name': 'filepath',
                          'type': 'file'
                      }
                  ]
                )|indent(16)}}
            
            
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

## **Reference**

### **`generate_http_request_code`**

```python
from http_request_codegen import generate_http_request_code
```

::: http_request_codegen.generate_http_request_code

[pypi-version-image]: https://img.shields.io/pypi/v/http-request-codegen?label=version
[pypi-link]: https://pypi.org/project/http-request-codegen
[test-image]: https://img.shields.io/github/workflow/status/mondeja/http-request-codegen/CI?label=tests&logo=github
[test-link]: https://github.com/mondeja/http-request-codegen/actions?query=workflow%3ACI
[docs-image]: https://img.shields.io/github/workflow/status/mondeja/http-request-codegen/Github%20Pages?label=docs&logo=github
[docs-link]: https://mondeja.github.io/http-request-codegen
[coverage-image]: https://img.shields.io/coveralls/github/mondeja/http-request-codegen?logo=coveralls
[coverage-link]: https://coveralls.io/github/mondeja/http-request-codegen

[faker-doc]: https://faker.readthedocs.io
[faker-providers-doc]: https://faker.readthedocs.io/en/master/providers.html
