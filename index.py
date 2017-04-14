 #!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot
from telebot import types
from telebot import util
import redis as r
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#######################################
redis = r.StrictRedis(host='localhost', port=6379, db=0)
con = "\n \033[01;31m Bot Is Online Now! :D\033[0m"
cdev= "\n \033[01;31m Devloper ~~> @HiddenDev\n  Channel ~~> @PG_TM \033[0m"

print(con + cdev) 
########################################################################################
sudo = 0 #Sudo Id
TOKEN = '' #Token
bot = telebot.TeleBot(TOKEN)
########################################################################################
@bot.edited_message_handler(func=lambda message: True)
def whyedit(m):
 try:
    gps = redis.sismember('botgps', '{}'.format(m.chat.id))
    if str(gps) == 'True': 
      if m.chat.type == "supergroup" or m.chat.type == "group":
        if m.from_user.id == sudo:
           bot.reply_to(m, '😉 My Sudo You Edit Your Message 😉')
        else:
          if bot.get_chat_member(m.chat.id, m.from_user.id).status == "creator" or bot.get_chat_member(m.chat.id, m.from_user.id).status == "administrator":
              bot.reply_to(m, '😉 Admin You Edit Your Message 😉') 
          else:
            text = redis.get("{}:{}".format(m.from_user.id,m.message_id))
            bot.reply_to(m, 'Why Edit Your Message??\nI See You Say \n{}'.format(text))  
 except Exception as e:
      bot.send_message(sudo, e)
########################################################################################
@bot.message_handler(commands=['start'])
def welcome(m):
 try:
    if m.chat.type == 'private':
     redis.sadd('botmems', int(m.from_user.id))
     markup = types.InlineKeyboardMarkup()
     markup.add(types.InlineKeyboardButton('👤 About 👥', callback_data = 'about'))
     markup.add(types.InlineKeyboardButton('🤖 Add To Group 🤖', url='https://telegram.me/{}?startgroup=new'.format(bot.get_me().username)))
     bot.send_message(m.chat.id, 'Hello\nWelcome To Py Dont Edit Bot', reply_markup=markup)
    else:
     bot.send_message(m.chat.id, 'Please Send /setting For Enable Or Disable BoT')
 except Exception as e:
    bot.send_message(sudo, e) 
########################################################################################
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
 try:
   if call.message:
      if call.data == "seti":
       s = bot.get_chat_member(call.message.chat.id, call.from_user.id)
       if s.status == "creator" or s.status == "administrator":
           markup = types.InlineKeyboardMarkup()
           gps = redis.sismember('botgps', '{}'.format(call.message.chat.id))
           if str(gps) == 'True': 
              markup.add(types.InlineKeyboardButton('Disable ❌', callback_data = 'seti'))
              bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Dont Edit Setting",reply_markup=markup)
              bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Disabled ❌")
              redis.srem('botgps', '{}'.format(call.message.chat.id))
           else:
              markup.add(types.InlineKeyboardButton('Enable ✅', callback_data = 'seti')) 
              bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Dont Edit Setting",reply_markup=markup)
              redis.sadd('botgps', int(call.message.chat.id))
              bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Enabled ✅")
       else:
          bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="🤖 You Are Not Group Admin 🤖")
########################################################################################
      if call.data == "menu":
             markup = types.InlineKeyboardMarkup()
             markup.add(types.InlineKeyboardButton('👤 About 👥', callback_data = 'about'))
             markup.add(types.InlineKeyboardButton('🤖 Add To Group 🤖', url='https://telegram.me/{}?startgroup=new'.format(bot.get_me().username)))
             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Welcome Back To Menu", reply_markup=markup)
########################################################################################
      if call.data == "about":
             markup = types.InlineKeyboardMarkup()
             markup.add(types.InlineKeyboardButton('👥 Channel 👥', url='https://telegram.me/PG_TM'))
             markup.add(types.InlineKeyboardButton('👤 Devloper 👤', url='https://telegram.me/HiddenDev'))
             markup.add(types.InlineKeyboardButton('🔙', callback_data = 'menu'))
             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "[PG TeaM](https://telegram.me/PG_TM) Dont Edit\nDevloper ==> [HiddenDev](https://telegram.me/HiddenDev)\nWriten In Python | TeleBot", reply_markup=markup,parse_mode='markdown')
 except Exception as e:
    bot.send_message(sudo, e) 
########################################################################################
@bot.message_handler(commands=['setting'])
def set(m):
 try:
    s = bot.get_chat_member(m.chat.id, m.from_user.id)
    if s.status == "creator" or s.status == "administrator":
       markup = types.InlineKeyboardMarkup()
       gps = redis.sismember('botgps', '{}'.format(m.chat.id))
       if str(gps) == 'False': 
          markup.add(types.InlineKeyboardButton('Disable ❌', callback_data = 'seti'))
          bot.send_message(m.chat.id, 'Dont Edit Setting', reply_markup=markup)
       else:
          markup.add(types.InlineKeyboardButton('Enable ✅', callback_data = 'seti')) 
          bot.send_message(m.chat.id, 'Dont Edit Setting', reply_markup=markup)
 except Exception as e:
      bot.send_message(sudo, e)
########################################################################################
@bot.message_handler(content_types=['text'])
def sett(m):
 try:
       gps = redis.sismember('botgps', '{}'.format(m.chat.id))
       if str(gps) == 'True':
         if m.chat.type == "supergroup" or m.chat.type == "group":
            redis.set("{}:{}".format(m.from_user.id,m.message_id),"{}".format(m.text))
 except Exception as e:
      bot.send_message(sudo, e)
########################################################################################
bot.polling(True)	  
