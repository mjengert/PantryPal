from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class LoginScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.add_widget(Label(text='[color=ff3333]User Name'))
        #self.username = TextInput(multiline=False,
         #                         size_hint=(10, 10),
          #                        pos_hint={'center_x': .5, 'center_y':.5})
        #self.add_widget(self.username)
        #self.add_widget(Label(text='Password'))
        #self.password = TextInput(password=True, multiline=False)
        #self.add_widget(self.password)
        self.add_widget(
            Button(text='Login', size_hint=(.15, .10), pos_hint={'center_x': .5, 'center_y': .25})
        )

class PantryPal(App):
    def build(self):
        self.root = root = LoginScreen()
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(255, 255, 255, 1)
            self.rect = Rectangle(size=root.size, pos=root.pos)
        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    PantryPal().run()