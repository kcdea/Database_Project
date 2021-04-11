import datetime

def dateToTimestamp(date):
    result = datetime.datetime(date.year, date.month, date.day, tzinfo = datetime.timezone.utc)
    return str(result.timestamp() * 1000)