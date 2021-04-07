import dash_core_components as dcc
import dash_html_components as html

from navbar import navbar


nav = navbar()


def info_page():
    info = html.Div([
        nav,
        html.P('This is the info page for our app, there will be instructions on how to use it as well as info about the data and where it came from')
    ])
    return info

