#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'attrs>=16.0',
    'requests==2.11.1',
    'email-validator==1.0.1',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='mgship',
    version='0.1.0',
    description=("Tool to ship the Mailgun event log for "
                 "archiving and later analytics."),
    long_description=readme + '\n\n' + history,
    author="Konstantinos Koukopoulos",
    author_email='koukopoulos@gmail.com',
    url='https://github.com/kouk/mgship',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mgship=mgship.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='mgship',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
