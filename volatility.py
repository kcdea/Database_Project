import datetime
from query import query

def volatility(currency, startDate = datetime.date(2012, 1, 1), endDate = datetime.date.today()):
    queryStr = "WITH RUNNING (DATE_TXT, ALLTIME, TWELVEHOUR) AS "
    queryStr = queryStr + "(SELECT DMIX.{0}.DATE_TXT, AVG(DMIX.{0}.OPEN) OVER (ORDER BY DMIX.{0}.DATE_TXT), AVG(DMIX.{0}.OPEN) OVER (ORDER BY DMIX.{0}.DATE_TXT ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) ".format(currency)
    queryStr = queryStr + "FROM DMIX.{0}), ".format(currency)
    queryStr = queryStr + "STDDEVTB (DATE_TXT, ALLTIME, TWELVEHOUR) AS "
    queryStr = queryStr + "(SELECT DMIX.{0}.DATE_TXT, STDDEV(DMIX.{0}.OPEN) OVER (ORDER BY DMIX.{0}.DATE_TXT), AVG(DMIX.{0}.OPEN) OVER (ORDER BY DMIX.{0}.DATE_TXT ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) ".format(currency)
    queryStr = queryStr + "FROM DMIX.{0}) ".format(currency)
    queryStr = queryStr + "SELECT DMIX.{0}.DATE_TXT, DMIX.{0}.OPEN, ".format(currency)
    queryStr = queryStr + "RUNNING.TWELVEHOUR, "
    queryStr = queryStr + "RUNNING.TWELVEHOUR + STDDEVTB.TWELVEHOUR, "
    queryStr = queryStr + "RUNNING.TWELVEHOUR - STDDEVTB.TWELVEHOUR, "
    queryStr = queryStr + "RUNNING.TWELVEHOUR + 2 * STDDEVTB.TWELVEHOUR, "
    queryStr = queryStr + "RUNNING.TWELVEHOUR - 2 * STDDEVTB.TWELVEHOUR, "
    queryStr = queryStr + "RUNNING.ALLTIME, "
    queryStr = queryStr + "RUNNING.ALLTIME + STDDEVTB.ALLTIME, "
    queryStr = queryStr + "RUNNING.ALLTIME - STDDEVTB.ALLTIME, "
    queryStr = queryStr + "RUNNING.ALLTIME + 2 * STDDEVTB.ALLTIME, "
    queryStr = queryStr + "RUNNING.ALLTIME - 2 * STDDEVTB.ALLTIME "
    queryStr = queryStr + "FROM DMIX.{0} ".format(currency)
    queryStr = queryStr + "INNER JOIN RUNNING ON DMIX.{0}.DATE_TXT = RUNNING.DATE_TXT ".format(currency)
    queryStr = queryStr + "INNER JOIN STDDEVTB ON DMIX.{0}.DATE_TXT = STDDEVTB.DATE_TXT".format(currency)
    queryStr = queryStr + " WHERE DMIX.{0}.DATE_TXT >= TO_DATE('{1}-{2}-{3}', 'MM-DD-YYYY')".format(currency, str(startDate.month).rjust(2, '0'), str(startDate.day).rjust(2, '0'), str(startDate.year).rjust(4, '0'))
    queryStr = queryStr + " AND DMIX.{0}.DATE_TXT <= TO_DATE('{1}-{2}-{3}', 'MM-DD-YYYY');".format(currency, str(endDate.month).rjust(2, '0'), str(endDate.day).rjust(2, '0'), str(endDate.year).rjust(4, '0'))
    headers = ["datetime", "actualPrice", "twelveHour", "twelveHourPlus", "twelveHourMinus", "twelveHourPlusPlus", "twelveHourMinusMinus", "allTime", "allTimePlus", "allTimeMinus", "allTimePlusPlus", "allTimeMinusMinus"]
    return query(queryStr, headers)