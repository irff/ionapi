from datetime import datetime, timedelta, date
import time

def create_timestamp(datetime_string):
    date = datetime_string.split(" ")
    return date[0] + "T" + date[1] + ".000Z"

def check_datetime(datetime_string):
    try:
        datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False


def create_unix_timestamp(datetime_string):
    date = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
    return time.mktime(date.timetuple())

def create_date(datetime_string):
    date_arr = datetime_string.split(" ")
    return datetime.strptime(date_arr[0], "%Y-%m-%d")

def add_days_timedelta(date, delta):
    return date + timedelta(days=delta)