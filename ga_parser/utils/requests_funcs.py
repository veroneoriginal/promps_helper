"""
Запросы на сайт Золотого яблока и cdn за изображением
"""
import time

import requests
from requests import Response

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager



def get_page_v2(
        url: str,
        timeout: int = 10,
        headless: bool = True,
) -> str | None:
    # Пауза после скрола страницы вниз (секунд)
    SLEEP_AUTO_SCROLL_PAGE_DOWN = 8

    # Настраиваем Chrome
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # Без GUI, если нужно
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Запускаем WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)  # Открываем страницу
        WebDriverWait(driver, timeout=timeout)  # Ожидаем загрузки

        # Скроллим вниз, чтобы элементы стали видимыми
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SLEEP_AUTO_SCROLL_PAGE_DOWN)

        # Получаем HTML после кликов
        html = driver.page_source

    finally:
        driver.quit()  # Закрываем браузер

    return html


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
