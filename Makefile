

setup:
	@chmod +x ./bin/*
	@bash ./bin/add-to-path "$$(pwd)/bin"
	@bash ./bin/update-profile USEFUL_SCRIPT_BIN "$$(pwd)/bin"
	@for FILE in "$$(pwd)/completions/*"; do \
		./bin/update-profile --source $$FILE; \
	done
	@for FILE in ./aliases/*; do \
		filename=$$(basename "$$FILE"); \
		contents=$$(cat "$$FILE"); \
		update-profile --alias "$$filename" "$$contents"; \
	done
	@mkdir -p servers


sync:
	git fetch
	git pull
	make setup-local
