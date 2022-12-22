import logging
import os
import time

import telepot
from telepot.loop import MessageLoop

from db import SubscriberDb

from config import conf



class Telega:




    def __init__(self):
        self.db = SubscriberDb()
        API_TOKEN = os.environ['API_TOKEN']        
        self.bot = telepot.Bot(API_TOKEN)

        


    def MessageHandler(self,msg):


        chat_id = msg['chat']['id']
        first_name = msg['chat']['first_name']
        last_name = msg['chat']['last_name']
        text = msg['text']




        user = self.db.GetByUserID(chat_id)

   
        if user is None:
            self.bot.sendMessage(chat_id,"введите имя и пароль")
            

            if conf.res['login'] in text:

                loginText = text

                loginText = loginText.replace(conf.res['login'],"").replace(" ","")

                loginText = loginText.split(":")

                username = loginText[0]
                password = loginText[1]

                print(username,password)

                
                if username == os.environ['username'] and password == os.environ['password']:

                    self.db.CreateUser(chat_id,
                        first_name,
                        last_name
                        )

                    self.bot.sendMessage(chat_id,"вы успешно вошли")
                else :
                    self.bot.sendMessage(chat_id,"xex")





        else:

            if text == conf.res['turnOnDetector'][0]:
                conf.is_detector_active = True
                # DetectMontion()

            elif text == conf.res['turnOFFDetector'][0]:
                conf.is_detector_active = False

                
            else :
                self.bot.sendMessage(chat_id,"есть следующие команды")

                for r in conf.res.items():

                    if (type(r[1]) != str):

                        self.bot.sendMessage(chat_id,f"{r[1][0]} {r[1][1]}")

                





    def SendAllSub(self):

        subs = self.db.GetAllUserID()

        for sub in subs:
            print("отправляю фото",sub[0])
            img = open('Files/fr.jpg','rb')
            self.bot.sendPhoto(sub[0],img)


    def RunTelega(self):
        MessageLoop(self.bot,self.MessageHandler).run_as_thread()

        print("bot is ready")

     




