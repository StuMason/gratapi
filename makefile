install: ## Install required libs
	pip3 install -r requirements.txt
	pip3 install -r requirements-dev.txt
	pre-commit install

black:
	black ./src ./tests ./handler_*

flake:
	flake8 ./src ./tests ./handler_* --count --max-complexity=10 --max-line-length=127 --statistics

autopep:
	autopep8 --in-place --aggressive --aggressive -a -r ./src ./tests ./handler_*

test: ## Run pytest with 70% coverage
	pytest ./tests --cov=src -vvv --cov-fail-under=70

test-missing: ## Run pytest and show the term-missing
	pytest --cov=src ./tests/ --cov-report term-missing -vvvls

test-missing-all: ## Run pytest and show the term-missing all
	pytest --cov=. ./tests/ --cov-report term-missing -vvvls

build: ## Build the docker image used to invoke the functions locally (5 minutes+)
	cp -fr .env src/.env
	sam build --use-container --debug -m ./requirements.txt

build-local: 
	cp -fr .env src/.env
	sam build -u --debug -t ./template-local.yaml -m ./requirements.txt

deploy:
	make build
	sam deploy

.SILENT: help
help: ## Show this help message
	set -x
	echo "Usage: make [target] ..."
	echo ""
	echo "Available targets:"
	grep ':.* ##\ ' ${MAKEFILE_LIST} | awk '{gsub(":[^#]*##","\t"); print}' | column -t -c 2 -s $$'\t' | sort
