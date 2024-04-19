.PHONY: re all build stop up down clean fclean

all: build up
re: clean all
build:
	docker compose build
stop:
	docker compose stop
up:
	docker compose up -d
down:
	docker compose down --remove-orphans

clean: down
	$(eval project := $(notdir $(shell pwd)))
	$(eval images := $(shell docker image ls -q --filter=reference="$(project)*"))
	@if [ -n "$(images)" ]; then \
		docker rmi -f $(images); \
	else \
		echo "clean: no images to remove"; \
	fi
fclean: clean
	$(eval volumes := $(shell docker volume ls -q --filter name=$(project)*))
	@if [ -n "$(volumes)" ]; then \
		docker volume rm $(volumes); \
	else \
		echo "fclean: no volumes to remove"; \
	fi