start_db:
	docker-compose up -d

stop_db:
	docker-compose down

server:
	cd app && python main.py

start:
	make start_db
	make server

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev

install:
	pip install -r requirements.txt

isort:
	isort app