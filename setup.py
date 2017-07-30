# -*- coding: utf-8 -*-

try:
    import logging
    import multiprocessing
except:
    pass

import sys
py_version = sys.version_info[:2]

try:
    from setuptools import setup, find_packages
except ImportError:
    from setuptools import setup, find_packages

packages = [
    'sitemap_generator',
]

requires = [
    'requests',
    'cherrypy'
]

test_requirements = []
setup(
    name='sitemap_generator',
    version='0.1.0',
    description='sitemap generator in python',
    author='eteamin',
    author_email='aminetesamian1371@gmail.com',
    url='https://github.com/eteamin/sitemap-generator',
    packages=packages,
    install_requires=requires,
    include_package_data=True,
)
