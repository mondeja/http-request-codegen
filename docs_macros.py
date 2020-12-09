import os
import random
import sys

import http_request_codegen
from http_request_codegen.hrc_factory import get_func_by_lang_impl_method


DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'docs'))
if DOCS_DIR not in sys.path:
    sys.path.append(DOCS_DIR)

import fake_module  # noqa: E402


def define_env(env):
    # library module exposed globally
    env.variables['http_request_codegen'] = http_request_codegen
    env.variables['get_func_by_lang_impl_method'] = \
        get_func_by_lang_impl_method

    # random seed for each build, only for fun
    env.variables['seed'] = random.randint(1, 10000)

    # fake module to perform imports in demos
    env.variables['fake_module'] = fake_module

    # builtins types to the environment
    env.variables['str'] = str
    env.variables['int'] = int
    env.variables['float'] = float
    env.variables['bool'] = bool

    @env.macro
    def supported_features_md_table(methods):
        response = f'''
        |                         | {' | '.join(methods.keys())} |
        |-------------------------|:---:|:----:|
'''
        features_included = []
        for method, features in methods.items():
            for feature, supported in features.items():
                if feature in features_included:
                    continue
                features_included.append(feature)

                if feature == '_supported':
                    continue
                response += f'        | {feature}             | '
                for i, _method in enumerate(methods.keys()):
                    if i > 0:
                        response += '| '
                    response += (
                        '%s ' % '✅' if methods[_method][feature] else ' ')

                response += '|\n'
        return response
