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
	docker rmi -f ft_transcendence-oauth2intra ft_transcendence-postgres ft_transcendence-nginx
	docker volume rm oauth2intra postgres nginx
fclean: clean
	docker system prune -a --force