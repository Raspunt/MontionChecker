
import time
import os

import RPi.GPIO as GPIO
import cv2
from dotenv import load_dotenv
load_dotenv()

from camera import SmartCamera
from telega import Telega

from config import conf



class Main:


    def __init__(self):


        self.tel = Telega()
        self.tel.RunTelega()
        self.cap = SmartCamera()


        GPIO.setmode(GPIO.BCM)
        GPIO.setup(conf.pin.DETECTOR, GPIO.IN)

        while True:

            if conf.is_detector_active:
                self.DetectMontion()

 


    def DetectMontion(self):


        if GPIO.input(conf.pin.DETECTOR) :
            print("движение замечено")
            img = self.cap.MobileNetStart()
            
            if img is not None:
                print("фото")
                cv2.imwrite('./Files/fr.jpg', img)
                self.tel.SendAllSub()
                print("фото готово")

            






    



Main()