#!/usr/bin/env python3

from argparse import ArgumentParser
from datetime import datetime
from flask import Flask
from os import path

from flask_rangerequest import RangeRequest


def main() -> None:
    args = arg_parser().parse_args()
    app = create_app(args.file)
    app.run(host='127.0.0.1', port=8080, debug=True)


def arg_parser() -> ArgumentParser:
    parser = ArgumentParser(path.basename(__file__),
                            description='Run an RFC 7233 enabled webserver.')
    parser.add_argument('-f', '--file', default=__file__)
    return parser


def create_app(file_) -> Flask:
    app = Flask(__name__)
    size = path.getsize(file_)
    with open(file_, 'rb') as f:
        etag = RangeRequest.make_etag(f)
    last_modified = datetime.utcnow()

    @app.route('/', methods=('GET', 'POST'))
    def index():
        return RangeRequest(open(file_, 'rb'),
                            etag=etag,
                            last_modified=last_modified,
                            size=size).make_response()

    return app


if __name__ == '__main__':
    main()
