.PHONY: docs

ifndef VTENV_OPTS
VTENV_OPTS = "--no-site-packages"
endif

bin/python:
	virtualenv $(VTENV_OPTS) .
	bin/python setup.py develop

docs: bin/python
	bin/pip install sphinx
	SPHINXBUILD=../bin/sphinx-build $(MAKE) -C docs html $^

