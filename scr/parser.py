import os

from bs4 import BeautifulSoup
from selenium import webdriver
from dataclasses import dataclass


@dataclass
class DataVideo:
    title: str
    url_video: str
    time_scheduled_video: str


class ParserYouTube:
    def __init__(self):
        self.url_channel = os.environ["YOUTUBE_CHANNEL_URL"]

    def _request(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Фоновый режим
        options.add_argument("--disable-gpu")  # Отключение GPU
        options.add_argument("--no-sandbox")  # Для Linux-систем
        options.add_argument(
            "--disable-dev-shm-usage"
        )  # Уменьшает использование памяти
        options.add_argument(
            "--blink-settings=imagesEnabled=false"
        )  # Отключаем загрузку изображений
        with webdriver.Chrome(options=options) as driver:
            driver.get(self.url_channel + "/streams")
            page_source = driver.page_source
        return page_source

    @staticmethod
    def _parser_data(page_source: str) -> DataVideo:
        soup = BeautifulSoup(page_source, "html.parser")
        first_video_data = soup.find("div", id="contents").find(
            "div", id="meta"
        )
        meta_data = first_video_data.find(id="video-title-link")

        return DataVideo(
            title=meta_data.text,
            url_video=meta_data["href"],
            time_scheduled_video=first_video_data.find_all("span")[-1].text,
        )

    def get_information(self) -> DataVideo:
        page_source = self._request()
        return self._parser_data(page_source=page_source)
