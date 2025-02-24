


def is_scheduled(scheduled_time_in_str: str | None) -> bool:
    if scheduled_time_in_str is None or "Scheduled" not in scheduled_time_in_str:
        return False
    return True
