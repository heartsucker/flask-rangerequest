import pytest
import socket
import time
from urllib.request import urlopen

from flask import Flask
from multiprocessing import Process
from os import path

from flask_rangerequest import RangeRequest


class Server:

    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.dummy_file = DummyFile()
        self.range_request = RangeRequest(self.dummy_file.contents)

        @self.app.route('/', methods=('GET', 'POST'))
        def index():
            return self.range_request.make_response()


class DummyFile:

    def __init__(self) -> None:
        self.full_path = path.join(path.dirname(__file__), '..', 'README.md')
        with open(self.full_path, 'rb') as f:
            self.contents = f.read()


@pytest.fixture(scope='function')
def server():
    return Server()


@pytest.fixture(scope='session')
def live_server():
    s = socket.socket()
    s.bind(("localhost", 0))
    port = s.getsockname()[1]
    s.close()

    server = Server()

    def run():
        server.app.run(host='127.0.0.1', port=port, debug=False)

    proc = Process(target=run)
    proc.start()

    address = '127.0.0.1:{}'.format(port)

    success = False
    for _ in range(20):
        try:
            urlopen('http://{}'.format(address))
            success = True
            break
        except Exception:
            time.sleep(0.5)

    if not success:
        raise Exception('Cannot connect to server.')

    yield address

    proc.terminate()
