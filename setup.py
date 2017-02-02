##############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from setuptools import setup, find_packages

setup(
    name='Products.ZCatalog',
    version='4.0a3',
    url='https://pypi.python.org/pypi/Products.ZCatalog',
    license='ZPL 2.1',
    description="Zope 2's indexing and search solution.",
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    packages=find_packages('src'),
    namespace_packages=['Products'],
    package_dir={'': 'src'},
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=[
        'setuptools',
        'AccessControl >= 4.0a4',
        'Acquisition',
        'BTrees',
        'DateTime',
        'DocumentTemplate',
        'ExtensionClass',
        'five.globalrequest',
        'Missing',
        'Persistence',
        'Record',
        'RestrictedPython',
        'zExceptions',
        'ZODB',
        'Zope2 >= 4.0.dev0',
        'zope.deferredimport',
        'zope.dottedname',
        'zope.globalrequest',
        'zope.interface',
        'zope.schema',
        'zope.testing',
    ],
    include_package_data=True,
    zip_safe=False,
)
