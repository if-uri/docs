.PHONY: site deploy help
help:
	@grep -E "^[a-zA-Z_-]+:.*?## .*$$" $(MAKEFILE_LIST) | awk "BEGIN{FS=\":.*?## \"}{printf \"  %-10s %s\\n\",\$$1,\$$2}"
site: ## Build docs _site/
	python3 scripts/build_site.py _site
deploy: ## Publish to docs.ifuri.com (Plesk)
	bash scripts/deploy-plesk.sh
