#!/usr/bin/env python
from setuptools import setup
import codecs
import os
import re


with codecs.open(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'fast_binance',
            '__init__.py'
        ), 'r', 'latin1') as fp:
    try:
        version = re.findall(r'^__version__ = "([^"]+)"\r?$', fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='fast-binance',
    version=version,
    packages=['fast_binance'],
    description='Asyncful wrapper around python-binance module.',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/mkaanerkoc/fast-binance',
    author='Kaan Erkoc',
    license='MIT',
    author_email='mkaanerkoc@gmail.com',
    install_requires=[
        'pandas', 'python-binance'
    ],
    keywords='binance exchange rest api bitcoin ethereum btc eth neo',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)