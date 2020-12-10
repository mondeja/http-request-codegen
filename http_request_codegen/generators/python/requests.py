'''Python requests code snippets generator.'''

from collections import OrderedDict

from http_request_codegen.generators.python._utils import (
    DEFAULT_INDENT,
    DEFAULT_QUOTE_CHAR,
    DEFAULT_WRAP,
    dict_definition,
    escape_by_quote,
    kwarg_definition,
    kwarg_definition_dict_valued,
    str_definition
)
from http_request_codegen.hrc_exceptions import (
    raise_post_text_plain_n_parameters_not_1
)
from http_request_codegen.hrc_valuer import (
    lazy_name_by_parameter,
    lazy_value_by_parameter
)


def get(url, parameters=[], headers={}, indent=DEFAULT_INDENT,
        quote_char=DEFAULT_QUOTE_CHAR, setup=True, teardown=None,
        oneline=False, wrap=DEFAULT_WRAP, seed=None, locale=None,
        **kwargs):
    '''Parameters are passed using
    [``requests.get``](https://requests.readthedocs.io/en/api/#requests.get)
    function ``params`` parameter, not by appending ``?foo=bar&...`` to the
    URL. If you want this behaviour, build the passed URL using
    [``lazy_name_by_parameter``](/reference#lazy_name_by_parameter) and
    [``lazy_value_by_parameter``](/reference#lazy_value_by_parameter) functions
    instead of use the ``parameters`` argument.

    If you want to import more modules in the initialization snippet, keep
    in mind that you must provide ``import requests`` line also in the
    ``setup`` argument. For example,
    ``setup=\'import requests\\nimport foo\\n\\n\'`` will render as:

    ```python
    import requests
    import foo

    requests.get('<url>'...
    ```
    '''
    _oneline = oneline
    response = ''

    # initialization
    setup_length = 0
    if setup:
        if isinstance(setup, str):
            response += setup
        else:
            response += ('import requests%(separator)s'
                         '%(newline)s%(newline)s') % {
                'separator': ';' if oneline else '',
                'newline': '\n' if not oneline else '',
            }
        if oneline:
            setup_length += len(response)

    # url length
    url_length = len(url) + 21  # 'req = requests.get(' (19) + '' (2)

    # parameters length
    parameters_line_length = 0
    if parameters:
        parameters_keys = OrderedDict({})
        parameters_line_length = 9  # 'params={}'
        for parameter in parameters:
            name = escape_by_quote(
                lazy_name_by_parameter(parameter, seed=seed),
                quote_char
            )
            value = str_definition(
                lazy_value_by_parameter(parameter, seed=seed, locale=locale),
                quote_char=quote_char,
                indent=indent + (' ' * (8 + len(name))),
                wrap=wrap
            )
            parameters_keys[name] = value
            parameters_line_length += len(name) + 4 + len(value)
        parameters_line_length += len(parameters) - 1  # commas except last
        if headers or kwargs:
            parameters_line_length += 2  # ', '

    headers_line_length = 0
    if headers:
        headers_keys = {} if not isinstance(headers, OrderedDict) \
            else OrderedDict({})
        headers_line_length += 10  # headers={}
        for key, value in headers.items():
            escaped_key = escape_by_quote(key, quote_char)
            escaped_value = escape_by_quote(value, quote_char)
            headers_keys[escaped_key] = escaped_value
            # 2 is ': '
            headers_line_length += \
                len(quote_char) * 4 + 2 + len(escaped_key) + len(escaped_value)
        headers_line_length += len(headers) - 1  # commas except last
        if kwargs:
            headers_line_length += 2  # ', '

    kwargs_line_length = 0
    if kwargs:
        kwargs_line_length = 2
        for key, value in kwargs.items():
            kwargs_line_length += len(key) + len(str(value))
            if isinstance(value, str):
                kwargs_line_length += 2
        kwargs_line_length += len(kwargs) - 1  # commas except last

    # oneliner by wrapping
    #   here + 1 is function call end ')' and - 1 is the character wrapping,
    #   so both are negated
    if setup_length + url_length + parameters_line_length + \
            headers_line_length + kwargs_line_length < wrap:
        oneline = True

    # url
    response += ('req = requests.get(%(newline)s%(indent)s%(url)s%(newline2)s'
                 '%(comma)s%(space)s%(newline3)s') % {
        'url': ('%(quote_char)s%(url)s%(quote_char)s' % {
            'url': url,
            'quote_char': quote_char
        }) if oneline else str_definition(url,
                                          indent=indent,
                                          quote_char=quote_char,
                                          wrap=wrap),
        'indent': indent if not oneline else '',
        'newline': '\n' if not oneline else '',
        'newline2': '\n' if not oneline and (
            not headers and not parameters and not kwargs) else '',
        'comma': ',' if headers or parameters or kwargs else '',
        'space': ' ' if oneline and (parameters or headers or kwargs) else '',
        'newline3': '\n' if not oneline and (
            headers or parameters or kwargs) else ''
    }

    # parameters render
    if parameters:
        response += '%(indent)sparams={%(newline)s' % {
            'indent': indent if not oneline else '',
            'newline': '\n' if not oneline else '',
        }
        for i, (pname, pvalue) in enumerate(parameters_keys.items()):
            response += ('%(indent)s%(quote_char)s%(parameter_name)s'
                         '%(quote_char)s: %(value)s%(comma)s') % {
                'parameter_name': pname,
                'indent': indent * 2 if not oneline else '',
                'quote_char': quote_char,
                'value': pvalue,
                'comma': ',' if i < len(parameters) - 1 else '',
            }
            response += '\n' if not oneline else ''

        response += '%(indent)s}%(comma)s%(newline)s' % {
            'indent': indent if not oneline else '',
            'comma': ',' if (headers or kwargs) else '',
            'newline': '\n' if not oneline else ('' if (
                not headers and not kwargs) else ' '),
        }

    # headers render
    if headers:
        response += '%(header)s%(comma)s%(newline)s' % {
            'header': kwarg_definition_dict_valued(
                'headers', headers_keys,
                indent=indent if not oneline else '',
                quote_char=quote_char,
                newline='\n' if not oneline else '',
                _escape_keys=False, _escape_values=False),
            'newline': '\n' if not oneline else (
                '' if not kwargs else ' '),
            'comma': ',' if kwargs else '',
        }

    # kwargs render
    if kwargs:
        for i, (key, value) in enumerate(kwargs.items()):
            response += '%(indent)s%(repr_kwarg)s%(comma)s%(newline)s' % {
                'indent': '' if oneline or isinstance(value, dict) else indent,
                'repr_kwarg': kwarg_definition(
                    key,
                    value,
                    indent='' if oneline else indent,
                    quote_char=quote_char,
                    wrap=wrap),
                'comma': ',' if i < len(kwargs) - 1 else '',
                'newline': '\n' if not oneline else (
                    ' ' if i < len(kwargs) - 1 else ''),
            }

    response += ')%(separator)s' % {'separator': ';' if _oneline else ''}

    if teardown:
        response += str(teardown)
    return response


def post(url, parameters=[], files={}, headers={}, indent=DEFAULT_INDENT,
         quote_char=DEFAULT_QUOTE_CHAR, setup=True, teardown=None,
         oneline=False, wrap=DEFAULT_WRAP, seed=None, locale=None,
         **kwargs):
    '''POST method code generator for Python requests library.'''
    # There are 4 possibilities of arguments build since we allow 4 forms
    #   of doing POST requests, depends on 'Content-Type' header content
    #   and the definition of 'files' optional argument. As default,
    #   'application/x-www-form-urlencoded'
    #   - len(files) > 0 -> files={}
    #   - Content-Type: 'multipart/form-data; boundary=-----...' -> files={}
    #   - Content-Type: 'application/x-www-form-urlencoded' -> data={}
    #   - Content-Type: 'text/plain' -> data=''
    #   - Content-Type: 'application/json' -> json={}
    _oneline = oneline
    response = ''

    # initialization
    setup_length = 0
    if setup:
        if isinstance(setup, str):
            response += setup
        else:
            response += ('import requests%(separator)s'
                         '%(newline)s%(newline)s') % {
                'separator': ';' if oneline else '',
                'newline': '\n' if not oneline else '',
            }
        if oneline:
            setup_length += len(response)

    # url length
    url_length = len(url) + 22  # 'req = requests.post(' (20) + '' (2)

    # headers length and content-type discovering
    if files:
        content_type = 'multipart/form-data'
        _content_type_found = True
    else:
        content_type = 'application/x-www-form-urlencoded'
        _content_type_found = False

    headers_line_length = 0
    if headers:
        headers_keys = {} if not isinstance(headers, OrderedDict) \
            else OrderedDict({})
        headers_line_length += 10  # headers={}
        for key, value in headers.items():
            escaped_key = escape_by_quote(key, quote_char)
            escaped_value = escape_by_quote(value, quote_char)
            headers_keys[escaped_key] = escaped_value
            # 2 is ': '
            headers_line_length += \
                len(quote_char) * 4 + 2 + len(escaped_key) + len(escaped_value)
            if not _content_type_found:
                _key_lower = str(key).lower()
                if _key_lower == 'content-type':
                    if 'text/plain' in value:
                        content_type = 'text/plain'
                        _content_type_found = True
                    elif 'application/json' in value:
                        content_type = 'application/json'
                        _content_type_found = True
        headers_line_length += len(headers) - 1  # commas except last
        if kwargs:
            headers_line_length += 2  # ', '

    if content_type == 'text/plain' and len(parameters) != 1:
        raise_post_text_plain_n_parameters_not_1(len(parameters))

    # data/json length
    parameters_line_length = 0
    if parameters:
        parameters_keys = OrderedDict({})

        # length depends on kwarg used in the request
        parameters_line_length = {
            'multipart/form-data': 0,                # files={}
            'application/json': 7,                   # json={}
            'application/x-www-form-urlencoded': 7,  # data={}
        }.get(content_type, 5)  # (text/*)             data=

        for parameter in parameters:
            if content_type == 'text/plain':
                name = ''
            else:
                name = escape_by_quote(
                    lazy_name_by_parameter(parameter, seed=seed),
                    quote_char
                )

            # JSON must accepts other data types than string
            _param_value = parameter.get('value')
            if content_type == 'application/json' and isinstance(
                    _param_value, (int, float, bool)):
                value = _param_value
                parameters_line_length += len(name) + 4 + len(str(value))
            else:
                if content_type == 'text/plain':
                    _param_value_def_indent = indent + (' ' * 5)
                else:
                    _param_value_def_indent = indent + (' ' * (8 + len(name)))
                value = str_definition(
                    lazy_value_by_parameter(parameter,
                                            seed=seed,
                                            locale=locale),
                    quote_char=quote_char,
                    indent=_param_value_def_indent,
                    wrap=wrap
                )
                parameters_line_length += len(name) + 4 + len(value)

            if content_type == 'text/plain':
                parameters_line_length += len(value) + 2
            elif content_type != 'application/json':
                parameters_line_length += len(name) + 4 + len(value)
            parameters_keys[name] = value
        parameters_line_length += len(parameters) - 1  # commas except last
        if files or headers or kwargs:
            parameters_line_length += 2  # ', '

    # files length
    files_line_length = 0
    if files:
        files_line_length = 8  # files={}
        files_keys = {} if not isinstance(files, OrderedDict) \
            else OrderedDict({})
        for key, value in files.items():
            escaped_key = escape_by_quote(key, quote_char)
            files_line_length += len(escaped_key) + 4

            files_keys[escaped_key] = []

            if isinstance(value, str) or value is None:
                # random filepath
                if value is None:
                    value = lazy_value_by_parameter(
                        {
                            'name': '',
                            'faker': 'faker.providers.file::file_path',
                        },
                        seed=seed,
                        locale=locale)

                escaped_value = escape_by_quote(value, quote_char)
                files_keys[escaped_key].append(escaped_value)

            else:  # iterable
                if len(value) > 2:
                    # file headers
                    _fheaders = {}
                    for hkey, hvalue in value[2].items():
                        _escaped_key = escape_by_quote(hkey, quote_char)
                        files_line_length += len(_escaped_key) + 4

                        _escaped_value = escape_by_quote(hvalue, quote_char)
                        files_line_length += len(_escaped_value) + 2

                        _fheaders[_escaped_key] = _escaped_value
                    # commas except last + prev ', '
                    files_line_length += len(value[2]) + 2
                    files_keys[escaped_key].append(_fheaders)
                if len(value) > 1:
                    # file content type
                    _escaped_value = escape_by_quote(value[1], quote_char)
                    files_line_length += len(_escaped_value) + 4  # prev ', '
                    files_keys[escaped_key].insert(0, _escaped_value)

                # random filepath
                if value[0] is None:
                    value = list(value)
                    value[0] = lazy_value_by_parameter(
                        {
                            'name': '',
                            'faker': 'faker.providers.file::file_path',
                        },
                        seed=seed,
                        locale=locale)
                escaped_value = escape_by_quote(value[0], quote_char)
                files_keys[escaped_key].insert(0, escaped_value)

            _filepath = value if isinstance(value, str) else value[0]
            _indent = indent * 4
            _filepath_def = str_definition(
                _filepath,
                indent=_indent,
                quote_char=quote_char,
                wrap=wrap)
            _open_file_multiline = len(_filepath_def) + len(_indent) > wrap
            _open_file_string = ('open(%(newline)s%(indent1)s%(value)s,'
                                 '%(newline)s%(indent2)s%(quote_char)srb'
                                 '%(quote_char)s%(newline)s%(indent3)s)') % {
                'quote_char': quote_char,
                'value': _filepath_def,
                'newline': '\n' if _open_file_multiline else '',
                'indent1': _indent if _open_file_multiline else '',
                'indent2': _indent if _open_file_multiline else ' ',
                'indent3': indent * 3 if _open_file_multiline else '',
            }
            files_keys[escaped_key].insert(1, _open_file_string)

            # 2 filename quotes + () of tuple + , open('', 'rb')
            files_line_length += len(escaped_value) * 2 + 20

        files_line_length += len(parameters) - 1  # commas except last

    kwargs_line_length = 0
    if kwargs:
        kwargs_line_length = 2
        for key, value in kwargs.items():
            kwargs_line_length += len(key) + len(str(value))
            if isinstance(value, str):
                kwargs_line_length += 2
        kwargs_line_length += len(kwargs) - 1  # commas except last

    # oneliner by wrapping
    #   here + 1 is function call end ')' and - 1 is the character wrapping,
    #   so both are negated
    if setup_length + url_length + parameters_line_length + \
            headers_line_length + files_line_length + \
            kwargs_line_length < wrap:
        oneline = True

    # url
    response += ('req = requests.post(%(newline)s%(indent)s%(url)s%(newline2)s'
                 '%(comma)s%(space)s%(newline3)s') % {
        'url': ('%(quote_char)s%(url)s%(quote_char)s' % {
            'url': url, 'quote_char': quote_char
        }) if oneline else str_definition(url,
                                          indent=indent,
                                          quote_char=quote_char,
                                          wrap=wrap),
        'indent': indent if not oneline else '',
        'newline': '\n' if not oneline else '',
        'newline2': '\n' if not oneline and (
            not headers and not files and not parameters and not kwargs
        ) else '',
        'comma': ',' if (files or headers or parameters or kwargs) else '',
        'space': ' ' if oneline and (
            files or parameters or headers or kwargs) else '',
        'newline3': '\n' if not oneline and (
            files or parameters or headers or kwargs) else ''
    }

    # parameters render
    if parameters:
        response += '%(indent)s%(kwarg_name)s=' % {
            'indent': indent if not oneline else '',
            'kwarg_name': 'json' if content_type == 'application/json'
            else 'data'
        }
        if content_type == 'text/plain':
            response += '%(value)s%(comma)s%(newline)s' % {
                'value': parameters_keys[''],
                'comma': ',' if (
                    not oneline or files or headers or kwargs) else '',
                'newline': '\n' if not oneline else ' '
            }
        else:
            response += '{%(newline)s' % {
                'newline': '\n' if not oneline else '',
            }
            for i, (pname, pvalue) in enumerate(parameters_keys.items()):
                response += ('%(indent)s%(quote_char)s%(parameter_name)s'
                             '%(quote_char)s: %(value)s%(comma)s') % {
                    'parameter_name': pname,
                    'indent': indent * 2 if not oneline else '',
                    'quote_char': quote_char,
                    'value': pvalue,
                    'comma': ',' if i < len(parameters) - 1 else '',
                }
                response += '\n' if not oneline else ''

            response += '%(indent)s}%(comma)s%(newline)s' % {
                'indent': indent if not oneline else '',
                'comma': ',' if (files or headers or kwargs) else '',
                'newline': '\n' if not oneline else ('' if (
                    not headers and not files and not kwargs) else ' '),
            }

    # files render
    if files:
        response += '%(indent)sfiles={%(newline)s' % {
            'indent': indent if not oneline else '',
            'newline': '\n' if not oneline else '',
        }

        for i, (fkey, fvalue) in enumerate(files_keys.items()):
            _value = ('(%(newline1)s%(indent)s%(fpath)s,%(newline2)s'
                      '%(indent)s%(open_file_string)s') % {
                'newline1': '\n' if not oneline else '',
                'newline2': '\n' if not oneline else ' ',
                'indent': indent * 3 if not oneline else '',
                'fpath': str_definition(
                    fvalue[0],
                    quote_char=quote_char,
                    indent=indent * 3,
                    wrap=wrap),
                'open_file_string': fvalue[1]
            }
            if len(fvalue) > 2:
                _value += ',%(newline)s%(indent)s%(content_type)s' % {
                    'content_type': str_definition(
                        fvalue[2],
                        quote_char=quote_char,
                        indent=indent * 3,
                        wrap=wrap),
                    'newline': '\n' if not oneline else '',
                    'indent': indent * 3 if not oneline else ' '
                }
            if len(fvalue) > 3:
                _value += ',%(newline)s%(indent)s%(headers)s' % {
                    'headers': dict_definition(
                        fvalue[3],
                        indent=indent if not oneline else '',
                        indent_depth=3,
                        quote_char=quote_char,
                        newline='\n' if not oneline else '',
                        _escape_keys=False, _escape_values=False),
                    'newline': '\n' if not oneline else '',
                    'indent': indent * 3 if not oneline else ' '
                }
            _value += '%(newline)s%(indent)s)' % {
                'newline': '' if oneline else '\n',
                'indent': '' if oneline else indent * 2
            }
            response += ('%(indent)s%(quote_char)s%(key)s'
                         '%(quote_char)s: %(value)s%(comma)s') % {
                'key': fkey,
                'indent': indent * 2 if not oneline else '',
                'quote_char': quote_char,
                'value': _value,
                'comma': ',' if i < len(files_keys) - 1 else '',
            }
            response += '\n' if not oneline else ''

        response += '%(indent)s}%(comma)s%(newline)s' % {
            'indent': indent if not oneline else '',
            'comma': ',' if (headers or kwargs) else '',
            'newline': '\n' if not oneline else (' ' if (
                headers or kwargs) else ''),
        }

    if headers:
        response += '%(headers)s%(comma)s%(newline)s' % {
            'headers': kwarg_definition_dict_valued(
                'headers', headers_keys,
                indent=indent if not oneline else '',
                quote_char=quote_char,
                newline='\n' if not oneline else '',
                _escape_keys=False, _escape_values=False),
            'newline': '\n' if not oneline else (
                '' if not kwargs else ' '),
            'comma': ',' if kwargs else '',
        }

    # kwargs render
    if kwargs:
        for i, (key, value) in enumerate(kwargs.items()):
            response += '%(indent)s%(repr_kwarg)s%(comma)s%(newline)s' % {
                'indent': '' if oneline or isinstance(value, dict) else indent,
                'repr_kwarg': kwarg_definition(
                    key,
                    value,
                    indent='' if oneline else indent,
                    indent_depth=1,
                    quote_char=quote_char,
                    wrap=wrap),
                'comma': ',' if i < len(kwargs) - 1 else '',
                'newline': '\n' if not oneline else (
                    ' ' if i < len(kwargs) - 1 else ''),
            }

    response += ')%(separator)s' % {'separator': ';' if _oneline else ''}

    if teardown:
        response += str(teardown)
    return response
