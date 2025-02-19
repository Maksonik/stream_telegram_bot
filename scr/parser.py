import os

from bs4 import BeautifulSoup
from selenium import webdriver

from scr.types import DataVideo


class ParserYouTube:
    def __init__(self):
        self.url_channel = os.environ["YOUTUBE_CHANNEL_URL"]

    def get_information(self) -> DataVideo:
        page_source = self._request()
        return self._parser_data(page_source=page_source)

    def _request(self):
        options = self._create_optinos()
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

    def _create_optinos(self) -> webdriver:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Фоновый режим
        options.add_argument("--disable-gpu")  # Отключение GPU
        options.add_argument("--no-sandbox")  # Для Linux-систем
        options.add_argument(  # Уменьшает использование памяти
            "--disable-dev-shm-usage"
        )
        options.add_argument(  # Отключаем загрузку изображений
            "--blink-settings=imagesEnabled=false"
        )
        return options
