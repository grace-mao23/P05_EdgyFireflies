PYTHON = python3

VIRTUAL_ENV_BIN = env/bin
VIRT_PIP = $(VIRTUAL_ENV_BIN)/pip
VIRT_PY = $(VIRTUAL_ENV_BIN)/python

run: setup
	FLASK_ENV=development $(VIRT_PY) application.py

setup: requirements.txt
	$(PYTHON) -m venv env
	$(VIRT_PIP) install -r requirements.txt

lint:
ifneq (, $(shell which flake8))
	flake8 ./app --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 ./*.py --count --select=E9,F63,F7,F82 --show-source --statistics
endif

format:
ifneq (, $(shell which yapf))
	yapf -r -i --style pep8 -p -vv ./app
	yapf -r -i --style pep8 -p -vv ./*.py
endif

clean:
	rm -r env
	rm -r instance/
	rm -r */__pycache__*
