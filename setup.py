#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='esindexer',
      version='1.1',
      description='Elastic Search Indexer',
      long_description=open('README.md').read(),
      install_requires=[
          'elasticsearch==5.4.0',
          'ijson==2.2',
          'urllib3==1.12'
      ],
      tests_require=[
          'mock==1.0.1',
      ],
      packages=find_packages(exclude=['test']),
      include_package_data = True,
      test_suite="test",
      entry_points={
          'console_scripts': [
              'esindexer = esindexer.main:main'
          ]})
