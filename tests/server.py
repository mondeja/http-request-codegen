'''Flask testing server.'''

import os
import sys

import flask


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
if TEST_DIR not in sys.path:
    sys.path.append(TEST_DIR)

from consts import TEST_SERVER_HOST, TEST_SERVER_PORT  # noqa: E402


def build_test_server():
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
            },
        }
        if flask.request.method == 'GET':
            response['parameters'] = [
                {
                    'name': name,
                    'value': value,
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
                            'value': value,
                        } for name, value in flask.request.form.items()
                    ]
                elif content_type == 'application/json':
                    json_data = flask.request.get_json(silent=True)
                    if json_data is not None:
                        response['parameters'] = [
                            {
                                'name': name,
                                'value': str(value),
                            } for name, value in json_data.items()
                        ]
                elif content_type == 'text/plain':
                    response['parameters'] = [
                        {
                            'name': '',
                            'value': flask.request.data.decode('utf-8'),
                        },
                    ]
                elif 'multipart/form-data' in content_type:
                    response['parameters'] = [
                        {
                            'name': name,
                            'value': value,
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
                                    if name in [
                                        'Content-Disposition',
                                        'Content-Type',
                                    ]:
                                        continue
                                    file_headers[name] = value
                                if file_headers:
                                    fvalue.append(file_headers)
                            response['files'][file_param_name] = fvalue
                elif len(content_type) < 50:
                    raise NotImplementedError(
                        (
                            'Content-Type \'%s\' not supported by POST method'
                            ' of Flask testing server'
                        ) % content_type,
                    )
                # else:  fake content type, only for test header wrapping
        else:
            raise NotImplementedError(
                (
                    'Method %s must be implemented in Flask testing'
                    ' server'
                ) % flask.request.method,
            )
        return response

    return test_server


def test_server_process():
    build_test_server().run(
        host=TEST_SERVER_HOST,
        port=TEST_SERVER_PORT,
        debug=True,
        use_reloader=False,
    )


if __name__ == '__main__':
    test_server_process()
