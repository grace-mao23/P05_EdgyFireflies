PYTHON = python3

VIRTUAL_ENV_BIN = env/bin
VIRT_PIP = $(VIRTUAL_ENV_BIN)/pip
VIRT_PY = $(VIRTUAL_ENV_BIN)/python

run: setup
	FLASK_ENV=development $(VIRT_PY) application.py

test: setup
	$(VIRT_PY) -m pytest

setup: requirements.txt
	$(PYTHON) -m venv env
	$(VIRT_PIP) install -r requirements.txt

lint:
	$(VIRTUAL_ENV_BIN)/flake8 ./app --count --select=E9,F63,F7,F82 --show-source --statistics
	$(VIRTUAL_ENV_BIN)/flake8 ./tests --count --select=E9,F63,F7,F82 --show-source --statistics
	$(VIRTUAL_ENV_BIN)/flake8 ./*.py --count --select=E9,F63,F7,F82 --show-source --statistics

format:
	$(VIRTUAL_ENV_BIN)/yapf -r -i --style pep8 -p -vv ./app
	$(VIRTUAL_ENV_BIN)/yapf -r -i --style pep8 -p -vv ./tests
	$(VIRTUAL_ENV_BIN)/yapf -r -i --style pep8 -p -vv ./*.py

remove-db:
	rm -r instance/

clean:
	rm -r env
	rm -r instance/
	rm -r */__pycache__*
	rm -r .pytest_cache
