# Flask-RangeRequest
[![PyPI Version](https://badge.fury.io/py/Flask-RangeRequest.svg)](https://pypi.python.org/pypi/Flask-RangeRequest) [![CI](https://api.travis-ci.org/heartsucker/flask-rangerequest.svg?branch=develop)](https://api.travis-ci.org/heartsucker/flask-rangerequest.svg?branch=develop) [![Documentation Status](https://readthedocs.org/projects/flask-rangerequest/badge/?version=latest)](https://flask-rangerequest.readthedocs.io/en/latest/?badge=latest)

`Flask-RangeRequest` adds range request ([RFC 7233](https://tools.ietf.org/html/rfc7233)) support to your Flask app.

## Example

```python
from datetime import datetime
from flask import Flask
from flask_rangerequest import RangeRequest
from os import path

my_file = '/path/to/file'
app = Flask(__name__)
size = path.getsize(my_file)
with open(my_file, 'rb') as f:
    etag = RangeRequest.make_etag(f)
last_modified = datetime.utcnow()

@app.route('/', methods=('GET', 'POST'))
def index():
    return RangeRequest(open(my_file, 'rb'),
                        etag=etag,
                        last_modified=last_modified,
                        size=size).make_response()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
```

## License

This work is dual licensed under the MIT and Apache-2.0 licenses. See [LICENSE-MIT](./LICENSE-MIT)
and [LICENSE-APACHE](./LICENSE-APACHE) for details.
