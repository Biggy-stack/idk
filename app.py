## v0.3 changelog
## -- fixed the fonts (yay css!)
## -- did a LOT of gui work (moving background!!!!)

## todo
## there's a bug with the gui where the css stuff doesn't load in time with the graphs, and the margins break and blah blah... I HATE GUI >:[ // ps - i gave up on the margin. no more bottom margin.

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
sourcepath = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(sourcepath, "data", "covid19data.csv") ## had to use os because the python file wasn't starting in the source folder for some reason??? guess this is more thorough though
data = pd.read_csv(path, thousands=",") ## Reads the .csv
data["collection_date"] = pd.to_datetime(data["collection_date"], format="%Y-%m-%d") ## Converts the collection dates to the format
data.sort_values("collection_date", inplace=True) ## Sorts the dates chronologically

## App properties
app = dash.Dash(__name__)
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
                        children="Version 0.3", className="title"
                    ),
                    html.P(
                        children='i will now cook the "berried delight" - vergil', className="title"
                    ),
                    html.H1(
                        children="Data Analysis Project of Love and Prosperity", className="mainTitle"
                    ),
                    html.P(
                        children="===============================================", className="title"
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
            className = 'dateWrapper'
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
                    className = 'paramWrapper'
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
                    className = 'paramWrapper'
                ),            
            ],
            className = 'wrapper'
        ),
        ## Graph Containers
        html.Div(
           children=[
                html.Div(
                    children=dcc.Graph(
                        id="GraphOne",
                        config={"displayModeBar": False, "responsive": True},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="GraphTwo",
                        config={"displayModeBar": False, "responsive": True},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",  
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
    plot_rgbcolor = 'rgba(255, 250, 240,1)'
    paper_rgbcolor = 'rgba(255, 250, 240,1 )'
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
        color = filteredData1["state"],
        labels = {'collection_date': "Date", 'y': attribute1},
        title = f'Graph One: {attribute1} from {startDate} to {endDate}.',
    )

    ## Make graph one transparent
    chartOne.update_layout({
        'plot_bgcolor': plot_rgbcolor,
        'paper_bgcolor': paper_rgbcolor,
    })

    chartTwo = px.line(
        data_frame = filteredData2,
        x = filteredData2.collection_date,
        y = np.sort(filteredData2[str(attribute2)].apply(pd.to_numeric)),  
        color = filteredData2["state"] ,
        labels = {'collection_date': "Date", 'y': attribute2},
        title = f'Graph Two: {attribute2} from {startDate} to {endDate}.',
    )

    ## Make graph two transparent
    chartTwo.update_layout({
        'plot_bgcolor': plot_rgbcolor,
        'paper_bgcolor': paper_rgbcolor,
    })

    ## i don't like this code that i wrote! maybe we can split it into different callback? idk! i tried and it hurt my head!
    ## also the graph layout update thing is pmo ... wanna change but it works for now so ...
    ## i don't remember how to make it reference the graph outside of this function!!!! so for now, this hack works :)

    ## Downloading code for downloading the files that you want to download onto your computer that you're using to download the files
    if ctx.triggered_id == "download_graphs":
        downloadDate = datetime.datetime.now().strftime("%H:%M:%S")

        chartOne.update_layout({
        'plot_bgcolor': 'rgba(204, 204, 255,1)',
        'paper_bgcolor': 'rgba(255,255,255,1)',
        })

        chartTwo.update_layout({
        'plot_bgcolor': 'rgba(204, 204, 255,1)',
        'paper_bgcolor': 'rgba(255,255,255,1)',
        })

        ## saves the image byte data into a buffer. pretty sure it's not necessary, but i don't want to change it because this works!
        buffer1 = io.BytesIO(chartOne.to_image(format="png"))
        buffer2 = io.BytesIO(chartTwo.to_image(format="png"))

        save1 = dcc.send_bytes(src = buffer1.getvalue(), filename = f"GraphOne_{downloadDate}.png")
        save2 = dcc.send_bytes(src = buffer2.getvalue(), filename = f"GraphTwo_{downloadDate}.png")

        chartOne.update_layout({
        'plot_bgcolor': plot_rgbcolor,
        'paper_bgcolor': paper_rgbcolor,
        })

        chartTwo.update_layout({
        'plot_bgcolor': plot_rgbcolor,
        'paper_bgcolor': paper_rgbcolor,
        })

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