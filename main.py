from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class ChatApp(App):
    def build(self):
        # إعداد التخطيط باستخدام FloatLayout لجعل العناصر في المنتصف
        self.layout = FloatLayout()

        # واجهة إدخال توكن البوت
        self.token_input = TextInput(size_hint=(None, None), size=(400, 40), pos_hint={'center_x': 0.5, 'center_y': 0.6}, 
                                     hint_text="Open Your Token", multiline=False)

        # زر بدء البوت
        self.start_button = Button(text="Start Bot Token", size_hint=(None, None), size=(200, 50), 
                                   pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.start_button.bind(on_press=self.start_bot)

        # إضافة العناصر إلى التخطيط
        self.layout.add_widget(self.token_input)
        self.layout.add_widget(self.start_button)

        return self.layout

    def start_bot(self, instance):
        token = self.token_input.text.strip()

        if token:
            # تعطيل زر البدء بعد إدخال التوكن
            self.start_button.disabled = True

            # بدء البوت
            self.bot = Bot(token=token)
            self.updater = Updater(token=token, use_context=True)
            self.dispatcher = self.updater.dispatcher

            # إضافة معالج الرسائل
            message_handler = MessageHandler(Filters.text & ~Filters.command, self.reply_message)
            self.dispatcher.add_handler(message_handler)

            # بدء البوت
            self.updater.start_polling()
            self.show_message("Bot is now running!")

    def reply_message(self, update, context):
        # الرد برسالة "مرحبا" على كل رسالة
        update.message.reply_text("مرحبا")

    def show_message(self, message):
        # عرض رسالة عند بدء البوت
        label = Label(text=message, size_hint=(None, None), size=(400, 40), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        self.layout.add_widget(label)

if __name__ == "__main__":
    ChatApp().run()