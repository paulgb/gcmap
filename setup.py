#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'gcmap',
    version = '0.0.1',
    description = 'Great circle visualization of many coordinate pairs',
    author = 'Paul Butler',
    author_email = 'paulgb@gmail.com',
    url = 'https://github.com/paulgb/gcmap',
    packages = ['gcmap'],
    install_requires = [
      'aggdraw==1.1-64bits',
      'numpy>=1.7.1',
      'Pillow>=2.0.0',
      'pyproj>=1.9.3'
    ],
    dependency_links = [ 
      'https://bitbucket.org/2degrees/aggdraw-64bits/downloads/aggdraw-1.1-64bits.tar.gz#egg=aggdraw-1.1.64bits'
    ]
)

