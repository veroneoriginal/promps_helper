# запуск линтера на ubuntu
lint:
	pylint $(shell git ls-files '*.py')

run_test:
	pytest -s