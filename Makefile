# запуск линтера на ubuntu
lint:
	pylint $(filter-out emojipy/%,$(shell git ls-files '*.py'))

run_tests:
	pytest -s

class_test_pdf_all_process:
	pytest -s pdf/tests/test_main.py::TestCreatePdf::test_analysis_composition_one_product

class_test_pdf_processing:
	pytest -s pdf/pdf_data_processing/tasks_logic/tests/test_tasks_logic_process.py::TestTasksDataProcessing

class_test_pdf_creator:
	pytest -s pdf/creator_logic/tests/test_main.py::TestPDFCreator::test_create_pdf

class_test_pdf_converter:
	pytest -s pdf/creator_logic/creator/tests/test_pdf_converter_to_image.py::TestPDFConverterToImage

class_test_dirs_creator:
	pytest -s dirs_structure_constructor/tests/test_main.py::TestDirsConstructor

class_test_pdf_main_utils:
	pytest -s pdf/tests/test_utils.py::TestUtils

class_test_pdf_tasks_utils:
	pytest -s pdf/pdf_data_processing/tests/test_task_utils.py::TestTasksUtils

excel_test:
	pytest -s excel_process_data/utils/test/test_utils.py::TestUtils::test_counting_hash_best_product

jsontest:
	pytest -s json_constructor/test/test_json_scheme.py::TestJsonScheme


prompt_test:
	pytest -s prompt_constructor/test_constructor/test_constructor.py::TestPromptConstructor

proc_test:
	pytest -s prompt_constructor/test_constructor/test_processing_data.py::TestProcessingData::test_decryption_key_best_couple

post_test:
	pytest -s post_constructor/test/test_post.py::TestPostConstructor::test_create_hashtag_2

parser_test:
	pytest -s ga_parser/parser_v2/parser/tests/test_parser_2.py::ParserTestCase::test_get_price_in_stock

veron_test:
	pytest -s excel_process_data/utils/test/test_utils.py::TestUtils
	pytest -s excel_process_data/utils/test/test_utils.py::TestUtils
	pytest -s prompt_constructor/test_constructor/test_processing_data.py::TestProcessingData
	pytest -s json_constructor/test/test_json_scheme.py::TestJsonScheme

