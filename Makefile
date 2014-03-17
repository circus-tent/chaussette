.PHONY: docs test

BIN = `pwd`/bin

ifndef VTENV_OPTS
VTENV_OPTS = "--no-site-packages"
endif

test:
	$(BIN)/pip install tox
	$(BIN)/tox

bin/python:
	virtualenv $(VTENV_OPTS) .
	$(BIN)/python setup.py develop

docs: bin/python
	$(BIN)/pip install sphinx
	$(BIN)/sphinx-build -b html -d docs/build/doctrees docs/source build/html

upload: bin/python
	$(BIN)/pip install wheel
	$(BIN)/python setup.py sdist --formats=zip,gztar bdist_wheel upload
