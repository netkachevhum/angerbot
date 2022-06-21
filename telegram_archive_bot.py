from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
import datetime
import random


updater = Updater(token="5317612709:AAE6jgx4lZkxioHUagNRKnL6ep3SAP9dS4A", use_context=True)

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#bot = Bot('5317612709:AAE6jgx4lZkxioHUagNRKnL6ep3SAP9dS4A')
channel_id = "@archiveofanger"
#bot.send_message(channel_id,"finally I can post via pyhton, fuck you")

#коэффициент, который влияет на количество цензуры в предложении
start_day = datetime.date(2022,6,20)
censorship = (datetime.date.today()- start_day).days
print(censorship)

# количество дней, за которое программа приходит к полному цензурированию
full_cycle = 10
censor_coeff = censorship / full_cycle


def get_sentences():
    with open("archive_messages.txt", encoding="UTF-8",mode = "r") as f:
        sentences = f.read().split("\n")
        return sentences


def get_censored(sentence):
    # эта штука берет предложение и возвращает зацензуренное -- просто исходя из словаря
    censored_roots = ["войн", "путин","украин",]
    new_sentence = []
    for word in sentence.split(" "):
        new_word = word
        for root in censored_roots:
            if word.lower().startswith(root):
                new_word = "*"*len(root)+word[len(root):]
        new_sentence.append(new_word)
    return " ".join(new_sentence)

def time_censor(string, censor_coeff):
    censored_indexes = []
    indexes_to_censor = []
    quant_to_censor = round(len([symb for symb in string if not symb in ["*"," "]])*censor_coeff)
    to_exclude = []
    new_string = ""
    for index, symb in enumerate(string):
        if symb == "*":
            censored_indexes.append(index)
        else:
            if not symb == " ":
                indexes_to_censor.append(index)
    for i in range(0, quant_to_censor):
        index_to_censor = random.choice(indexes_to_censor)
        indexes_to_censor.remove(index_to_censor)
        to_exclude.append(index_to_censor)
    for index, symb in enumerate(string):
        if index in to_exclude:
            new_string = new_string+"*"
        else:
            new_string = new_string+symb
    return(new_string)

def send_message(context: CallbackContext):
    global censor_coeff
    if censor_coeff < 1:
        censorship = (datetime.date.today() - start_day).days
        censor_coeff = censorship / full_cycle
    non_censored = random.choice(get_sentences())
    censored_message = time_censor(get_censored(non_censored),censor_coeff)
    context.bot.send_message(channel_id,censored_message)

now_utc = datetime.datetime.now(datetime.timezone.utc)
print(now_utc)

updater.start_polling()
# важно указывать время старта в utc -- x
j = updater.job_queue
reperater = j.run_repeating(send_message,interval=14400)