# Importing modules
from tkinter import *
import pyttsx3
from nltk.corpus import wordnet
import nltk

# Download WordNet data if not already downloaded
nltk.download('wordnet')

# Function to speak the audio
def speak(audio):
    # Initialize pyttsx3 engine
    engine = pyttsx3.init('sapi5')

    # Set the voice property to the default
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    
    # Speak the given audio text
    engine.say(audio)
    engine.runAndWait()

# Function to find synonyms using NLTK's WordNet
def find_synonyms(word):
    syn_words = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            syn_words.add(lemma.name())
    return list(syn_words)

# Function to get the meaning of a word using NLTK's WordNet
def meaning():
    # Taking the string input
    query = str(text.get())
    synsets = wordnet.synsets(query)
    res = ''
    
    if synsets:
        # Fetch the definition of the first meaning
        for syn in synsets:
            res += f"{syn.definition()}\n"
        
        # Set and speak the output
        spokenText.set(res)
        speak("The meaning is: " + res)
    else:
        res = "Meaning not found"
        spokenText.set(res)
        speak(res)

# Creating the window 
wn = Tk() 
wn.title("Senapati's Dictionary")
wn.geometry('700x500')
wn.config(bg='SlateGray1')

# Creating the variables to get the word and set the correct word
text = StringVar(wn)
spokenText = StringVar(wn)

# The main label
Label(wn, text="Kodi - Speak the Meaning", bg='SlateGray1',
      fg='gray30', font=('Times', 20, 'bold')).place(x=100, y=10)

# Getting the input of word from the user
Label(wn, text='Please enter the word', bg='SlateGray1', font=('calibre', 13, 'normal'),
      anchor="e", justify=LEFT).place(x=20, y=70)

Entry(wn, textvariable=text, width=35, font=('calibre', 13, 'normal')).place(x=20, y=110)

# Label to show the correct word
queryLabel = Label(wn, textvariable=spokenText, bg='SlateGray1', anchor="e",
                   font=('calibre', 13, 'normal'), justify=LEFT, wraplength=500).place(x=20, y=130)
spokenText.set("Which word do you want to find the meaning of, sir/madam?")
speak("Which word do you want to find the meaning of, sir or madam")

# Button to get the meaning
Button(wn, text="Speak Meaning", bg='SlateGray4', font=('calibre', 13),
       command=meaning).place(x=230, y=350)

# Runs the window till it is closed by the user
wn.mainloop()
