import dash_bootstrap_components as dbc


def navbar():
    nav = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Percent Change", href="/percent_change")),
            dbc.NavItem(dbc.NavLink("Currency Stability", href='/currency_stability')),
            dbc.NavItem(dbc.NavLink("Currency Correlation", href='/currency_correlation')),
            dbc.NavItem(dbc.NavLink("Volatility", href="/volatility")),
            dbc.NavItem(dbc.NavLink('Instability Exchange Rates', href='/instability_exchange_rates')),
            dbc.NavItem(dbc.NavLink("Info Page", href="/info_page"))
        ],
        brand="Home",
        brand_href="/home_page",
        sticky="top",
        color='primary'
    )
    return nav
