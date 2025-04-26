## =============== TODO LIST =================== ##
## - Fix the axis labels on graphs one and two - ##
## -             GUI improvement               - ##
## -          Fix font (comic sans?)           - ##
## ============================================= ##

## IMPORT DEPENDENCIES ##
from dash import dash, dcc, html, Input, Output
import pandas as pd
import numpy as np
import os
import plotly.express as px
## ------------------- ##

## File reading code
path = "C:/Users/caste/Desktop/jupyter_workingdirs/bme_finalProject/data/covid19data.csv" ## TODO: pleas find out how to use the working directory to access the data file so we don't keep accessing it manually 😭😭
data = pd.read_csv(path, thousands=",") ## Reads the .csv
data["collection_date"] = pd.to_datetime(data["collection_date"], format="%Y-%m-%d") ## Converts the collection dates to the format
data.sort_values("collection_date", inplace=True) ## Sorts the dates chronologically


## IMPORT FREDOKA FONT || Sidenote: this doesn't work? help? can we replace this with comic sans? :[ ##
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?family=Fredoka"
        "family=Lato:wght@300..700&display=swap",
        "rel": "stylesheet",
    },
]

## App properties
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Analysis Project"

## Main Gui
app.layout = html.Div(
    ## Main Div
    children=[
        ## Title Div
        html.Div(
            html.Center(
                children=[
                    html.P(
                        children="Where's everyone going? Bingo?", className="headerTitle"
                    ),
                    html.H1(
                        children="Super Awesome Data Analysis Project (created in Python with love)", className="header"
                    ),
                    html.P(
                        children="===============================================", className="headerTitle"
                    ),
                ],
                className="header"
            ),
        ),
        ## Date Range Div
        html.Div(
            children=[
                html.P(
                    children="Date Range", className="title"
                ),
                dcc.DatePickerRange(
                    id="dateRange",
                    min_date_allowed=data.collection_date.min().date(),
                    max_date_allowed=data.collection_date.max().date(),
                    start_date=data.collection_date.min().date(),
                    end_date=data.collection_date.max().date(),
                ),
            ],
        ),
        ## Graph One Parameter Div Container
        html.Div(
            children=[
                ## Dropdown Div (State, Graph One)
                html.Div(
                    children=[
                        html.P(
                            children="State (Graph #1)", className="graph1State"
                        ),
                        dcc.Checklist(
                            id="state-filter1",
                            options=np.sort(data.state.unique()),
                            value=["AK"], ## default state
                            className="checkbox",
                            inline=True,
                        ),
                    ],
                ),
                ## Dropdown Div (Attribute, Graph One)
                html.Div(
                    children=[
                        html.P(
                            children="Attribute (Graph #1)", className="attribute1State"
                        ),
                        dcc.Dropdown(
                            id="attribute-filter1",
                            options=[
                                {"label" : attribute, "value" : attribute} for attribute in np.sort(data.columns[2:].unique())
                            ],
                            value="Count LL (All Inpatient)", ## default attribute
                            clearable=False,
                            className="dropdown"
                        ),
                    ],
                ),
            ],
        ),
        ## Graph Two Parameter Div Container
        html.Div(
            children=[
                ## Dropdown Div (State, Graph Two)
                html.Div(
                    children=[
                        html.P(
                            children="State (Graph #2)", className="graph2State"
                        ),
                        dcc.Checklist(
                            id="state-filter2",
                            options=np.sort(data.state.unique()),
                            value=["AK"], ## default state
                            className="checkbox",
                            inline=True,
                        ),
                    ],
                ),
                ## Dropdown Div (Attribute, Graph Two)
                html.Div(
                    children=[
                        html.P(
                            children="Attribute (Graph #2)", className="attribute2State"
                        ),
                        dcc.Dropdown(
                            id="attribute-filter2",
                            options=[
                                {"label" : attribute, "value" : attribute} for attribute in np.sort(data.columns[2:].unique())
                            ],
                            value="Count LL (All Inpatient)", ## default attribute
                            clearable=False,
                            className="dropdown"
                        ),
                    ],
                ),
            ],
        ),
        ## Graph Containers
        html.Div(
           children=[
                html.Div(
                    children=dcc.Graph(
                        id="GraphOne",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="GraphTwo",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",           
        ),
    ],

)

## Main app callback
@app.callback(
    [
        Output(component_id="GraphOne", component_property="figure"),
        Output(component_id="GraphTwo", component_property="figure"),
    ],
    [
        Input(component_id="state-filter1", component_property="value"),
        Input(component_id="attribute-filter1", component_property="value"),
        Input(component_id="state-filter2", component_property="value"),
        Input(component_id="attribute-filter2", component_property="value"),
        Input(component_id="dateRange", component_property="start_date"),
        Input(component_id="dateRange", component_property="end_date"),
    ]
)
## Main app callback function
def update(state1, attribute1, state2, attribute2, startDate, endDate):
    ## Filter Dataset One for graph one
    mask1 = (
        (data.state.isin(state1))
        &(data.collection_date >= startDate)
        & (data.collection_date <= endDate) 
    )
    filteredData1 = data.loc[mask1, :]

    ## Filter Dataset Two for graph two
    mask2 = (
        (data.state.isin(state2))
        &(data.collection_date >= startDate)
        & (data.collection_date <= endDate) 
    )
    filteredData2 = data.loc[mask2, :]

    ## Set up graphs
    chartOne = px.line(
        data_frame = filteredData1,
        x = filteredData1.collection_date,
        y = np.sort(filteredData1[str(attribute1)].apply(pd.to_numeric)),
        color=filteredData1["state"]
    )

    chartTwo = px.line(
        data_frame = filteredData2,
        x = filteredData2.collection_date,
        y = np.sort(filteredData2[str(attribute2)].apply(pd.to_numeric)),  
        color=filteredData2["state"] 
    )

    return chartOne, chartTwo

## Main thread
if __name__ == "__main__":
    app.run(debug=True)