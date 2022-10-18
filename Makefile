PYTHON=poetry run
SRC = roboquote main.py

.PHONY: init
.SILENT: init
init:
	poetry install

.PHONY: format
.SILENT: format
format:
	$(PYTHON) black .
	$(PYTHON) isort .

.PHONY: style
.SILENT: style
style:
	shellcheck scripts/*.sh
	$(PYTHON) pflake8 $(SRC)
	$(PYTHON) mypy -- $(SRC)
	$(PYTHON) black --check $(SRC)
	$(PYTHON) isort --check-only $(SRC)

.PHONY: update-examples
.SILENT: update-examples
update-examples:
	scripts/update_examples.sh
