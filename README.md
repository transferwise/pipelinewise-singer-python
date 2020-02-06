pipelinewise-singer-python
===================
[![PyPI version](https://badge.fury.io/py/pipelinewise-singer-python.svg)](https://badge.fury.io/py/pipelinewise-singer-python)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pipelinewise-singer-python.svg)](https://pypi.org/project/pipelinewise-singer-python/)
[![License: MIT](https://img.shields.io/badge/License-Apache2-yellow.svg)](https://opensource.org/licenses/Apache-2.0)

Writes the Singer format from Python.

This is a fork of [Singer's singer-python](https://github.com/singer-io/singer-python) made for [PipelineWise](https://transferwise.github.io/pipelinewise).

Usage
---

### Setup environment
This library depends on python3. We recommend using a `virtualenv` like this:

```bash
python3 -m venv ~/.virtualenvs/singer-python
```

### Installation
Next, install this library:

```bash
source ~/.virtualenvs/singer-python/bin/activate
git clone http://github.com/singer-io/singer-python
cd singer-python
make install
```

### Usage example
Now, from python code within the same `virtualenv`, you can use the library:

```python
import singer

singer.write_schema('my_table',
	            {'properties':{'id': {'type': 'string', 'key': True}}},
		    ['id'])
singer.write_records('my_table',
                     [{'id': 'b'}, {'id':'d'}])
singer.write_state({'my_table': 'd'})
```

### Logging configuration

**pipelinewise-singer-python** by default doesn't use any predefined logging configuration, it's up to the calling 
library to define it. However, if the environment variable `LOGGING_CONF_FILE` is found and set then the **pipelinewise-singer-python** 
would use the path provided in the env variable as the logging configuration for the logger. 


License
-------

Distributed under the Apache License Version 2.0
