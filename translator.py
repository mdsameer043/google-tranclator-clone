import requests
from flask import Flask,render_template,request
import pyttsx3  # converts words into voice
from gtts import gTTS
import speech_recognition as sr # conerts voice into text
import webbrowser
import datetime
import pyjokes
import os
import time
import random



# getting language for different languages
def language_code(language):
    url = "https://text-translator2.p.rapidapi.com/getLanguages"
    headers = {
        "X-RapidAPI-Key": "your api key", # enter your api key
        "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers).json().get('data').get('languages')
    # print(response.get('languages')[1].get('code')," : ",response.get('data').get('languages')[1].get('name'))
    # languages_list=[]
    # for item in response:
    #     languages_list.append((item.get('code')," : ",item.get('name')))
    list={}
    for item in response:
        list[item.get('name')]=item.get('code')
        # languages_list.append((item.get('code')," : ",item.get('name')))
    return list.get(language)



# getting translated data
def translate(input_language,output_language,input_text):
    url = "https://text-translator2.p.rapidapi.com/translate"
    payload = {
        "source_language": input_language,
        "target_language": output_language,
        "text": input_text
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "your api key",
        "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
    }
    response = requests.post(url, data=payload, headers=headers).json().get('data').get('translatedText')
    return response
# translatedText=translate("en","ur","what is your name")




# listening audio source form microphone
def listen():
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening....")
        recognizer.adjust_for_ambient_noise(source)
        audio =recognizer.listen(source)
        try:
            print("recognising....")
            data =recognizer.recognize_google(audio)
            #print(data)
            return data
        except sr.UnknownValueError:
            print("not understanding...")


# function to read input data
def say(data):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[0].id)  
    rate = engine.getProperty('rate')     
    engine.setProperty('rate',150)
    engine.say(data)
    engine.runAndWait() 
    
# function to read different languages
def secondboxspeaker_output_read(mytext,language_code):
    myobj= gTTS(text=mytext, lang=language_code, slow=False)
    myobj.save("./static/hello.mp3")
    print(mytext)
        

# second box output language selection
output_language_selection="ur"
def set_output_language(value):
    global output_language_selection
    output_language_selection=value
    print(output_language_selection)
def get_outPut_language():
    value=output_language_selection
    return value




# flask app for displaying data
app = Flask(__name__)

@app.route("/")
def login_to_mainpage():
    return hello_world()

@app.route('/login',methods=['GET', 'POST'])
def hello_world():
    i=0
    input_language_selection="en"

    # button selection
    try:
        if request.method=="POST" and request.form['language_validation']=="valid":
            i=1
            language=request.form['checked_value_for_flask_next']
            set_output_language(language_code(language))
            return render_template("main_page.html",button=language)
        
    except Exception as e:
        print(e) 
    try:
        if request.method=="POST" and request.form['language_validation']=="valid":
            i=1
            language=request.form['checked_value_for_flask']
            input_field_value=request.form['input_field_value']
            set_output_language(language_code(language))
            mytranslatedtext=translate("en",get_outPut_language(),input_field_value)
            return render_template("main_page.html", translatedtext=mytranslatedtext,user_input_field=input_field_value,button=language)
    except Exception as e:
        print(e)
    
    # user input field function
    try:
        if request.method=="POST" and request.form['input_text_up']=="valid":
            i=1
            data=request.form['input_text']
            mytranslatedtext=translate("en",get_outPut_language(),data)                                    
            secondboxspeaker_output_read(mytranslatedtext,"ur")
            return render_template("main_page.html", translatedtext=mytranslatedtext,user_input_field=data)
    except Exception as e:
        print(e)
    
    # first box mic function 
    try:
        if request.method=="POST" and request.form['mic_key']=="mic":
            data=listen()
            i=1
            mytranslatedtext=translate("en",get_outPut_language(),data)
            secondboxspeaker_output_read(mytranslatedtext,"ur")
            return render_template("main_page.html", translatedtext=mytranslatedtext,user_input_field=data)
    except Exception as e:
        print(e)
    
    # first box speaker function
    try:
        if  request.method=="POST" and request.form['first_box_speaker_key']=="first_box_speaker":
            speaker_data=request.form['speaker_python_value']
            output_text=translate("en",get_outPut_language(),speaker_data)
            say(speaker_data)
            i=1    
            return render_template("main_page.html",user_input_field=speaker_data,translatedtext=output_text)
    except Exception as e:
        print(e)
        
    
           
    return render_template("main_page.html",name="Translate",mic_input="")


if __name__=="__main__":
    app.run(debug=True)