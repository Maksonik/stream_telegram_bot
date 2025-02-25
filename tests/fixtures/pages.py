import pytest


@pytest.fixture
def page_without_scheduled_stream_video() -> str:
    with open("statistics/html_page_without_scheduled_stream_video", mode="r", encoding="utf-8") as file:
        page_data = file.read()
    return page_data


@pytest.fixture
def page_with_not_soon_scheduled_stream_video() -> str:
    with open("statistics/html_page_with_not_soon_scheduled_stream_video", mode="r", encoding="utf-8") as file:
        page_data = file.read()
    return page_data

@pytest.fixture
def page_with_soon_scheduled_stream_video() -> str:
    with open("statistics/html_page_with_soon_scheduled_stream_video", mode="r", encoding="utf-8") as file:
        page_data = file.read()
    return page_data