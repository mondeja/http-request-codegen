
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

=== "Formal API"

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

- [x] Implement implementation autodiscovering in `http_request_codegen.factory`.
- [x] Document and doctest `http_request_codegen.generators.python._utils`
 module.
- [x] Document and doctest `http_request_codegen.inspector` module.
- [x] Document `http_request_codegen.support` module.
- [ ] Add parametrizer that list all combinations of arguments passed to
 implementations.
- [ ] Document `http_request_codegen.api::generate_http_request_md_code_block`
 function.
- [ ] Add parameter name randomization support.
- [ ] Add url randomization support.
- [ ] Add support for random choosing from list of provider functions as
 parameter values.
