#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="pipelinewise-singer-python",
      version='3.0.2',
      description="Singer.io utility library - PipelineWise compatible",
      python_requires=">=3.12, <3.13",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="TransferWise",
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3 :: Only'
      ],
      url="https://github.com/transferwise/pipelinewise-singer-python",
      setup_requires=[
        'wrapt>=1.14.0',
      ],
      install_requires=[
          'wrapt>=1.14.0',
          'pytz',
          'jsonschema==3.2.0',
          'orjson==3.11.8',
          'python-dateutil>=2.6.0',
          'backoff==2.2.1',
          'ciso8601',
      ],
      extras_require={
          'dev': [
              'pylint==4.0.5',
              'pytest==9.0.3',
              'coverage[toml]~=6.3',
              'ipython',
              'ipdb',
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
