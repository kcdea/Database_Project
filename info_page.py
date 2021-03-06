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
        html.P("Percent Change: Demonstrates the correlation, or lack thereof, between the price shifts of two cryptocurrencies"),
        html.P("Currency Stability: Demonstrates the distinction between various methods of calculating the standard deviation of a cryptocurrency, as well as the ability of said methods to demonstrate the volatility of said cryptocurrency."),
        html.P("Currency Correlation: On this page, a function is given to determine the Pearson correlation coefficient between the price  of a particular cryptocurrency of interest (call this currency1) and the price of either a second cryptocurrency, or some real-world currency (other than the US Dollar, which is used as the standard in our data, and which has already seen to have a strong negative correlation to the price of certain cryptocurrencies, such as Bitcoin https://cointelegraph.com/news/bitcoin-vs-usd-why-only-a-weaker-dollar-will-push-btc-above-20-000)."),
        html.P("Volatility: Demonstrates the distinction between various methods of calculating the standard deviation of a cryptocurrency, as well as the ability of said methods to demonstrate the volatility of said cryptocurrency."),
        html.P("Instability: It finds the economicinstability of a country and it's exchange rate during thea specified year a monthly bases."),
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

