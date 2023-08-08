#from pathlib import Path
#import uuid
import os
#import dash
from dash import html,dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import speech_recognition as sr
import syllables
from wordcounter import wordcounter
from pydub import AudioSegment
from app import app

recognizer = sr.Recognizer()

def cnt_words(transcript):
    w = wordcounter.WordCounter(transcript)
    wc=w.get_word_count()
    return wc

def cnt_syllables(transcript):
    syl=syllables.estimate(transcript)
    return syl

def convert_transcript(audio_text):
    transcript=recognizer.recognize_google(audio_text, key=None)
    return transcript
    
layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Audio File Transcript")),
        html.Br(),
        html.Hr(),
        html.Br(),
        dcc.Textarea(id='pt1_transcript',style={'textAlign': 'center','width': '100%', 'height': 100}),
        html.P(" "),
        html.P("Number of words", style={'textAlign': 'center',}),
        html.P(id="pt1_output1",style={'textAlign': 'center',}),
        html.P("Number of syllables",style={'textAlign': 'center',}),
        html.P(id="pt1_output2",style={'textAlign': 'center',})
            ])
            
        ])
     

@app.callback([Output('pt1_transcript','value'),
              Output('pt1_output1','children'),
              Output('pt1_output2','children'),
              Output('t_store1','data'),
              Output('word_store1','data'),
              Output('syl_store1','data'),
              Output('final_url_store','data')],
              [Input('file_url_store','data'),
              Input('record_url_store','data'),
              Input('file_url_store','modified_timestamp'),
              Input('record_url_store','modified_timestamp')]
              )
              
def trans_calc(f1,f2,ts1,ts2):
    if f2==0:
        latest=ts1
    else:    
        latest=max((ts1,ts2))
        
    if latest==ts1:
        filename=f1
    else:
        filename=f2
    print(filename)
    head, tail = os.path.split(filename)
    if 'mp3' in tail:
        src = filename
        tail = "test.wav"
        sound = AudioSegment.from_mp3(src)
        sound.export(tail, format="wav")
        filename="test.wav"
    audioFile = sr.AudioFile(tail)
    with audioFile as source:
        audio_data = recognizer.record(source)
        transcript = convert_transcript(audio_data)
        syl=cnt_syllables(transcript)
        wc=cnt_words(transcript)
        return transcript,wc,syl,transcript,wc,syl,filename


