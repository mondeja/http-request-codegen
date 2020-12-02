
import os
import sys

import inflection

from http_request_codegen.string import replace_multiple


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
if TEST_DIR not in sys.path:
    sys.path.append(TEST_DIR)


def values_list():
    return ['foo', 'bar', 'baz', 1, -1.5, True, False, None]


def value():
    return 'foo'


def argument_combination_to_filename(combination_name, index):
    return '%s.%s.expect.txt' % (
        str(index).zfill(3),
        inflection.parameterize(
            replace_multiple(combination_name, replacements={
                '"': '-double-quote-',
                '\'': '-single-quote-',
            })
        )
    )


def combination_arguments_to_kwargs(arguments):
    kwargs = {}
    for key, value in arguments.items():
        if key == 'kwargs':
            kwargs.update(value)
        else:
            kwargs[key] = value
    return kwargs


def get_argument_combinations(include_filenames=True, dirpath=None):
    response = [
        {
            'name': 'URL',
            'arguments': {
                'url': 'localhost',
            }
        },
        {
            'name': 'URL wrapping (no wrap)',
            'arguments': {
                'url': 'localhost',
                'wrap': 99999
            }
        },
        {
            'name': 'URL wrapping (wrap 15)',
            'arguments': {
                'url': 'https://fakewebsite.extension',
                'wrap': 15,
            }
        },
        {
            'name': 'URL + parameter',
            'arguments': {
                'url': 'localhost',
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1'
                    }
                ]
            }
        },
        {
            'name': 'URL + parameters',
            'arguments': {
                'url': 'https://fakewebsite.extension',
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'foo'
                    },
                    {
                        'name': 'param-2',
                        'value': 1
                    },
                    {
                        'name': 'param-3',
                        'value': .777
                    },
                    {
                        'name': 'param-4',
                        'value': True
                    },
                ]
            }
        },
        {
            'name': 'URL + parameter wrapping value',
            'arguments': {
                'url': 'localhost',
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'foo-bar-baz' * 50,
                    }
                ]
            }
        },
        {
            'name': 'URL + parameters, one wrapping value',
            'arguments': {
                'url': 'localhost',
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'foo-bar-baz' * 50,
                    },
                    {
                        'name': 'param-2',
                        'value': 'value-2'
                    }
                ]
            }
        },
        {
            'name': 'URL + parameter wrapping value smart spaces',
            'arguments': {
                'url': 'localhost',
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'Wrap me handling spaces smartly ' * 15,
                    }
                ]
            }
        },
        {
            'name': 'URL + parameter escaping quotes',
            'arguments': {
                'url': 'localhost',
                'parameters': [
                    {
                        'name': 'param-1-with-\'\'-quotes',
                        'value': 'value-1-with-\'\'-quotes'
                    }
                ]
            }
        },
        {
            'name': 'URL + header',
            'arguments': {
                'url': 'localhost',
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        },
        {
            'name': 'URL + headers',
            'arguments': {
                'url': 'localhost',
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': 'es',
                }
            }
        },
        {
            'name': 'URL + header wrapping value',
            'arguments': {
                'url': 'localhost',
                'headers': {
                    'Content-Type': 'application/json' * 5,
                }
            }
        },
        {
            'name': 'URL + headers, one wrapping value',
            'arguments': {
                'url': 'localhost',
                'headers': {
                    'Content-Type': 'application/json' * 5,
                    'Accept-Language': '*'
                }
            }
        },
        {
            'name': 'URL + header escaping quote',
            'arguments': {
                'url': 'localhost',
                'headers': {
                    'Header name with \'\' quotes':
                    'Header value with \'\' quotes'
                }
            }
        },
        {
            'name': 'URL + kwarg',
            'arguments': {
                'url': 'localhost',
                'kwargs': {
                    'timeout': 5,
                }
            }
        },
        {
            'name': 'URL + kwargs',
            'arguments': {
                'url': 'localhost',
                'kwargs': {
                    'timeout': 5,
                    'stream': True
                }
            }
        },
        {
            'name': 'URL + kwarg escaping quotes',
            'arguments': {
                'url': 'localhost',
                'kwargs': {
                    'timeout': 'value with \'\' quotes'
                }
            }
        },
        {
            'name': 'URL + kwarg wrapping value',
            'arguments': {
                'url': 'localhost',
                'kwargs': {
                    'timeout': 'hello ' * 20,
                }
            }
        },
        {
            'name': 'URL + kwargs, one wrapping value',
            'arguments': {
                'url': 'localhost',
                'kwargs': {
                    'timeout': 'hello ' * 20,
                    'stream': True
                }
            }
        },
        {
            'name': 'URL + parameter + header',
            'arguments': {
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1'
                    }
                ],
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        },
        {
            'name': 'URL + parameters + header',
            'arguments': {
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1'
                    },
                    {
                        'name': 'param-2',
                        'value': 'value-2'
                    },
                ],
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        },
        {
            'name': 'URL + parameter + headers',
            'arguments': {
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1'
                    }
                ],
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': '*'
                }
            }
        },
        {
            'name': 'URL + parameters + headers',
            'arguments': {
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1'
                    },
                    {
                        'name': 'param-2',
                        'value': 'value-2'
                    },
                ],
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': '*'
                }
            }
        },
        {
            'name': 'URL + parameter + kwarg',
            'arguments': {
                'url': 'localhost',
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    }
                ],
                'kwargs': {
                    'timeout': 10
                }
            }
        },
        {
            'name': 'URL + parameters + kwarg',
            'arguments': {
                'url': 'localhost',
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                    {
                        'name': 'param-2',
                        'value': 'value-2',
                    }
                ],
                'kwargs': {
                    'timeout': 10
                }
            }
        },
        {
            'name': 'URL + parameter + kwargs',
            'arguments': {
                'url': 'localhost',
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    }
                ],
                'kwargs': {
                    'timeout': 10,
                    'stream': True
                }
            }
        },
        {
            'name': 'URL + parameters + kwargs',
            'arguments': {
                'url': 'localhost',
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1',
                    },
                    {
                        'name': 'param-2',
                        'value': 'value-2',
                    }
                ],
                'kwargs': {
                    'timeout': 10,
                    'stream': True
                }
            }
        },
        {
            'name': 'URL + header + kwarg',
            'arguments': {
                'headers': {
                    'Content-Type': 'application/json'
                },
                'kwargs': {
                    'timeout': 5
                }
            }
        },
        {
            'name': 'URL + headers + kwarg',
            'arguments': {
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': '*'
                },
                'kwargs': {
                    'timeout': 5
                }
            }
        },
        {
            'name': 'URL + header + kwargs',
            'arguments': {
                'headers': {
                    'Accept-Language': '*'
                },
                'kwargs': {
                    'timeout': 5,
                    'stream': False
                }
            }
        },
        {
            'name': 'URL + headers + kwargs',
            'arguments': {
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': '*'
                },
                'kwargs': {
                    'timeout': 5,
                    'stream': False
                }
            }
        },
        {
            'name': 'URL + parameter + header + kwarg',
            'arguments': {
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1'
                    }
                ],
                'headers': {
                    'Content-Type': 'application/json'
                },
                'kwargs': {
                    'timeout': 5
                }
            }
        },
        {
            'name': 'URL + parameter + header + kwargs',
            'arguments': {
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1'
                    }
                ],
                'headers': {
                    'Content-Type': 'application/json'
                },
                'kwargs': {
                    'timeout': 5,
                    'stream': True
                }
            }
        },
        {
            'name': 'URL + parameters + header + kwarg',
            'arguments': {
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1'
                    },
                    {
                        'name': 'param-2',
                        'value': 7.77
                    }
                ],
                'headers': {
                    'Content-Type': 'application/json'
                },
                'kwargs': {
                    'timeout': 5
                }
            }
        },
        {
            'name': 'URL + parameters + header + kwargs',
            'arguments': {
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1'
                    },
                    {
                        'name': 'param-2',
                        'value': 7.77
                    }
                ],
                'headers': {
                    'Content-Type': 'application/json'
                },
                'kwargs': {
                    'timeout': 5,
                    'stream': False
                }
            }
        },
        {
            'name': 'URL + parameters + headers + kwarg',
            'arguments': {
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1'
                    },
                    {
                        'name': 'param-2',
                        'value': 7.77
                    }
                ],
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': 'fr'
                },
                'kwargs': {
                    'timeout': 5
                }
            }
        },
        {
            'name': 'URL + parameters + headers + kwargs',
            'arguments': {
                'parameters': [
                    {
                        'name': 'param-1',
                        'value': 'value-1'
                    },
                    {
                        'name': 'param-2',
                        'value': 7.77
                    }
                ],
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept-Language': 'fr'
                },
                'kwargs': {
                    'timeout': 5,
                    'stream': True
                }
            }
        },
        {
            'name': 'No setup',
            'arguments': {
                'setup': False,
            }
        },
        {
            'name': 'Custom setup',
            'arguments': {
                'setup': 'custom_setup=1\n\n'
            }
        },
        {
            'name': 'Custom teardown',
            'arguments': {
                'teardown': '\n\ncustom_teardown=1'
            }
        },
        {
            'name': 'Quote character \'',
            'arguments': {
                'quote_char': '\''
            }
        },
        {
            'name': 'Quote character "',
            'arguments': {
                'quote_char': '"'
            }
        },
        {
            'name': 'Indent two spaces',
            'arguments': {
                'indent': '  ',
                'url': 'localhost ' * 10,
            }
        },
        {
            'name': 'Indent four spaces',
            'arguments': {
                'indent': '    ',
                'url': 'localhost ' * 10,
            }
        },
        {
            'name': 'Indent tab',
            'arguments': {
                'indent': '\t',
                'url': 'localhost ' * 10,
            }
        },
        {
            'name': 'One line',
            'arguments': {
                'oneline': True
            }
        },
        {
            'name': 'One line + no setup',
            'arguments': {
                'oneline': True,
                'setup': False
            }
        },
        {
            'name': 'Wrap 0',
            'arguments': {
                'wrap': 0
            }
        },
        {
            'name': 'Wrap 1',
            'arguments': {
                'wrap': 1
            }
        },
        {
            'name': 'Wrap 10',
            'arguments': {
                'wrap': 10
            }
        },
        {
            'name': 'Wrap 20',
            'arguments': {
                'wrap': 20
            }
        },
        {
            'name': 'Wrap 30',
            'arguments': {
                'wrap': 30
            }
        },
        {
            'name': 'Wrap 35',
            'arguments': {
                'wrap': 35
            }
        },
        {
            'name': 'Wrap 40',
            'arguments': {
                'wrap': 40
            }
        },
        {
            'name': 'Wrap infinite',
            'arguments': {
                'wrap': float('inf')
            }
        },
        {
            'name': 'Wrap null is infinite',
            'arguments': {
                'wrap': None
            }
        }
    ]

    if include_filenames:
        for index, args_group in enumerate(response):
            fname = argument_combination_to_filename(
                args_group['name'], index)
            if dirpath and os.path.exists(dirpath):
                fname = os.path.join(dirpath, fname)
            args_group['filename'] = fname
    return response
