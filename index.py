import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from pages import pta
from pages import ptb
from pages import pt1
from pages import pt2
from pages import pt3
from pages import pt4
from app import app

server = app.server
app.config.suppress_callback_exceptions = True

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H3("Audio Analysis", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Upload", href="/", active="exact"),
                dbc.NavLink("Record", href="/pageb", active="exact"),
                dbc.NavLink("Transcript", href="/page1", active="exact"),
                dbc.NavLink("Visualization", href="/page2", active="exact"),
                dbc.NavLink("Segments", href="/page3", active="exact"),
                dbc.NavLink("Result", href="/page4", active="exact")
               ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url",refresh=False),
                       dcc.Store(id='file_url_store',data=[],storage_type="memory",modified_timestamp=0),
                       dcc.Store(id='record_url_store',data=[],storage_type="memory",modified_timestamp=0),
                       dcc.Store(id='final_url_store',data=[],storage_type="memory"),
                       
                       dcc.Store(id='t_store1',data=[],storage_type="memory"), 
                       dcc.Store(id='word_store1',data=[],storage_type="memory"), 
                       dcc.Store(id='syl_store1',data=[],storage_type="memory"), 
                       
                       dcc.Store(id='word_store2',data=[],storage_type="memory"), 
                       dcc.Store(id='syl_store2',data=[],storage_type="memory"), 
                       
                       dcc.Store(id='sil_time_store',data=[],storage_type="memory"), 
                       dcc.Store(id='speech_time_store',data=[],storage_type="memory"), 
                       dcc.Store(id='mean_store',data=[],storage_type="memory"),
                       sidebar,content])

@app.callback(Output("page-content", "children"), 
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return pta.layout
    elif pathname == "/pageb":
        return ptb.layout
    elif pathname == "/page1":
        return pt1.layout
    elif pathname == "/page2":
        return pt2.layout
    elif pathname == "/page3":
        return pt3.layout
    elif pathname == "/page4":
        return pt4.layout



if __name__ == "__main__":
    app.run_server(port=8014,debug=True,use_reloader=False)
