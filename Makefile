SHELL :=/bin/bash

.PHONY: test clean build
.DEFAULT_GOAL=help
VENV_DIR = .venv


build-all: # build all sandboxes
	@echo ">>>>> Building STREAMLIT SANDBOX environment"
	@$(MAKE) build-st

	@echo ">>>>> Building STATIC SANDBOX environment"
	@$(MAKE) build-static

	@echo ">>>>> Building VUE SANDBOX environment"
	@$(MAKE) build-vue

build-st: # build streamlit docker image
	@docker build -t streamlit-image-artifact ./sandbox/streamlit

build-vue: # build vue docker image
	@docker build -t vue-image-artifact ./sandbox/vue-app

build-static: # build static content docker image
	@docker build -t static-image-artifact ./sandbox/static

run: # run local streamlit app
	@streamlit run app.py

clean: # Clean temporary files
	@rm -rf $(TMP_PATH) __pycache__ .pytest_cache
	@find . -name '*.pyc' -delete
	@rm -rf .ruff_cache
	@find . -name '__pycache__' -delete
	@rm -rf build dist

setup: # Initial project setup
	@echo "Creating virtual env at: $(VENV_DIR)"
	@python3.10 -m venv $(VENV_DIR)
	@echo "Installing dependencies..."
	@source $(VENV_DIR)/bin/activate && pip install -r requirements.txt
	@echo -e "\n✅ Done.\n🎉 Run the following commands to get started:\n\n ➡️ source $(VENV_DIR)/bin/activate\n ➡️ make build-all run\n"

help: # Show this help
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
