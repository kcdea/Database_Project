import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dateToTimestamp import dateToTimestamp
from query import query
import data

from navbar import navbar

nav = navbar()

dff = query('SELECT DATE_TXT, OPEN FROM DMIX.BTC '
            'WHERE TIMESTAMP >= {} ORDER BY DATE_TXT ASC'.format(dateToTimestamp(data.DEFAULT_DATE)),
            ['Date', 'Price'])

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Crypto Cracker"),
                        html.P(
                            """\
                            Welcome to Crypto Cracker!\n
                            Navigate through our site to gain powerful insights on the most prominent cryptocurrencies 
                            as well as the currencies of today's most economically influential countries.\n
                            Each page provides an interactive insight into currencies over a period of several years.\n
                            To learn more about each graph and where the data used in this site is from navigate to the 
                            'Info Page' in the top right corner."""
                        )
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.H4("Bitcoin Price for This Year"),
                        dcc.Graph(
                            figure=go.Figure(go.Scatter(
                                x=dff['Date'],
                                y=dff['Price'],
                                mode='lines'
                            ))
                        ),
                    ]
                ),
            ]
        )
    ],
    className="mt-4",
)


def home_page():
    layout = html.Div([nav, body])
    return layout