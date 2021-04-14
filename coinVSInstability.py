import datetime
from query import query

def getWithClause(currencies, startDate=datetime.date(2012, 1, 1), endDate=datetime.date.today()):
    queryStr = "WITH "
    currencyIt = 0
    yearMonths = []
    dateIt = startDate
    while not(dateIt.year == endDate.year and dateIt.month == endDate.month):
        yearMonths.append([dateIt.year, dateIt.month])
        tempMonth = dateIt.month
        while dateIt.month == tempMonth:
            dateIt = dateIt + datetime.timedelta(days = 28)
    while currencyIt < len(currencies):
        queryStr = queryStr + "{0}AVG(MONTH, AVERAGE) AS (".format(currencies[currencyIt])
        queryStr = queryStr + "SELECT MIN(DMIX.{0}.DATE_TXT), AVG(DMIX.{0}.OPEN) FROM DMIX.{0} WHERE EXTRACT(YEAR FROM DMIX.{0}.DATE_TXT) = {1} AND EXTRACT(MONTH FROM DMIX.{0}.DATE_TXT) = {2}".format(currencies[currencyIt], yearMonths[0][0], yearMonths[0][1])
        yearMonthsIt = 1
        while yearMonthsIt < len(yearMonths):
            queryStr = queryStr + " UNION SELECT MIN(DMIX.{0}.DATE_TXT), AVG(DMIX.{0}.OPEN) FROM DMIX.{0} WHERE EXTRACT(YEAR FROM DMIX.{0}.DATE_TXT) = {1} AND EXTRACT(MONTH FROM DMIX.{0}.DATE_TXT) = {2}".format(currencies[currencyIt], yearMonths[yearMonthsIt][0], yearMonths[yearMonthsIt][1])
            yearMonthsIt = yearMonthsIt + 1
        queryStr = queryStr + ")"
        if currencyIt != len(currencies) - 1:
            queryStr = queryStr + ", "
        currencyIt = currencyIt + 1
    return queryStr

def coinVSInstability(currencies, countries, startDate=datetime.date(2012, 1, 1), endDate=datetime.date.today()):
    queryStr = getWithClause(currencies, startDate, endDate) + " SELECT "
    for country in countries:
        queryStr = queryStr + "DMIX.ECONOMICINSTABILITY.{0}, ".format(country)
    currencyIt = 0
    while currencyIt < len(currencies):
        if currencyIt == 0:
            queryStr = queryStr + "{0}AVG.MONTH, ".format(currencies[currencyIt])
        queryStr = queryStr + "{0}AVG.AVERAGE".format(currencies[currencyIt])
        if currencyIt != len(currencies) - 1:
            queryStr = queryStr + ","
        queryStr = queryStr + " "
        currencyIt = currencyIt + 1
    queryStr = queryStr + "FROM DMIX.ECONOMICINSTABILITY"
    for currency in currencies:
        queryStr = queryStr + " INNER JOIN {0}AVG ON DMIX.ECONOMICINSTABILITY.MONTH = EXTRACT(MONTH FROM {0}AVG.MONTH) AND DMIX.ECONOMICINSTABILITY.YEAR = EXTRACT(YEAR FROM {0}AVG.MONTH);".format(currency)
    
    headers = countries
    headers.append("month")
    for currency in currencies:
        headers.append(currency)
    return query(queryStr, headers)