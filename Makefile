.PHONY: help up down logs ps restart clean build test

help:
	@echo "Data Platform - Available Commands"
	@echo "===================================="
	@echo ""
	@echo "make up              - Start all services"
	@echo "make down            - Stop all services"
	@echo "make restart         - Restart all services"
	@echo "make logs            - View logs from all services"
	@echo "make logs-airflow    - View Airflow logs"
	@echo "make logs-postgres   - View PostgreSQL logs"
	@echo "make logs-grafana    - View Grafana logs"
	@echo "make ps              - Show running containers"
	@echo "make clean           - Stop and remove all containers"
	@echo "make build           - Build Docker images"
	@echo "make shell-postgres  - Open PostgreSQL shell"
	@echo "make shell-airflow   - Open Airflow shell"
	@echo "make load-data       - Load sample data"
	@echo "make backup          - Backup PostgreSQL database"
	@echo "make restore         - Restore PostgreSQL database"
	@echo "make test            - Run tests"
	@echo ""

up:
	docker-compose up -d
	@echo "Services started. Waiting for initialization..."
	@sleep 10
	@echo "Access the services at:"
	@echo "  Airflow:  http://localhost:8080"
	@echo "  Grafana:  http://localhost:3000"
	@echo "  Jupyter:  http://localhost:8888"
	@echo "  Adminer:  http://localhost:8081"
	@echo "  MinIO:    http://localhost:9001"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-airflow:
	docker-compose logs -f airflow-webserver

logs-postgres:
	docker-compose logs -f postgres

logs-grafana:
	docker-compose logs -f grafana

ps:
	docker-compose ps

clean:
	docker-compose down -v
	@echo "All containers and volumes removed"

build:
	docker-compose build

shell-postgres:
	docker-compose exec postgres psql -U datauser -d datawarehouse

shell-airflow:
	docker-compose exec airflow-webserver bash

load-data:
	docker-compose exec postgres python /scripts/load_sample_data.py

backup:
	@mkdir -p backups
	docker-compose exec postgres pg_dump -U datauser datawarehouse > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backup created successfully"

restore:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make restore FILE=backups/backup_YYYYMMDD_HHMMSS.sql"; \
	else \
		docker-compose exec -T postgres psql -U datauser datawarehouse < $(FILE); \
		echo "Restore completed"; \
	fi

test:
	@echo "Running tests..."
	docker-compose exec postgres psql -U datauser -d datawarehouse -c "SELECT COUNT(*) FROM raw_data.customers;"
	@echo "Test completed"

status:
	@echo "Checking service status..."
	@docker-compose exec postgres pg_isready -U datauser && echo "✓ PostgreSQL is ready" || echo "✗ PostgreSQL is not ready"
	@curl -s http://localhost:8080 > /dev/null && echo "✓ Airflow is ready" || echo "✗ Airflow is not ready"
	@curl -s http://localhost:3000 > /dev/null && echo "✓ Grafana is ready" || echo "✗ Grafana is not ready"
	@curl -s http://localhost:8888 > /dev/null && echo "✓ Jupyter is ready" || echo "✗ Jupyter is not ready"

stats:
	docker stats

prune:
	docker system prune -f
	@echo "Docker system pruned"
