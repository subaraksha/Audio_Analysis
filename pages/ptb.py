from dash import html,dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import speech_recognition as sr
from app import app

r = sr.Recognizer()

layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Microphone Audio Input")),
        html.Br(),
        html.Hr(),
        dbc.Col([html.Div([
            html.Div([
                    html.Button(id='ptb_listen-pause',children='Record Message'),
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
        }),
       dcc.Textarea(id='ptb_record-message', value="No Recording Yet!!!",style={'textAlign': 'center','width': '100%', 'height': 100},children="No Recodring yet!!!"), 
       html.P(id='ptb_file-upload',children="Click Button and Start Speaking", style={'textAlign': 'center',}),     
            ]),
        ])
   ])

@app.callback([Output('ptb_record-message','value'),
              Output('ptb_file-upload','children'),
              Output('record_url_store','data'),
              ],
              Input('ptb_listen-pause','n_clicks'),
              prevent_initial_call=True)             

def transcribe_speech(n_clicks):
    if n_clicks > 0:
        try:
            with sr.Microphone() as source:
                audio_data = r.listen(source)
                transcript=r.recognize_google(audio_data, key=None)
                filename="speech.wav"
                with open(filename,'wb') as f:
                    f.write(audio_data.get_wav_data())
                f1=str(filename)
                return [transcript,"Audio Recorded and Saved in speech.wav",f1] #[transcript,wc,syl,"Record Message",filename,transcript,wc,syl]
        except sr.UnknownValueError:
            return ["Could not parse input", "Click Record Message",0]
    
    



