import numpy as np
from dash import html,dcc
from dash.dependencies import Input, Output, State
#from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from app import app
import syllables
from wordcounter import wordcounter

def cnt_words(transcript):
    w = wordcounter.WordCounter(transcript)
    wc=w.get_word_count()
    return wc

def cnt_syllables(transcript):
    syl=syllables.estimate(transcript)
    return syl


layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Segmentation")),
        html.Br(),
        html.Hr(),
        html.Br(),
        dcc.Textarea(id="pt3_transcript",style={'width': '100%', 'height': 100}),
        html.Br(),
        dbc.Col([
            html.Br(),
            html.Button(id="pt3_submit", n_clicks=0, children="Submit"),
            html.Br(),
            html.Br(),
            html.P(id="pt3_segment",children="1"),
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
    )   
])     
    
@app.callback(Output('pt3_transcript','value'),
              Input('t_store1','data')) 

def new_transcript(data):
    return data       

@app.callback([Output('pt3_segment','children'),
              Output('word_store2','data'),
              Output('syl_store2','data'),
              Output('mean_store','data')],
              State('pt3_transcript','value'),
              Input("pt3_submit","n_clicks"))
           
def segment_calc(value,n_clicks):
    seg_cnt=len(value.split(",")) 
    w=cnt_words(value)
    s=cnt_syllables(value)
    seg=value.split(",")
    seg_len=[]
    for i in range(0,len(seg)):
        seg_len.append(len(seg[i].split()))
    mean_len=round(np.mean(seg_len),2)
    return "Number of Segments : {}" .format(seg_cnt),w,s,mean_len

'''@app.callback([Output('word_store2','data'),
               Output('syl_store2','data'),
               Output('mean_store','data')],
               Input('pt3_transcript','value'),
               )
def mean_calc(value,data):
    w=cnt_words(value)
    s=cnt_syllables(value)
    seg=value.split(",")
    seg_len=[]
    for i in range(0,len(seg)):
        seg_len.append(len(seg[i].split()))
    mean_len=round(np.mean(seg_len),2)
    return w,s,mean_len '''
