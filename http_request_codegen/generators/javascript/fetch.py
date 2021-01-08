'''Javascript fetch code snippets generator.'''

import os
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
from http_request_codegen.hrc_exceptions import (
    raise_post_text_plain_n_parameters_not_1
)
from http_request_codegen.hrc_valuer import (
    lazy_name_by_parameter,
    lazy_value_by_parameter
)


def _promises_chain_render(quote_char=DEFAULT_QUOTE_CHAR,
                           indent=DEFAULT_INDENT,
                           oneline=False):
    return (').then(function(response) {%(newline)s%(indent)s'
            'console.log(response)%(separator)s%(newline)s}).catch('
            'function(err) {%(newline)s%(indent)sconsole.error('
            '%(quote_char)sError:%(quote_char)s, err)%(separator)s'
            '%(newline)s});') % {
        'newline': '\n' if not oneline else '',
        'indent': indent if not oneline else '',
        'quote_char': quote_char,
        'separator': ';' if not oneline else ''
    }


def _headers_render(headers, indent=DEFAULT_INDENT,
                    quote_char=DEFAULT_QUOTE_CHAR, oneline=False,
                    wrap=DEFAULT_WRAP, _comma_at_end=False):
    response = ('%(indent)s%(indent)sheaders:'
                ' {%(newline)s') % {
        'indent': indent if not oneline else '',
        'newline': '\n' if not oneline else '',
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
        'comma': ',' if _comma_at_end else '',
        'newline': '\n' if not oneline else ''
    }

    return response


def _kwargs_render(kwargs, indent=DEFAULT_INDENT, wrap=DEFAULT_WRAP,
                   quote_char=DEFAULT_QUOTE_CHAR, oneline=False):
    response = ''
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
    return response


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

    '''Implementation details:

    Note that this implementation does not discover the length of the code to
    generate it in multiple lines, like Python requests does. This is because
    in Javascript, promises are chained in multiple lines, thus next structure
    of code would be weird:

    ```javascript
    fetch('<url>').then(function(response) {}, function(err) {});
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
            response += ('const fetch = require(%(quote_char)snode-fetch'
                         '%(quote_char)s);%(newline)s%(newline)s') % {
                'newline': '\n' if not oneline else '',
                'quote_char': quote_char
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
        response += _headers_render(headers, indent=indent, oneline=oneline,
                                    quote_char=quote_char, wrap=wrap,
                                    _comma_at_end=bool(kwargs))

    if kwargs:
        response += _kwargs_render(kwargs, indent=indent, oneline=oneline,
                                   quote_char=quote_char, wrap=wrap)

    if headers or kwargs:
        response += '%(indent)s}%(newline)s' % {
            'indent': indent if not oneline else '',
            'newline': '\n' if not oneline else '',
        }

    response += _promises_chain_render(quote_char=quote_char, indent=indent,
                                       oneline=oneline)

    if teardown:
        response += teardown

    return response


def post(url, parameters=[], files={}, headers={}, indent=DEFAULT_INDENT,
         quote_char=DEFAULT_QUOTE_CHAR, setup=True, teardown=None,
         oneline=False, wrap=DEFAULT_WRAP, seed=None, locale=None,
         **kwargs):
    # (no setup -> web / setup -> node)
    response = ''

    # Discover content-type
    content_type = 'application/x-www-form-urlencoded'
    for key, value in headers.items():
        if key.lower() == 'content-type':
            content_type = value
            break
    if content_type.startswith('multipart/form-data') or files:
        content_type = 'multipart/form-data'

    # Initialization will depend on content type
    if setup:
        if isinstance(setup, str):
            response += setup
        else:
            if content_type == 'multipart/form-data':
                response += ('const fs = require(%(quote_char)s'
                             'fs%(quote_char)s);%(newline)s%(newline)s') % {
                    'quote_char': quote_char,
                    'newline': '\n' if not oneline else '',
                }
            response += ('const fetch = require(%(quote_char)s'
                         'node-fetch%(quote_char)s);') % {
                'quote_char': quote_char,
            }
            if content_type == 'multipart/form-data':
                response += ('%(newline)sconst FormData = require('
                             '%(quote_char)sform-data%(quote_char)s);') % {
                    'quote_char': quote_char,
                    'newline': '\n' if not oneline else '',
                }
            if not oneline:
                response += '\n\n'

    if content_type == 'multipart/form-data':
        body = 'formData'

        # if we are sending files from the browser, select all files
        if not setup and files:
            response += ('const files = document.querySelector('
                         '%(quote_char)sinput[type=%(other_quote_char)s'
                         'file%(other_quote_char)s]%(quote_char)s);'
                         '%(newline)s%(newline)s') % {
                'quote_char': quote_char,
                'other_quote_char': '"' if quote_char == '\'' else '\'',
                'newline': '\n' if not oneline else ''
            }

        response += 'const formData = new FormData();%(newline)s' % {
            'newline': '\n' if not oneline else '',
        }

        # parameters render
        for parameter in parameters:
            name = lazy_name_by_parameter(parameter, seed=seed)
            value = lazy_value_by_parameter(
                parameter, seed=seed, locale=locale)

            # 20 here is the length of `formData.append(, );`
            _multiline_param = False
            if 20 + len(quote_char) * 4 + len(name) + len(str(value)) > wrap:
                _multiline_param = True

            if _multiline_param:
                _param_name = str_definition(name, indent=indent,
                                             quote_char=quote_char, wrap=wrap)
                _param_value = str_definition(value, indent=indent,
                                              quote_char=quote_char, wrap=wrap)
            else:
                _value_name_schema = '%(quote_char)s%(string)s%(quote_char)s'
                _param_name = _value_name_schema % {
                    'quote_char': quote_char,
                    'string': escape_by_quote(name, quote_char),
                }
                _param_value = _value_name_schema % {
                    'quote_char': quote_char,
                    'string': escape_by_quote(str(value), quote_char),
                }

            response += ('formData.append(%(newline)s%(indent)s'
                         '%(param_name)s,%(space)s'
                         '%(newline)s%(indent)s%(param_value)s'
                         '%(newline)s);') % {
                'newline': '\n' if (not oneline and _multiline_param) else '',
                'indent': indent if (not oneline and _multiline_param) else '',
                'space': ' ' if (oneline or _multiline_param) else '',
                'param_name': _param_name,
                'param_value': _param_value,
            }
            if not oneline:
                response += '\n'

        # files render
        for i, (file_param_name, file_data) in enumerate(files.items()):
            response += 'formData.append('
            if not oneline:
                _file_param_name = str_definition(file_param_name,
                                                  quote_char=quote_char,
                                                  wrap=wrap,
                                                  indent=indent)
            else:
                _file_param_name = ('%(quote_char)s'
                                    '%(file_param_name)s'
                                    '%(quote_char)s') % {
                    'quote_char': quote_char,
                    'file_param_name': escape_by_quote(file_param_name,
                                                       quote_char)
                }

            response += ('%(newline)s%(indent)s%(file_param_name)s,%(space)s'
                         '%(newline)s%(indent)s') % {
                'newline': '\n' if not oneline else '',
                'indent': indent if not oneline else '',
                'file_param_name': _file_param_name,
                'space': ' ' if oneline else '',
            }

            if setup:
                response += 'fs.createReadStream('  # length: 20

                if isinstance(file_data, str):
                    filepath = file_data
                else:
                    filepath = file_data[0] if file_data is not None else None
                if filepath is None:
                    filepath = lazy_value_by_parameter(
                        {
                            'name': '',
                            'faker': 'faker.providers.file::file_path',
                        },
                        seed=seed,
                        locale=locale)

                if not oneline:
                    _filepath = str_definition(
                        filepath,
                        quote_char=quote_char,
                        wrap=wrap,
                        indent=' ' * (len(indent) + 20))
                    _filename = str_definition(
                        os.path.basename(filepath),
                        quote_char=quote_char,
                        wrap=wrap,
                        indent=' ' * (len(indent) * 2 + 10))  # 'filename: '
                else:
                    _filepath = '%(quote_char)s%(filepath)s%(quote_char)s' % {
                        'quote_char': quote_char,
                        'filepath': escape_by_quote(filepath, quote_char)
                    }
                    _filename = '%(quote_char)s%(filename)s%(quote_char)s' % {
                        'quote_char': quote_char,
                        'filename': escape_by_quote(
                            os.path.basename(filepath), quote_char)
                    }

                response += ('%(filepath)s),%(space)s%(newline)s%(indent)s{'
                             '%(newline)s%(indent)s%(indent)s'
                             'filename: %(filename)s') % {
                    'space': ' ' if oneline else '',
                    'newline': '\n' if not oneline else '',
                    'indent': indent if not oneline else '',
                    'filepath': _filepath,
                    'filename': _filename
                }
                if not isinstance(file_data, str) and file_data is not None:
                    if len(file_data) > 1:
                        if not oneline:
                            _content_type = str_definition(
                                file_data[1],
                                quote_char=quote_char,
                                wrap=wrap,
                                indent=' ' * (len(indent) * 2 + 13))
                        else:
                            _content_type = ('%(quote_char)s%(content_type)s'
                                             '%(quote_char)s') % {
                                'quote_char': quote_char,
                                'content_type': escape_by_quote(
                                    file_data[1], quote_char)
                            }

                        response += (',%(newline)s%(indent)s%(indent)s'
                                     'contentType: %(content_type)s') % {
                            'content_type': _content_type,
                            'newline': '\n' if not oneline else '',
                            'indent': indent if not oneline else ''
                        }
                response += '%(newline)s%(indent)s}%(newline)s' % {
                    'newline': '\n' if not oneline else '',
                    'indent': indent if not oneline else ''
                }
            else:
                # TODO: Manage content_type and filename?
                response += 'inputs[%(input_index)d].files[0]%(newline)s' % {
                    'input_index': i,
                    'newline': '\n' if not oneline else ''
                }
            response += ');%(newline)s' % {
                'newline': '\n' if not oneline else ''
            }
        response += '\n'
    elif content_type == 'text/plain':
        if len(parameters) != 1:
            raise_post_text_plain_n_parameters_not_1(len(parameters))

        _value = lazy_value_by_parameter(parameters[0],
                                         seed=seed,
                                         locale=locale)
        body = str_definition(_value,
                              indent=' ' * (len(indent) * 2 + 6),
                              quote_char=quote_char,
                              wrap=wrap)
    else:  # 'application/json' or 'application/x-www-form-urlencoded'
        object_content = ''

        for i, parameter in enumerate(parameters):
            name = lazy_name_by_parameter(parameter, seed=seed)
            value = lazy_value_by_parameter(
                parameter, seed=seed, locale=locale)

            if oneline:
                name_def = '%(quote_char)s%(name)s%(quote_char)s' % {
                    'name': escape_by_quote(name, quote_char),
                    'quote_char': quote_char
                }
                value_def = '%(quote_char)s%(value)s%(quote_char)s' % {
                    'value': escape_by_quote(value, quote_char),
                    'quote_char': quote_char
                }
            else:
                name_def = str_definition(name,
                                          indent=indent * 3,
                                          quote_char=quote_char,
                                          wrap=wrap)
                _value_def_indent = ' ' * (
                    len(indent) * 3 + len(name_def) + 2)
                value_def = str_definition(value,
                                           indent=_value_def_indent,
                                           quote_char=quote_char,
                                           wrap=wrap)

            object_content += ('%(indent)s%(name)s: %(value)s%(comma)s'
                               '%(newline)s') % {
                'name': name_def,
                'indent': indent * 3,
                'value': value_def,
                'comma': ',' if i < (len(parameters) - 1) else '',
                'newline': '\n' if (
                    not oneline and i < (len(parameters) - 1)) else ''
            }

        if object_content:
            body = ('%(object_wrapper)s({%(newline)s'
                    '%(object_content)s%(newline)s%(indent)s})') % {
                'object_wrapper': 'JSON.stringify'
                if content_type == 'application/json'
                else 'new URLSearchParams',
                'object_content': object_content,
                'newline': '\n' if not oneline else '',
                'indent': indent * 2,
            }
        else:
            body = ''

    response += ('fetch(%(newline)s%(indent)s%(url)s,%(space)s%(newline)s'
                 '%(indent)s{%(indent)s%(newline)s%(indent)s%(indent)smethod:'
                 ' %(quote_char)sPOST%(quote_char)s%(comma)s%(newline)s') % {
        'newline': '\n' if not oneline else '',
        'indent': indent if not oneline else '',
        'space': ' ' if oneline else '',
        'quote_char': quote_char,
        'comma': ',' if (body or kwargs or headers) else '',
        'url': str_definition(url, quote_char=quote_char,
                              indent=indent, wrap=wrap),
    }

    if body:
        response += ('%(indent)s%(indent)sbody:'
                     ' %(body)s%(comma)s%(newline)s') % {
            'newline': '\n' if not oneline else '',
            'indent': indent if not oneline else '',
            'comma': ',' if (kwargs or headers) else '',
            'body': body,
        }

    # headers render
    if headers:
        response += _headers_render(headers, indent=indent, oneline=oneline,
                                    quote_char=quote_char, wrap=wrap,
                                    _comma_at_end=bool(kwargs))

    # kwargs render
    if kwargs:
        response += _kwargs_render(kwargs, indent=indent, oneline=oneline,
                                   quote_char=quote_char, wrap=wrap)

    response += '%(indent)s}%(newline)s' % {
        'indent': indent if not oneline else '',
        'newline': '\n' if not oneline else ''
    }

    response += _promises_chain_render(quote_char=quote_char, indent=indent,
                                       oneline=oneline)

    if teardown:
        response += teardown

    return response
