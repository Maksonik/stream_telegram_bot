


def is_scheduled(scheduled_time_in_str: str) -> bool:
    if "Scheduled for" not in scheduled_time_in_str:
        return False
    return True
