
import os
import sys


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
if TEST_DIR not in sys.path:
    sys.path.append(TEST_DIR)


def values_list():
    return ['foo', 'bar', 'baz', 1, -1.5, True, False, None]


def value():
    return 'foo'


def _foo_bar_baz_6():
    return ['foo-6', 'bar-6', 'baz-6']


def get_argument_combinations():
    def create_foo_bar_baz_list(num):
        def foo_bar_baz_list():
            return ['foo-%d' % num, 'bar-%d' % num, 'baz-%d' % num]
        return foo_bar_baz_list

    #   - url + parameter  + header + kwarg
    #   - url + parameter  + header + kwargs
    #   - url + parameters + header + kwarg
    #   - url + parameters + header + kwargs
    #   - url + parameter  + headers + kwargs
    #   - url + parameters + headers + kwargs

    return [
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
                        'value': 'foo-1'
                    },
                    {
                        'name': 'param-2',
                        'value': ['foo-2', 'bar-2', 'baz-2']
                    },
                    {
                        'name': 'param-3',
                        'value': create_foo_bar_baz_list(3)
                    },
                    {
                        'name': 'param-4',
                        'values': ['foo-4', 'bar-4', 'baz-4']
                    },
                    {
                        'name': 'param-5',
                        'values': create_foo_bar_baz_list(5)
                    },
                    {
                        'name': 'param-6',
                        'values': 'conftest::_foo_bar_baz_6'
                    },
                    {
                        'name': 'param-7',
                        'type': 'str'
                    },
                    {
                        'name': 'param-8',
                        'type': 'int'
                    },
                    {
                        'name': 'param-9',
                        'type': 'float'
                    },
                    {
                        'name': 'param-10',
                        'faker': 'faker.providers.lorem::word'
                    }
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
            'name': 'No init',
            'arguments': {
                'init': False,
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
            'name': 'One line + no init',
            'arguments': {
                'oneline': True,
                'init': False
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
            'name': 'Wrap infinite',
            'arguments': {
                'wrap': float('inf')
            }
        },
        {
            'name': 'Wrap null',
            'arguments': {
                'wrap': None
            }
        }
    ]
