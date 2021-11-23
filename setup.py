#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="pipelinewise-singer-python",
      version='2.0.1',
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
          'pytz',
          'jsonschema==3.2.0',
          'orjson==3.6.1',
          'python-dateutil>=2.6.0',
          'backoff==1.11.1',
          'ciso8601',
      ],
      extras_require={
          'dev': [
              'pylint==2.11.1',
              'ipython',
              'ipdb',
              'nose',
              'unify==0.5'
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
