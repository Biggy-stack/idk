from dash import Dash, dcc, html, Input, Output
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    html.H4("COVID-19_Estimated_Patient_Impact_and_Hospital_Capacity_by_State_20250309"),


    html.P("State:"), 
    dcc.Checklist(id="states", options=[
        "CW",
        "AK",
        "AL",
        "AR", 
        "AZ",
        "CA",
        "CO", 
        "CT",
        "DC",
        "DE",
        "FL",
        "GA",
        "HI",
        "IA",
        "ID",
        "IL",
        "IN",
        "KS",
        "KY",
        "LA",
        "MA",
        "MD",
        "ME",
        "MI",
        "MN",
        "MO",
        "MS",
        "MT",
        "NC",
        "ND",
        "NH",
        "NJ",
        "NM",
        "NY",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VA",
        "VT",
        "WA",
        "WI",
        "WV",
        "WY"

], value=["CA", "NY"], inline=True),

    dcc.Graph(id="graph"),
])

@app.callback(
    Output(component_id="graph", component_property="figure"),
    Input("states", "value")
)


def update_line_chart(states):
    data = (
    pd.read_csv("data\\COVID-19_Estimated_Patient_Impact_and_Hospital_Capacity_by_State_20250309.csv")
    .assign(Date=lambda data: pd.to_datetime(data["collection_date"], format="%m/%d/%Y"))
    .sort_values(by="Date")
    )
    mask = data.state.isin(states)
    fig = px.line(data[mask], x= "collection_date", y = "Inpatient Beds Occupied Estimated (All Inpatient)", color='state')
    return fig

if __name__ == "__main__":
    app.run (debug=True) 