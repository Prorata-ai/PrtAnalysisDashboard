.DEFAULT_GOAL := help

# Define the shell to use
SHELL := /bin/bash

#  Define folders for git operations
folders:= \
	PrtDockerLocalNetwork \
	PrtRedisService \
	PrtAttributionService \
	PrtDocumentService \
	PrtInferenceService \
	PrtIndexingDomain \
	PrtAISearch

# Add update target to handle git operations
clone: ## clone all service repositories
	@for folder in $(folders); do \
		echo "Cloning $$folder"; \
		if [ ! -d "$$folder" ]; then \
			git clone "git@github.com:Prorata-ai/$$folder.git"; \
		fi; \
	done

# Add update target to handle git operations
update: ## Update all service repositories
	@for folder in $(folders); do \
		echo "Updating $$folder"; \
		if [ "$$folder" = "PrtInferenceService" ]; then \
			(cd $$folder && git checkout timing_logs) || true; \
		elif [ "$$folder" = "PrtAttributionService" ]; then \
			(cd $$folder && git checkout main) || true; \
		elif [ "$$folder" = "PrtDocumentService" ]; then \
			(cd $$folder && git checkout develop) || true; \
		elif [ "$$folder" = "PrtIndexingDomain" ]; then \
			(cd $$folder && git checkout PPS-128-search-endpoint) || true; \
		elif [ "$$folder" = "PrtAISearch" ]; then \
			(cd $$folder && git checkout develop) || true; \
		fi; \
		(cd $$folder && git pull) || true; \
	done

# .PHONY: help clean all docker-network redis attribution document inference opensearch opensearch-dashboards dask-scheduler ingest-api search-api update clone

.PHONY: help clean all init proxy-services docker-network redis attribution document inference opensearch opensearch-dashboards dask-scheduler ingest-api search-api update clone

help: ## Show this help message
	@echo 'Usage:'
	@echo '  make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)


# Clean target to stop and remove all containers
clean: ## Remove all Docker containers, images, and volumes
	docker system prune -a; \
	docker system prune -a --volumes;

# all: docker-network redis attribution document inference opensearch opensearch-dashboards dask-scheduler ingest-api search-api ## Start all services
all: init proxy-services inference

init: docker-network redis

# New target for proxy services
proxy-services: ## Start proxy scripts for attribution and document services
	@echo "Starting proxy services..."
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD) && bash proxy-attribution.sh"'
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD) && bash proxy-document.sh"'
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD) && bash proxy-index.sh"'
	
docker-network: ## Start Docker Network service
	@echo "Starting $@"
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD)/PrtDockerLocalNetwork && docker-compose up --build"'

redis: ## Start Redis service
	@echo "Starting $@"
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD)/PrtRedisService && docker-compose up --build"'

attribution: ## Start Attribution service
	@echo "Starting $@"
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD)/PrtAttributionService && docker-compose up --build"'

document: ## Start Document service
	@echo "Starting PrtDocumentService"
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD)/PrtDocumentService && docker-compose up --build"'
    
inference: ## Start Inference service
	@echo "Starting $@"
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD) && bash local-env.sh && cd $(PWD)/PrtInferenceService && docker-compose up --build"'

opensearch: ## Start OpenSearch service
	@echo "Starting $@"
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD)/PrtIndexingDomain/IndexingIndexStore/opensearch && docker-compose up --build indexing-opensearch"'

opensearch-dashboards: ## Start OpenSearch Dashboards
	@echo "Starting $@"
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD)/PrtIndexingDomain/IndexingIndexStore/opensearch_dashboards && docker-compose up --build indexing-opensearch-dashboards"'

dask-scheduler: ## Start Dask Scheduler
	@echo "Starting $@"
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD)/PrtIndexingDomain/IndexingIngest/indexing_ingest_workflows && docker-compose up --build dask-scheduler"'

ingest-api: ## Start Indexing Ingest API
	@echo "Starting $@"
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD)/PrtIndexingDomain/IndexingIngest/indexing_ingest_api && docker-compose up --build indexing-ingest-api"'

search-api: ## Start Indexing Search API
	@echo "Starting $@"
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD)/PrtIndexingDomain/IndexingSearch/indexing_search_api && docker-compose up --build indexing-search-api"'

aisearch: ## Start AI Search service
	@echo "Starting $@"
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD)/PrtAISearch && DOCKER_BUILDKIT=1 docker compose build --ssh default && docker compose up"'

