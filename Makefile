

setup:
	@chmod +x ./bin/*
	@bash ./bin/add-to-path "$$(pwd)/bin"
	@for FILE in "$$(pwd)/completions/*"; do \
		./bin/update-profile --source $$FILE; \
	done


sync:
	git fetch
	git pull
	make setup-local
