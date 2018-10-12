# Flask-RangeRequest

`Flask-RangeRequest` adds range request ([RFC 7233](https://tools.ietf.org/html/rfc7233)) support to your Flask app.

## Example

```python
from datetime import datetime
from flask import Flask
from flask_rangerequest import RangeRequest
from os import path

app = Flask(__name__)
size = path.getsize(__file__)
with open(__file__, 'rb') as f:
    etag = RangeRequest.make_etag(f)
last_modified = datetime.utcnow()

@app.route('/', methods=('GET', 'POST'))
def index():
    return RangeRequest(open(__file__, 'rb'),
                        etag=etag,
                        last_modified=last_modified,
                        size=size).make_response()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
```

## License

This work is dual licensed under the MIT and Apache-2.0 licenses. See [LICENSE-MIT](./LICENSE-MIT)
and [LICENSE-APACHE](./LICENSE-APACHE) for details.
