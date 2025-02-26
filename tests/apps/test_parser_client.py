import pytest

from scr.apps.parser_client import ParserYouTube
from scr.core.settings import get_settings
from scr.types import DataVideo


@pytest.mark.vcr
def test_parser_client(page_without_scheduled_stream_video):
    parser = ParserYouTube(settings=get_settings())
    data = parser.get_information()
    assert data == DataVideo(
        title="От Джуна до Мидла | День 11",
        url_video="/watch?v=-_j_EboM3Bs",
        time_scheduled_video="Streamed 3 weeks ago",
    )
