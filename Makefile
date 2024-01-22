db:
	docker-compose up -d

stop_db:
	docker-compose down

start:
	cd app && python main.py