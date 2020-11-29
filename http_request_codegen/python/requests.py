
from http_request_codegen.python._utils import (
    DEFAULT_INDENT,
    DEFAULT_QUOTE_CHAR,
    escape_quote,
    repr_dict_kwarg,
    repr_kwarg
)
from http_request_codegen.valuer import value_by_parameter


def get(url, parameters=[], headers={}, indent=None, quote_char=None,
        oneline=False, seed=None, locale=None, **kwargs):
    """GET method code generator for python requests library."""
    quote_char = quote_char or DEFAULT_QUOTE_CHAR
    indent = indent or DEFAULT_INDENT
    response = ('import requests%(separator)s%(newline)s%(newline)s'
                'req = requests.get(%(newline)s%(indent)s%(quote_char)s'
                '%(url)s%(quote_char)s') % {
        'url': url,
        'indent': indent if not oneline else '',
        'quote_char': quote_char,
        'newline': '\n' if not oneline else '',
        'separator': ';' if oneline else '',
    }
    if headers or parameters or kwargs:
        response += ',%(space)s%(newline)s' % {
            'newline': '\n' if not oneline else '',
            'space': ' ' if oneline else '',
        }
    if parameters:
        response += '%(indent)sparams={%(newline)s' % {
            'indent': indent,
            'newline': '\n' if not oneline else '',
        }
        for i, parameter in enumerate(parameters):
            response += ('%(indent)s%(indent)s%(quote_char)s'
                         '%(parameter_name)s%(quote_char)s:'
                         ' %(quote_char)s%(value)s%(quote_char)s%(comma)s') % {
                # TODO: Multiple possible parameter names by list, function
                # or list of functions
                'parameter_name': parameter['name'],
                'indent': indent if not oneline else '',
                'quote_char': quote_char,
                'value': escape_quote(
                    value_by_parameter(parameter, seed=seed, locale=locale),
                    quote_char,
                ),
                'comma': ',' if i < len(parameters) - 1 else '',
            }
            response += '\n' if not oneline else ''
        response += '%(indent)s},%(newline)s' % {
            'indent': indent,
            'newline': '\n' if not oneline else '',
        }
    if headers:
        response += '%(header)s%(comma)s%(newline)s' % {
            'header': repr_dict_kwarg('headers',
                                      headers,
                                      indent=indent if not oneline else '',
                                      quote_char=quote_char,
                                      newline='\n' if not oneline else ''),
            'newline': '\n' if not oneline else '',
            'comma': ',' if kwargs else '',
        }
    for i, (kwarg_name, value) in enumerate(kwargs.items()):
        response += '%(indent)s%(repr_kwarg)s%(comma)s%(newline)s' % {
            'indent': indent if not oneline else ' ',
            'repr_kwarg': repr_kwarg(kwarg_name, value, indent=indent,
                                     quote_char=quote_char),
            'comma': ',' if i < len(kwargs) - 1 else '',
            'newline': '\n' if not oneline else '',
        }
    response += ')%(separator)s' % {'separator': ';' if oneline else ''}
    return response


def post():
    pass
