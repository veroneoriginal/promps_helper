# pylint: disable=C0301: line-too-long
import json
from pathlib import Path
from typing import Union

from post_constructor.post_processing_data import get_smile_for_key


class PostConstructor:
    """
    Класс для создания постов для соц.сетей
    """

    def __init__(
            self,
    ):
        self.post_for_task = {
            'Лучшее средство': self.create_text_for_post_code_best_product,
            'Лучшее средство без канцерогенов':
                self.create_text_for_post_code_best_product_canc_free,
            'Разбор состава одного средства': self.create_text_for_post_code_one_product,
            'Лучшая пара': self.create_text_for_post_code_best_couple,
            'Лучшее сочетание': self.create_text_for_post_code_best_combination,
            'Аналог': self.create_text_for_post_code_analog,
            'Лучшая компоновка': None,
            'Наиболее похож': None,
            'Наименее похож': None,
        }

    def create_text_for_post_code_best_product(
            self,
            data: dict,
    ) -> str:
        """
        Метод возвращает строку с типами и запросом пользователя
        для кода задачи "Лучшее средство".

        :param data: словарь с данными о пользователе и косметических средствах
        :return: строка с данными о потребностях пользователя
        """

        return f"**🔍 Решаем следующие задачи:**\n{data['Запрос']}."

    def create_text_for_post_code_best_product_canc_free(
            self,
            data: dict,
    ) -> str:
        """
        Метод возвращает строку с типами и запросом пользователя
        для кода задачи "Лучшее средство без канцерогенов".

        :param data: словарь с данными о пользователе и косметических средствах
        :return: строка с данными о потребностях пользователя
        """

        return f"""**🔍 Решаем следующие задачи:**\n{data["Запрос"]}.

‼Для нас важно, чтобы состав лучшего средства был максимально безопасным и чистым.
"""

    def create_text_for_post_code_one_product(
            self,
            data: dict,
    ) -> str:
        """
        Метод возвращает строку с типами и запросом пользователя
        для кода задачи "Разбор состава одного средства".

        :param data: словарь с данными о пользователе и косметических средствах
        :return: строка с данными о потребностях пользователя
        """

        return f"""**🔍 С помощью данного средства решаем следующие задачи:**\n{data["Запрос"]}.
    
⭐ Проводим максимально детальный анализ состава каждого компонента.
"""

    def create_text_for_post_code_best_couple(
            self,
            data: dict,
    ) -> str:
        """
        Метод возвращает строку с типами и запросом пользователя
        для кода задачи "Лучшая пара".

        :param data: словарь с данными о пользователе и косметических средствах
        :return: строка с данными о потребностях пользователя
        """

        return f"""**🔍 Подбираем полноценный набор средств, с помощью которого сможем решить следующие задачи:**\n{data["Запрос"]}."""

    def create_text_for_post_code_best_combination(
            self,
            data: dict,
    ) -> str:
        """
        Метод возвращает строку с типами и запросом пользователя
        для кода задачи "Лучшее сочетание".

        :param data: словарь с данными о пользователе и косметических средствах
        :return: строка с данными о потребностях пользователя
        """

        return (
            f"**🔍 У нас есть средство: \"{data['Средства']['Исходное средство']}\".\n"
            f"Нам необходимо подобрать к нему пару для комплексного решения следующих задач:**\n{data['Запрос']}."
        )

    def create_text_for_post_code_analog(
            self,
            data: dict,
    ) -> str:
        """
        Метод возвращает строку с типами и запросом пользователя
        для кода задачи "Аналог".

        :param data: словарь с данными о пользователе и косметических средствах
        :return: строка с данными о потребностях пользователя
        """

        return (
            f"**🔍 У нас есть средство - \"{data['Средства']['Исходное средство'][0]}\".\n"
            f"Является ли \"{data['Средства']['Аналог средство'][0]}\" его аналогом "
            f"и сможет ли предполагаемый аналог так же эффективно, как исходное средство, "
            f"справляться со следующими задачами:** {data['Запрос']}."
        )

    def load_result_recommendation(
            self,
            result_dir: Union[str, Path],
    ) -> str:
        """
        Загружает результат итоговой рекомендации от OPENAI из JSON-файла.

        :param result_dir: Путь до файла 'Анализ_средств.json'.
        :return: значение по ключу 'result' из JSON-файла.
        Если ключ отсутствует — вернёт пустую строку.
        """

        path_to_file = Path(result_dir) / "Анализ_средств.json"

        with path_to_file.open('r', encoding='utf-8') as file:
            answer_gpt = json.load(file)

        return answer_gpt.get('result', '')

    def create_text_for_post(
            self,
            data: dict,
            path_to_result_recommend: str,
            task: str,
    ) -> str:
        """
        Вызывает нужный метод для формирования поста в зависимости от того,
        учитываются ли данные пользователя или нет

        :param data: словарь с данными о пользователе и косметических средствах
        :param path_to_result_recommend: путь до json-файла, в котором находится
        ответ от GPT по подборке
        :param task: код задачи по текущей подборке

        :return: строка с данными о пользователе, его потребностях, итог.рекомендацией
        """
        if data['Параметры'].strip().lower() == 'учитывать':
            return self.create_text_for_post_with_user_parameters(
                data=data,
                path_to_result_recommend=path_to_result_recommend,
                task=task,
            )
        return self.create_text_for_post_without_user_parameters(
            data=data,
            path_to_result_recommend=path_to_result_recommend,
        )

    def create_text_for_post_without_user_parameters(
            self,
            data: dict,
            path_to_result_recommend: str,
    ) -> str:
        """
        Метод с общей информацией для поста:
        Формирует текст для поста с информацией о пользователе,
        его потребностях и итоговой рекомендации по средствам БЕЗ УЧЁТА данных пользователя

        :param data: словарь с данными о пользователе и косметических средствах
        :param path_to_result_recommend: путь до json-файла, в котором находится
        ответ от GPT по подборке

        :return: строка с данными о пользователе, его потребностях, итог.рекомендацией
        """

        # Забираем ключ 'result'
        result_recommend = self.load_result_recommendation(result_dir=path_to_result_recommend).strip()

        # Формируем содержимое поста
        return f"""**🏆 Итоговая рекомендация по текущей подборке**:
        
{result_recommend}

{data['Хештег']}

⚠️ Вся информация предоставляется исключительно в образовательных целях и не является медицинским или юридическим заключением. Мы основываемся на анализе составов косметических средств с помощью искусственного интеллекта, обученного на открытых научных источниках, данные которых могут обновляться. Перед использованием продукта рекомендуем консультироваться с врачом или специалистом."""

    def create_text_for_post_with_user_parameters(
            self,
            data: dict,
            path_to_result_recommend: str,
            task: str,
    ) -> str:
        """
        Метод с общей информацией для поста:
        Формирует текст для поста с информацией о пользователе,
        его потребностях и итоговой рекомендации по средствам С УЧЁТОМ данных пользователя

        :param data: словарь с данными о пользователе и косметических средствах
        :param path_to_result_recommend: путь до json-файла, в котором находится
        ответ от GPT по подборке
        :param task: код задачи по текущей подборке

        :return: строка с данными о пользователе, его потребностях, итог.рекомендацией
        """

        # Забираем ключ 'result'
        result_recommend = self.load_result_recommendation(result_dir=path_to_result_recommend).strip()

        # формируем содержимое пользовательского запроса
        user_request = self.post_for_task[task](data=data)
        gender = data["Пол"]
        # 4. Формируем содержимое поста
        return f"""**📌 Подборка средств для**:

**{get_smile_for_key(gender)} Пол:** {gender}  
**🎂 Возраст:** {data["Возраст"]} года/лет
{data["Тип"]}

{user_request}
**🏆 Итоговая рекомендация по текущей подборке**:
{result_recommend}

{data['Хештег']}

⚠️ Вся информация предоставляется исключительно в образовательных целях и не является медицинским или юридическим заключением. Мы основываемся на анализе составов косметических средств с помощью искусственного интеллекта, обученного на открытых научных источниках, данные которых могут обновляться. Перед использованием продукта рекомендуем консультироваться с врачом или специалистом."""
