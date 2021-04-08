import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from data import df, available_indicators

from navbar import navbar

nav = navbar()

graph_body = html.Div([
    html.Div([
        dcc.Dropdown(
            id='xaxis-column',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='Fertility rate, total (births per woman)'
            ),
        dcc.RadioItems(
            id='xaxis-type',
            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            value='Linear',
            labelStyle={'display': 'inline-block'}
            ),
        dcc.Dropdown(
            id='yaxis-column',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='Life expectancy at birth, total (years)'
            ),
        dcc.RadioItems(
            id='yaxis-type',
            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            value='Linear',
            labelStyle={'display': 'inline-block'}
            )],
        style={'width': '30%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='indicator-graphic'),
        dcc.Slider(
            id='year--slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=df['Year'].max(),
            marks={str(year): str(year) for year in df['Year'].unique()},
            step=None
        )],
        style={'width': '65%', 'display': 'inline-block'})])


def graph_page():
    layout = html.Div([nav, graph_body])
    return layout