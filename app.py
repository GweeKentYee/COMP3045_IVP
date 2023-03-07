from dash import Dash, Input, Output, State, dcc, callback, dash_table, html
from dash_extensions.enrich import DashProxy, MultiplexerTransform
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

app = DashProxy(external_stylesheets=[dbc.themes.DARKLY], transforms=[MultiplexerTransform()])

app.layout = html.Div([
    html.Br(),
    html.Center(
        html.H4(
            "Global Alcohol Statistics Dashboard", 
        )
    ),  
    html.Hr(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id = "demo-dropdown",
                options = [
                    {'label': 'Total Alcohol Consumption', 'value':'option1'},
                    {'label': 'Beer Consumption', 'value':'option2'},
                    {'label': 'Wine Consumption', 'value':'option3'},
                    {'label': 'Spirit Consumption', 'value':'option4'}
                ],
                value = 'option1',
                multi=False,
                style={
                    'color': 'black'
                }
            )
        ], width={
            "size": 3,
            "offset": 1
        })
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Container(
                [
                    html.Br(),
                    dbc.Row([
                        html.Div(id="data-table"),
                    ]),
                ], 
                style = {
                    'background': '#696969',
                    'height': '580px'
                }
            )
        ], width={
            "size": 5,
            "offset": 1
        }),
        dbc.Col([
            dbc.Container(
                [
                    html.Br(),
                    dcc.Graph(id="simple-bar-chart"),
                    html.Br(),
                    html.Div([
                        html.Label("Year: 2019", id = "year-label"),
                        dcc.Slider(
                            id = "year-slider",
                            step = 1,
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ],id="year-slider-div"),
                ], 
                style = {
                    'background': '#696969',
                    'height': '580px'
                }
            )
        ], width={
            "size": 5,
        }),
    ]),
    html.Hr(),
    dbc.Col([
        dbc.Container([
            dbc.Row([
                
            ]),
        ]),
    ]
    ),
    
])


@app.callback(Output("data-table", "children"), Output("year-slider", "min"), Output("year-slider", "max"), Output("year-slider", "marks"), Output("year-slider", "step"), Output("year-slider", "value"), Input("demo-dropdown", "value",))
def update_output(value):

    # fig = px.histogram(df_10, x="Alcohol Consumption (Litres)", y="Entity", orientation="h", barmode="group")
    # fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    global df
    min_year = 1960
    max_year = 2019
    year_value = 2019
    marks={
            1960: {
                'label': '1960',
                'style': {
                    'color': '#FFFFFF'
                }
            },
            2019: {
                'label': '2019',
                'style': {
                    'color': '#FFFFFF'
                }
            }
    }
    step = 1

    if str(value) == "option1":
        df = pd.read_csv('Dataset/total-alcohol-consumption.csv')
        min_year = 2000
        max_year = 2018
        year_value = 2018
        marks={
            2000: {
                'label': '2000',
                'style': {
                    'color': '#FFFFFF'
                }
            },
            2018: {
                'label': '2018',
                'style': {
                    'color': '#FFFFFF'
                }
            }
        }
        step = 5

    elif str(value) == "option2":
        df = pd.read_csv('Dataset/Beer_Consumption.csv')

    elif str(value) == "option3":
        df = pd.read_csv('Dataset/Wine_Consumption.csv')

    elif str(value) == "option4":
        df = pd.read_csv('Dataset/Spirit_Consumption.csv')

    columns = []
    for col in df.columns:
        col_options = {"name": col, "id": col}
        for value in df[col]:
            if not (isinstance(value, str)):
                col_options["type"] = "numeric"
        columns.append(col_options)

    data_table = html.Div(
        [
            dash_table.DataTable(
                data=df.to_dict("records"),
                columns=columns,
                style_table={'height':480},
                style_header={'backgroundColor':'rgb(30, 30, 30)','color':'#FFFFFF', 'fontWeight': 'bold'},
                style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                style_cell={'textAlign':'center', 'font_size': '12px','whiteSpace':'normal','height':'auto', 'width': 'auto', 'maxWidth': "10px"},
                style_filter={'backgroundColor': 'rgb(50, 50, 50)'},
                fixed_rows={'headers': True, 'data':0},
                sort_action='native',
                filter_action='native'
            )
        ]
    )
    
    return data_table, min_year, max_year, marks, step, year_value

@app.callback(Output('year-label', 'children'), Output('simple-bar-chart', 'figure'), Input('year-slider', 'value'), State("demo-dropdown", "value"), prevent_initial_call=True)
def display_value(year, value):
    label = 'Year: {}'.format(year)
    
    if str(value) == "option1":
        df = pd.read_csv('Dataset/total-alcohol-consumption.csv')
        df_10 = df[df['Year'] == year].sort_values('Alcohol Consumption (Litres)', ascending = False).head(10)
        data = [
            go.Bar(x = df_10["Alcohol Consumption (Litres)"], y=df_10["Entity"], orientation="h", name='Alcohol'),
        ]

        layout = go.Layout(
            {
                "title": "Top 10 Alcohol consumption per person by countries, {}".format(year),
                "yaxis": {"title":"Country"},
                "xaxis": {"title":"Consumption by Litres"},
            },
        )
    elif str(value) == "option2":
        df = pd.read_csv('Dataset/Beer_Consumption.csv')
        df_10 = df[df['Year'] == year].sort_values('Alcohol Consumption (Litres)', ascending = False).head(10)
        data = [
            go.Bar(x = df_10["Alcohol Consumption (Litres)"], y=df_10["Entity"], orientation="h", name='Alcohol'),
            go.Bar(x = df_10["Beer Consumption (Litres)"], y=df_10["Entity"], orientation="h", name='Beer'),
        ]

        layout = go.Layout(
            {
                "title": "Top 10 Beer consumption per person by countries, {}".format(year),
                "yaxis": {"title":"Country"},
                "xaxis": {"title":"Consumption by Litres"},
                "barmode": "group"
            },
        )
    elif str(value) == "option3":
        df = pd.read_csv('Dataset/Wine_Consumption.csv')
        df_10 = df[df['Year'] == year].sort_values('Alcohol Consumption (Litres)', ascending = False).head(10)
        data = [
            go.Bar(x = df_10["Alcohol Consumption (Litres)"], y=df_10["Entity"], orientation="h", name='Alcohol'),
            go.Bar(x = df_10["Wine Consumption (Litres)"], y=df_10["Entity"], orientation="h", name='Wine'),
        ]

        layout = go.Layout(
            {
                "title": "Top 10 Wine consumption per person by countries, {}".format(year),
                "yaxis": {"title":"Country"},
                "xaxis": {"title":"Consumption by Litres"},
                "barmode": "group"
            },
        )
    elif str(value) == "option4":
        df = pd.read_csv('Dataset/Spirit_Consumption.csv')
        df_10 = df[df['Year'] == year].sort_values('Alcohol Consumption (Litres)', ascending = False).head(10)
        data = [
            go.Bar(x = df_10["Alcohol Consumption (Litres)"], y=df_10["Entity"], orientation="h", name='Alcohol'),
        ]

        layout = go.Layout(
            {
                "title": "Top 10 Spirit consumption per person by countries, {}".format(year),
                "yaxis": {"title":"Country"},
                "xaxis": {"title":"Consumption by Litres"},
            },
        )

    fig = go.Figure(data,layout)
    fig.update_layout(yaxis=dict(autorange="reversed"))

    return label, fig
    
if __name__ == "__main__":
    app.run_server(debug=True)