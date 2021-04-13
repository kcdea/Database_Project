from query import query

# currency1: any cryptocurrency
# currency2: any other cryptocurrency, or any currency other than USD
# crypto: boolean value that is True is currency2 is a cryptocurrency, False if currency2 is not a cryptocurrency
def correlationCoef(currency1, currency2, crypto):
        queryStr = ""
        if(crypto):
                queryStr = "SELECT CORR(DMIX." + currency1 + ".open, DMIX." + currency2 + ".open) FROM DMIX." + currency1 + " JOIN DMIX." + currency2 + " ON DMIX." + currency1 + ".timestamp = DMIX." + currency2 + ".timestamp"
        else:
                queryStr = "SELECT CORR(crypto_price, " + currency2 + ") FROM DMIX.EXCHANGERATES NATURAL JOIN (SELECT date_txt, AVG(DMIX." + currency1 + ".open) AS crypto_price FROM DMIX." + currency1 + " GROUP BY date_txt)"
        title = 'CorrelationCoefficient'
        headers = [title]
        return query(queryStr, headers)
# returns correlation coefficient (scalar value) between currency1 and currency2