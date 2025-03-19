# pylint: skip-file

"""В этом модуле тестируем всю логику работы приложения"""

import unittest
from pprint import pprint

from control_manager.control_manager import ControlManager

# словарь с данными для формирования путей для сохранения данных
from source.structure_folders import scheme_for_folders_name

# словарь со всеми параметрами для разных категорий продуктов
from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES

file_path_tools = '00_base/Средства.xlsx'
file_path_collection = '00_base/Подборки для тестов.xlsx'
path_to_output_folder = '00_base/00_info_for_post/'


class TestUtils(unittest.TestCase):
    """Класс для тестирования всей логики работы приложения"""

    def setUp(self):
        self.control_manager = ControlManager(
            scheme_for_folders=scheme_for_folders_name,
            param_dif_products_categories=PARAMETERS_DIF_PRODUCT_CATEGORIES
        )

        self.data_tools = self.control_manager._take_data_from_table_tool(
            file_path_tools_table=file_path_tools,
        )

    # def test__take_data_from_table_tool(self):
    #     """
    #     Расшифровка данных из словаря текущей подборки
    #     """
    #     data_tools = self.control_manager._take_data_from_table_tool(
    #         file_path_tools_table=file_path_tools,
    #     )
    #     pprint(data_tools)

    def test_get_count_collections(self):
        """
        Подсчет количества незаполненных подборок в таблице.
        """

        result = self.control_manager._get_count_collections(file_path_collection)
        self.assertEqual(2, result)

    def test_take_data_from_collection(self):
        """
        Формирование словаря с подборкой
        """

        result = self.control_manager._take_data_from_collection(
            file_path_collection=file_path_collection,
            checking_unique=False,
        )

        # pprint(result)

        if result['Задача'] == 'Лучшее средство':
            # Если код "Лучшее средство", то ожидаемый словарь имеет вид
            expected_result = {
                'Возраст': 32,
                'Задача': 'Лучшее средство',
                'Запрос': 'ЗВ8, ЗВ12',
                'Итог': None,
                'Лучший вариант': None,
                'Пол': 'женский',
                'Категория': 'шампуни',
                'Специалист': 'Т',
                'Средства': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
                             'Средство_2': 'OUSHEN Curl & shine shampoo',
                             'Средство_3': 'NATURA SIBERICA Oblepikha',
                             'Средство_4': 'WELEDA Millet Nourishing',
                             'Средство_5': 'PAYOT Shampoing doux biome-friendly',
                             'Средство_6': 'LADOR Keratin LPP'},
                'Тип': 'В1, В10',
                'Хеш': '68dd4868b0ba1a96e83295d05327e97af4f2748a34fb45281023729d8532c326'}

            # Проверка, что результат равен ожидаемому
            self.assertEqual(result, expected_result)

        elif result['Задача'] == 'Разбор состава одного средства':
            expected_result = {
                'Возраст': 32,
                'Задача': 'Разбор состава одного средства',
                'Запрос': 'ЗЛ2',
                'Итог': None,
                'Категория': 'уход за кожей лица',
                'Лучший вариант': None,
                'Пол': 'женский',
                'Специалист': 'Т',
                'Средства': {'Средство_1': 'PULANNA Bio-gold & Grape'},
                'Тип': 'КЛ1, КЛ2',
                'Хеш': '5be8b5391782b170c129765d1b7500816e2309aa682d468f368ffb8cfaa02d40',
            }

            # Проверка, что результат равен ожидаемому
            self.assertEqual(result, expected_result)

    def test_get_output_folders(self):
        """
        Формирование путей для сохранения данных
        """

        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучшее средство',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Категория': 'шампуни',
            'Специалист': 'Т',
            'Средства': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
                         'Средство_2': 'OUSHEN Curl & shine shampoo',
                         'Средство_3': 'NATURA SIBERICA Oblepikha',
                         'Средство_4': 'WELEDA Millet Nourishing',
                         'Средство_5': 'PAYOT Shampoing doux biome-friendly',
                         'Средство_6': 'LADOR Keratin LPP'},
            'Тип': 'В1, В10',
            'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1'}

        self.control_manager._get_output_folders(
            path_to_output_folder=path_to_output_folder,
            category=data_collection['Категория'],
        )
        folders = self.control_manager.paths_to_folders

        expected_keys = [
            'answer_gpt',
            'instagram_jpg',
            'instagram_text',
            'pinterest_jpg',
            'prompt',
            'telegram_jpg',
            'telegram_pdf',
            'telegram_text'
        ]

        self.assertCountEqual(folders.keys(), expected_keys)

        # получатся пути такого плана
        # {'answer_gpt': '00_base/00_info_for_post/17_03_25/3_шампуни/answer_gpt',
        #  'instagram_jpg': '00_base/00_info_for_post/17_03_25/3_шампуни/instagram/jpg',
        #  'instagram_text': '00_base/00_info_for_post/17_03_25/3_шампуни/instagram/text',
        #  'pinterest_jpg': '00_base/00_info_for_post/17_03_25/3_шампуни/pinterest/jpg',
        #  'prompt': '00_base/00_info_for_post/17_03_25/3_шампуни/prompt',
        #  'telegram_jpg': '00_base/00_info_for_post/17_03_25/3_шампуни/telegram/jpg',
        #  'telegram_pdf': '00_base/00_info_for_post/17_03_25/3_шампуни/telegram/pdf',
        #  'telegram_text': '00_base/00_info_for_post/17_03_25/3_шампуни/telegram/text'}

    def test_bring_prompt(self):

        data_tools = self.control_manager._take_data_from_table_tool(
            file_path_tools_table=file_path_tools,
        )

        data_collection = self.control_manager._take_data_from_collection(
            file_path_collection=file_path_collection,
            checking_unique=False,
        )

        # cобираю промпт
        prompt = self.control_manager._bring_prompt(
            data_tools=data_tools,
            data_collection=data_collection,
        )

        expected_data = {
            'prompt': '\n'
                      'Подборка осуществляется для человека, который имеет женский пол,\n'
                      'возраст: 32 года/лет.\n'
                      'Так же у человека следующие параметры: Тип кожи лица: Нормальная. '
                      'Сбалансированная, гладкая, без излишней сухости или жирности. Поры '
                      'малозаметны, цвет лица ровный. Минимальные проблемы, хорошая '
                      'упругость и эластичность. Тип кожи лица: Сухая. Недостаток влаги '
                      'и/или липидов. Может быть стянутость, шелушение, тусклый цвет '
                      'лица. Тонкая, чувствительная, склонна к раннему появлению '
                      'морщин..\n'
                      'С помощью этого средства человек хочет решить следующую проблему:\n'
                      'Кожа лица: Глубокое увлажнение и питание. Кожа лица стала '
                      'обезвоженной и тусклой из-за воздействия внешних факторов (ветер, '
                      'солнце, мороз), требует интенсивного увлажнения и питания..\n'
                      '\n'
                      'Информация о средстве и его составе: Средство №1 - PULANNA '
                      'Bio-gold & Grape. Состав: Основные действующие компоненты: '
                      'экстракт листьев винограда, гриба рейши, корня женьшеня, витамин '
                      'Е, диоксид титана, мика, био-золото, гиалуроновая кислота. Полный '
                      'состав: aqua, glycerin, gold, sodium hyalurone, propylene glycol, '
                      'vitis vinifera leaf extract, ganoderma lucidum stem extract, '
                      'ginseng (panax ginseng) root extract, tocopheryl acetate, mica, '
                      'titanium dioxide carbomer, triethanolamine, methylparaben, '
                      'propylparaben, parfum, hydroxycitronellal, geraniol, butylphenyl '
                      'metylpropional, linalool, citronellol, imidazolidynyl urea.. Тип '
                      'продукта: крем для лица. .\n'
                      '\n'
                      'Учти всю вышепредставленную информацию и проведи детальный анализ '
                      'состава.\n'
                      '\n'
                      'Ответ ты должен дать в следующем виде: Разбираешь состав одного '
                      'средства, особенно уделяя внимание следующим пунктам: основные '
                      'компоненты, активные компоненты, Увлажняющие и ухаживающие '
                      'компоненты, Консерванты и регуляторы pH, Запрещенные или '
                      'нежелательные компоненты, Дополнительные свойства, Текстура, Плюсы '
                      'средства, Минусы средства, Вывод',
            'system_prompt': 'Ты профессиональный трихолог с медицинским образованием. '
                             'Твоя задача подобрать максимально подходящее средство для '
                             'человека. Данные человека будут даны.'}

        self.assertEqual(prompt, expected_data)
