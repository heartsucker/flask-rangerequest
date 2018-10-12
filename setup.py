#!/usr/bin/env python

import flask_rangerequest
import setuptools

from os import path

base_dir = path.abspath(path.dirname(__file__))

with open(path.join(base_dir, 'README.md')) as f:
    long_description = f.read()

setuptools.setup(
    name='Flask-RangeRequest',
    version=flask_rangerequest.__version__,
    author='heartsucker',
    author_email='heartsucker@autistici.org',
    url='https://github.com/heartsucker/flask-rangerequest',
    description='Range Requests for Flask',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'flask_rangerequest': 'flask_rangerequest'},
    packages=['flask_rangerequest'],
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
    ],
    python_requires='>=3.4',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
)
