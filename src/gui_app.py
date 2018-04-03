import random
from multiprocessing.dummy import Pool as ThreadPool 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.scatter import Scatter
import img_util
import face_id
import db
import json
import arduino_interface
import weather
import numpy as np
Window.clearcolor = [1, 1, 1, 1]
Builder.load_file('makentu.kv')

def numpyToTexture(img):
    buf = img.tostring()
    image_texture = Texture.create(
        size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
    image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
    return image_texture


class MainScreen(Screen):
    img1 = StringProperty()
    img2 = StringProperty()
    ig_img1 = StringProperty()
    ig_img2 = StringProperty()
    ig_img3 = StringProperty()
    ig_img4 = StringProperty()
    info_prompt = StringProperty()
    weather_info = StringProperty()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.info_prompt = "Take a picture to login!"
        self.logged_in = False
        self.img1 = "main_blank.png"
        self.img2 = "main_blank.png"
        self.ig_img1 = "main_blank.png"
        self.ig_img2 = "main_blank.png"
        self.ig_img3 = "main_blank.png"
        self.ig_img4 = "main_blank.png"
        w = weather.getWeather()
        self.weather_info = "Weather: " + w['weather'] + "\n" + \
                            "Temperature (now): " + str(w['temp']) + "\n" + \
                            "Temperature (min): " + str(w['temp_min']) + "\n" + \
                            "Temperature (max): " + str(w['temp_max']) + "\n"

    def getAnotherOutfit(self):
        if self.img1 == "user_db/clothing_img/6.jpg":
            self.img1 = "user_db/clothing_img/4.jpg"
        else:
            self.img1 = "user_db/clothing_img/6.jpg"
        
        if self.img2 == "user_db/clothing_img/7.jpg":
            self.img2 = "user_db/clothing_img/2.jpg"
        else:
            self.img2 = "user_db/clothing_img/7.jpg"

    def login(self):
        camera = self.ids['camera']
        if camera.play == True and not self.logged_in:
            img = img_util.captureImage()
            img = img[:, img.shape[1]//4:img.shape[1]//4*3, :]
            camera.play = False
            faceId = face_id.identifyByFace(img)
            if faceId:
                self.logged_in = True
                name = face_id.faceIdToName(faceId)
                self.info_prompt = 'Welcome, ' + name + '!'
                if name == 'Victor Huang':
                    self.img1 = "user_db/clothing_img/6.jpg"
                    self.img2 = "user_db/clothing_img/7.jpg"
                    self.ig_img1 = "ig_img/higracechang/26181238_1587970761295410_8973669282579742720_n.jpg"
                    self.ig_img2 = "ig_img/nohkyungim/29094132_2052187341691037_2659727131625390080_n.jpg"
                    self.ig_img3 = "ig_img/zhuzhulifenotes/19120696_1593836724016261_5698263794573115392_a.jpg"
                    self.ig_img4 = "ig_img/matildatheminimalist/19764361_303424120122563_622706292972060672_a.jpg"
                elif name == 'Adelaide Hsu':
                    self.img1 = "user_db/clothing_img/20.jpg"
                    self.img2 = "user_db/clothing_img/14.jpg"
                    self.ig_img1 = "ig_img/higracechang/29417860_230504887509939_3777100952859836416_n.jpg"
                    self.ig_img2 = "ig_img/nohkyungim/29093090_223319795080141_3715536513681850368_n.jpg"
                    self.ig_img3 = "ig_img/zhuzhulifenotes/29401769_1846951138936786_6491480525419577344_n.jpg"
                    self.ig_img4 = "ig_img/matildatheminimalist/29093954_357116771460205_5353970776515018752_n.jpg"
                elif name == 'Danny Tsai':
                    self.img1 = "user_db/clothing_img/24.jpg"
                    self.img2 = "user_db/clothing_img/23.jpg"
                    self.ig_img1 = "ig_img/nohkyungim/29094132_2052187341691037_2659727131625390080_n.jpg"
                    self.ig_img2 = "ig_img/zhuzhulifenotes/19120696_1593836724016261_5698263794573115392_a.jpg"
                    self.ig_img3 = "ig_img/matildatheminimalist/19764361_303424120122563_622706292972060672_a.jpg"
                    self.ig_img4 = "ig_img/higracechang/26181238_1587970761295410_8973669282579742720_n.jpg"
            else:
                self.info_prompt = "Login failed! Try again"
                camera.play = True
        
    def logout(self):
        if self.logged_in:
            self.logged_in = False
            self.info_prompt = "Take a picture to login!"
            self.img1 = "main_blank.png"
            self.img2 = "main_blank.png"
            self.ig_img1 = "main_blank.png"
            self.ig_img2 = "main_blank.png"
            self.ig_img3 = "main_blank.png"
            self.ig_img4 = "main_blank.png"
            camera = self.ids['camera']
            camera.play = True

    def sendArduino(self):
        arduino_interface.sendByteToArduino(b'1')


class ClothingScreen(Screen):
    result_prompt = StringProperty()
    
    def __init__(self, **kwargs):
        super(ClothingScreen, self).__init__(**kwargs)
        self.result_prompt = 'Powered by Azure!'

    def capture_and_analyze(self):
        camera = self.ids['camera']
        if camera.play == True:
            img = img_util.captureImage()
            img = img[:, img.shape[1]//4:img.shape[1]//4*3, :]
            camera.play = False
            azure_analysis = db.addClothingByImage(img)
            self.result_prompt = 'Results from Azure:\n\n'+"Image caption:\n"+azure_analysis['caption']+'\n\n'+"Tags:\n"+json.dumps(azure_analysis['tags'])+'\n\n'+"Dominant colors:\n"+json.dumps(azure_analysis['color'])
    
    def add_next_clothing(self):
        camera = self.ids['camera']
        if camera.play == False:
            camera.play = True
    

sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(ClothingScreen(name='clothing'))


class MakentuApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    MakentuApp().run()