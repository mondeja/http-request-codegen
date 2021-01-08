'''Bash curl code snippets generator.'''

import json
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


def _render_options_map(options_map, options_string, url, oneline=False,
                        indent=DEFAULT_INDENT, quote_char=DEFAULT_QUOTE_CHAR):
    response = ''
    if not oneline:
        response += '\\\n'
    for i, (option, value) in enumerate(options_map):
        if value:
            value_string = ' %(quote_char)s%(value)s%(quote_char)s' % {
                'value': escape_by_quote(value, quote_char),
                'quote_char': quote_char
            }
        else:
            value_string = ''
        response += '%(indent)s%(option)s%(value_string)s %(newline)s' % {
            'indent': indent if not oneline else '',
            'option': option,
            'value_string': value_string,
            'newline': '\\\n' if not oneline else ''
        }
    response += '%(indent)s%(url)s' % {
        'indent': indent if not oneline else '',
        'url': url
    }
    return response


def _build_headers(headers, quote_char=DEFAULT_QUOTE_CHAR,
                   content_type='application/x-www-form-urlencoded'):
    map, string = ([], '')
    for name, value in headers.items():
        option = '-H'
        value = ('%(header_name)s: %(header_value)s') % {
            'header_name': name,
            'header_value': escape_by_quote(str(value), quote_char)
        }
        map.append([option, value])

        string += (' %(option)s %(value)s') % {
            'option': option,
            'value': value
        }
        if name.lower() == 'content-type':
            if value in (
                'multipart/form-data',
                'application/json',
                'application/x-www-form-urlencoded',
                'text/plain'
            ):
                content_type = value
    return (map, string, content_type)


def get(url, parameters=[], headers={}, indent=DEFAULT_INDENT,
        quote_char=DEFAULT_QUOTE_CHAR, setup=False, teardown=None,
        oneline=False, wrap=DEFAULT_WRAP, seed=None, locale=None, **kwargs):
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
                option_value_string = escape_by_quote(
                    str(option_value), quote_char)
                options_string += ' ' + option_value_string
            else:
                option_value_string = None
            options_map.append([option_name, option_value_string])

            if option_name == '-X' and option_value != "GET":
                raise ValueError('\'-X\' option, if defined, must be \'GET\'')

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
        headers_map, headers_string, _ = _build_headers(headers,
                                                        quote_char=quote_char)
        options_map.extend(headers_map)
        options_string += headers_string

    # 1 here is a space
    if len(options_string) + len(url) + len(response) + 1 < wrap:
        oneline = True
    response += ' '

    response += _render_options_map(options_map,
                                    options_string,
                                    url,
                                    oneline=oneline,
                                    indent=indent,
                                    quote_char=quote_char)

    if teardown:
        response += str(teardown)

    return response


def post(url, parameters=[], files={}, headers={}, indent=DEFAULT_INDENT,
         quote_char=DEFAULT_QUOTE_CHAR, setup=False, teardown=None,
         oneline=False, wrap=DEFAULT_WRAP, seed=None, locale=None, **kwargs):
    response = ''

    if setup:
        response += str(setup)

    response += 'curl'

    options_string = ''
    options_map = []

    # Build headers and discover content type
    headers_map, headers_string, content_type = _build_headers(
        headers,
        quote_char=quote_char,
        content_type='application/x-www-form-urlencoded'
                     if not files else 'multipart/form-data')

    _x_post_defined = False
    if kwargs:
        for option_name, option_value in kwargs.items():
            options_string += ' %(option_name)s' % {'option_name': option_name}
            if option_value:
                option_value_str = str(option_value)
                options_string += (' %(quote_char)s%(value)s'
                                   '%(quote_char)s') % {
                    'quote_char': quote_char,
                    'value': option_value_str,
                }
            else:
                option_value_str = None
            options_map.append([option_name, option_value_str])

            if option_name == '-X':
                if option_value != "POST":
                    raise ValueError(
                        '\'-X\' option, if defined, must be \'POST\'')
                else:
                    _x_post_defined = True

    if not _x_post_defined:
        options_string += ' -X POST'
        options_map.append(['-X', 'POST'])

    # Add parameters
    if parameters:
        parameters_dict = OrderedDict({})
        for parameter in parameters:
            parameter_name = lazy_name_by_parameter(parameter, seed=seed)
            parameter_value = lazy_value_by_parameter(parameter,
                                                      seed=seed,
                                                      locale=locale)
            parameters_dict[parameter_name] = parameter_value

        # parameters codification
        if content_type == 'multipart/form-data':
            for param_name, param_value in parameters_dict.items():
                option_value = '%(name)s=%(value)s' % {
                    'name': param_name,
                    'value': param_value
                }
                options_map.append(['-F', option_value])
                options_string += ' -F %(params)s' % {'params': option_value}
        else:
            encode_func = json.dumps if content_type == 'application/json' \
                else urlencode

            option_value = encode_func(parameters_dict)
            options_map.append(['-d', option_value])
            options_string += ' -d %(quote_char)s%(params)s%(quote_char)s' % {
                'quote_char': quote_char,
                'params': option_value,
            }
    else:
        parameters_dict = {}

    # Add files
    if files:
        for file_param_name, file_data in files.items():
            if file_data is None:
                file_data = lazy_value_by_parameter(
                    {
                        'name': '',
                        'faker': 'faker.providers.file::file_path',
                    },
                    seed=seed,
                    locale=locale)
            elif isinstance(file_data, str):
                file_data = file_data
            else:  # Iterable
                file_data = file_data[0]
            option_value = '%(name)s=@' % {'name': file_param_name}
            option_value += file_data
            options_string += ' -F %(value)s' % {'value': option_value}
            options_map.append(['-F', option_value])

    # Add headers
    options_string += headers_string
    options_map.extend(headers_map)

    # 1 here is a space
    _current_length = len(options_string) + len(url) + len(response) + 1 \
        + len(headers) * 2 * len(quote_char)
    if _current_length < wrap:
        oneline = True

    response += ' '
    response += _render_options_map(options_map,
                                    options_string,
                                    url,
                                    oneline=oneline,
                                    indent=indent,
                                    quote_char=quote_char)

    if teardown:
        response += str(teardown)

    return response
