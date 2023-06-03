

setup-local:
	@chmod +x ./bin/*
	@bash ./bin/add-to-path "$$(pwd)/bin"

sync:
	git fetch
	git pull
	make setup-local
