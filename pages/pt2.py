import librosa
import os
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State
from pydub import AudioSegment
from app import app

def silence_speech(filename,db,secs):
    x,sr = librosa.load(filename)
    y=librosa.amplitude_to_db(abs(x))
    #refDBVal = np.max(y)
    n_fft = 2048
    S = librosa.stft(x, n_fft=n_fft, hop_length=n_fft//2)
    # convert to db
    D = librosa.amplitude_to_db(np.abs(S), ref=np.max)
    np.max(abs(D))
    nonMuteSections = librosa.effects.split(x,top_db=db,frame_length=secs*n_fft)
    speech_time=0
    for i in nonMuteSections:    
        speech_time+=((i[1]/sr)-(i[0]/sr))
        audio_time=librosa.get_duration(y=y, sr=sr)
        sil_time=(audio_time-speech_time)
        speech_time=round(speech_time,2)
        silence_time=round(sil_time,2)
        return silence_time,speech_time

layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Audio Waveform")),
        html.Br(),
        html.Hr(),
        dbc.Row([html.Div([
            html.Div([
                html.P("Decibel"),
                dcc.Input(
                    id="input_decibel",
                    type="number",
                    placeholder=80,
                    value=80
                    ),
                html.P("Seconds"),
                dcc.Input(
                    id="input_secs",
                    type="number",
                    placeholder=1,
                    value=1
                    ),
                html.P(" "),
                html.Button(id="submit-val", n_clicks=0, children="Submit"),
                dcc.Graph(id="graph",style={'width':'100%'}),
                html.P(" "),
                html.P("Total Seconds of Silence:"),
                html.P(id="pt2_silence"),
                html.P(" "),
                html.P("Total Seconds of Sound Produced:"),
                html.P(id="pt2_speech"),
                ],
                    ),
        ],
        style={
            'textAlign': 'center',
        },
    )]),
         
       
    ])
    ])
  

@app.callback(
    Output("graph",'figure'),
    Output("pt2_silence",'children'),
    Output("pt2_speech",'children'),
    Output("sil_time_store",'data'),
    Output("speech_time_store",'data'),
    Input("submit-val","n_clicks"),
    Input("final_url_store",'data'),
    State("input_decibel", "value"),
    State("input_secs","value"),
    prevent_initial_call=True
    )
def update_graph(n_clicks,filename,db,secs):
    print("Graph",filename)
    filename=str(filename)
    wavfile = AudioSegment.from_file(file = filename,
                                format = "wav")
    x1,sr=librosa.load(filename)
    #wavfile=librosa.effects.trim(x1)
    arr = np.array(wavfile.get_array_of_samples())
    df = pd.DataFrame(arr)
    silence1,speech1=silence_speech(filename,db,secs)
    fig = px.line(df,x=df.index,y=0,render_mode="webgl")
    fig.add_hline(y=db,line_width=3,line_color="red")
    #fig.add_hrect(y0=0.9, y1=2.6, line_width=0,fillcolor="red", opacity=0.2)
    return fig,silence1,speech1,silence1,speech1



