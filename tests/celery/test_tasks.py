import datetime
from unittest.mock import AsyncMock

import pytest
from freezegun import freeze_time

from scr.celery.tasks import (
    _determine_notification_action,
    sync_notify_about_first_youtube_video,
    send_notification,
    delete_notification,
)
from scr.types import DataVideo, NotificationAction


@pytest.mark.parametrize(
    "time_scheduled_video, existing_titles, now, expected_action",
    [
        ("None", {"Existing Video"}, datetime.datetime(2025, 2, 27, 12, 0, 0), NotificationAction.DELETE),
        ("None", set(), datetime.datetime(2025, 2, 27, 12, 0, 0), NotificationAction.NOTHING),
        ("Scheduled for 28/02/2025, 12:00", set(), datetime.datetime(2025, 2, 27, 12, 0, 0), NotificationAction.NOTIFY),
        (
            "Scheduled for 27/02/2025, 12:10",
            {"Test Video"},
            datetime.datetime(2025, 2, 27, 11, 56, 0),
            NotificationAction.NOTIFY_15,
        ),
        (
            "Scheduled for 27/02/2025, 13:10",
            {"Test Video"},
            datetime.datetime(2025, 2, 27, 11, 30, 0),
            NotificationAction.NOTHING,
        ),
    ],
)
def test_determine_notification_action(time_scheduled_video, existing_titles, now, expected_action):
    data = DataVideo(title="Test Video", url_video="https://youtube.com", time_scheduled_video=time_scheduled_video)

    action = _determine_notification_action(data, existing_titles, now)
    assert action == expected_action


async def test_sync_notify_about_first_youtube_video(mocker):
    """Тестируем выполнение Celery-задачи."""

    mock_parser = mocker.patch("scr.apps.parser_client.ParserYouTube.get_information")

    test_data = DataVideo(
        title="Test Video",
        url_video="https://youtube.com",
        time_scheduled_video="Scheduled for 28/02/2025, 12:00",
    )

    mock_now = datetime.datetime(2025, 2, 27, 12, 0, 0)
    with freeze_time(mock_now):
        mock_parser.return_value = test_data

        mock_determine_action = mocker.patch(
            "scr.celery.tasks._determine_notification_action", return_value=NotificationAction.NOTIFY
        )
        mock_send_notification = mocker.patch("scr.celery.tasks.send_notification")

        await sync_notify_about_first_youtube_video()

        mock_determine_action.assert_called_once_with(test_data, set(), mock_now)
        mock_send_notification.assert_called_once_with(test_data)


async def test_sync_notify_about_first_youtube_video_for_15_minutes(mocker):
    """Тестируем выполнение Celery-задачи."""

    mock_parser = mocker.patch("scr.apps.parser_client.ParserYouTube.get_information")

    test_data = DataVideo(
        title="Test Video",
        url_video="https://youtube.com",
        time_scheduled_video="Scheduled for 28/02/2025, 12:00",
    )

    mock_now = datetime.datetime(2025, 2, 28, 10, 0, 0)
    with freeze_time(mock_now):
        mock_parser.return_value = test_data

        mock_determine_action = mocker.patch(
            "scr.celery.tasks._determine_notification_action", return_value=NotificationAction.NOTIFY_15
        )
        mock_send_notification = mocker.patch("scr.celery.tasks.send_notification")

        await sync_notify_about_first_youtube_video()

        mock_determine_action.assert_called_once_with(test_data, set(), mock_now)
        mock_send_notification.assert_called_once_with(test_data, has_15_minutes_notice=True)


async def test_sync_notify_about_first_youtube_video_delete(mocker):
    """Тестируем выполнение Celery-задачи."""

    mock_parser = mocker.patch("scr.apps.parser_client.ParserYouTube.get_information")

    test_data = DataVideo(
        title="Test Video",
        url_video="https://youtube.com",
        time_scheduled_video="Scheduled for 28/02/2025, 12:00",
    )

    mock_now = datetime.datetime(2025, 2, 28, 13, 0, 0)
    with freeze_time(mock_now):
        mock_parser.return_value = test_data

        mock_determine_action = mocker.patch(
            "scr.celery.tasks._determine_notification_action", return_value=NotificationAction.DELETE
        )
        mock_delete_notification = mocker.patch("scr.celery.tasks.delete_notification")

        await sync_notify_about_first_youtube_video()

        mock_determine_action.assert_called_once_with(test_data, set(), mock_now)
        mock_delete_notification.assert_called_once_with(test_data)


async def test_sync_notify_about_first_youtube_video_nothing(mocker):
    mock_parser = mocker.patch("scr.apps.parser_client.ParserYouTube.get_information")

    test_data = DataVideo(
        title="Test Video",
        url_video="https://youtube.com",
        time_scheduled_video="Scheduled for 28/02/2025, 12:00",
    )

    mock_now = datetime.datetime(2025, 2, 28, 13, 0, 0)
    with freeze_time(mock_now):
        mock_parser.return_value = test_data

        mock_determine_action = mocker.patch(
            "scr.celery.tasks._determine_notification_action", return_value=NotificationAction.NOTHING
        )
        await sync_notify_about_first_youtube_video()
        mock_determine_action.assert_called_once_with(test_data, set(), mock_now)


async def test_send_notification(mocker):
    mock_telegram = mocker.patch("scr.celery.tasks.telegram.send_message", new_callable=AsyncMock)

    data = DataVideo(
        title="Test Video", url_video="https://youtube.com/test", time_scheduled_video="Scheduled for 28/02/2025, 12:00"
    )

    await send_notification(data, has_15_minutes_notice=True)

    mock_telegram.assert_awaited_once_with(
        title="Test Video",
        url="https://youtube.com/test",
        has_15_minutes_notice=True,
        time=datetime.datetime(2025, 2, 28, 12, 0),
    )


async def test_delete_notification(mocker):
    mock_telegram = mocker.patch("scr.celery.tasks.telegram.delete_message", new_callable=AsyncMock)

    data = DataVideo(
        title="Test Video", url_video="https://youtube.com/test", time_scheduled_video="Scheduled for 28/02/2025, 12:00"
    )

    await delete_notification(data)

    mock_telegram.assert_awaited_once_with()
