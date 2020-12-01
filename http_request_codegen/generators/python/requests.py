'''Python requests code snippets generator.'''

from collections import OrderedDict

from http_request_codegen.generators.python._utils import (
    DEFAULT_INDENT,
    DEFAULT_QUOTE_CHAR,
    DEFAULT_WRAP,
    escape_by_quote,
    kwarg_definition,
    kwarg_definition_dict_valued,
    raw_str_definition
)
from http_request_codegen.string import lazy_string
from http_request_codegen.valuer import (
    lazy_name_by_parameter,
    lazy_value_by_parameter
)


def get(url, parameters=[], headers={}, indent=DEFAULT_INDENT,
        quote_char=DEFAULT_QUOTE_CHAR, init=True, oneline=False,
        wrap=DEFAULT_WRAP, seed=None, locale=None, **kwargs):
    '''GET method code generator for python requests library.'''
    indent = indent or DEFAULT_INDENT
    quote_char = quote_char or DEFAULT_QUOTE_CHAR
    url = lazy_string(url)

    _oneline = oneline
    response = ''

    # import
    if init:
        response += 'import requests%(separator)s%(newline)s%(newline)s' % {
            'separator': ';' if oneline else '',
            'newline': '\n' if not oneline else '',
        }

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
            value = raw_str_definition(
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
        headers_line_length += 2  # {}
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
    if url_length + parameters_line_length + headers_line_length + \
            kwargs_line_length < wrap:
        oneline = True

    # url
    response += ('req = requests.get(%(newline)s%(indent)s%(url)s%(newline2)s'
                 '%(comma)s%(space)s%(newline3)s') % {
        'url': ('%(quote_char)s%(url)s%(quote_char)s' % {
            'url': url, 'quote_char': quote_char
        }) if oneline else raw_str_definition(url,
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
                # TODO: Multiple possible parameter names by list, function
                # or list of functions
                'parameter_name': pname,
                'indent': indent * 2 if not oneline else '',
                'quote_char': quote_char,
                'value': pvalue,
                'comma': ',' if i < len(parameters) - 1 else '',
            }
            response += '\n' if not oneline else ''

        response += '%(indent)s}%(comma)s%(newline)s' % {
            'indent': indent if not oneline else (
                '' if (not headers and not kwargs) else ' '),
            'comma': ',' if not oneline and (headers or kwargs) else '',
            'newline': '\n' if not oneline else '',
        }

    if headers:
        response += '%(header)s%(comma)s%(newline)s' % {
            'header': kwarg_definition_dict_valued(
                'headers', headers_keys,
                indent=indent if not oneline else '',
                quote_char=quote_char,
                newline='\n' if not oneline else '',
                _escape_keys=False, _escape_values=False),
            'newline': '\n' if not oneline else '',
            'comma': ',' if kwargs else '',
        }

    if kwargs:
        for i, (key, value) in enumerate(kwargs.items()):
            response += '%(indent)s%(repr_kwarg)s%(comma)s%(newline)s' % {
                'indent': indent if not oneline else '',
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
    return response


def post():
    pass
