import os
from gtts import gTTS
mytext = 'Please say your name'
language = 'en'
myobj = gTTS(text=mytext, lang=language, slow=True)
myobj.save("welcome.mp3")
os.system("mpg321 welcome.mp3")
print("COmplete")
