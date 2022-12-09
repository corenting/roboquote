PYTHON := poetry run
ROME := npx rome
SRC := roboquote main.py
JS_SRC := static/js/

.PHONY: init
.SILENT: init
init:
	poetry install

.PHONY: format
format:
	$(PYTHON) black $(SRC)
	$(PYTHON) ruff --fix $(SRC)
	$(ROME) format --write $(JS_SRC)
	$(ROME) check --apply-suggested $(JS_SRC)

.PHONY: style
style:
	shellcheck scripts/*.sh
	$(PYTHON) black --check $(SRC)
	$(PYTHON) ruff $(SRC)
	$(PYTHON) mypy -- $(SRC)
	$(ROME) check $(JS_SRC)

.PHONY: update-examples
.SILENT: update-examples
update-examples:
	scripts/update_examples.sh

.PHONY: run-web
.SILENT: run-web
run-web:
	$(PYTHON) uvicorn --reload roboquote.web.app:app

.PHONY: build-docker
.SILENT: build-docker
build-docker:
	docker build -t roboquote .

