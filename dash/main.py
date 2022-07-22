"""
Dashboard application example.
After docker compose up visit http://127.0.0.1:8050/ in your web browser.
"""

import os
import pandas as pd
from dash import Dash, html, dcc
from deck import plot_stacked_area, plot_time_series, plot_bar

DEBUG = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
os.environ['FLASK_ENV'] = 'development'

app = Dash(__name__)

# Data Source
data = pd.read_excel("data/claims.xlsx", engine='openpyxl')

# Preprocessing & Clean up
data = data[~data['MONTH'].isin([201900, 202007])]  # obviously this is something wrong for these periods
# combine together similar specialties (from 900 unique specialties to 785)
data['CLAIM_SPECIALTY'] = data['CLAIM_SPECIALTY'].apply(
    lambda x: x.upper() if isinstance(x, str) else float('nan'))
data['MONTH'] = pd.to_datetime(data['MONTH'], format='%Y%m')  # use proper date

# Line Chart
fig1 = plot_time_series(data)
# Stacked Area Chart
fig2 = plot_stacked_area(data)
# Bar Chart
fig3 = plot_bar(data)

app.layout = html.Div(children=[
    html.H1(children='Claims Dashboard'),

    html.Div(children='''
        Claims are expenses that insurance companies have to pay for medical services provided to patients.
    '''),

    html.H2("Data Quality Check"),
    html.Div("There are some negative values in data. It could be money returns."),
    html.Div("Probably something wrong for periods [201900, 202007]. We skip them."),
    html.Div("It is recommended to use some semantic associations "
             "rules for such filed as SERVICE_CATEGORY, CLAIM_SPECIALTY. "
             "By using just an uppercase for CLAIM_SPECIALTY we can reduce unique values by -13%."),

    dcc.Graph(
        id='example-graph-1',
        figure=fig1
    ),

    html.Div(children=[
        dcc.Graph(
            id='example-graph-2',
            figure=fig2,
            style={'display': 'inline-block', "margin-left": "auto", "margin-right": "auto"}),

        dcc.Graph(
            id='example-graph-3',
            figure=fig3,
            style={'display': 'inline-block', "margin-left": "auto", "margin-right": "auto"})
    ])
])

if __name__ == '__main__':
    app.run_server(debug=DEBUG, host='0.0.0.0', port=8050)
