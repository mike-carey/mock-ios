###
# Project commands
##

# Variables

## Defaults
ENV_FILE ?= .env
PACKAGE_INFO ?= .package-info

DOCKER_SERVER =
DOCKER_USERNAME =
DOCKER_PASSWORD =

## Load the environment
ifneq (,$(wildcard $(ENV_FILE)))
	include $(ENV_FILE)
	export $(shell sed 's/=.*//' $(ENV_FILE))
endif

APP_NAME = $(shell grep 'APP_NAME = ' $(PACKAGE_INFO) | sed 's/APP_NAME = //g')
VERSION = $(shell grep 'VERSION = ' $(PACKAGE_INFO) | sed 's/VERSION = //g')

DOCKER_TAG ?= $(DOCKER_USERNAME)/$(APP_NAME)

# Helpers

.PHONY: *

help:
	@echo "Usage: make <command>"
	@echo ""
	@echo "  .env   Creates the .env file from .env.example"
	@echo "  build  Builds the docker image"
	@echo "  shell  Starts a shell in the docker image"
	@echo ""
# help

.DEFAULT_GOAL := help

.env:
	cp .env.example .env
# .env

version:
	@echo $(VERSION)
# version

# DOCKER TASKS

# Builds the docker image
build:
	docker build -t $(APP_NAME) .
# build

# Builds the docker image without cache
build-nc:
	docker build --no-cache -t $(APP_NAME) .
# build-nc

## Publishes the docker image to the docker hub
release: build-nc publish

# Docker publish

LOGIN_CMD := "docker login"
ifneq (,$(DOCKER_USERNAME))
	LOGIN_CMD += " --username $(DOCKER_USERNAME)"
endif
ifneq (,$(DOCKER_PASSWORD))
	LOGIN_CMD += " --password $(DOCKER_PASSWORD)"
endif
ifneq (,$(DOCKER_SERVER))
	LOGIN_CMD += " $(DOCKER_SERVER)"
endif

login:
	@eval $(LOGIN_CMD)
# login

## Publish the `{version}` ans `latest` tagged containersto ECR
publish: login publish-latest publish-version

## Publish the `latest` taged container to ECR
publish-latest: tag-latest
	@echo 'publish latest to $(DOCKER_TAG)'
	docker push $(DOCKER_TAG):latest
# publish-latest

## Publish the `{version}` taged container to ECR
publish-version: tag-version
	@echo 'publish $(VERSION) to $(DOCKER_TAG)'
	docker push $(DOCKER_TAG):$(VERSION)
# publish-version

# Docker tagging

## Generate container tags for the `{version}` ans `latest` tags
tag: tag-latest tag-version

## Generate container `{version}` tag
tag-latest: build
	@echo 'create tag latest'
	docker tag $(APP_NAME) $(DOCKER_TAG):latest
# tag-latest

## Generate container `latest` tag
tag-version: build
	@echo 'create tag $(VERSION)'
	docker tag $(APP_NAME) $(DOCKER_TAG):$(VERSION)
# tag-version

# Starts a shell in the docker image
shell: build .env
	docker run -it -v $(PWD):/srv -w /srv --env-file $(ENV_FILE) $(DOCKER_TAG) sh
# shell


# Makefile
