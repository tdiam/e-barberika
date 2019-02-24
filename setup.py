'''Setup script

Usage: pip install .

To install development dependencies too, run: pip install .[dev]
'''
from setuptools import setup, find_packages
from _version import __version__

setup(
    name='asoures',
    version=__version__,
    packages=find_packages(),
    scripts=['manage.py'],
    url='https://bitbucket.com/asoures/asoures',
    author='Asoures Team',
    install_requires=[
        'dj-database-url',
        'Django',
        'psycopg2-binary',
        'django-cors-headers',
        'mod-wsgi',
        'requests'
    ],
    extras_require={
        'dev': [
            'pylint',
            'pylint-django',
            'git-pylint-commit-hook',
            'faker',
        ],
    },
)
