from http_request_codegen.api import (
    generate_http_request_code,
    generate_http_request_md_code_block
)
from http_request_codegen.support import supported_features, supported_methods


__version__ = '0.0.1'
__version_info__ = tuple([int(i) for i in __version__.split('.')])
__title__ = 'http-request-codegen'
__description__ = 'Multilanguage HTTP requests code generator.'
__all__ = (
    'generate_http_request_code',
    'generate_http_request_md_code_block',
    'supported_features',
    'supported_methods',
)
