.PHONY: re all build stop up down clean fclean env

all: build up
re: clean all
build:
	chmod +x setup.sh
	bash setup.sh
	docker compose build 
stop:
	docker compose stop
up:
	docker compose up -d
down:
	docker compose down --remove-orphans

clean: down
	$(eval images := $(shell docker image ls -q --filter=reference='ft_transcendence*'))
	@if [ -n "$(images)" ]; then \
		docker rmi -f $(images); \
	else \
		echo "clean: no images to remove"; \
	fi
fclean: clean
	chmod +x delete_migrations.sh
	bash delete_migrations.sh
	$(eval volumes := $(shell docker volume ls -q --filter name='ft_transcendence*'))
	@if [ -n "$(volumes)" ]; then \
		docker volume rm $(volumes); \
	else \
		echo "fclean: no volumes to remove"; \
	fi
env:
	chmod +x setup_env.sh
	bash setup_env.sh

rebuild modsec:
	docker-compose up --build  --no-deps -d modsecurity