
## Setup development environment


=== "Linux/MacOS"

    === "pip + virtualenv"

        ```bash
        git clone https://github.com/mondeja/http-request-codegen.git
        python3 -m virtualenv venv
        . venv/bin/activate
        pip install -e .[dev]
        pre-commit install
        ```

=== "Windows"

    === "pip + virtualenv"

        ```cmd
        git clone https://github.com/mondeja/http-request-codegen.git
        python3 -m virtualenv venv
        venv\Scripts\activate.bat
        pip install -e .[dev]
        pre-commit install
        ```

## Development commands

### Test

=== "All"

    ```bash
    pytest -sv
    ```

=== "Coverage"

    ```bash
    pytest -s --cov=http_request_codegen --cov-config=setup.cfg --cov-report=html
    ```

=== "Doctests"

    ```bash
    pytest -svv --doctest-modules http_request_codegen
    ```

### Lint

```bash
pre-commit run --all-files
```

## TODO

- [x] Implement implementation autodiscovering in
 `http_request_codegen.factory`.
- [x] Document and doctest `http_request_codegen.generators.python._utils`
 module.
- [x] Document and doctest `http_request_codegen.inspector` module.
- [x] Document `http_request_codegen.support` module.
- [x] Add parameter name randomization support.
- [x] Add url randomization support.
- [x] Implement random parameter type (lazy string and `'random'` type).
- [x] Document lazy strings in parameter type.
- [x] Document ``bool`` type in parameters types.
- [x] Implement nullable value for ``bool`` type.
- [x] Document ``random`` type in parameters types.
- [x] Implement ``random`` type filtering between set of types.
- [x] Document ``uuid`` type in parameters types.
- [x] Document ``id`` type in parameters types.
- [x] Document ``float`` type ``max``, ``min`` and ``round`` parameters.
- [x] Document ``int`` type ``max`` and ``min`` parameters.
- [x] Add parametrizer that list all combinations of arguments passed to
 implementations.
- [x] Implement custom code block fence string in
 `http_request_codegen.api::generate_http_request_md_fenced_code_block` function.
- [x] Document `http_request_codegen.api::generate_http_request_md_fenced_code_block`
 function.
- [x] Document `http_request_codegen.valuer::lazy_value_by_parameter` function.
- [x] Document `http_request_codegen.valuer::lazy_name_by_parameter` function.
- [x] Change `init` argument by `setup`.
- [x] Allow `setup` argument to take a string for customize the initialization.
- [x] Implement `teardown` argument.
- [x] Implement real testing of generated HTTP requests against Flask server.
- [x] Implement Python requests POST.
- [x] Add complete demo for POST methods.
- [x] Use [mkdocs-exclude-plugin](https://github.com/apenwarr/mkdocs-exclude)
 to remove `fake_module.py` and `__pycache__` from built documentation.
- [ ] Test ``http_request_codegen.valuer.::lazy_name_by_parameter`` function.
- [ ] Add more oneline tests for POST requests.
- [x] Implement real server testing for POST requests.
- [ ] Add support for random URLs passing ``None`` to ``url`` argument.
- [ ] Create Python string wrapping algorithm that could wrap whitespaces in a
 smart way.
