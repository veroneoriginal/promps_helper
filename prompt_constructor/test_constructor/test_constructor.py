# pylint: skip-file
"""В этом модуле тестируем выбор промпта"""

import unittest
from prompt_constructor.prompt_constructor import PromptConstructor
from control_manager.control_manager import ControlManager

# словарь с данными для формирования путей для сохранения данных
from source.structure_folders import scheme_for_folders_name

# словарь со всеми параметрами для разных категорий продуктов
from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES

file_path_tools = '00_base/Средства.xlsx'
file_path_collection = '00_base/Подборки для тестов.xlsx'
path_to_output_folder = '00_base/00_info_for_post/'


class TestPromptConstructor(unittest.TestCase):
    """
    Тесты на main_constructor_prompt у PromptConstructor
    """

    def setUp(self):
        """
        Готовим объект PromptConstructor перед каждым тестом
        """

        self.prompt_constructor = PromptConstructor()

        self.control_manager = ControlManager(
            scheme_for_folders=scheme_for_folders_name,
            param_dif_products_categories=PARAMETERS_DIF_PRODUCT_CATEGORIES
        )

        self.data_tools = self.control_manager._take_data_from_table_tool(
            file_path_tools_table=file_path_tools,
        )

    def test_main_constructor_prompt_best_product(self):
        """
        Тест задачи 'Лучшее средство'
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
            'Хеш': '68dd4868b0ba1a96e83295d05327e97af4f2748a34fb45281023729d8532c326'}

        data_collection_for_best_product = {
            'Возраст': 32,
            'Задача': 'Создаешь рейтинг средств по приоритету от наиболее подходящего до '
                      'наименее подходящего по твоему мнению. При составлении этого '
                      'рейтинга лучшим средством считай то, в составе которого содержится '
                      'минимальное количество вредных веществ и которое наиболее подходит '
                      'под запрос пользователя. В "Итоговой рекомендации" укажи только '
                      'одно лучшее средство и развернутое пояснение почему.',
            'Запрос': 'Волосы: Увлажнение и питание. Необходимо восстановить водный '
                      'баланс волос и насытить их полезными веществами, так как '
                      'недостаток влаги делает волосы сухими, ломкими и тусклыми. Важно '
                      'обеспечить глубокое питание по всей длине, укрепить структуру и '
                      'защитить волосы от внешних воздействий, чтобы они оставались '
                      'мягкими, гладкими и здоровыми. Волосы: Для частого мытья. '
                      'Необходимо мягкое и бережное очищение волос и кожи головы, так как '
                      'частое мытье может привести к пересушиванию, потере естественного '
                      'баланса и защитного слоя. Важно подобрать средство с деликатной '
                      'формулой, которое будет поддерживать свежесть волос, увлажнять и '
                      'укреплять их, не утяжеляя и не пересушивая.',
            'Итог': None,
            'Категория': 'шампуни',
            'Количество средств': 6,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Специалист': 'Ты профессиональный трихолог с медицинским образованием. Твоя '
                          'задача подобрать максимально подходящее средство для человека. '
                          'Данные человека будут даны.',
            'Средства': 'Средство №1 - ALTEREGO ITALY Curego Hydraday. Состав: Aqua '
                        '(Water), Ammonium Lauryl Sulfate, Cocamidopropyl Betaine, '
                        'Erythritol, Lactic Acid, Polysorbate 20, Parfum (Fragrance), '
                        'Sodium Benzoate, Sodium Gluconate, Sodium Hydroxide, '
                        'Propanediol, Guar Hydroxypropyltrimonium Chloride, Hexyl '
                        'Cinnamal, Citric Acid, Geraniol, Linalool, Hydroxycitronellal, '
                        'Tartaric Acid, Oryza Sativa (Rice) Extract, Gluconic Acid, '
                        'Saccharomyces Ferment Lysate Filtrate, Sodium Chloride, '
                        'Potassium Sorbate, Vitis Vinifera Seed Oil (Vitis Vinifera '
                        '(Grape) Seed Oil), Glycerin, Sorbitol, Lecithin, Xanthan Gum.. '
                        'Тип продукта: шампунь. \n'
                        'Средство №2 - OUSHEN Curl & shine shampoo. Состав: Aqua(water, '
                        'eau), sodium c14-16 olefin sulfonate, cocamidopropyl betaine, '
                        'sodium chloride, cocamide methyl mea, dimethicone, glycol '
                        'distearate, benzyl alcohol, parfum, sodium benzoate, '
                        'phenoxyethanol, glycerin, polyquaternium-7, guar '
                        'hydroxypropyltrimonium chloride, disodium edta, sodium methyl '
                        'cocoyl taurate, hydrogenated castor oil, lauric acid, citric '
                        'acid, trideceth-10, trideceth-3, simmondsia chinensis (jojoba) '
                        'seed oil, butyrospermum parkii (shea) butter, hydrolyzed '
                        'keratin, polyquaternium-11, ethylhexylglycerin, butylene glycol, '
                        'tocopherol.. Тип продукта: шампунь. \n'
                        'Средство №3 - NATURA SIBERICA Oblepikha. Состав: Aqua with '
                        'infusions of Novosieversia Glacialis ExtractWH (экстракт розы '
                        'арктической), Angelica Archangelica Root ExtractWH (экстракт '
                        'ангелики лекарственной), Rubus Chamaemorus Seed ExtractWH '
                        '(экстракт морошки сахалинской), Rosa Davurica Leaf ExtractWH '
                        '(экстракт шиповника даурского), Aralia Mandshurica Root Extract* '
                        '(экстракт аралии маньчжурской), Rosa Davurica Flower Water* '
                        '(гидролат розы даурской), Rhodiola Rosea Root Extract* (экстракт '
                        'родиолы розовой), Hippophae Rhamnoidesamidopropyl BetaineHR, '
                        'Pineamidopropyl BetainePS; Sodium Coco-Sulfate, Lauryl '
                        'Glucoside, Cocamidopropyl Betaine, Coco-Glucoside, Panthenol, '
                        'Guar Hydroxypropyltrimonium Chloride, Glycol Distearate, '
                        'Glyceryl Oleate, Sodium Chloride, Hydrolyzed Vegetable Protein '
                        '(растительный кератин), Argania Spinosa Kernel Oil* '
                        '(марокканское масло арганы), Hippophae Rhamnoides Fruit Oil* '
                        '(масло алтайской облепихи), Vaccinium Macrocarpon Seed Oil* '
                        '(масло семян клюквы), Hydrolyzed Wheat Protein (протеины '
                        'пшеницы), Lactic Acid (молочная кислота), Glycolic Acid '
                        '(гликолевая кислота), Benzyl Alcohol, Benzoic Acid, Sorbic Acid, '
                        'Glycerin, Citric Acid, Parfum. (*) – органические ингредиенты '
                        '(WH) – органические экстракты дикорастущих растений Сибири (PS) '
                        '– производное масла сибирского кедра (HR) – производное масла '
                        'алтайской облепихи. Тип продукта: шампунь. \n'
                        'Средство №4 - WELEDA Millet Nourishing. Состав: Вода '
                        'Двунатриевый кокоил глутамат Двунатриевый кокогликозид цитрат '
                        'Аминокислоты овса Спирт Глицерин Ксантан, или ксантановая камедь '
                        'Аромат Глицерил каприлат Пироглутамат натрия Экстракт семян '
                        'проса Масло ореха макадамии Экстракт шалфея Лактоза, или '
                        'молочный сахар Натрия кокоил глутамат Сахарозы лаурат Глицерил '
                        'олеат Аргинин Фитат натрия Лимонен*1 Линалоол*1 Цитраль* '
                        'Кумарин* 1 из концентрата натуральных масел.. Тип продукта: '
                        'шампунь. \n'
                        'Средство №5 - PAYOT Shampoing doux biome-friendly. Состав: Aqua '
                        '(Water), Sodium Lauroyl Methyl Isethionate, Lauryl Glucoside, '
                        'Cocamidopropyl Betaine, Sodium Methyl Cocoyl Taurate, Parfum '
                        '(Fragrance), Pogostemon Cablin Leaf/Stem Extract, Salvia '
                        'Officinalis Leaf Extract, Glycerin, Alpha-Glucan '
                        'Oligosaccharide, Coco-Glucoside, Glyceryl Oleate, Tocopherol, '
                        'Hydrogenated Palm Glycerides Citrate, Citric Acid, '
                        'Polyquaternium-10, Phenethyl Alcohol, Chlorphenesin, Sodium '
                        'Benzoate, Potassium Sorbate.. Тип продукта: шампунь. \n'
                        'Средство №6 - LADOR Keratin LPP. Состав: Water,Cocamidopropyl '
                        'Betaine,Disodium Laureth Sulfosuccinate,Lauramine '
                        'Oxide,Glycerin,Butylene Glycol,TEA Cocoyl Glutamate,Cocamide DEA '
                        ',PEG-120 Methyl Glucose Dioleate,PPG-3 Caprylyl Ether,PEG-7 '
                        'Glyceryl cocoate,Betaine,Hydroxypropyl Chitosan '
                        'Liquid,Trehalose,Hydrolyzed wheat protein,Hydrolyzed '
                        'Keratin,Hydrolyzed silk,Sodium Hyaluronate,Moringa Oleifera Seed '
                        'Oil,Hydrolyzed Zein,Argania Spinosa Kernel Oil,Persea Gratissima '
                        '(Avocado) Oil,Ricinus Communis (Castor) Seed Oil,Camellia '
                        'Japonica Seed Oil,Simmondsia Chinensis (Jojoba) Seed '
                        'Oil,Eucalyptus Globulus Leaf Oil,Lavandula Angustifolia '
                        '(Lavender) Oil,Adansonia Digitata Seed Oil,Orbignya '
                        'Oleifera(Babassu) Seed Oil,Caprylohydroxamic Acid,Caprylyl '
                        'Glycol,Citric Acid,Polyquaternium-10,PVP,Perfume. Тип продукта: '
                        'шампунь. ',
            'Тип': 'Тип волос: Нормальные. Волосы не слишком жирные, не слишком сухие. '
                   'Хорошо держат форму и имеют естественный блеск. Тип волос: Сухие. '
                   'Волосы Могут выглядеть тусклыми и ломкими. Часто спутываются и теряют '
                   'эластичность. Требуют увлажнения и питания.',
            'Хеш': '68dd4868b0ba1a96e83295d05327e97af4f2748a34fb45281023729d8532c326'}

        result = self.prompt_constructor.main_constructor_prompt(
            data_decrypted=data_collection_for_best_product,
            data_collection=data_collection,
        )

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

        self.assertIn('prompt', result)
        self.assertIsInstance(result['prompt'], str)

    def test_main_constructor_prompt_one_product(self):
        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучшее средство',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Категория': 'шампуни',
            'Специалист': 'Т',
            'Средства': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday'},
            'Тип': 'В1, В10',
            'Хеш': 'c4e6fde76375f11000f171b5e4fa943922c8d4b11f1ef69a2fd5be158018b54c',
        }

        data_collection_for_one_product = {
            'Возраст': '32',
            'Задача': 'Разбираешь состав одного средства, особенно уделяя внимание '
                      'следующим пунктам: основные компоненты, активные компоненты, '
                      'Увлажняющие и ухаживающие компоненты, Консерванты и регуляторы pH, '
                      'Запрещенные или нежелательные компоненты, Дополнительные свойства, '
                      'Текстура, Плюсы средства, Минусы средства, Вывод',
            'Запрос': 'Волосы: Увлажнение и питание. Необходимо восстановить водный '
                      'баланс волос и насытить их полезными веществами, так как '
                      'недостаток влаги делает волосы сухими, ломкими и тусклыми. Важно '
                      'обеспечить глубокое питание по всей длине, укрепить структуру и '
                      'защитить волосы от внешних воздействий, чтобы они оставались '
                      'мягкими, гладкими и здоровыми. Волосы: Для частого мытья. '
                      'Необходимо мягкое и бережное очищение волос и кожи головы, так как '
                      'частое мытье может привести к пересушиванию, потере естественного '
                      'баланса и защитного слоя. Важно подобрать средство с деликатной '
                      'формулой, которое будет поддерживать свежесть волос, увлажнять и '
                      'укреплять их, не утяжеляя и не пересушивая.',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Содержимое': 'Шампуни',
            'Специалист': 'Ты профессиональный трихолог с медицинским образованием. Твоя '
                          'задача подобрать максимально подходящее средство для человека. '
                          'Данные человека будут даны.',
            'Средства': 'Средство №1 - ALTEREGO ITALY Curego Hydraday. Состав: Aqua '
                        '(Water), Ammonium Lauryl Sulfate, Cocamidopropyl Betaine, '
                        'Erythritol, Lactic Acid, Polysorbate 20, Parfum (Fragrance), '
                        'Sodium Benzoate, Sodium Gluconate, Sodium Hydroxide, '
                        'Propanediol, Guar Hydroxypropyltrimonium Chloride, Hexyl '
                        'Cinnamal, Citric Acid, Geraniol, Linalool, Hydroxycitronellal, '
                        'Tartaric Acid, Oryza Sativa (Rice) Extract, Gluconic Acid, '
                        'Saccharomyces Ferment Lysate Filtrate, Sodium Chloride, '
                        'Potassium Sorbate, Vitis Vinifera Seed Oil (Vitis Vinifera '
                        '(Grape) Seed Oil), Glycerin, Sorbitol, Lecithin, Xanthan Gum.. '
                        'Тип продукта: шампунь. ',
            'Тип': 'Тип волос: Нормальные. Волосы не слишком жирные, не слишком сухие. '
                   'Хорошо держат форму и имеют естественный блеск. Тип волос: Сухие. '
                   'Волосы Могут выглядеть тусклыми и ломкими. Часто спутываются и теряют '
                   'эластичность. Требуют увлажнения и питания.',
            'Хеш': 'c4e6fde76375f11000f171b5e4fa943922c8d4b11f1ef69a2fd5be158018b54c',
        }

        result = self.prompt_constructor.main_constructor_prompt(
            data_decrypted=data_collection_for_one_product,
            data_collection=data_collection,
        )

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

        self.assertIn('prompt', result)
        self.assertIsInstance(result['prompt'], str)
