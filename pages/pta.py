import uuid
from dash import html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import dash_uploader as du
from app import app


UPLOAD_FOLDER ="/assets"
 
du.configure_upload(app, UPLOAD_FOLDER)

def get_upload_component(id):
    return du.Upload(
        id=id,
        max_file_size=1800,  # 1800 Mb
        filetypes=['mp3', 'wav'],
        upload_id=uuid.uuid1(),  # Unique session id
    )

layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Audio File Input")),
        html.Br(),
        html.Hr(),
        dbc.Col([html.Div([
            html.Div(
                [
                    get_upload_component(id='pta_dash-uploader'),
                    html.P(" "),
                    ],
                style={  # wrapper div style
                    'textAlign': 'center',
                    'width': '600px',
                    'padding': '10px',
                    'display': 'inline-block'
                }),
        ],
        style={
            'textAlign': 'center',
        },
    )]),
    html.P(id='pta_file-upload', style={
            'textAlign': 'center',
        }),
    
    ])
 
])
     

@du.callback(output=[Output("pta_file-upload",'children'),
                     Output("file_url_store",'data')],
              id="pta_dash-uploader",
              )
def callback_on_completion(status: du.UploadStatus):
    filename=status.latest_file
    f=str(filename)
    return "File Uploaded Sucessfully",f





        
        



    