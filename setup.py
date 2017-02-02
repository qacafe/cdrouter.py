#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

from setuptools import setup, find_packages
from codecs import open
from os import path
import sys

here = path.abspath(path.dirname(__file__))

sys.path.insert(0, here)

import cdrouter

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cdrouter',
    version=cdrouter.__version__,
    description='Python client for the CDRouter Web API',
    long_description=long_description,
    url='https://github.com/qacafe/cdrouter.py',
    author='QA Cafe',
    author_email='support@qacafe.com',
    license='MIT',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        "Environment :: Web Environment",
        "Topic :: Software Development",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='cdrouter json rest api client',
    packages=['cdrouter'],
    install_requires=['future', 'marshmallow', 'requests', 'requests-toolbelt']
)
