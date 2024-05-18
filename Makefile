.PHONY: re all build stop up down clean fclean

all: build up
re: fclean all
build:
	chmod +x setup.sh
	bash setup.sh
	docker compose build --no-cache
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
	chmod +x delete_migrations.sh
	bash delete_migrations.sh
	$(eval volumes := $(shell docker volume ls -q --filter name=$(project)*))
	@if [ -n "$(volumes)" ]; then \
		docker volume rm $(volumes); \
	else \
		echo "fclean: no volumes to remove"; \
	fi

perge: 
	docker rm -f $(docker ps -aq) 2>/dev/null || true
	docker rmi -f $(docker images -aq) 2>/dev/null || true
	docker volume rm $(docker volume ls -q) 2>/dev/null || true
	docker network rm $(docker network ls -q) 2>/dev/null || true
	docker network prune -f

