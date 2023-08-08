from dash import html,dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app


        
layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Audio Analysis Result")),
        html.Br(),
        html.Hr(),
        dbc.Col([html.Div([
            html.Div([
                    
                    html.Br(),
                    html.P("Total Number of Words: "),
                    html.P(id="pt4_word"),
                    html.P("Total Number of Syllables:"),
                    html.P(id="pt4_syl"),
                    html.P("Total Seconds of Silence:"),
                    html.P(id="pt4_silence"),
                    html.P("Total Seconds of Speech:"),
                    html.P(id="pt4_speech"),
                    html.P("Mean Length of Segments:"),
                    html.P(id="pt4_mean_score"),
                    html.Br(),
                    html.Button(id="pt4_download",children="Download",n_clicks=0),
                    dcc.Download(id='pt4_download-file')
                    
                    
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
        ]),
])  

@app.callback(Output('pt4_word','children'),
               Output('pt4_syl','children'),
               Output('pt4_silence','children'),
               Output('pt4_speech','children'),
               Output('pt4_mean_score','children'),
               Input('word_store2','data'),
               Input('syl_store2','data'),
               Input('sil_time_store','data'),
               Input('speech_time_store','data'),
               Input('mean_store','data'))
                
def result(data1,data2,data3,data4,data5):
    return data1,data2,data3,data4,data5

@app.callback(
    Output("pt4_download-file", "data"),
    Input("pt4_download", "n_clicks"),
    Input("final_url_store",'data'),
    Input("word_store2", "data"),
    Input("syl_store2", "data"),
    Input("sil_time_store", "data"),
    Input("speech_time_store", "data"),
    Input("mean_store", "data"),
    prevent_initial_call=True,
)
def create_download_file(n_clicks,v,v1,v2,v3,v4,v5):
    text='Input File:{} \n\n Words:{} \n Syllables:{} \n Silence_Time(secs){} \n Speech_Time (secs):{} \n Mean_length:{}'.format(v,v1,v2,v3,v4,v5)
    return dict(content=text, filename="file.txt")
             