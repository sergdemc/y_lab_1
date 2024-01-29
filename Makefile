
start:
	docker-compose up -d

stop:
	docker-compose down --volumes --remove-orphans

server:
	cd app && python main.py

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev

install:
	pip install -r requirements.txt

test:
	pytest --no-header -vv

test-in-docker:
	docker-compose -f docker-compose.test.yml up --build --exit-code-from web-app-test

isort:
	isort app