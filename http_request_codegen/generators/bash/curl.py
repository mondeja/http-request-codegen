'''Bash curl code snippets generator.'''

from collections import OrderedDict


try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from http_request_codegen.generators.bash._utils import (
    DEFAULT_INDENT,
    DEFAULT_QUOTE_CHAR,
    DEFAULT_WRAP,
    escape_by_quote
)
from http_request_codegen.hrc_valuer import (
    lazy_name_by_parameter,
    lazy_value_by_parameter
)


def get(url, parameters=[], headers={}, indent=DEFAULT_INDENT,
        quote_char=DEFAULT_QUOTE_CHAR, setup=False, teardown=None,
        oneline=False, wrap=DEFAULT_WRAP, seed=None, locale=None,
        **kwargs):
    '''Pass extra options to 'curl' command in ``kwargs`` parameter. For
    example, to save the response in a file, pass
    ``kwargs={'-o': 'filename.ext'}``:

    ```bash
    curl -o "filename.ext"
    ```
    '''
    '''In this implementation, options values and URLs are not wrapped in
    multiples lines if these values exceed the wrap length.
    '''
    response = ''

    if setup:
        response += str(setup)

    response += 'curl'

    options_string = ''
    options_map = []
    if kwargs or parameters:
        _d_option_included = False
        for option_name, option_value in kwargs.items():
            options_string += ' %(option_name)s' % {'option_name': option_name}
            if option_value:
                option_value_string = ('%(quote_char)s%(option_value)s'
                                       '%(quote_char)s') % {
                    'quote_char': quote_char,
                    'option_value': escape_by_quote(
                        str(option_value), quote_char)
                }
                options_string += ' ' + option_value_string
            else:
                option_value_string = None
            options_map.append([option_name, option_value_string])

            if option_name == '-d':
                _d_option_included = True

        if parameters:
            if _d_option_included:
                raise ValueError(
                    ('You can\'t pass the option \'-d\' and parameters with'
                     ' \'parameters\' value.'))

            parameters_dict = OrderedDict({})
            for parameter in parameters:
                parameter_name = lazy_name_by_parameter(parameter, seed=seed)
                parameter_value = lazy_value_by_parameter(
                    parameter, seed=seed, locale=locale)
                parameters_dict[parameter_name] = parameter_value

            params_string = escape_by_quote(urlencode(parameters_dict),
                                            quote_char)
            options_string += ' -d %(quote_char)s%(params)s%(quote_char)s' % {
                'quote_char': quote_char,
                'params': params_string
            }
            options_map.append(['-d', params_string])

    if headers:
        for name, value in headers.items():
            option = '-H'
            value = ('%(quote_char)s%(header_name)s:'
                     ' %(header_value)s%(quote_char)s') % {
                'quote_char': quote_char,
                'header_name': name,
                'header_value': escape_by_quote(str(value), quote_char)
            }
            options_map.append([option, value])

            options_string += (' %(option)s %(value)s') % {
                'option': option,
                'value': value
            }

    # 1 here is a space
    if len(options_string) + len(url) + len(response) + 1 < wrap:
        oneline = True

    if oneline:
        response += options_string + ' ' + url
    else:
        response += ' \\\n'
        for option, value in options_map:
            if value:
                value_string = ' %(quote_char)s%(value)s%(quote_char)s' % {
                    'value': escape_by_quote(value, quote_char),
                    'quote_char': quote_char
                }
            else:
                value_string = ''
            response += '%(indent)s%(option)s%(value_string)s \\\n' % {
                'indent': indent,
                'option': option,
                'value_string': value_string
            }
        response += '%(indent)s%(url)s' % {'indent': indent, 'url': url}

    if teardown:
        response += str(teardown)

    return response


def post():
    return
