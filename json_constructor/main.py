# from pprint import pprint

from json_constructor.json_creator import JsonCreator
from json_constructor.json_processing_data import JsonProcessingData


def get_json_scheme(
        data_collection: dict,
        product_categories: dict,
) -> dict:
    """
    Функция для получения json-схемы для текущей подборки

    :param data_collection: словарь с текущей подборкой
    :param product_categories: словарь со всеми параметрами для разных категорий продуктов
    :return: json-схема для текущей подборки
    """

    # Создание экземпляра класса обработчика словаря перед созданием json-схемы
    json_processing = JsonProcessingData(
        data_collection=data_collection,
    )

    # Вызов метода по преобразованию словаря по коду задачи
    update_data_collection = json_processing.distribution_on_task()


    # pprint(data_collection)
    # print()

    # Создание экземпляра класса по созданию json-схемы
    json_creator = JsonCreator(
        data_collection=update_data_collection,
        product_categories=product_categories,
    )

    # вызов метода для создания json-схемы
    return json_creator.get_json_scheme_for_distribution_on_task()
