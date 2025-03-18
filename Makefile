# запуск линтера на ubuntu
lint:
	pylint $(shell git ls-files '*.py')

run_tests:
	pytest -s

class_test:
	pytest -s /home/veronika/00_projects/promps_helper/utils/tests/test_utils.py::TestUtils
one_test:
	pytest -s /home/veronika/00_projects/promps_helper/utils/tests/test_utils.py::TestUtils::test_take_data_from_collection


jsontest:
	pytest -s /home/veronika/00_projects/promps_helper/json_constructor/test/test_json_scheme.py::TestJsonScheme