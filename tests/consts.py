'''Tests constants.'''

import tempfile


TEST_SERVER_HOST = 'localhost'
TEST_SERVER_PORT = '8876'
TEST_BASE_URL = 'http://%s:%s' % (TEST_SERVER_HOST, TEST_SERVER_PORT)

TEMPDIR = tempfile.gettempdir()
