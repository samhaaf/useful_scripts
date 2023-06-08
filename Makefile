

setup:
	@chmod +x ./commands/*
	@bash ./commands/add-to-path "$$(pwd)/commands"
	@bash ./commands/add-to-profile USEFUL_SCRIPTS_DIR "$$(pwd)"
	@# Add all completions to the profile
	@for FILE in "$$(pwd)/completions/*"; do \
		./commands/add-to-profile --source $$FILE; \
	done
	@# Add all aliases to the profile
	@for FILE in ./aliases/*; do \
		filename=$$(basename "$$FILE"); \
		contents=$$(cat "$$FILE"); \
		./commands/add-to-profile --alias "$$filename" "$$contents"; \
	done
	@mkdir -p servers


sync:
	git fetch
	git pull
	make setup-local
