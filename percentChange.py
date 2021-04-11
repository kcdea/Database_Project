import datetime
from dateToTimestamp import dateToTimestamp
from query import query

def percentChange(currencies, startDate = datetime.date.min, endDate = datetime.date.max):
    start = dateToTimestamp(startDate)
    end = dateToTimestamp(endDate)
    
    queryStr = 'SELECT {0}.DATE_TXT, '.format(currencies[0])
    position = 0
    while position < len(currencies):
        if position != 0:
            queryStr = queryStr + ', '
        queryStr = queryStr + '(({0}.CLOSE - {0}.OPEN) / {0}.OPEN)'.format(currencies[position])
        position = position + 1;
    position = 0
    queryStr = queryStr + ' FROM '
    while position < len(currencies):
        if position == 0:
            queryStr = queryStr + currencies[position]
        else:
            queryStr = queryStr + ' INNER JOIN {1} ON {0}.DATE_TXT = {1}.DATE_TXT'.format(currencies[0], currencies[position])
        position = position + 1
    queryStr = queryStr + ' WHERE {0}.TIMESTAMP >= {1} AND {0}.TIMESTAMP <= {2}'.format(currencies[0], start, end)
    for currency in currencies:
        queryStr = queryStr + ' AND {0}.OPEN > 0'.format(currency)
    queryStr = queryStr + ' ORDER BY {0}.DATE_TXT ASC'.format(currencies[0])
    
    headers = currencies
    headers.insert(0, "datetime")
    return query(queryStr, headers)