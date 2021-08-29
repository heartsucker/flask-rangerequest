#!/usr/bin/env python

import re
import setuptools

from os import path

base_dir = path.abspath(path.dirname(__file__))

with open(path.join(base_dir, 'README.md')) as f:
    long_description = f.read()

with open(path.join(base_dir, 'flask_rangerequest', '__init__.py')) as f:
    version = re.search("^__version__ = '(?P<version>.*)'$",
                        f.read(),
                        re.MULTILINE).group('version')

setuptools.setup(
    name='Flask-RangeRequest',
    version=version,
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
        'Flask>=2',
    ],
    python_requires='>=3.6',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ),
)
