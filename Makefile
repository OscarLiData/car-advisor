build:
	docker compose build

run:
	docker compose run --rm app

up:
	docker compose up

down:
	docker compose down

test:
	docker compose run --rm app pytest -vv tests

clean:
	docker system prune -f
