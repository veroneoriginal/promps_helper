# запуск линтера на ubuntu
lint:
	pylint $(shell git ls-files '*.py')

run_tests:
	pytest -s

class_test_pdf_all_process:
	pytest -s pdf/tests/test_main.py::TestCreatePdf

class_test_pdf_processing:
	pytest -s pdf/pdf_data_processing/tasks_logic/best_product/tests/test_best_product.py::TestBestProduct

class_test_pdf_creator:
	pytest -s pdf/creator_logic/tests/test_main.py::TestPDFCreator

class_test_pdf_converter:
	pytest -s pdf/creator_logic/creator/tests/test_pdf_converter_to_image.py::TestPDFConverterToImage

class_test_dirs_creator:
	pytest -s dirs_structure_constructor/tests/test_main.py::TestDirsConstructor

class_test_pdf_main_utils:
	pytest -s pdf/tests/test_utils.py::TestUtils


one_test:
	pytest -s /home/veronika/00_projects/promps_helper/utils/tests/test_utils.py::TestUtils

jsontest:
	pytest -s /home/veronika/00_projects/promps_helper/json_constructor/test/test_json_scheme.py::TestJsonScheme


prompt_test:
	pytest -s /home/veronika/00_projects/promps_helper/prompt_constructor/test_constructor/test_constructor.py::TestPromptConstructor