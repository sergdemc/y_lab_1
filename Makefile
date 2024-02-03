
start:
	docker-compose up -d --build --remove-orphans

stop:
	docker-compose down --volumes --remove-orphans

db:
	docker run --rm -d -p 5432:5432 -e POSTGRES_USER=dbuser -e POSTGRES_PASSWORD=dbpassword -e POSTGRES_DB=dbname postgres:15.1-alpine

server:
	cd app && python main.py

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev

install:
	pip install -r requirements.txt

test:
	pytest --no-header -vv

test-in-docker:
	docker-compose -f docker-compose.test.yml up --build --exit-code-from web-app-test --remove-orphans

isort:
	isort app