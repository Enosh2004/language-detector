import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Select a voice: 0 for David (Male), 1 for Zira (Female)
engine.setProperty('voice', voices[0].id)  # Change index to 0 for David

engine.say("Hello, this is Enosh thomas paty.")
engine.runAndWait()
