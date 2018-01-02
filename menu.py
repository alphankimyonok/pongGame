from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

class menu(Screen):
    txt = ObjectProperty(None)
    submit = ObjectProperty(None)
    button_pressed = False

    def __init__(self):
        super(menu, self).__init__()

    def returnvalues(self):
         self.button_pressed = True


