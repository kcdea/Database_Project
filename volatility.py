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
    print(queryStr)
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
                dcc.Graph(id='volatility-12-hours-graph'),
                dcc.Graph(id='volatility-all-time-graph')
            ])
        ])
    ])
    return layout
