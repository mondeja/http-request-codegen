
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

=== "Basic"

    ```bash
    pytest -sv
    ```

=== "With coverage"

    ```bash
    pytest -s --cov=http_request_codegen --cov-config=setup.cfg --cov-report=html
    ```

### Lint

```bash
pre-commit run --all-files
```

## TODO

- [x] Implement implementation autodiscovering in `http_request_codegen.factory`.
- [ ] Test `http_request_codegen.python._utils::repr_str_kwarg`.
- [ ] Test `http_request_codegen.python._utils::repr_kwarg`.
