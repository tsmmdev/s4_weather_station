# import sys
import datetime


def log_time_zone(timezone="UTC"):
    now_utc = datetime.datetime.utcnow()
    utc_str = now_utc.strftime('%Y-%m-%d %H:%M:%S.%f ' + timezone)[:-3] + f"{timezone}"
    return utc_str

