import os
import json


def merge_json_files(
        folder_path: str,
        output_filename: str
) -> None:
    """
    Объединяет все JSON-файлы в указанной папке в один и сохраняет результат в output_filename.
    Повторяющиеся ключи перезаписываются.

    :param folder_path: Путь к папке с JSON-файлами.
    :param output_filename: Имя итогового файла (по умолчанию "merged_result.json").
    """
    merged_data = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    merged_data.update(data)
            except json.JSONDecodeError as e:
                print(f"Ошибка при чтении {filename}: {e}")

    output_path = os.path.join(folder_path, output_filename)
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(merged_data, file, ensure_ascii=False, indent=4)


def get_list_composition_elements(
        data_tools: dict,
        collection_data: dict,
) -> list:
    """
    Возвращает списко элементов состава средства
    """
    # Получаем ('EAU THERMALE AVENE SUN', '19000077114')
    product_title_article = collection_data['Средства']['Средство_1']
    product_title_lower = product_title_article[0].lower()
    product_article = product_title_article[1]

    list_composition_elements = (
        data_tools['Средства'][product_title_lower][product_article]['Список элементов состава']
    )
    list_composition_elements.sort()
    numbered_composition_elements_list = [
        element.strip(' .') for element in list_composition_elements
    ]

    return numbered_composition_elements_list
