.DEFAULT_GOAL := test

check_prereqs:
	bash -c '[[ -n $$VIRTUAL_ENV ]]'
	bash -c '[[ $$(python3 --version) == *3.[5-7]* ]]'

install: check_prereqs
	python3 -m pip install -e '.[dev]'

pylinting:
	pylint singer

test:
	nosetests --with-doctest -v
