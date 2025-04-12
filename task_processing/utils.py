import os
import json
from decimal import Decimal


def recursive_add(target: dict, source: dict) -> None:
    """
    Рекурсивно обходит словарь `source` и добавляет значения в `target`.
    Все значения считаются как Decimal, включая count.
    :param target: словарь, в который добавляются значения
    :param source: словарь-источник данных
    """
    for key, value in source.items():
        if isinstance(value, dict):
            if key not in target:
                target[key] = {}
            recursive_add(target[key], value)
        else:
            if key not in target:
                target[key] = Decimal("0")
            target[key] += Decimal(value)


def convert(obj: dict) -> dict | str:
    """
    Рекурсивно преобразует все значения типа Decimal в строки для корректного сохранения в JSON.

    :param obj: вложенный словарь (или значение), содержащий Decimal-объекты
    :return: словарь/значение с Decimal, преобразованными в строки
    """
    if isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return str(obj)
    return obj


def sum_token_price_in_folder(
        folder_path: str,
        output_filename: str

):
    """
    Складывает значения всех JSON-файлов в папке, сохраняя структуру.
    Все значения (включая count) обрабатываются как Decimal.
    Результат сохраняется в указанный JSON-файл.
    :param folder_path: путь к папке с файлами информации по стоимости токенов
    :param output_filename: имя итогового файла
    :return: dict с суммированной информацией
    """
    target = {}
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                path = os.path.join(folder_path, filename)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    recursive_add(target=target, source=data)
        result = convert(target)
        # Сохраняем
        output_path = os.path.join(folder_path, output_filename)
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
    except Exception as exc:
        print(f"❌ Ошибка при подсчёте общей стоимости токенов: {exc}")
        raise


def merge_json_files(
        folder_path: str,
        output_filename: str
) -> None:
    """
    Объединяет все JSON-файлы в указанной папке в один и сохраняет результат в output_filename.
    Повторяющиеся ключи перезаписываются.

    :param folder_path: Путь к папке с JSON-файлами.
    :param output_filename: Имя итогового файла
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
