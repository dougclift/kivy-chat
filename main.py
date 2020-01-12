from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.theming import ThemeManager
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout

from pusher import Pusher
import pysher
import os
import json

# get Settings
with open('config.json', 'r') as config_file:
    settings = json.load(config_file)


class LoginScreen(Screen):
    pass


class ChatScreen(Screen):
    pass


class MainApp(MDApp):
    pusher = None
    channel = None
    chatroom = None
    clientPusher = None
    username = None

    def __init__(self, **kwargs):
        self.title = "KivyMD Chat"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        self.items = ["Select Chatroom", "sports",
                      "general", "education", "health", "technology"]
        super().__init__(**kwargs)

        # print(self.theme_cls.primary_color)

    def build(self):
        self.root = Builder.load_file('main.kv')

    def change_screen(self, screen_name, direction='left'):
        # get the screen manager for the kv file
        screen_manager = self.root.ids['screen_manager']
        screen_manager.transition.direction = direction
        screen_manager.current = screen_name

    def login(self, username, chatroom):
        self.username = username
        self.chatroom = chatroom
        self.root.ids['chat_screen'].ids['toolbar'].title = '#' + self.chatroom
        self.initPusher()
        self.change_screen("chat_screen")

    def send_msg(self, msg):
        # print(msg)
        self.root.ids['chat_screen'].ids['msg'].text = ''

        add_box = BoxLayout(orientation='horizontal',
                            spacing="130dp", padding="10dp")
        build_msg = f'[b]{self.username}: [/b]' + msg
        add_msg = MDLabel(text=build_msg, font_style='Body1',
                          theme_text_color='Primary', size_hint_y=.1, halign='left', markup=True)
        add_box.add_widget(add_msg)

        self.root.ids['chat_screen'].ids['chat_log'].add_widget(add_box)

        self.pusher.trigger(self.chatroom, u'newmessage', {
                            "user": self.username, "message": msg})

    def initPusher(self):
        self.pusher = Pusher(app_id=settings['PUSHER_APP_ID'], key=settings['PUSHER_APP_KEY'],
                             secret=settings['PUSHER_APP_SECRET'], cluster=settings['PUSHER_APP_CLUSTER'])
        self.clientPusher = pysher.Pusher(
            settings['PUSHER_APP_KEY'], settings['PUSHER_APP_CLUSTER'])
        self.clientPusher.connection.bind(
            'pusher:connection_established', self.connectHandler)
        self.clientPusher.connect()

        # Connection established change screens
        self.change_screen("chat_screen")

    def connectHandler(self, data):
        self.channel = self.clientPusher.subscribe(self.chatroom)
        self.channel.bind('newmessage', self.pusherCallback)

    # called when pusher receives a new message

    def pusherCallback(self, message):
        print(message)
        message = json.loads(message)
        if self.username != message['user']:
            add_box = BoxLayout(orientation='horizontal',
                                spacing="130dp", padding="10dp")
            build_msg = f"[b]{message['user']}:[/b] {message['message']}"
            add_msg = MDLabel(text=build_msg, font_style='Body1',
                              theme_text_color='Primary', size_hint_y=.1, halign='right', markup=True)
            add_box.add_widget(add_msg)

            self.root.ids['chat_screen'].ids['chat_log'].add_widget(add_box)

    #         print(f"{message['user']}: {message['message']}")


MainApp().run()
