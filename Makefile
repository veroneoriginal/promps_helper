# запуск нового приложения
run:
	python manage.py runserver 8080

# создание нового приложения
create_new_app:
	python manage.py startapp example_app

# запуск линтера
lint:
	pylint $(shell git ls-files '*.py')

# Создаёт файлы миграций на основе изменений моделей
migrations:
	python manage.py makemigrations

# Применяет миграции к базе данных
migrate:
	python manage.py migrate

test_openai:
	python manage.py test content_gen_app.test.test_main_manage_class
	python manage.py test content_gen_app.openai.test.test_main_openai
	python manage.py test content_gen_app.openai.limiter.test.test_limiter
	python manage.py test content_gen_app.openai.utils.test.test_utils
	python manage.py test content_gen_app.openai.tokenizer.test.test_tokenizer
	python manage.py test content_gen_app.openai.limiter.test.test_utils
	python manage.py test content_gen_app.openai.key_manager.test.test_key_manager
	python manage.py test api_v1.users.tests.test_views
	python manage.py test api_v1.users.tests.test_serializers
	python manage.py test user_app.test.test_model
	python manage.py test user_app.services.test.test_user_registration
	python manage.py test notifications_app.test.test_send_notification

coverage:
	coverage run --source='.' manage.py test
	coverage report --omit=settings/asgi.py,settings/wsgi.py,manage.py
	coverage html -d coverage_html_report --omit=settings/asgi.py,settings/wsgi.py,manage.py

before_pool:
	make lint
	make test_openai
	make coverage
