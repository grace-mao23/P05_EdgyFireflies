PYTHON := python3

VPYTHON := env/bin/python3
VPIP := env/bin/pip

run: setup
	@export FLASK_APP=app
	FLASK_ENV=development $(VPYTHON) -m flask run

clear-db: setup
ifneq ($(wildcard instance/*.sqlite),)
	@export FLASK_APP=app
	$(VPYTHON) -m flask clear-db
else
	@echo "Database does not exist"
endif

test: setup
	$(VPYTHON) -m pytest

setup: venv requirements.txt
	$(VPIP) install -r requirements.txt --quiet
	
venv:
ifneq ($(wildcard env),)
	@echo "Python virtual environment already exist"
else
	$(PYTHON) -m venv env
endif

clean:
	rm -r env
	rm -r instance
	rm -r .pytest_cache
