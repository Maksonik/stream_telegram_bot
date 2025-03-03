from unittest.mock import patch, MagicMock


from scr.apps.parser_client import ParserYouTube
from scr.core.settings import get_settings
from scr.types import DataVideo


def test_parser_client(page_without_scheduled_stream_video):
    parser = ParserYouTube(settings=get_settings())

    mock_page_source = """
    <div id="contents">
        <div id="meta">
            <a id="video-title-link" href="/watch?v=-_j_EboM3Bs">От Джуна до Мидла | День 11</a>
            <span>Streamed 3 weeks ago</span>
        </div>
    </div>
    """

    with patch("selenium.webdriver.Chrome") as MockWebDriver:
        mock_driver = MagicMock()
        mock_driver.page_source = mock_page_source
        MockWebDriver.return_value.__enter__.return_value = mock_driver

        data = parser.get_information()

    assert data == DataVideo(
        title="От Джуна до Мидла | День 11",
        url_video="/watch?v=-_j_EboM3Bs",
        time_scheduled_video="Streamed 3 weeks ago",
    )
