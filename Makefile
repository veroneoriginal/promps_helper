# запуск линтера на ubuntu
lint:
	pylint $(shell git ls-files '*.py')

run_test:
	pytest -s

one_test:
	pytest -s /home/veronika/00_projects/promps_helper/utils/tests/test_utils.py::TestUtils