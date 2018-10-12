import pytest
import subprocess

from tempfile import NamedTemporaryFile
from werkzeug.exceptions import RequestedRangeNotSatisfiable

from flask_rangerequest._utils import parse_range_header


VALID_RANGES = [
    (None, 500, [(0, 499)]),
    ('bytes=0', 500, [(0, 499)]),
    ('bytes=100', 500, [(100, 499)]),
    ('bytes=100-', 500, [(100, 499)]),  # not in the RFC, but how curl sends
    ('bytes=0-99', 500, [(0, 99)]),
    ('bytes=0-599', 500, [(0, 499)]),
    ('bytes=0-0', 500, [(0, 0)]),
    ('bytes=-100', 500, [(400, 499)]),
    ('bytes=0-99,100-199', 500, [(0, 199)]),
    ('bytes=0-100,100-199', 500, [(0, 199)]),
    ('bytes=0-99,101-199', 500, [(0, 99), (101, 199)]),
    ('bytes=0-199,100-299', 500, [(0, 299)]),
    ('bytes=0-99,200-299', 500, [(0, 99), (200, 299)]),
]


INVALID_RANGES = [
    'bytes=200-100',
    'bytes=0-100,300-200',
]


def test_parse_ranges():
    for case in VALID_RANGES:
        (header, target_size, expected) = case
        parsed = parse_range_header(header, target_size)
        assert parsed == expected, case

    for invalid in INVALID_RANGES:
        with pytest.raises(RequestedRangeNotSatisfiable):
            parse_range_header(invalid, 500)


def test_headers(server):
    with server.app.test_client() as client:
        resp = client.get('/')
        assert resp.headers['ETag'].startswith('"sha256:')
        assert resp.headers['Accept-Ranges'] == 'bytes'
        assert resp.headers.get('Last-Modified') is not None
        assert resp.headers.get('Content-Length') is not None


def test_ignore_post(server):
    '''RFC 7233 Section 3.1
       A server MUST ignore a Range header field received with a request method other than GET.
    '''

    with server.app.test_client() as client:
        # First we check that GET/POST serve all the content without range headers
        resp = client.get('/')
        assert resp.status_code == 200
        assert resp.data == server.dummy_file.contents
        resp = client.post('/')
        assert resp.status_code == 200
        assert resp.data == server.dummy_file.contents

        # Second, we check that POST ignores range headers
        resp = client.post('/', headers={'Range': 'bytes=39-50'})
        assert resp.status_code == 200
        assert resp.data == server.dummy_file.contents


def test_reassemble(server):
    with server.app.test_client() as client:
        resp = client.get('/', headers={'Range': 'bytes=0-10'})
        assert resp.status_code == 206
        bytes_out = resp.data

        resp = client.get('/', headers={'Range': 'bytes=11-100000'})
        assert resp.status_code == 206
        bytes_out += resp.data

        assert bytes_out == server.dummy_file.contents


def test_mismatched_etags(server):
    '''RFC 7233 Section 3.2
       The "If-Range" header field allows a client to "short-circuit" the second request.
       Informally, its meaning is as follows: if the representation is unchanged, send me the
       part(s) that I am requesting in Range; otherwise, send me the entire representation.
    '''

    with server.app.test_client() as client:
        resp = client.get('/')
        assert resp.status_code == 200

        resp = client.get('/',
                          headers={'If-Range': 'mismatched etag',
                                   'Range': 'bytes=10-100'})
        assert resp.status_code == 200


def test_if_unmodified_since(server):
    with server.app.test_client() as client:
        resp = client.get('/')
        assert resp.status_code == 200
        last_mod = resp.headers['Last-Modified']

        resp = client.get('/', headers={'If-Unmodified-Since': last_mod})
        assert resp.status_code == 304


def test_curl(live_server):
    # Debugbing help from `man curl`, on error 33
    #       33     HTTP range error. The range "command" didn't work.
    subprocess.check_call(['curl', '--continue-at', '10', live_server])


def test_wget(live_server):
    tmp = NamedTemporaryFile()
    tmp.write(b'x' * 10)
    subprocess.check_call(['wget', '--continue', '-O', tmp.name, live_server])
