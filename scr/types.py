from dataclasses import dataclass
from enum import Enum


@dataclass
class DataVideo:
    title: str = ""
    url_video: str = ""
    time_scheduled_video: str = ""


@dataclass
class DataMessage:
    title: str
    id: int
    has_15_minutes_notice: bool = False


class NotificationAction(Enum):
    NOTIFY = "notify"
    NOTIFY_15 = "notify_15"
    DELETE = "delete"
    NOTHING = "nothing"
