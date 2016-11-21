.PHONY: build deploy lint test functions help
.DEFAULT_GOAL := help

build:  ## Build docker container
	docker build -f Dockerfile.deploy -t c-bata/lambda_deploy .

deploy: ## Deploy to AWS Lambda and API Gateway
	make build
	docker run -it --rm \
		-e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
		-e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
		-e AWS_DEFAULT_REGION=$(AWS_DEFAULT_REGION) \
		-e S3_BUCKET_NAME=$(S3_BUCKET_NAME) \
		-e LINE_BOT_CHANNEL_ACCESS_TOKEN=$(LINE_BOT_CHANNEL_ACCESS_TOKEN) \
		-e LINE_BOT_CHANNEL_ACCESS_SECRET=$(LINE_BOT_CHANNEL_ACCESS_SECRET) \
		-v `PWD`/.chalice:/app/.chalice \
		c-bata/lambda_deploy chalice deploy

lint: ## Check coding styles
	@flake8 --ignore=E501 app.py chalicelib/

test: ## Run tests
	@python -m unittest tests

functions: ## Show the list of AWS Lambda functions
	@aws lambda list-functions | jq '.Functions | .[] | .FunctionName'

help: ## Show help text
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "    \033[36m%-20s\033[0m %s\n", $$1, $$2}'
