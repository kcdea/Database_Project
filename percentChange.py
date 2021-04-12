import datetime
from dateToTimestamp import dateToTimestamp
from query import query

def percentChange(currencies, startDate = datetime.date.min, endDate = datetime.date.max):
    start = dateToTimestamp(startDate)
    end = dateToTimestamp(endDate)
    
    queryStr = 'SELECT DMIX.{0}.DATE_TXT, '.format(currencies[0])
    position = 0
    while position < len(currencies):
        if position != 0:
            queryStr = queryStr + ', '
        queryStr = queryStr + '((DMIX.{0}.CLOSE - DMIX.{0}.OPEN) / DMIX.{0}.OPEN)'.format(currencies[position])
        position = position + 1;
    position = 0
    queryStr = queryStr + ' FROM '
    while position < len(currencies):
        if position == 0:
            queryStr = queryStr + "DMIX." + currencies[position]
        else:
            queryStr = queryStr + ' INNER JOIN DMIX.{1} ON DMIX.{0}.DATE_TXT = DMIX.{1}.DATE_TXT'.format(currencies[0], currencies[position])
        position = position + 1
    queryStr = queryStr + ' WHERE DMIX.{0}.TIMESTAMP >= {1} AND DMIX.{0}.TIMESTAMP <= {2}'.format(currencies[0], start, end)
    for currency in currencies:
        queryStr = queryStr + ' AND DMIX.{0}.OPEN > 0'.format(currency)
    queryStr = queryStr + ' ORDER BY DMIX.{0}.DATE_TXT ASC'.format(currencies[0])
    
    headers = currencies
    headers.insert(0, "datetime")
    return query(queryStr, headers)