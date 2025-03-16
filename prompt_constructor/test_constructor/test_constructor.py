"""В этом модуле тестируем выбор промпта"""

import unittest
from prompt_constructor.prompt_constructor import PromptConstructor


class TestPromptConstructor(unittest.TestCase):
    """
    Тесты на main_constructor_prompt у PromptConstructor
    """

    def setUp(self):
        """
        Готовим объект PromptConstructor перед каждым тестом
        """
        self.prompt_constructor = PromptConstructor()

    def test_main_constructor_prompt_best_product(self):
        """
        Тест задачи 'Лучшее средство'
        """

        # формирую словарь с информацией для json-схемы
        data_for_best_product = {
            # определяем задачу для выбора в json-схемы
            "Задача": 'Лучшее средство',
            # считаем сколько средств подаем для анализа
            "Количество элементов": 6,
            "Категория": 'Шампуни',
        }

        data_collection_for_best_product = {
            'Возраст': '32',
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
            'Лучший вариант': None,
            'Пол': 'женский',
            'Содержимое': 'Шампуни',
            'Специалист': 'Ты профессиональный трихолог с медицинским образованием. Твоя '
                          'задача подобрать максимально подходящее средство для человека. '
                          'Данные человека будут даны.',
            'Средства': 'Средство №1 - AUSSIE Miracle Moist. Состав: Aqua, sodium lauryl '
                        'sulfate, sodium laureth sulfate, cocamidopropyl betaine, glycol '
                        'distearate, sodium citrate, cocamide mea, sodium '
                        'xylenesulfonate, sodium chloride, parfum, sodium benzoate, '
                        'citric acid, tetrasodium edta, guar hydroxypropyltrimonium '
                        'chloride, sodium hydroxide, limonene, magnesium nitrate, aloe '
                        'barbadensis leaf juice, macadamia ternifolia seed oil, ci 19140, '
                        'methylchloroisothiazolinone, magnesium chloride, ci 17200, '
                        'methylisothiazolinone.. Тип продукта: шампунь. \n'
                        'Средство №2 - ICE BY NATURA SIBERICA REFRESH MY SCALP. Состав: '
                        'Aqua, Sodium Coco-Sulfate, Coco-Glucoside, Sodium Chloride, '
                        'Polyglyceryl- 10 Oleate, Decyl Glucoside, Mentha Arvensis Leaf '
                        'Extract (Organic Wild Mint Extract), Laminaria Saccharina '
                        'Extract WH (Organic Laminaria Extract), Eleutherococcus '
                        'Senticosus Extract WH (Organic Siberian Ginseng Extract), '
                        'Flavocetraria Nivalis Extract WH (Organic Snow Cladonia '
                        'Extract), Dasiphora Fruticosa Extract (Organic Kuril Tea '
                        'Extract), Salicylic Acid, Salvia Sclarea Oil (Organic Clary Sage '
                        'Essential Oil), Melaleuca Alternifolia Leaf Oil (Organic Tea '
                        'Tree Essential Oil), Guar Hydroxypropyltrimonium Chloride, '
                        'Glyceryl Oleate, Allantoin, Menthyl Lactate, Taurine, Benzyl '
                        'Alcohol, Sodium Benzoate, Potassium Sorbate, Citric Acid, '
                        'Parfum, Linalool, Benzyl Salicylate. (WH) - Wild Harvested '
                        'Siberian Plants Organic Extracts. Тип продукта: шампунь. \n'
                        'Средство №3 - LADOR Keratin LPP. Состав: Water,Cocamidopropyl '
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
                        'шампунь. \n'
                        'Средство №4 - NATURA SIBERICA Oblepikha. Состав: Aqua with '
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
                        'Средство №5 - PAYOT Shampoing doux biome-friendly. Состав: Aqua '
                        '(Water), Sodium Lauroyl Methyl Isethionate, Lauryl Glucoside, '
                        'Cocamidopropyl Betaine, Sodium Methyl Cocoyl Taurate, Parfum '
                        '(Fragrance), Pogostemon Cablin Leaf/Stem Extract, Salvia '
                        'Officinalis Leaf Extract, Glycerin, Alpha-Glucan '
                        'Oligosaccharide, Coco-Glucoside, Glyceryl Oleate, Tocopherol, '
                        'Hydrogenated Palm Glycerides Citrate, Citric Acid, '
                        'Polyquaternium-10, Phenethyl Alcohol, Chlorphenesin, Sodium '
                        'Benzoate, Potassium Sorbate.. Тип продукта: шампунь. \n'
                        'Средство №6 - КУДРЯВЫЙ МЕТОД for curly hair. Состав: Aqua, '
                        'Sodium Laureth Sulfate, Cocamidopropyl Betaine, Sodium Chloride, '
                        'Betaine, Potassium Laureth-4 Carboxylate, Coco-Glucoside, Decyl '
                        'Glucoside, Panthenol, Persea Gratissima (Avocado) Oil, Hamamelis '
                        'Virginiana (Witch Hazel) Leaf Extract, Olive Oil Glycereth-8 '
                        'Esters, Almond Oil Glycereth-8 Esters, Polyquaternium-7, '
                        'Glycerin, Tetrasodium Glutamate Diacetate, Potassium Sorbate, '
                        'Sodium Benzoate, Methylchloroisothiazolinone, '
                        'Methylisothiazolinone, Citric Acid, Sodium Hydroxide, Parfum, '
                        'Linalool, Limonene.. Тип продукта: шампунь. ',
            'Тип': 'Тип волос: Нормальные. Волосы не слишком жирные, не слишком сухие. '
                   'Хорошо держат форму и имеют естественный блеск. Тип волос: Сухие. '
                   'Волосы Могут выглядеть тусклыми и ломкими. Часто спутываются и теряют '
                   'эластичность. Требуют увлажнения и питания.',
            'Хеш': '86f799964e21a4860a86a1097655310173b941cb5df6e011ba131b810fab1a50'}

        result = self.prompt_constructor.main_constructor_prompt(
            data=data_for_best_product,
            data_collection=data_collection_for_best_product,
        )

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

        self.assertIn('prompt', result)
        self.assertIsInstance(result['prompt'], str)

    def test_main_constructor_prompt_one_product(self):
        # формирую словарь с информацией для json-схемы
        data_for_one_product = {
            # определяем задачу для выбора в json-схемы
            "Задача": 'Разбор состава одного средства',
            # считаем сколько средств подаем для анализа
            "Количество элементов": None,
            "Категория": None,
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
            'Хеш': 'c4e6fde76375f11000f171b5e4fa943922c8d4b11f1ef69a2fd5be158018b54c'}

        result = self.prompt_constructor.main_constructor_prompt(
            data=data_for_one_product,
            data_collection=data_collection_for_one_product,
        )


        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

        self.assertIn('prompt', result)
        self.assertIsInstance(result['prompt'], str)
