import schedule
from typing import Callable


market_trend = ""


def is_diff_market_trend(responsed_market_trend):
    global market_trend
    if market_trend != responsed_market_trend:
        return True
    return False


def re_apply_schedule(responsed_market_trend: str, job_func: Callable):
    if is_diff_market_trend(responsed_market_trend):
        schedule.clear()
