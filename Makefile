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
	docker compose down
	docker rmi -f django-oauth2-42-oauth2intra postgres:16.1-alpine nginx
	docker volume rm django-oauth2-42_oauth2intra django-oauth2-42_postgres_data django-oauth2-42_nginx
fclean: clean
	docker system prune -a --force