#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name="pipelinewise-singer-python",
      version='1.0.0',
      description="Singer.io utility library - PipelineWise compatible",
      author="Stitch",
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3 :: Only'
      ],
      url="https://github.com/transferwise/pipelinewise-singer-python",
      install_requires=[
          'pytz==2018.4',
          'jsonschema==2.6.0',
          'simplejson==3.11.1',
          'python-dateutil>=2.6.0',
          'backoff==1.8.0',
          'ciso8601',
      ],
      extras_require={
          'dev': [
              'pylint',
              'ipython',
              'ipdb',
              'nose',
              'singer-tools'
          ]
      },
      packages=find_packages(),
      )
