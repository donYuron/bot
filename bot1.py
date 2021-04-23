from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import requests
import sqlite3
from telethon import TelegramClient
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telethon import TelegramClient, sync
import schedule
import time
import sys

class Wrong_number(Exception):
    pass

def request_kill(name): 
    response = requests.get('https://api.telegram.org/bot1783637262:AAEORdlVWehNXD_AhMR2RvZ-r8kbvh9rYJM/kickChatMember?chat_id=-1001440448740&user_id='+name+'&until_date=1508230000')
    
def info(update, context):
    update.message.reply_text('''Привет, меня зовут YrBot, и я слежу что-бы в эту группу не было непосвященных людей
Если сюда пригласят человека не присутствующего в базе данных, то я его выкину)''')
    
def delete(result):
    users = []
    for u in result:
        users.append([u.id, u.phone])    
    con = sqlite3.connect('members.sqlite')
    cursor = con.cursor()    
    True_users = cursor.execute("""SELECT phone FROM TrueMembers;""").fetchall()
    for user in users:
        if ((('+' + str(user[1])),) not in True_users):
            request_kill(str(user[0]))
    con.close()
            
def add(update, context):
    phone = update.message.text.split()[-1]
    ind = 0
    try:
        if (len(phone) != 12) or (phone[0] != '+'):
            raise Wrong_number()
    except Wrong_number:
        update.message.reply_text('Некорректный номер')
        ind = 1
        
    try:
        int(phone[1:])
    except Exception:
        update.message.reply_text('Номер должен состоять из цифр')
        ind = 1
        
    if ind == 0:    
        con = sqlite3.connect('members.sqlite')
        cursor = con.cursor()
        cursor.execute("INSERT INTO TrueMembers(phone) VALUES(?)", (phone,)) 
        con.commit()
        con.close()
        update.message.reply_text('Пользователь с номером ' + phone + ' добавлен в базу данных')
               
    
def main(): 
    # delete()
    api_id = 5385164
    api_hash = 'f5555ae9cfe22a489cac34f283d658f1'
    phone_number = '+79104666582'
    
    client = TelegramClient(phone_number, api_id, api_hash).start()
    
    channel = 'https://t.me/joinchat/FJejQDF4bDQ0ZjAy'

    res = client.get_participants(channel)
    
    updater = Updater('1783637262:AAEORdlVWehNXD_AhMR2RvZ-r8kbvh9rYJM', use_context=True)  
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("info", info))
    #dp.add_handler(CommandHandler("kick", delete))
    dp.add_handler(CommandHandler("add", add))
    #dp.add_handler(CommandHandler("kick", delete))
    updater.start_polling()
    schedule.every(1).minutes.do(delete, result=res)
    while True:
        schedule.run_pending()
        time.sleep(1)
    updater.idle()
   
if __name__ == '__main__':
    main()