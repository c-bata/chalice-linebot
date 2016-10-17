.PHONY: help roles upload functions ls-bucket upload invoke undeploy deploy update
.DEFAULT_GOAL := help

INPUT_PYFILE   := app.py
ZIP_FILE_NAME  := linebot.zip
LAMBDA_NAME    := linebot

S3_BUCKET      := takesone-lambda-packages
REGION         := ap-northeast-1

roles: ## Show the list of IAM Roles
	aws iam list-roles | jq '.Roles | .[] | .RoleName, .Arn'

functions: ## Show the list of AWS Lambda functions
	aws lambda list-functions | jq '.Functions | .[] | .FunctionName'

buckets: ## Show the files in S3 Bucket
	aws s3 ls s3://$(S3_BUCKET)

help: ## Show help text
	@echo "Description:"
	@echo "    AWS CLI Wrapper."
	@echo ""
	@echo "Requirements:"
	@echo "    - AWS CLI"
	@echo "    - jq"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "    \033[36m%-20s\033[0m %s\n", $$1, $$2}'
