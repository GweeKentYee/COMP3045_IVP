from dash import Dash, Input, Output, State, dcc, callback, dash_table, html
from dash_extensions.enrich import DashProxy, MultiplexerTransform
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

pd.options.plotting.backend = "plotly"

app = DashProxy(external_stylesheets=[dbc.themes.DARKLY], transforms=[MultiplexerTransform()])

dataset = pd.read_csv('Dataset/rate_of_premature_death.csv')

labels = dataset['Entity'].unique()

country = [{'label': labels[i], 'value':labels[i]} for i in range(len(labels))]

app.layout = html.Div([
    html.Br(),
    html.Center(
        html.H3(
            "Global Alcohol's Risk Statistics Dashboard", 
        )
    ),  
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.H4(
                "Alcohol Consumption", 
            )
        ], width = {
            "offset" : 1
        })
    ]),
    dbc.Row([
        dbc.Col([
            html.Br(),
            dcc.Dropdown(
                id = "alcohol-dropdown",
                options = [
                    {'label': 'Total Alcohol Consumption', 'value':'option1'},
                    {'label': 'Beer Consumption', 'value':'option2'},
                    {'label': 'Wine Consumption', 'value':'option3'},
                    {'label': 'Spirit Consumption', 'value':'option4'}
                ],
                value = 'option1',
                multi=False,
                clearable = False,
                style={
                    'color': 'black'
                }
            )
        ], width={
            "size": 3,
            "offset": 1
        }),
        dbc.Col([
            html.Br(),
            dcc.Checklist(
                ['Choropleth Map'],
                id = "choropleth-checkbox-1",
                inputStyle={
                    "margin-right": "6px",
                    "margin-top": "13px"
                },
                labelStyle={
                    "font-size": 18
                },
            ),
        ])
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
    dbc.Row([
        dbc.Col([
            html.H4(
                "Health Impact of Alcohol", 
            )
        ], width = {
            "offset" : 1
        })
    ]),
    dbc.Row([
        dbc.Col([
            html.Br(),
            dcc.Dropdown(
                id = "risk-dropdown",
                options = [
                    {'label': 'Death By Risk Factor', 'value':'option1'},
                    {'label': 'Deaths to Alcohol By Age Group', 'value':'option2'},
                ],
                value = 'option1',
                clearable = False,
                multi=False,
                style={
                    'color': 'black'
                }
            )
        ], width={
            "size": 3,
            "offset": 1
        }),
        dbc.Col([
            html.Br(),
            dcc.Dropdown(
                id = "country-dropdown",
                options = country,
                value = "Afghanistan",
                clearable = False,
                multi=False,
                style={
                    'color': 'black'
                }
            )
        ], width={
            "size": 2,
        })
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Container([
                html.Br(),
                dcc.Graph(id="line-graph"),
            ], 
            style = {
                'background': '#696969',
                'height': '495px'
            }),
        ], 
        width={
            "size": 10,
            "offset": 1
        }),
        dbc.Col([
            html.Hr()
        ], 
        width={
            "size": 10,
            "offset": 1
        }),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id = "checkbox-risk-dropdown",
                options = [
                    {'label': 'Disease Burden from Alcohol Use', 'value':'option1'},
                    {'label': 'Rate of Premature Death Due to Alcohol', 'value':'option2'},
                ],
                value = 'option1',
                clearable = False,
                multi=False,
                style={
                    'color': 'black'
                }
            )
        ], width={
            "size": 3,
            "offset": 1
        }),
        dbc.Col([
            dbc.Button("Add Countries", id="open", n_clicks=0, color="info"),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Choose Countries to Show")),
                    dbc.ModalBody([
                    dcc.Checklist(
                        options = country,
                        value = ["Afghanistan", "Algeria"],
                        id = "country-checklist",
                        inputStyle={
                            "margin-right": "6px"
                        },
                        labelStyle={
                            "display": "block", 
                            "margin": "5px"
                        },
                    )
                    ]),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id="modal",
                centered=True,
                scrollable=True,
                is_open=False,
            ),
        ], width={
            "size": 2,
        }),
        dbc.Col([
            dcc.Checklist(
                ['Choropleth Map'],
                id = "choropleth-checkbox-2",
                inputStyle={
                    "margin-right": "6px",
                    "margin-top": "13px"
                },
                labelStyle={
                    "font-size": 18
                },
            )
        ])
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Container([
                html.Br(),
                dcc.Graph(id="checkbox-line-graph"),
                html.Br(),
                html.Div([
                    html.Label("Year: 2019", id = "map-year-label"),
                    dcc.Slider(
                        id = "map-year-slider",
                        step = 1,
                        min = 1990,
                        max = 2019,
                        value = 2019,
                        marks={
                            1990: {
                                'label': '1990',
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
                        },
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ],id="map-year-slider-div"),
            ], 
            style = {
                'background': '#696969',
                'height': '580px'
            }),
        ], 
        width={
            "size": 10,
            "offset": 1
        })
    ]),
    html.Br()
])


@app.callback(Output("data-table", "children"), Output("year-slider", "min"), Output("year-slider", "max"), Output("year-slider", "marks"), Output("year-slider", "step"), Output("year-slider", "value"), Input("alcohol-dropdown", "value",))
def update_output(value):

    # fig = px.histogram(df_10, x="Alcohol Consumption (Litres)", y="Entity", orientation="h", barmode="group")
    # fig.update_layout(yaxis={'categoryorder': 'total ascending'})
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

@app.callback(Output('year-label', 'children'), Output('simple-bar-chart', 'figure'), Input('year-slider', 'value'), Input('choropleth-checkbox-1', 'value'), State("alcohol-dropdown", "value"), prevent_initial_call=True)
def display_value(year, choropleth, value):
    label = 'Year: {}'.format(year)
    if choropleth == None or choropleth == []:
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
    else:
        if str(value) == "option1":
            df = pd.read_csv('Dataset/total-alcohol-consumption.csv')
            df_year = df[df['Year'] == year]
            data = go.Choropleth(
                locations= df_year['Code'],
                z = df_year['Alcohol Consumption (Litres)'],
                text = df_year['Entity'],
                colorscale='reds',
                autocolorscale=False,
                marker_line_color = 'darkgray',
                marker_line_width = 0.5,
                colorbar_title = 'Litres',
                colorbar_thickness= 15,
            )

            layout = go.Layout(
                {
                    "title": "Alcohol consumption per person, {}".format(year),
                },
            )
        elif str(value) == "option2":
            df = pd.read_csv('Dataset/Beer_Consumption.csv')
            df_year = df[df['Year'] == year]
            data = go.Choropleth(
                locations= df_year['Code'],
                z = df_year['Alcohol Consumption (Litres)'],
                text = df_year['Entity'],
                colorscale='reds',
                autocolorscale=False,
                marker_line_color = 'darkgray',
                marker_line_width = 0.5,
                colorbar_title = 'Litres',
                colorbar_thickness= 15,
            )

            layout = go.Layout(
                {
                    "title": "Beer (Alcohol) consumption per person, {}".format(year),
                },
            )
        elif str(value) == "option3":
            df = pd.read_csv('Dataset/Wine_Consumption.csv')
            df_year = df[df['Year'] == year]
            data = go.Choropleth(
                locations= df_year['Code'],
                z = df_year['Alcohol Consumption (Litres)'],
                text = df_year['Entity'],
                colorscale='reds',
                autocolorscale=False,
                marker_line_color = 'darkgray',
                marker_line_width = 0.5,
                colorbar_title = 'Litres',
                # colorbar_orientation='h',
                # colorbar_y=-1.0,
                colorbar_thickness= 15,
            )

            layout = go.Layout(
                {
                    "title": "Wine (Alcohol) consumption per person, {}".format(year),
                },
            )
        elif str(value) == "option4":
            df = pd.read_csv('Dataset/Spirit_Consumption.csv')
            df_year = df[df['Year'] == year]
            data = go.Choropleth(
                locations= df_year['Code'],
                z = df_year['Alcohol Consumption (Litres)'],
                text = df_year['Entity'],
                colorscale='reds',
                autocolorscale=False,
                marker_line_color = 'darkgray',
                marker_line_width = 0.5,
                colorbar_title = 'Litres',
                # colorbar_orientation='h',
                # colorbar_y=-1.0,
                colorbar_thickness= 15,
            )

            layout = go.Layout(
                {
                    "title": "Spirit (Alcohol) consumption per person, {}".format(year),
                },
            )

        fig = go.Figure(data,layout)

    return label, fig

@app.callback(Output('line-graph', 'figure'), Input("risk-dropdown", "value",), Input("country-dropdown", "value",))
def display_value(value, country):
    if str(value) == "option1":
        df = pd.read_csv('Dataset/death_by_risk_factor.csv')
        df_country = df[df['Entity'] == country]
        column_header = list(df.columns)
        del column_header[0:3]
        fig = df_country.plot(title = "Death By Risk Factor, {} (1990 - 2019)".format(country), labels= dict(index = "Year", value = "Cases", variable = "Risk Factor"), x='Year', y=column_header)
    elif str(value) == "option2":
        df = pd.read_csv('Dataset/deaths_to_alcohol_use_by_age.csv')
        df_country = df[df['Entity'] == country]
        column_header = list(df.columns)
        del column_header[0:3]
        fig = df_country.plot(title = "Deaths To Alcohol by Age Group, {} (1990 - 2019)".format(country), labels= dict(index = "Year", value = "Cases", variable = "Age Group"), x='Year', y=column_header)     

    return fig

@app.callback(Output('checkbox-line-graph', 'figure'), Input("checkbox-risk-dropdown", "value",), Input("country-checklist", "value",), Input('choropleth-checkbox-2', 'value'), Input('map-year-slider', 'value'))
def display_value(value, country, choropleth, year):
    if choropleth == None or choropleth == []:
        if str(value) == "option1":
            df = pd.read_csv('Dataset/alcohol_DALY.csv')
            mask = df.Entity.isin(country)
            try:
                fig = px.line(df[mask], 
                    x="Year", y="DALYs", color='Entity',
                    labels={
                        "Entity": "Country"
                    },
                    title="Disease Burden from Alcohol Use (1990 - 2019)")
            except:
                fig = px.line(df[mask], 
                    x="Year", y="DALYs", color='Entity',
                    labels={
                        "Entity": "Country"
                    },
                    title="Disease Burden from Alcohol Use (1990 - 2019)")
        elif str(value) == "option2":
            df = pd.read_csv('Dataset/rate_of_premature_death.csv')
            mask = df.Entity.isin(country)
            try:
                fig = px.line(df[mask], 
                    x="Year", y="Rate", color='Entity',
                    labels={
                        "Entity": "Country"
                    },
                    title="Rate of Premature Death Due to Alcohol (1990 - 2019)")
            except:
                fig = px.line(df[mask], 
                    x="Year", y="Rate", color='Entity',  
                    labels={
                        "Entity": "Country"
                    },
                    title="Rate of Premature Death Due to Alcohol (1990 - 2019)")
    else:
        if str(value) == "option1":
            df = pd.read_csv('Dataset/alcohol_DALY.csv')
            df_year = df[df['Year'] == year]
            data = go.Choropleth(
                locations= df_year['Code'],
                z = df_year['DALYs'],
                text = df_year['Entity'],
                colorscale='reds',
                autocolorscale=False,
                marker_line_color = 'darkgray',
                marker_line_width = 0.5,
                colorbar_title = 'DALY',
                # colorbar_orientation='h',
                # colorbar_y=-1.0,
                colorbar_thickness= 30,
            )

            layout = go.Layout(
                {
                    "title": "Disease Burden from Alcohol Use, {}".format(year),
                },
            )
        elif str(value) == "option2":
            df = pd.read_csv('Dataset/rate_of_premature_death.csv')
            df_year = df[df['Year'] == year]
            data = go.Choropleth(
                locations= df_year['Code'],
                z = df_year['Rate'],
                text = df_year['Entity'],
                colorscale='reds',
                autocolorscale=False,
                marker_line_color = 'darkgray',
                marker_line_width = 0.5,
                colorbar_title = 'Death',
                # colorbar_orientation='h',
                # colorbar_y=-1.0,
                colorbar_thickness= 30,
            )

            layout = go.Layout(
                {
                    "title": "Rate of Premature Death Due to Alcohol, {}".format(year),
                },
            )
        fig = go.Figure(data,layout)

    return fig

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(Output('map-year-slider', 'disabled'),
             [Input('choropleth-checkbox-2', 'value')])
def set_button_enabled_state(choropleth):
    if choropleth == None or choropleth == []:
        return True
    else:
        return False
    
@app.callback(Output('open', 'disabled'),
             [Input('choropleth-checkbox-2', 'value')])
def set_button_enabled_state(choropleth):
    if choropleth == None or choropleth == []:
        return False
    else:
        return True
    
if __name__ == "__main__":
    app.run_server(debug=True)