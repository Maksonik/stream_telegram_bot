from datetime import datetime


def is_scheduled(scheduled_time_in_str: str | None) -> bool:
    """
    Checks whether the video is scheduled or not
    ______
    Examples:
    scheduled_time_in_str = 'Scheduled for 25/02/2025, 16:45'
    is_scheduled(scheduled_time_in_str) -> True

    scheduled_time_in_str = 'The broadcast ended three weeks ago'
    is_scheduled(scheduled_time_in_str) -> False
    _____
    :param scheduled_time_in_str:
    :return: True or False
    """
    if scheduled_time_in_str is None or "Scheduled" not in scheduled_time_in_str:
        return False
    return True

def get_time(scheduled_time_in_str: str | None) -> datetime:
    """
    Get datetime type from string
    :param scheduled_time_in_str:
    :return: time of datetime
    """
    time = scheduled_time_in_str.replace("Scheduled for ", "")
    return datetime.strptime(time, "%d/%m/%Y, %H:%M")

