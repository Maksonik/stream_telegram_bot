

def check_time_with_now(scheduled_time_in_str: str) -> bool:
    if not "Scheduled for" in scheduled_time_in_str:
        return False
    return True