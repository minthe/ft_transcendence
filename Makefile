.PHONY: re all build stop up down clean fclean

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
	docker compose down
clean:
	docker compose down
	docker rmi -f ft_transcendence-nginx ft_transcendence-auth_backend ft_transcendence-auth_db ft_transcendence-game_chat_frontend ft_transcendence-game_chat_backend ft_transcendence-game_chat_db
	docker volume rm ft_transcendence_game_chat_db ft_transcendence_auth_db
fclean: clean
	docker system prune -a --force
