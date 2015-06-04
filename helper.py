from datetime import datetime, timedelta, date
import time

def create_timestamp(datetime_string):
    """ to create a string with ES timestamp format
    :param datetime_string: a string with format (YYY-MM-DD HH:ii:SS)
    :return: a string with format (yyyy-mm-ddThh:mm;ss.000Z)
    """
    date = datetime_string.split(" ")
    return date[0] + "T" + date[1] + ".000Z"

def check_datetime(datetime_string):
    """ to check if a string is a timestamp
    :param datetime_string: a string with format (YYYY-MM-DD HH:ii:SS))
    :return: boolean
    """
    try:
        datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def create_unix_timestamp(datetime_string):
    """ to create time object from string
    :param datetime_string: a string with format (YYYY-MM-DD HH:ii:SS)
    :return: a unix timestamp
    """
    date = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
    return time.mktime(date.timetuple())

def create_date(datetime_string):
    """ to create datetime object from string
    :param datetime_string: a string with format (YYYY-MM-DD HH:ii:SS)
    :return: a datetime object
    """
    date_arr = datetime_string.split(" ")
    return datetime.strptime(date_arr[0], "%Y-%m-%d")

def add_days_timedelta(date, delta):
    """ to add date object
    :param date: a datetime object
    :param delta: int
    :return: new datetime add delta
    """
    return date + timedelta(days=delta)

def check_keyword_phrase(keyword):
    """ to check if a keyword is phrase
    :param keyword: a string
    :return: booelan
    """
    if keyword[0] == "*" and keyword[len(keyword) - 1] == "*":
        return True
    else:
        return False