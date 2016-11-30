from datetime import datetime


def cast_time_to_datetime(time=datetime.now().time()):
    string_datetime = str(datetime.now().date()) + " " + time.strftime("%H:%M:%S")
    return datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")


def get_difference_in_seconds(datetime1, datetime2):
    diff = datetime1 - datetime2
    return diff.total_seconds()

