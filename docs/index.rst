``Flask-RangeRequest``
======================

``Flask-RangeRequest`` adds range request (RFC 7233) to your Flask app.

Quick Start
-----------

.. code:: python

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

Full API Docs
-------------

Full :doc:`API Docs </api/modules>` cover basic usage of this package.

.. toctree::
    :maxdepth: 2
    :caption: API Docs:

    api/modules
