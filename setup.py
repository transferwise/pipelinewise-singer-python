#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="pipelinewise-singer-python",
      version='1.1.1',
      description="Singer.io utility library - PipelineWise compatible",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="TransferWise",
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3 :: Only'
      ],
      url="https://github.com/transferwise/pipelinewise-singer-python",
      install_requires=[
          'pytz==2019.3',
          'jsonschema==3.2.0',
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
              'nose'
          ]
      },
      packages=['singer'],
      package_data={
          'singer': [
              'logging.conf'
          ]
      },
      include_package_data=True
      )
