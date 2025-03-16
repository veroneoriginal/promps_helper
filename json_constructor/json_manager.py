from json_constructor.json_creator import JsonCreator
from json_constructor.json_processing_data import JsonProcessingData


def get_json_scheme(
        data_collection: dict,
) -> dict:
    """
    Функция для получения json-схемы для текущей подборки

    :param data_collection: словарь с текущей подборкой
    :return: json-схема для текущей подборки
    """

    json_processing = JsonProcessingData(
        data_collection=data_collection,
    )
    # Вызов метода расшифровки словаря по коду задачи
    deciphered_dict = json_processing.distribution_on_task()

    json_creator = JsonCreator(data_collection=deciphered_dict)
    # вызов методадля создания json-схемы
    return json_creator.get_json_scheme_for_distribution_on_task()


