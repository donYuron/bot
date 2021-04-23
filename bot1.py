from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import requests
import sqlite3
from telethon import TelegramClient
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telethon import TelegramClient, sync


def request_kill(name): 
    con = sqlite3.connect('members.sqlite')
    cursor = con.cursor()
    result = cursor.execute("""SELECT telegram_id FROM TrueMembers WHERE name = ?""",(name,)).fetchone()
    response = requests.get('https://api.telegram.org/bot1783637262:AAEORdlVWehNXD_AhMR2RvZ-r8kbvh9rYJM/kickChatMember?chat_id=-1001440448740&user_id='+result[0]+'&until_date=1508230000')
    
def info(update, context):
    update.message.reply_text('''Привет, меня зовут YrBot, и я слежу что-бы в эту группу не было непосвященных людей
Если сюда пригласят человека не присутствующего в базе данных, то я его выкину)''')
    
def delete(update, context):
    words = update.message.text.split()
    if len(words) == 2:
        request_kill(words[1])
    else:
        update.message.reply_text('Такого участника не существует')
               
    
def main():
    api_id = 5385164
    api_hash = 'f5555ae9cfe22a489cac34f283d658f1'
    phone_number = '+79104666582'
    
    client = TelegramClient(phone_number, api_id, api_hash).start()
    
    # choose the one that I want list users from
    channel = 'bot_group'
    
    # get all the users and print them
    print(client.get_participants(channel))
     
    
    updater = Updater('1783637262:AAEORdlVWehNXD_AhMR2RvZ-r8kbvh9rYJM', use_context=True)  
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("kick", delete))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()