#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
   "polib",
   "pyyaml",
   "docopt",
   "layered-yaml-attrdict-config"
]

test_requirements = [
]

setup(
    name='iconframer',
    version='0.1.1',
    description='Generate SVG icons',
    long_description=readme + '\n\n' + history,
    author='Petri Savolainen',
    author_email='petri.savolainen@koodaamo.fi',
    url='https://github.com/koodaamo/iconframer',
    packages=[
        'iconframer',
    ],
    package_dir={'iconframer':
                 'iconframer'},
    include_package_data=True,
    install_requires=requirements,
    entry_points="""
    [console_scripts]
    iconframer = iconframer.cli:iconframer
    """,
    license="BSD",
    zip_safe=False,
    keywords='iconframer',
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
    ],
    test_suite='tests',
    tests_require=test_requirements
)
