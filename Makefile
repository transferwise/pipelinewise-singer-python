.DEFAULT_GOAL := test

check_prereqs:
	bash -c '[[ -n $$VIRTUAL_ENV ]]'
	bash -c '[[ $$(python3 --version) == *3.[5-7]* ]]'

install: check_prereqs
	python3 -m pip install -e '.[dev]'

pylinting:
	pylint singer -d missing-docstring,broad-except,bare-except,too-many-return-statements,too-many-branches,too-many-arguments,no-else-return,too-few-public-methods,fixme,protected-access

test:
	nosetests --with-doctest -v
