.PHONY: re all build stop up down clean fclean

all: build up
re: down all
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
	docker rmi -f ft_transcendence-oauth2intra ft_transcendence-postgres ft_transcendence-nginx ft_transcendence-backend ft_transcendence-frontend
	docker volume rm ft_transcendence_postgres_data
fclean: clean
	docker system prune -a --force