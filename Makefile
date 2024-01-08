include .env

.PHONY: re all build stop up down clean fclean

all: build up
re: all
build:
	docker compose build
stop:
	docker compose stop
up:
	docker compose up -d
down:
	docker compose down
clean:
	docker compose down -v --remove-orphans
	docker rmi -f oauth2intra
	docker rmi -f postgres
	docker rmi -f nginx
fclean: clean
	docker system prune -a --force