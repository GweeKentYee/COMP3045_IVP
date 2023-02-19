from dash import Dash, Input, Output, dcc, callback, dash_table, html
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.Div([
        dcc.Dropdown(
            id = "demo-dropdown",
            options = [
                {'label': '1', 'value':'option1'},
                {'label': '2', 'value':'option2'},
                {'label': '3', 'value':'option3'}
            ],
            value = 'option1',
            multi=False
        ),
    ]),
    dash_table.DataTable(
        id ='tbl'
    )
])


@app.callback(Output("tbl", "data"), Input("demo-dropdown", "value",))
def update_output(value):
    df = pd.read_csv('Dataset/lifeexpectancy.csv')
    if str(value) == "option1":
        df = pd.read_csv('Dataset/lifeexpectancy.csv')
    elif str(value) == "option2":
        df = pd.read_csv('Dataset/drinks.csv')
    elif str(value) == "option3":
        df = pd.read_csv('Dataset/alcoholByCountry2023.csv') 
    return df.to_dict("records")

if __name__ == "__main__":
    app.run_server(debug=True)