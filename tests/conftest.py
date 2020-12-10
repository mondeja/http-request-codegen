'''Tests configuration.'''

import multiprocessing
import os
import sys

import pytest


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
if TEST_DIR not in sys.path:
    sys.path.append(TEST_DIR)

from server import test_server_process  # noqa: E402


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
    proc = multiprocessing.Process(target=test_server_process, args=())
    proc.start()
    return proc


@pytest.fixture(autouse=True, scope='session')
def _session_fixture():
    proc = on_start()
    yield
    proc.terminate()
