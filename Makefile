.PHONY : build up bootstrap down removevolumes mypy test test managepy precommit testci

build:
	docker build -t shopping-cart-backend \
	--build-arg USER_ID=$(shell id -u) \
	--build-arg GROUP_ID=$(shell id -g) \
	$(arguments) .
up:
	docker-compose up -d $(arguments)
bootstrap: down removevolumes
	docker-compose run --rm backend bootstrap
	make up
down:
	docker-compose down --remove-orphans
removevolumes: down
	-docker volume rm `docker volume ls -f name=shopping-cart -q|grep -v "pycharm"`
mypy:
	docker-compose exec -T backend mypy --config-file ../mypy.ini ./
test:
	docker-compose exec backend python manage.py test $(arguments) --verbosity 3 --parallel
managepy:
	docker-compose exec -T backend python manage.py $(arguments)
precommit:
	pre-commit run --all-files
testci:
	act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 --env-file "no-default-env-file" $(arguments)
