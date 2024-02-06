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
	docker compose down
clean:
	docker compose down -v --remove-orphans
	docker rmi -f django-oauth2-42-oauth2intra
	docker rmi -f postgres:16.1-alpine
	docker rmi -f nginx
fclean: clean
	docker system prune -a --force