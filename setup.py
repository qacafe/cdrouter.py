#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

from setuptools import setup, find_packages
from codecs import open
from os import path
import sys


def read(rel_path):
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


here = path.abspath(path.dirname(__file__))

sys.path.insert(0, here)


with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cdrouter",
    version=get_version("cdrouter/__init__.py"),
    description="Python client for the CDRouter Web API",
    long_description=long_description,
    url="https://github.com/qacafe/cdrouter.py",
    author="QA Cafe",
    author_email="support@qacafe.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "Topic :: Software Development",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    keywords="cdrouter json rest api client",
    packages=["cdrouter"],
    install_requires=["future", "marshmallow<3", "requests", "requests-toolbelt"],
)
