def forming_info_for_pdf_best_product(
        data: dict,
) -> list:
    """
    Функция для формирования списка словарей, которые нужны для наполнения картинки
    для кодов 'Лучшее средство' и 'Лучшее средство без канцерогенов'

    :param data: словарь со всей информацией по средствам для текущей подборки
    :return: список словарей с информацией для вставки в изображение
     [
    {'Название': 'YVES ROCHER Volume Plumping Shampoo Sulfate Free',
    'Плюсы': 'Содержит экстракт киноа и инулин, которые могут укреплять и '
           'увлажнять волосы. Без сульфатов, что делает его мягким для волос.',
    'Минусы': 'Основной акцент на объем, а не на увлажнение, что может быть '
            'недостаточно для сухих волос.',
    'Соотношение': '300''мл'/ 750 руб.,
    'Ссылка на изображение в базе': '00_base/products/00_img/yves_free.jpg',
    'Лучшее средство': False,
    ]
    """

    # создаем список
    list_for_pdf = []

    # формируем список из словарей по средствам, которые надо преобразовать в картинку
    for name_product, info in data.items():
        ratio = (f'{info.get("Количество меры (число)")} '
                 f'{info.get("Юниты меры (мл/шт)")} / {info.get("Стоимость руб")} рублей')

        list_for_pdf.append(
            {
                "Название": name_product,
                "Плюсы": info["plus"],
                "Минусы": info["minus"],
                "Соотношение": ratio,
                "Ссылка на изображение в базе": info.get("Ссылка на изображение в базе"),
                "Лучшее средство": info["best_product"],
            }
        )

    return list_for_pdf


def forming_info_for_pdf_one_product(
        data: dict,
        data_task: dict,
        product_categories: dict,
) -> dict | None:
    """
    Функция для формирования списка словарей, которые
    нужны для наполнения картинки для кода 'Разбор состава одного средства'

    :param data: словарь со средством, его плюсами, минусами и другими параметрами
    :param data_task: словарь с кодом задачи, количеством средств, категорией продукта
    :param product_categories: словарь со всеми параметрами для разных категорий продуктов

    :return: словарь с ключами для отображения для на pdf для одного средства
    """
    for name_product, info in data.items():
        # Получаем категорию из задачи
        category = data_task.get("Категория", "")

        # Берём базовые свойства
        base_params = product_categories.get("Базовые настройки", {})

        # Берём параметры для категории (если есть)
        category_params = product_categories.get(category, {})

        # Маппинг полей (eng -> rus)
        field_titles = product_categories.get("Маппинг", {})

        # Объединяем базу и категорию
        merged_params = {**base_params, **category_params}

        # Базовые данные, которые идут всегда
        pdf_data = {
            "Название": name_product,
            "Соотношение": (
                f'{info.get("Количество меры (число)", "")} '
                f'{info.get("Юниты меры (мл/шт)", "")} / {info.get("Стоимость руб", "")} рублей'
            ),
            "Ссылка на изображение в базе": info.get("Ссылка на изображение в базе", ""),
        }

        # Заполняем поля из параметров по маппингу
        for field_key in merged_params:
            title = field_titles.get(field_key, field_key)  # Русское название или ключ
            pdf_data[title] = info.get(field_key, "")

        # Так как обрабатываем одного продукта, сразу возвращаем
        return pdf_data


def main_forming_info_for_pdf(
        data: dict,
        data_task: dict,
        product_categories: dict,
) -> list:
    """
    Главная функция, которая определяет какая схема построения pdf-файла
    будет формироваться для текущей подборки

    :param data: словарь со средствами, их плюсами, минусами и прочим
    :param data_task: словарь с кодом задачи, количеством средств, категорией продукта
    :param product_categories: словарь со всеми параметрами для разных категорий продуктов

    :return: список словарей с информацией для вставки в изображение
    """

    forming = {
        'Лучшее средство': forming_info_for_pdf_best_product,
        'Лучшее средство без канцерогенов': forming_info_for_pdf_best_product,
        'Разбор состава одного средства': forming_info_for_pdf_one_product,
    }

    task = data_task["Задача"]

    if task == 'Разбор состава одного средства':
        result = forming_info_for_pdf_one_product(
            data=data,
            data_task=data_task,
            product_categories=product_categories,
        )
    else:
        result = forming[task](data)

    return result
