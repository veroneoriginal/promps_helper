"""
Запросы на сайт Золотого яблока и cdn за изображением
"""

import requests
from requests import Response

# Заголовки для запроса (имитируем запрос от браузера)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}


def get_page(url: str) -> str | None:
    """
    Отправляет запрос в Золотое яблоко, возвращает содержимое страницы

    :param url: ссылка на страницу средства
    :return:
    """

    response = requests.get(url, headers=HEADERS, timeout=5)

    if response.status_code == 200:
        html = response.text  # HTML содержимое страницы
        print("Страница успешно загружена!")
        return html
    print(f"Ошибка при загрузке страницы. Статус код: {response.status_code}")
    return None


def get_image(url: str) -> Response | None:
    """
    Отправляет запрос для получения изображения

    :param url: ссылка на изображение средства
    :return:
    """

    try:
        response = requests.get(url, stream=True, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Ошибка загрузки изображения: {e}")
    return None
