import streamlit as st
import os
from time import sleep
import requests
import sounddevice as sd
from scipy.io.wavfile import write



### fct

def speak():
    fs = 44100  
    seconds = 10  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait() 
    write('input.wav', fs, myrecording) 


    bar.progress(10)


def detect_languages(file):

    current_dir = os.getcwd()
    
    if file == "":
        for file in os.listdir(current_dir):
            if file.endswith(".wav"):
                mp4_file = os.path.join(current_dir, file)

    else : 
        mp4_file = os.path.join(current_dir, file)
    
    filename = mp4_file
        
    bar.progress(20)

    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data
                
                
    headers = {'authorization': api_key}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                            headers=headers,
                            data=read_file(filename))
    
    
    audio_url = response.json()['upload_url']


    bar.progress(30)


    endpoint = "https://api.assemblyai.com/v2/transcript"

    json = {
    "audio_url": audio_url,
    "language_detection": True
    }

    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }

    transcript_input_response = requests.post(endpoint, json=json, headers=headers)


    bar.progress(40)


    transcript_id = transcript_input_response.json()["id"]


    bar.progress(50)


    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {
        "authorization": api_key,
    }
    transcript_output_response = requests.get(endpoint, headers=headers)

    bar.progress(60)


    
    bar_progress = 60

    while transcript_output_response.json()['status'] != 'completed':
        sleep(5)
        if bar_progress < 91:
            bar_progress += 5
            bar.progress(bar_progress)
        transcript_output_response = requests.get(endpoint, headers=headers)
    
    bar.progress(100)


    st.header('Detection terminée...')
    langue=""
    if transcript_output_response.json()["language_code"] == "fr":
        langue = "L'audio est en Français"
    if transcript_output_response.json()["language_code"] == "en":
        langue = "L'audio est en Anglais"
    if transcript_output_response.json()["language_code"] == "it":
        langue = "L'audio est en Italien"
    if transcript_output_response.json()["language_code"] == "de":
        langue = "L'audio est en Allemand"
    if transcript_output_response.json()["language_code"] == "es":
        langue = "L'audio est en Espagnol"
        
    
    st.success(langue)
    
    st.header('Extrait audio : ')
    st.success(transcript_output_response.json()["text"])



   
#####

# App

with open ('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>' , unsafe_allow_html=True)
    

api_key = "72166864bcfd440e8982268da0bd1e40"

   
st.markdown('# Application web de detection de langue')
submit_button = st.button(label=' 10 secondes Recording  🔴')

st.warning('Enregistrez votre voix en cliquant le bouton de record.')
bar = st.progress(0)

st.sidebar.header('tester des langues')


with st.sidebar.form(key='test_fr'):
	st.markdown('test audio francais')
	fr_btn = st.form_submit_button(label='Go')
    
with st.sidebar.form(key='test_en'):
	st.markdown('test audio anglais')
	en_btn = st.form_submit_button(label='Go')

with st.sidebar.form(key='test_sp'):
	st.markdown('test audio espagnol')
	sp_btn = st.form_submit_button(label='Go')
    
with st.sidebar.form(key='test_de'):
	st.markdown('test audio allemand')
	de_btn = st.form_submit_button(label='Go')
    
with st.sidebar.form(key='test_it'):
	st.markdown('test audio italien')
	it_btn = st.form_submit_button(label='Go')
    

if submit_button:
    detect_languages("")


if fr_btn:
    file = "video/audio_fr.wav"
    audio_file = open(file, 'rb')
    audio_bytes = audio_file.read()
    st.sidebar.audio(audio_bytes, format='audio/wav')
    detect_languages(file)
    
    
if en_btn:
    file = "video/audio_en.wav"
    audio_file = open(file, 'rb')
    audio_bytes = audio_file.read()
    st.sidebar.audio(audio_bytes, format='audio/wav')  
    detect_languages(file)

if sp_btn:
    file = "video/audio_sp.wav"
    audio_file = open(file, 'rb')
    audio_bytes = audio_file.read()
    st.sidebar.audio(audio_bytes, format='audio/wav')
    detect_languages(file)
    
    
if de_btn:
    file = "video/audio_de.wav"
    audio_file = open(file, 'rb')
    audio_bytes = audio_file.read()
    st.sidebar.audio(audio_bytes, format='audio/wav')
    detect_languages(file)
    
if it_btn:
    file = "video/audio_it.wav"
    audio_file = open(file, 'rb')
    audio_bytes = audio_file.read()
    st.sidebar.audio(audio_bytes, format='audio/wav')
    detect_languages(file)
    



