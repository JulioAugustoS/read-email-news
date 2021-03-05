import imaplib
import credentials
from bs4 import BeautifulSoup
import quopri
import pyttsx3
import speech_recognition as sr

my_name = "Julio"
message_empty = f"{my_name}, não encontrei novas noticias no momento!"
message_welcome = f"{my_name}, vou ler as últimas noticias que encontrei para você!"
message_font = "Essas noticias são do blog do Felipe Deschamps."

speek_command = "noticias"
speek_return = f"Olá, {my_name}, como posso te ajudar?"

host = 'imap.gmail.com'
port = 993
user = credentials.user
password = credentials.password

server = imaplib.IMAP4_SSL(host, port)
server.login(user, password)

server.select("Deschamps")
status, data = server.search(None, "(UNSEEN)")

data_list = data[0].split()

engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty("voice", voices[22].id)
engine.setProperty("rate", 200)

def ouvir_microfone(data_list, data):
 microfone = sr.Recognizer()
 with sr.Microphone() as source:
  microfone.adjust_for_ambient_noise(source)

  engine.say(speek_return)
  engine.runAndWait()

  print("Escutando...")

  audio = microfone.listen(source)

  try:
    frase = microfone.recognize_google(audio,language='pt-BR')

    print("Você disse: " + frase)
    if frase.find(speek_command):
      if len(data_list) == 0:
        engine.say(message_empty)
        engine.runAndWait()

      for num in data[0].split():
        status, data = server.fetch(num, "(RFC822)")
        email_msg = data[0][1]

        soup = BeautifulSoup(markup=email_msg,features="html.parser")
        news = soup.find_all("td")[0].text

        utf = quopri.decodestring(news)
        text = utf.decode('utf-8')

        engine.say(message_welcome)
        engine.say(message_font)
        engine.say(text)
        engine.say("Essas foram as noticiais recentes do mundo da tecnologia, até a próxima!")
        engine.runAndWait()
    else:
      engine.say(f"Desculpe, {my_name} não entendi o comando informado!")
      engine.runAndWait()

  except sr.UnkownValueError:
    engine.say(f"Desculpe, {my_name} não entendi!")
    engine.runAndWait()
    print("Não entendi")
  return frase

ouvir_microfone(data_list, data)