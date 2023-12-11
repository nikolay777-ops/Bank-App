DOCKER_COMPOSE_FILE = docker-compose.dev.yml
PROJECT_DIR = /opt/bank_app/

dbshell:
	docker exec -it bank_app_web ./manage.py dbshell

shell:
	docker exec -it bank_app_web ./manage.py shell

pytest:
	docker exec -i -w ${PROJECT_DIR} bank_app_web pytest --reuse-db src

pytest-cov:
	docker exec -i -w ${PROJECT_DIR} bank_app_web_test pytest --cov-config=.coveragerc --cov=src --reuse-db src
	docker exec -i -w ${PROJECT_DIR} bank_app_web_test coverage html

pylint:
	docker exec -i -w ${PROJECT_DIR} bank_app_web_test pylint ./src --errors-only --django-settings-module=src.settings

migrations:
	docker exec bank_app_web ./manage.py makemigrations

migrate:
	docker exec bank_app_web ./manage.py migrate --noinput

build:
	docker compose -f ${DOCKER_COMPOSE_FILE} build

up:
	docker compose -f ${DOCKER_COMPOSE_FILE} up -d

log:
	docker compose -f ${DOCKER_COMPOSE_FILE} logs -f --tail 100

stop:
	docker compose -f ${DOCKER_COMPOSE_FILE} stop

down:
	docker compose -f ${DOCKER_COMPOSE_FILE} down

load_all_fixtures:
	docker exec bank_web ./manage.py loaddata currencies currency_rate_views
