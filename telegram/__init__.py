import config
import telebot

tb = telebot.TeleBot(config.get_config()['telegram']['token'])


def _prepare_msg(flat):
    return "🏠 Ich habe eine neue Wohnung gefunden! \n" \
           "🛏 Zimmer: " + flat['rooms'] + "\n" + \
           "📐 Größe: " + flat['size'] + "\n" + \
           "💸 Preis: " + flat['price'] + "\n" + \
           "📍 Adresse: " + flat['address'] + "\n" + \
           "🌍 Link:  " + flat['link'] + "\n"


def send_flat(flat):
    tb.send_message(config.get_config()['telegram']['chat_id'], _prepare_msg(flat))
