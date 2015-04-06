def create_timestamp(datetime_string):
    date = datetime_string.split(" ")
    return date[0] + "T" + date[1] + ".000Z"