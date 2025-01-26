# запуск линтера

lint:
	pylint $(shell git ls-files '*.py')
