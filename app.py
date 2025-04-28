## =============== TODO LIST =================== ##
## - Fix the axis labels on graphs one and two - ##
## -             GUI improvement               - ##
## -          Fix font (comic sans?)           - ##
## ============================================= ##

## IMPORT DEPENDENCIES ##
from dash import dash, dcc, html, Input, Output, callback, ctx
import pandas as pd
import numpy as np
import os
import plotly.express as px
import datetime
import io
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
                        children="Version 0.0.2", className="headerTitle"
                    ),
                    html.P(
                        children="me when queen bee infects and kills all my employees during the qliphoth meltdown", className="headerTitle"
                    ),
                    html.H1(
                        children="Data Analysis Project of Doom and Despair", className="header"
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
            html.Center(
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
        ),
        ## Graph Parameter Container
        html.Div(
            children=[
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
                    style={
                        'flex': 1,
                        'padding': '10px'
                    },
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
                    style={
                        'flex': 1,
                        'padding': '10px'
                    },
                ),            
            ],
            style={
                'display': 'flex',
                'justifyContent': 'space-between'
            },   
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
                    style={
                        'flex': 1,
                        'padding': '10px'
                    },
                ),
                html.Div(
                    children=dcc.Graph(
                        id="GraphTwo",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                    style={
                        'flex': 1,
                        'padding': '10px'
                    },
                ),
            ],
            className="wrapper",  
            style={
                'display': 'flex',
                'justifyContent': 'space-between'
            },  
        ),
        ## Save Button Container
        html.Div(
            html.Center(
                children = [
                    html.Button('Download Graphs', id='download_graphs', n_clicks=0),
                    dcc.Download(id="download1"),
                    dcc.Download(id="download2"),       
                ],
            ),
            className="download",
        ),
    ],
)

## Main app callback
@app.callback(
    [
        Output(component_id="GraphOne", component_property="figure"),
        Output(component_id="GraphTwo", component_property="figure"),
        Output(component_id="download1", component_property="data"),
        Output(component_id="download2", component_property="data")
    ],
    [
        Input(component_id="state-filter1", component_property="value"),
        Input(component_id="attribute-filter1", component_property="value"),
        Input(component_id="state-filter2", component_property="value"),
        Input(component_id="attribute-filter2", component_property="value"),
        Input(component_id="dateRange", component_property="start_date"),
        Input(component_id="dateRange", component_property="end_date"),
        Input(component_id="download_graphs", component_property="n_clicks")
    ]
)
## Main app callback function
def update(state1, attribute1, state2, attribute2, startDate, endDate, n_clicks):
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
        color=filteredData1["state"],
        labels={'collection_date': "Date", 'y': attribute1},
        title=f'Graph One: {attribute1} from {startDate} to {endDate}.'
    )

    chartTwo = px.line(
        data_frame = filteredData2,
        x = filteredData2.collection_date,
        y = np.sort(filteredData2[str(attribute2)].apply(pd.to_numeric)),  
        color=filteredData2["state"] ,
        labels={'collection_date': "Date", 'y': attribute2},
        title=f'Graph Two: {attribute2} from {startDate} to {endDate}.'
    )

    ## i don't like this code that i wrote! maybe we can split it into different callback? idk! i tried and it hurt my head!
    ## i don't remember how to make it reference the graph outside of this function!!!! so for now, this hack works :)

    ## Downloading code for downloading the files that you want to download onto your computer that you're using to download the files
    if ctx.triggered_id == "download_graphs":
        downloadDate = datetime.datetime.now().strftime("%H:%M:%S")

        ## saves the image byte data into a buffer. pretty sure it's not necessary, but i don't want to change it because this works!
        buffer1 = io.BytesIO(chartOne.to_image(format="png"))
        buffer2 = io.BytesIO(chartTwo.to_image(format="png"))

        save1 = dcc.send_bytes(src = buffer1.getvalue(), filename = f"GraphOne_{downloadDate}.png")
        save2 = dcc.send_bytes(src = buffer2.getvalue(), filename = f"GraphTwo_{downloadDate}.png")

        return chartOne, chartTwo, save1, save2
    else:
        ## returns the saves as none to the dcc.download so it doesn't trigger a download
        ## this is my main gripe with this section of code! it feels like too much for something that should probably be simpler?
        save1 = None
        save2 = None


    return chartOne, chartTwo, save1, save2


## Main thread
if __name__ == "__main__":
    app.run(debug=True)