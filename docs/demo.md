# Available generators

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
