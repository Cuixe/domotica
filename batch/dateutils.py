from datetime import datetime


def cast_time_to_datetime(time=datetime.now().time()):
    string_datetime = str(datetime.now().date()) + " " + str(time)
    return datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")


def get_seconds_diff_between_datetime(datetime1, datetime2):
    diff = datetime1 - datetime2
    return diff.total_seconds()

