import os


http_generators_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'generators'),
)

METHODS = [
    'GET',
    'POST',
    'PUT',
    'HEAD',
    'DELETE',
    'PATCH',
    'OPTIONS',
]
