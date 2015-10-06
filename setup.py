"""Standard installer for the celerybot library."""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='celerybot',
    version='0.1.0',
    description='CMake helpers for celery',
    url='https://github.com/jbeezley/celerybot',
    author='Jonathan Beezley',
    author_email='jonathan.beezley@kitware.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=['celery'],
    package_data={
        'celerybot': ['common.ctest']
    }
)
