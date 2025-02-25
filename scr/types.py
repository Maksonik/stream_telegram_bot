from dataclasses import dataclass


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
