from json_constructor.json_creator import JsonCreator
from json_constructor.json_processing_data import JsonProcessingData
# словарь со всеми параметрами для разных категорий продуктов
from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES

def get_json_scheme(
        data_tools: dict,
        data_collection: dict,
) -> dict:
    """
    Функция для получения json-схемы для текущей подборки

    :param data_tools: словарь со всеми данными по средствам
    :param data_collection: словарь с текущей подборкой
    :return: json-схема для текущей подборки
    """

    # Создание экземпляра класса обработчика словаря перед созданием json-схемы
    json_processing = JsonProcessingData(
        data_tools=data_tools,
        data_collection=data_collection,
    )

    # Вызов метода по преобразованию словаря по коду задачи
    update_data_collection = json_processing.distribution_on_task()

    # Создание экземпляра класса по созданию json-схемы
    json_creator = JsonCreator(
        data_collection=update_data_collection,
        product_categories=PARAMETERS_DIF_PRODUCT_CATEGORIES,
    )

    # вызов метода для создания json-схемы
    return json_creator.get_json_scheme_for_distribution_on_task()
