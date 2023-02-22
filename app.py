from dash import Dash, Input, Output, dcc, callback, dash_table, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.DARKLY])

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
                    {'label': 'Beer Consumption', 'value':'option1'},
                    {'label': 'Wine Consumption', 'value':'option2'},
                    {'label': 'Spirit Consumption', 'value':'option3'}
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
                    'height': '550px'
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
                    html.Div(id="year-slider"),
                ], 
                style = {
                    'background': '#696969',
                    'height': '550px'
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


@app.callback(Output("data-table", "children"), Output("simple-bar-chart", "figure"), Output("year-slider", "children"), Input("demo-dropdown", "value",))
def update_output(value):
    df = pd.read_csv('Dataset/Beer_Consumption.csv')
    min = df['Year'].min()
    max = df['Year'].max()
    fig = px.histogram(df, x="Alcohol Consumption (Litres)", y="Entity", animation_frame="Year", animation_group="Alcohol Consumption (Litres)", orientation="h")
    if str(value) == "option1":
        df = pd.read_csv('Dataset/Beer_Consumption.csv')
        fig = px.histogram(df, x="Alcohol Consumption (Litres)", y="Entity", orientation="h")
    elif str(value) == "option2":
        df = pd.read_csv('Dataset/Wine_Consumption.csv')
        fig = px.histogram(df, x="Alcohol Consumption (Litres)", y="Entity", orientation="h")
    elif str(value) == "option3":
        df = pd.read_csv('Dataset/Spirit_Consumption.csv')
        fig = px.histogram(df, x="Alcohol Consumption (Litres)", y="Entity", orientation="h")
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
                style_table={'height':420},
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

    year_slider = html.Div(
        [
            dcc.Slider(
                min= min,
                max = max
            )
        ]
    )
    
    return data_table, fig, year_slider
    

if __name__ == "__main__":
    app.run_server(debug=True)