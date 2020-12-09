'''Javascript fetch code snippets generator.'''

from collections import OrderedDict


try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from http_request_codegen.generators.javascript._utils import (
    DEFAULT_INDENT,
    DEFAULT_QUOTE_CHAR,
    DEFAULT_WRAP,
    escape_by_quote,
    str_definition
)
from http_request_codegen.hrc_valuer import (
    lazy_name_by_parameter,
    lazy_value_by_parameter
)


def get(url, parameters=[], headers={}, indent=DEFAULT_INDENT,
        quote_char=DEFAULT_QUOTE_CHAR, setup=False, teardown=None,
        oneline=False, wrap=DEFAULT_WRAP, seed=None, locale=None,
        **kwargs):
    '''This implementation will emulate browsers\' fetch API by default.
    using Promises-like response processing.

    If you want to simulate a NodeJS environment, pass the parameter ``setup``
    as ``True`` and the next initialization snippet will be prepended to the
    generated code:

    ```javascript
    const fetch = require(\'node-fetch\');
    ```

    For ESM imports emulation, use
    ``setup='import fetch from \\'node-fetch\\';\\n\\n'``, thus the
    initialization snippet will be:

    ```javascript
    import fetch from \'node-fetch\';
    ```

    Of course, you can customize this initialization for other environments.
    For example, polyfill the API using
    [whatwg](https://github.com/github/fetch) as ESM module with
    ``setup='import \\'whatwg-fetch\\';\\n\\n'``:

    ```javascript
    import \'whatwg-fetch\';
    ```
    '''

    '''
    Note that this implementation does not discover the length of the code to
    generate it in multiple lines, like Python requests does. This is because
    in Javascript, promises are chained in multiple lines, thus next structure
    of code would be weird:

    ```javascript
    fetch('<url>').then(function(response) {}, function(error) {});
    ```

    So ``wrap`` argument is used only to wrap strings in multiples lines,
    instead of use it for implement the request in multiples or one line.
    '''

    response = ''

    # initialization
    if setup:
        if isinstance(setup, str):
            response += setup
        else:
            # If `setup == True`, 'node-fetch' for NodeJS is required
            response += ('const fetch = require(\'node-fetch\');'
                         '%(newline)s%(newline)s') % {
                'newline': '\n' if not oneline else '',
            }

    if parameters:
        parameters_dict = OrderedDict({})
        for parameter in parameters:
            parameters_dict[lazy_name_by_parameter(parameter, seed=seed)] = \
                lazy_value_by_parameter(parameter, seed=seed, locale=locale)
        url = '?'.join([url, urlencode(parameters_dict)])

    if oneline:
        _url = ('%(quote_char)s%(url)s%(quote_char)s') % {
            'quote_char': quote_char,
            'url': escape_by_quote(url, quote_char)
        }
    else:
        _url = str_definition(url, indent=indent, quote_char=quote_char,
                              wrap=wrap)
    response += ('fetch(%(newline)s%(indent)s%(url)s%(comma)s'
                 '%(space)s%(newline)s') % {
        'newline': '\n' if not oneline else '',
        'indent': indent if not oneline else '',
        'url': _url,
        'comma': ',' if (parameters or headers or kwargs) else '',
        'space': ' ' if (oneline and (parameters or headers or kwargs))
                 else '',
    }

    # options render
    if headers or kwargs:
        response += '%(indent)s{%(newline)s' % {
            'indent': indent if not oneline else '',
            'newline': '\n' if not oneline else ''
        }

    if headers:
        response += ('%(indent)s%(indent)s%(quote_char)sheaders%(quote_char)s:'
                     ' {%(newline)s') % {
            'indent': indent if not oneline else '',
            'newline': '\n' if not oneline else '',
            'quote_char': quote_char if kwargs else ''
        }

        for i, (key, value) in enumerate(headers.items()):
            response += ('%(indent)s%(quote_char)s%(key)s'
                         '%(quote_char)s: %(value)s%(comma)s%(newline)s') % {
                'newline': '\n' if not oneline else '',
                'indent': indent * 3 if not oneline else '',
                'quote_char': quote_char,
                'key': escape_by_quote(key, quote_char),
                'value': str_definition(value,
                                        indent=' ' * (
                                            len(indent) * 3 + len(key) + 4),
                                        quote_char=quote_char,
                                        wrap=wrap),
                'comma': ',' if i < len(headers) - 1 else ''
            }
        response += '%(indent)s}%(comma)s%(newline)s' % {
            'indent': indent * 2 if not oneline else '',
            'comma': ',' if kwargs else '',
            'newline': '\n' if not oneline else ''
        }

    if kwargs:
        for i, (key, value) in enumerate(kwargs.items()):
            if isinstance(value, str):
                _value = str_definition(value,
                                        indent=' ' * (
                                            len(indent) * 3 + len(key) + 3),
                                        quote_char=quote_char,
                                        wrap=wrap)
            else:
                _value = str(value)
            response += ('%(indent)s%(quote_char)s%(key)s%(quote_char)s:'
                         ' %(value)s%(comma)s%(newline)s') % {
                'newline': '\n' if not oneline else '',
                'indent': indent * 2 if not oneline else '',
                'quote_char': quote_char,
                'key': escape_by_quote(key, quote_char),
                'value': _value,
                'comma': ',' if i < len(kwargs) - 1 else '',
            }

    if headers or kwargs:
        response += '%(indent)s}%(newline)s' % {
            'indent': indent if not oneline else '',
            'newline': '\n' if not oneline else '',
        }

    response += (').then(function(response) {%(newline)s%(indent)s'
                 'console.log(response)%(separator)s%(newline)s}).catch('
                 'function(error) {%(newline)s%(indent)sconsole.error('
                 '%(quote_char)sError:%(quote_char)s, error)%(separator)s'
                 '%(newline)s});') % {
        'newline': '\n' if not oneline else '',
        'indent': indent if not oneline else '',
        'quote_char': quote_char,
        'separator': ';' if not oneline else ''
    }

    if teardown:
        response += teardown

    return response


def post():
    pass
