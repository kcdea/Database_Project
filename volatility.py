import datetime
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from query import query
from navbar import navbar
import data


def volatility(currency, startDate = datetime.date(2012, 1, 1), endDate = datetime.date.today()):
    queryStr = "WITH RUNNING (DATE_TXT, ALLTIME, TWELVEHOUR) AS "
    queryStr = queryStr + "(SELECT DMIX.{0}.DATE_TXT, AVG(DMIX.{0}.OPEN) OVER (ORDER BY DMIX.{0}.DATE_TXT), AVG(DMIX.{0}.OPEN) OVER (ORDER BY DMIX.{0}.DATE_TXT ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) ".format(currency)
    queryStr = queryStr + "FROM DMIX.{0}".format(currency)
    queryStr = queryStr + " WHERE DMIX.{0}.DATE_TXT >= TO_DATE('{1}-{2}-{3}', 'MM-DD-YYYY')".format(currency, str(startDate.month).rjust(2, '0'), str(startDate.day).rjust(2, '0'), str(startDate.year).rjust(4, '0'))
    queryStr = queryStr + " AND DMIX.{0}.DATE_TXT <= TO_DATE('{1}-{2}-{3}', 'MM-DD-YYYY')".format(currency, str(endDate.month).rjust(2, '0'), str(endDate.day).rjust(2, '0'), str(endDate.year).rjust(4, '0'))
    queryStr = queryStr + "), "
    queryStr = queryStr + "STDDEVTB (DATE_TXT, ALLTIME, TWELVEHOUR) AS "
    queryStr = queryStr + "(SELECT DMIX.{0}.DATE_TXT, STDDEV(DMIX.{0}.OPEN) OVER (ORDER BY DMIX.{0}.DATE_TXT), STDDEV(DMIX.{0}.OPEN) OVER (ORDER BY DMIX.{0}.DATE_TXT ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) ".format(currency)
    queryStr = queryStr + "FROM DMIX.{0}".format(currency)
    queryStr = queryStr + " WHERE DMIX.{0}.DATE_TXT >= TO_DATE('{1}-{2}-{3}', 'MM-DD-YYYY')".format(currency, str(startDate.month).rjust(2, '0'), str(startDate.day).rjust(2, '0'), str(startDate.year).rjust(4, '0'))
    queryStr = queryStr + " AND DMIX.{0}.DATE_TXT <= TO_DATE('{1}-{2}-{3}', 'MM-DD-YYYY')".format(currency, str(endDate.month).rjust(2, '0'), str(endDate.day).rjust(2, '0'), str(endDate.year).rjust(4, '0'))
    queryStr = queryStr + ") "
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
    queryStr = queryStr + " AND DMIX.{0}.DATE_TXT <= TO_DATE('{1}-{2}-{3}', 'MM-DD-YYYY')".format(currency, str(endDate.month).rjust(2, '0'), str(endDate.day).rjust(2, '0'), str(endDate.year).rjust(4, '0'))
    headers = ["datetime", "actualPrice", "twelveHour", "twelveHourPlus", "twelveHourMinus", "twelveHourPlusPlus", "twelveHourMinusMinus", "allTime", "allTimePlus", "allTimeMinus", "allTimePlusPlus", "allTimeMinusMinus"]
    return query(queryStr, headers)



def volatility_page():
    layout = html.Div([
        navbar(),
        dbc.Row([
            dbc.Col([html.H6('Crypto-Currency:'),
                     dcc.Dropdown(
                         id='volatility-currency',
                         options=[{'label': i, 'value': i} for i in data.CURRENCIES],
                         value='BTC'
                     ),
                     html.Div([
                         html.Div([
                             html.H6('Start Date:'),
                             dcc.DatePickerSingle(
                                 id='volatility-start',
                                 min_date_allowed=data.MIN_DATE,
                                 max_date_allowed=data.MAX_DATE,
                                 date=data.DEFAULT_DATE
                             )],
                             style={'display': 'inline-block'}),
                         html.Div([
                             html.H6('End Date:'),
                             dcc.DatePickerSingle(
                                 id='volatility-end',
                                 min_date_allowed=data.MIN_DATE,
                                 max_date_allowed=data.MAX_DATE,
                                 date=data.MAX_DATE
                             )],
                             style={'display': 'inline-block'})]),
                     dcc.RadioItems(
                         id='toggle',
                         options=[{'label': i, 'value': i} for i in ['last 12 hours', 'All time']],
                         value='last 12 hours',
                         labelStyle={'display': 'inline-block'}
                     )],
                    md=4),
            dbc.Col([
                dcc.Graph(id='volatility-graph'),
                html.P(
                    """\
                    This page demonstrates the distinction between various methods of calculating the standard deviation of a cryptocurrency, as well as the ability of said methods to demonstrate the volatility of said cryptocurrency.\n
                    Historically, stock traders have used the standard deviation of a stock's price in a preceding timeframe as a means of determining its "volatility", which is best defined as its range of probable price shifts in an upcoming market segment. 
                    Cryptocurrencies, like stocks, are also investments, and are often referred to as some of the most volatile investments traders can place their money in. Of course, as with any investment, high risks can yield high rewards, but awareness of these risks is critical to making an informed decision. \n
                    The graph shown above is able to make use of one of two running averages to demonstrate the standard deviation's ability to predict price shifts. In "All time" mode, a running average of all data within the specified range is used to determine the standard deviation at a given point. This prevents significant changes in predictions from occurring due to price spikes, but can become wildly inaccurate over long intervals.
                    "Last 12 hours" mode, on the other hand, utilizes a running average of the 12 hours of data preceding a given data point to determine the standard deviation. This allows the standard deviation to "forget" past trends to enable more accurate short-term predictions. However, this can result in gross overestimations of future value during moments of extreme volatility. \n
                    Regardless of which mode is chosen, the graph displays six lines over the selected time interval. The most jagged and erratic of these is the actual price graph of the currency, similarly to that shown on this website's homepage. Surrounding it are five lines, four of which appear to nearly mirror about a centerline. The "centerline" is the running average for the selected mode at a given data points.
                    Above and below this average are the first standard deviations from the mean. Due to the mathematical properties of standard deviation calculations and limitations of reliance on historical data, it can be assumed that there is a 68.1% chance for the following price point to fall within this range. \n
                    The two lines surrounding the first standard deviations are the second standard deviations. It can be assumed that there is a 95.3% chance for the following price point to fall within this range. \n
                    Key concepts covered for this query included the use of the Oracle SQL "OVER" clause to generate running averages, the use of the SQL "STDDEV" command to determine the standard deviation of a given data set, and combination of these results to generate appropriate statistical ranges for the data."""
                )
            ])
        ])
    ])
    return layout
