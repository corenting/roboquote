PYTHON := poetry run
SRC := roboquote main.py
BIOME_FILES := static/js/ static/css

.PHONY: init
.SILENT: init
init:
	poetry install

.PHONY: format
format:
	$(PYTHON) ruff format $(SRC)
	$(PYTHON) ruff check --fix $(SRC)
	biome format --write $(BIOME_FILES)
	biome check --write $(BIOME_FILES)

.PHONY: style
style:
	shellcheck scripts/*.sh
	$(PYTHON) ruff format --check $(SRC)
	$(PYTHON) ruff check $(SRC)
	$(PYTHON) pyright -- $(SRC)
	biome lint  $(BIOME_FILES)

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

