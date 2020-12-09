'''Tests configuration.'''

import multiprocessing
import os
import sys

import flask
import pytest


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
if TEST_DIR not in sys.path:
    sys.path.append(TEST_DIR)

from consts import TEST_SERVER_HOST, TEST_SERVER_PORT  # noqa: E402


def values_list():
    return ['foo', 'bar', 'baz', 1, -1.5, True, False, None]


def value():
    return 'foo'


@pytest.fixture
def create_request_args_files():
    def _create_request_args_files(args_group):
        files = []
        if 'arguments' in args_group:
            if 'files' in args_group['arguments']:
                fileargs = args_group['arguments']['files']
                for filearg, value in fileargs.items():
                    if isinstance(value, str):
                        files.append(open(value, 'wb'))
                    else:
                        files.append(open(value[0], 'wb'))
        return files
    return _create_request_args_files


@pytest.fixture
def assert_request_args():
    def _assert_request_args(request_args, response_args):
        # print('\nREQUEST ARGS: ', request_args)
        # print('RESPONSE ARGS:', response_args)

        content_type = None
        if 'headers' in request_args:
            for hname, hvalue in request_args['headers'].items():
                assert hname
                assert isinstance(hname, str)
                assert hvalue
                assert isinstance(hvalue, str)

                assert hname in response_args['headers']
                assert hvalue == request_args['headers'][hname]

                if hname.lower() == 'content-type':
                    content_type = hvalue

        if 'parameters' in request_args:
            for param in request_args['parameters']:
                if content_type == 'text/plain':
                    assert not param['name']
                else:
                    assert param['name']
                assert isinstance(param['name'], str)

                _param_found = False
                for _param in response_args['parameters']:
                    if str(param['name']) == _param['name']:
                        _param_found = True
                        assert str(param['value']) == _param['value']

                        if content_type == 'text/plain':
                            assert not _param['name']
                        else:
                            assert _param['name']
                        assert isinstance(_param['name'], str)
                        break
                assert _param_found

        if 'files' in request_args:
            for fp_name, fp_value in request_args['files'].items():
                assert fp_name
                assert isinstance(fp_name, str)

                _file_param_found = False
                for _fp_name, _fp_value in response_args['files'].items():
                    assert _fp_name
                    assert isinstance(_fp_name, str)

                    if str(fp_name) == _fp_name:
                        _file_param_found = True

                        if isinstance(fp_value, str):
                            request_value = fp_value
                        else:
                            request_value = [
                                el if i != 1 else el.strip()
                                for i, el in enumerate(fp_value)
                            ]
                        assert request_value == _fp_value
                assert _file_param_found

        if 'kwargs' in request_args:
            if 'cookies' in request_args['kwargs']:
                for cname, cvalue in request_args['kwargs']['cookies'].items():
                    assert cname
                    assert isinstance(cname, str)
                    assert cvalue
                    assert isinstance(cvalue, str)

                    assert cname in response_args['cookies']
                    assert cvalue == request_args['kwargs']['cookies'][cname]

    return _assert_request_args


def on_start():
    # Setup Flask server in new process
    test_server = flask.Flask('http-request-codegen_tests')

    @test_server.route('/', methods=['GET', 'POST'])
    def hello_world():
        response = {
            'headers': {
                name: value
                for name, value in flask.request.headers.items()
            },
            'cookies': {
                name: value
                for name, value in flask.request.cookies.items()
            }
        }
        if flask.request.method == 'GET':
            response['parameters'] = [
                {
                    'name': name,
                    'value': value
                } for name, value in flask.request.args.items()
            ]
        elif flask.request.method == 'POST':
            try:
                content_type = response['headers']['Content-Type']
            except KeyError:
                pass
            else:
                if content_type in 'application/x-www-form-urlencoded':
                    response['parameters'] = [
                        {
                            'name': name,
                            'value': value
                        } for name, value in flask.request.form.items()
                    ]
                elif content_type == 'application/json':
                    json_data = flask.request.get_json(silent=True)
                    if json_data is not None:
                        response['parameters'] = [
                            {
                                'name': name,
                                'value': str(value)
                            } for name, value in json_data.items()
                        ]
                elif content_type == 'text/plain':
                    response['parameters'] = [
                        {
                            'name': '',
                            'value': flask.request.data.decode('utf-8'),
                        }
                    ]
                elif 'multipart/form-data' in content_type:
                    response['parameters'] = [
                        {
                            'name': name,
                            'value': value
                        } for name, value in flask.request.form.items()
                    ]

                    for file_param_name, file in flask.request.files.items():
                        if 'files' not in response:
                            response['files'] = {}
                        if file.content_type is None:
                            response['files'][file_param_name] = file.filename
                        else:
                            fvalue = [file.filename, file.content_type]
                            if file.headers is not None:
                                file_headers = {}
                                for name, value in file.headers.items():
                                    if name in ['Content-Disposition',
                                                'Content-Type']:
                                        continue
                                    file_headers[name] = value
                                if file_headers:
                                    fvalue.append(file_headers)
                            response['files'][file_param_name] = fvalue
                elif len(content_type) < 50:
                    raise NotImplementedError(
                        ('Content-Type \'%s\' not supported by POST method of'
                         ' Flask testing server') % content_type)
                # else:  fake content type, only for test header wrapping
        else:
            raise NotImplementedError(
                ('Method %s must be implemented in Flask testing'
                 ' server') % flask.request.method)
        return response

    def flask_proc():
        test_server.run(host=TEST_SERVER_HOST,
                        port=TEST_SERVER_PORT,
                        debug=True,
                        use_reloader=False)

    proc = multiprocessing.Process(target=flask_proc, args=())
    proc.start()
    return proc


@pytest.fixture(autouse=True, scope='session')
def _session_fixture():
    proc = on_start()
    yield
    proc.terminate()
