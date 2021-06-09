from http_request_codegen.hrc_api import (
    generate_http_request_code,
    generate_http_request_md_fenced_code_block,
)
from http_request_codegen.hrc_support import (
    supported_features,
    supported_methods,
)
from http_request_codegen.hrc_valuer import (
    lazy_name_by_parameter,
    lazy_value_by_parameter,
)


__version__ = '0.0.8'
__title__ = 'http-request-codegen'
__all__ = (
    'generate_http_request_code',
    'generate_http_request_md_fenced_code_block',
    'lazy_name_by_parameter',
    'lazy_value_by_parameter',
    'supported_features',
    'supported_methods',
)
