import dash_bootstrap_components as dbc


def navbar():
    nav = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Info Page", href="/info_page")),
            dbc.NavItem(dbc.NavLink("Graph Page", href="/graph_page")),
            dbc.NavItem(dbc.NavLink("Complex Queries", href="/complex_queries"))
        ],
        brand="Home",
        brand_href="/home_page",
        sticky="top",
    )
    return nav
