PYTHON := poetry run
BIOME := npx @biomejs/biome@latest
SRC := roboquote main.py
JS_SRC := static/js/

.PHONY: init
.SILENT: init
init:
	poetry install

.PHONY: format
format:
	$(PYTHON) ruff format $(SRC)
	$(PYTHON) ruff --fix $(SRC)
	$(BIOME) format --write $(JS_SRC)
	$(BIOME) check --apply $(JS_SRC)

.PHONY: style
style:
	shellcheck scripts/*.sh
	$(PYTHON) ruff format --check $(SRC)
	$(PYTHON) ruff $(SRC)
	$(PYTHON) pyright -- $(SRC)
	$(BIOME) lint  $(JS_SRC)

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

