
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

## Developing implementations

To develop an HTTP method function for a library or a program, you need to take
in accounts all parameters described in
[``generate_http_request_code``](/reference#generate_http_request_code)
function, but not the randomized values passed in ``parameters`` argument,
because ``http_request_codegen`` provides functions that can handle these.

### Oone line wrapping behaviour

The first thing to take in account (and the most complicated one) is the
behaviour of wrapping (``wrap`` argument) rendering as if ``oneline=True``
is passed. The question is: can a snippet of code be outputted in one line if
the estimated length of the request is lower than ``wrap`` argument value?

For example, Python requests can be rendered using this kind of code, in one
line:

```python
import requests

req = requests.get('https://github.com/mondeja/http-request-codegen')
```

...or using multiple lines (``wrap`` is lower than expected length):

```python
import requests

req = requests.get(
  'https://github.com/mondeja/http-request-codegen'
)
```

Of course, this also affects ``parameters``, ``headers`` and ``kwargs``:

```python
import requests

req = requests.get('localhost', params={'foo': 'bar'}, headers={'foo': 'bar'})
```

...which can be outputted in multiple lines:

```python
import requests

req = requests.get(
    'localhost',
    params={'foo': 'bar'},
    headers={'foo': 'bar'}
)
```

Since this behaviour can depend both ``oneline`` and ``wrap`` arguments, the
recommended way of implement this is to calculate the length of the expected
request inside the code snippet, and, if it is greater or equal to ``wrap``
argument, must be rendered as if ``oneline=True``.

!!! tip

    You can see an example of this type of implementation at
    ``http_request_codegen.generators.python.requests::get`` function.
    
But other implementations could be rendered in multiples lines regardless the
``wrap`` argument value.

For example, the Javascript fetch API implementation will output always a
multiline code snippet (unless ``oneline=True`` is explicitly defined), because
the Javascript Promises writing in single line is not a common syntax and there
is a little chance that the generated request could not be wrapped given the
default wrap value (80 in this case). The minimum reasonable possible code
snippet in one line for Javascript fetch API implementation would be:

```javascript
fetch('localhost').then(function(response) {}).catch(function(error) {console.error(error)});
```

...which exceeds the default ``wrap`` value length (80). In such type of cases,
there is no need of calculate the expected generated code snippet request
length before build their output.

!!! tip

    You can see an example of this type of implementation at
    ``http_request_codegen.generators.javascript.fetch::get`` function.

In the first case, you need to iterate over ``parameters``, ``headers`` and
``kwargs`` arguments to compute the expected length, then compare the expected
length with ``wrap`` argument value and, if it reaches it, define an internal
``oneline=True`` like behaviour. In the second, you can assume that the
generated code is multiline unless ``oneline=True`` is explicitly defined as
argument.

### Randomizing values

The library provides the functions
[``lazy_name_by_parameter``](/reference#lazy_name_by_parameter) and
[``lazy_value_by_parameter``](/reference#lazy_value_by_parameter) which returns
the name and the value of a parameter given a parameter dictionary
specification. 

- These must be used to randomize parameters in a unified way across
 implementations as described in
 [``generate_http_request_code``](/reference#generate_http_request_code)
 function documentation.
- Both always must take ``seed`` and ``locale`` arguments passed to the method
 function implementor.

### Language/platform utilities

You can create an `_utils.py` module inside a language or platform package
to store utilities that could help in the process of building the code snippet,
like:

- Define default indentation for the language/platform (``indent`` argument).
- Define default wrapping length value (``wrap`` argument).
- Define default quotation character/s (``quote_char`` argument).
- Escape quotes of values (according to given ``quote_char`` argument).
- Create greater level functions of code generation for the language/platform,
 such as string definitions with wrapping behaviour, dictionary definitions...

!!! tip

    See current ``_utils.py`` modules of ``generators`` packages as reference.

### Creating test cases

Use the script ``scripts/create-impl-test-cases.py`` to create possible
generated code snippets cases accordingly to combination of arguments. This
will help you developing implementations because saves you the need of execute
every possible combination of arguments. Use it as follows:

```bash
rm -rf cases && python3 scripts/create-impl-test-cases.py \
  --language python \
  --implementation requests \
  --method GET \
  --directory cases
```

Previous command will create a ``cases/`` directory with a lot of code snippets
generated, given the combinations described in ``tests/combinations.py``.

When you will have manually revised that all code snippets are generated
correctly, you can create a test for the implementation at
``tests/test_generators/test_<lang>/test_<impl>/test_<impl>.py``, placing the
``cases/`` directory at
``tests/test_generators/test_<lang>/test_<impl>/<METHOD>``.

For example, for Python requests GET method, the test module would be
``tests/test_generators/test_python/test_requests/test_requests.py`` and
the ``cases/`` directory would be placed at
``tests/test_generators/test_python/test_requests/GET/``.

!!! tip

    You can use an already implemented test module as a reference to write the
    one for the implementation.


## TODO

- [x] Implement real server testing for POST requests.
- [x] Implement fetch Javascript GET. 
- [ ] Implement fetch Javascript POST.
- [ ] Implement curl Bash GET. 
- [ ] Implement curl Bash POST. 
- [ ] Add more oneline tests for POST requests.
- [ ] Add support for random URLs passing ``None`` to ``url`` argument.
- [ ] Create Python string wrapping algorithm that could wrap whitespaces in a
 smart way.
- [ ] Create Javascript string wrapping algorithm that could wrap whitespaces
 in a smart way.
