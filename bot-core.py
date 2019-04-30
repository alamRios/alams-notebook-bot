import telebot
import credentials as cd_
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import nltk
from nltk.corpus import cess_esp

cidx = nltk.text.ContextIndex([word.lower() for word in cess_esp.words()])
cred = credentials.Certificate('firebase-credentials.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL':'https://alams-notebook-bot.firebaseio.com'
})

bot = telebot.TeleBot(cd_.get_bot_token())

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    ref = db.reference('user')
    usr_id = message.from_user.id
    print('>> user connected:',usr_id)

    if(not any(ref.order_by_child("userid").equal_to(usr_id).get())):
        data = {message.from_user.id:{'userid':usr_id}}
        ref.update(data)
        bot.reply_to(message, "Hola, ¿cómo debería llamarte?")
    else:
        bot.reply_to(message, "Bienvenido de nuevo, ¿cómo puedo ayudarte?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    usr_id = message.from_user.id
    bot.send_chat_action(usr_id,'typing')
    res = []
    for word in nltk.word_tokenize(message.text):
        res += cidx.similar_words(word)
    if len(res) > 0:
        bot.reply_to(message, ' '.join(res))
    else:
        bot.reply_to(message, "no se encontraron coincidencias")
    
bot.polling()