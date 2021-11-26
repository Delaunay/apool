#!/usr/bin/env python
from setuptools import setup


if __name__ == '__main__':
    setup(
        name='apool',
        version='0.0.0',
        description='Pool Adapter library for multiprocess and threading',
        author='Pierre Delaunay',
        packages=[
            'apool',
        ],
        setup_requires=['setuptools'],
        tests_require=['pytest', 'flake8', 'codecov', 'pytest-cov'],
    )
