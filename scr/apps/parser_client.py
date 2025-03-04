import logging

from bs4 import BeautifulSoup
from selenium import webdriver

from scr.core.settings import Settings
from scr.types import DataVideo


class ParserYouTube:
    """Parser to retrieve video data from youtube channel"""

    def __init__(self, settings: Settings):
        self.url_channel = settings.YOUTUBE_CHANNEL_URL

    def get_information(self) -> DataVideo:
        """
        Get data about the first stream video from list page
        :return: data of first video
        """
        page_source = self._request()
        return self._parser_data(page_source=page_source)

    def _request(self) -> str:
        """
        Get a page with a list of streaming videos
        :return: html page in python type of str
        """
        options = self._create_options()
        with webdriver.Chrome(options=options) as driver:
            driver.get(self.url_channel + "/streams")
            page_source = driver.page_source
        return page_source

    @staticmethod
    def _parser_data(page_source: str) -> DataVideo | None:
        """
        Get necessary information from the page
        :param page_source: html page
        :return: DataVideo or None
        """
        soup = BeautifulSoup(page_source, "html.parser")
        try:
            first_video_data = soup.find("div", id="contents").find("div", id="meta")
        except AttributeError:
            logging.error(msg=f"error in parser data {soup}")
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
    def _create_options() -> webdriver.ChromeOptions:
        """
        Create optimized options for Selenium WebDriver.
        :return: ChromeOptions instance
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Фоновый режим
        options.add_argument("--disable-gpu")  # Отключение GPU
        options.add_argument("--no-sandbox")  # Для Linux
        options.add_argument("--disable-dev-shm-usage")  # Уменьшает использование памяти
        options.add_argument("--blink-settings=imagesEnabled=false")  # Отключаем изображения
        return options
