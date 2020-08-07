up:
	docker-compose up -d
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
