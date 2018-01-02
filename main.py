from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
#from menu import menu
from kivy.clock import Clock
from pong import PongGame
from kivy.uix.screenmanager import ScreenManager, Screen
import math
'''from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '900')
Config.set('graphics', 'resizable', False)
Config.write()'''
#Window.size = (800, 600)
#Builder.load_file("menu.kv")
Builder.load_file("pong.kv")

class menu(Screen):
    txt = ObjectProperty(None)
    submit = ObjectProperty(None)
    button_pressed = False

    def __init__(self):
        super(menu, self).__init__()

    def returnvalues(self):
         self.button_pressed = True


class PongApp(App):
    #screen1 = Builder.load_file("welcome.kv")
    #screen2 = Builder.load_file("pong.kv")
    sm = ScreenManager()
    welcomeMenu = menu()
    game = PongGame()
    def build(self):
        
        #game = PongGame()
        
        #self.sm.add_widget(self.welcomeMenu)
        self.game.serve_ball()
        Clock.schedule_interval(self.game.update, 1.0 / 60.0)
        self.sm.add_widget(self.game)
        return self.sm
        

if __name__ == '__main__':
    PongApp().run()
