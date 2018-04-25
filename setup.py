#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'gcmap',
    version = '0.0.5',
    url = 'https://github.com/paulgb/gcmap',
    description = 'Great circle visualization of many coordinate pairs',
    author = 'Paul Butler',
    author_email = 'paulgb@gmail.com',
    packages = ['gcmap'],
    install_requires = [
        'aggdraw>=1.2,<2',
        'numpy>=1.7.1',
        'Pillow>=2.0.0',
        'pyproj>=1.9.3'
    ]
)
