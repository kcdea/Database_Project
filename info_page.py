import dash_core_components as dcc
import dash_html_components as html

from navbar import navbar


nav = navbar()


def info_page():
    info = html.Div([
        nav,
        html.H1("Information"),
        html.H2("How to use:"),
        html.P('    Each page is tied to a query. Use the navigation bar to expolre the different queries available.On each page, there will be a graph and a series of dropdown menus, slides, and other interactive functions. Choose the data you wish to see and wait to see how the graph changes in response.'),
        html.H2("Queries:"),
        html.P("Percent Change: Expolres blah"),
        html.P("Currency Stability: Expolres blah"),
        html.P("Currency Correlation: Expolres blah"),
        html.P("Volatility: Expolres blah"),
        html.P("Instability: Expolres blah"),
        html.H2("Our Data:"),
        html.P("Our data was collected from many places"),
        html.Label(['Exchange Rates: ', html.A('International Monetary Fund', href='https://www.imf.org/external/np/fin/ert/GUI/Pages/CountryDataBase.aspx')]),
        html.P(),
        html.Label(['Crypto data(BAT, DASH, ETC, NEO, OMG, TRX) Bitfinex via: ', html.A('cryptodatadownload', href='cryptodatadownload.com')]),
        html.P(),
        html.Label(['Crypto data(XRP) Bitstamp via: ', html.A('cryptodatadownload', href='cryptodatadownload.com')]),
        html.P(),
        html.Label(['Crypto data(BTC, ETH, LTC, ZEC) Gemini via: ', html.A('cryptodatadownload', href='cryptodatadownload.com')]),
        html.P(),
        html.Label(['Education Spending, Literacy Rates, People On the Internet: ', html.A('Our World In Data', href='https://ourworldindata.org/')]),
        html.P(),
        html.Label(['Economic Uncertainty: ', html.A('Policy Uncertainty', href='https://www.policyuncertainty.com/all_country_data.html')])
    ])
    return info

