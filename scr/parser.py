import logging
import os
from typing import ClassVar

from bs4 import BeautifulSoup
from selenium import webdriver

from scr.types import DataVideo


class ParserYouTube:
    url_channel: ClassVar = os.environ["YOUTUBE_CHANNEL_URL"]

    @classmethod
    def get_information(cls) -> DataVideo:
        page_source = cls._request()
        return cls._parser_data(page_source=page_source)

    @classmethod
    def _request(cls) -> str:
        options = cls._create_optinos()
        with webdriver.Chrome(options=options) as driver:
            driver.get(cls.url_channel + "/streams")
            page_source = driver.page_source
        return page_source

    @staticmethod
    def _parser_data(page_source: str) -> DataVideo | None:
        soup = BeautifulSoup(page_source, "html.parser")
        try:
            first_video_data = soup.find("div", id="contents").find("div", id="meta")
        except AttributeError:
            return None
        meta_data = first_video_data.find(id="video-title-link")
        result = DataVideo(
            title=meta_data.text,
            url_video=meta_data["href"],
            time_scheduled_video=first_video_data.find_all("span")[-1].text,
        )
        logging.info(msg=f"parsed fata: {result}")
        return result

    @staticmethod
    def _create_optinos() -> webdriver:
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
