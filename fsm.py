from transitions.extensions import GraphMachine
from utils import send_text_message,send_button_message, send_image_message
import requests
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction
import pandas as pd

# global variable

class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # user start
    def is_going_to_pic1(self, event):
        text = event.message.text
        return text == '開始'or text== '返回教室'or text == '右轉去教室→'or text =='左轉去教室←'
    def on_enter_pic1(self, event):
        title = '睡午覺起床，發現教室沒人，門也鎖起來了。我想回家啊……😭'
        text = '要做什麼？'
        url = 'https://i.imgur.com/a3PWEUM.png'
        btn = [
            MessageTemplateAction(
                label = '調查門',
                text ='調查門'
            ),
            MessageTemplateAction(
                label = '左轉去黑板←',
                text = '左轉去黑板←'
            ),
            MessageTemplateAction(
                label = '右轉去置物櫃→',
                text ='右轉去置物櫃→'
            )
        ]
        send_button_message(event.reply_token, title, text, btn, url)
    def is_going_to_door(self, event):
        text = event.message.text
        return text == '調查門'
    def on_enter_door(self, event):
        title = '門鎖起來了，旁邊有密碼鎖。（……教室以前有裝這種鎖嗎？）'
        text = '要做什麼？'
        url = 'https://i.imgur.com/xR45Jpr.png'
        btn = [
            MessageTemplateAction(
                label = '輸入密碼',
                text='輸入密碼'
            ),
            MessageTemplateAction(
                label = '返回教室',
                text = '返回教室'
            ),
        ]
        send_button_message(event.reply_token, title, text, btn, url)

    def back_to_pic1(self, event):
        text = event.message.text
        return text.lower() == '返回教室'
    def is_going_to_check_door(self,event):
        text = event.message.text
        return text.lower() == '輸入密碼'
    def on_enter_check_door(self,event):
        send_text_message(event.reply_token, '請輸入密碼，或按下「返回教室」回去😗')

    def back_to_check_door(self, event):
        text = event.message.text
        if text!='2543' and text!='返回教室':
            send_text_message(event.reply_token, '密碼錯誤！請重新輸入密碼，或按下「返回教室」回去😗')
            return True
        return False


    def is_going_to_success(self,event):
        text = event.message.text
        return text=='2543'
    def on_enter_success(self,event):
        text=event.message.text
        title='門開了！'
        text1 = '終於可以回家了！🤩'
        url = 'https://i.imgur.com/ZtSJBif.png'
        btn = [
            MessageTemplateAction(
                label = '開門🥳',
                text='開門'
            )
             ]
        send_button_message(event.reply_token, title, text1, btn, url)
    def is_going_to_open(self,event):
        text=event.message.text
        return text=='開門'
    def on_enter_open(self,event):
        send_image_message(event.reply_token,'https://i.imgur.com/cqJeBdF.png')
        return False


    def is_going_to_pic2(self,event):
        text = event.message.text
        return text == '左轉去黑板←' or text == '返回黑板' or text=='右轉去黑板→'
    def on_enter_pic2(self, event):
        title = '黑板下有一些奇怪的東西？？？👀'
        text = '要做什麼？'
        url = 'https://i.imgur.com/R6527gN.png'
        btn = [
            MessageTemplateAction(
                label = '調查保險箱',
                text ='調查保險箱'
            ),
            MessageTemplateAction(
                label = '調查牆上的方塊',
                text ='調查牆上的方塊'
            ),
            MessageTemplateAction(
                label = '左轉去書桌←',
                text = '左轉去書桌←'
            ),
            MessageTemplateAction(
                label = '右轉去教室→',
                text ='右轉去教室→'
            )
        ]
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_safe(self, event):
        text = event.message.text
        return text == '調查保險箱'
    def on_enter_safe(self, event):
        title = '調查保險箱🤨'
        text = '鎖起來了。'
        url = 'https://i.imgur.com/KMvC7D2.png'
        btn = [
            MessageTemplateAction(
                label = '轉動密碼',
                text='轉動密碼'
            ),
            MessageTemplateAction(
                label = '返回黑板',
                text = '返回黑板'
            )
        ]
        send_button_message(event.reply_token, title, text, btn, url)
    def back_to_pic2(self, event):
        text = event.message.text
        return text.lower() == '返回黑板'
    def is_going_to_check_safe(self,event):
        text = event.message.text
        return text.lower() == '轉動密碼'
    def on_enter_check_safe(self,event):
        send_text_message(event.reply_token, '請轉動密碼，或按下「返回黑板」回去😗')

    def back_to_check_safe(self, event):
        text = event.message.text
        if text!='3742' and text!='返回黑板':
            send_text_message(event.reply_token, '密碼錯誤！請重新轉動密碼，或按下「返回黑板」回去😗')
            return True
        return False
    def is_going_to_safe_pen(self,event):
        text = event.message.text
        return text=='3742'
    def on_enter_safe_pen(self,event):
        text=event.message.text
        title='保險箱打開了'
        text1 = '裡面有一些鉛筆。'
        url = 'https://i.imgur.com/8qWmZNE.png'
        btn = [
            MessageTemplateAction(
                label = '返回黑板',
                text = '返回黑板'
            )
             ]
        send_button_message(event.reply_token, title, text1, btn, url)
    def is_going_to_brick(self,event):
        text = event.message.text
        return text=='調查牆上的方塊'
    def on_enter_brick(self,event):
        text=event.message.text
        title='調查牆上的方塊'
        text1 = '是誰畫的？'
        url = 'https://i.imgur.com/gPywi5J.png'
        btn = [
            MessageTemplateAction(
                label = '返回黑板',
                text = '返回黑板'
            )
             ]
        send_button_message(event.reply_token, title, text1, btn, url)


#######################

    def is_going_to_pic3(self,event):
        text = event.message.text
        return text == '左轉去書桌←' or text== '返回書桌' or text=='右轉去書桌→'
    def on_enter_pic3(self, event):
        title = '已經是放學時間了。'
        text = '桌上有一本書📘'
        url = 'https://i.imgur.com/d9QGwlE.png'
        btn = [
            MessageTemplateAction(
                label = '調查書',
                text ='調查書'
            ),
            MessageTemplateAction(
                label = '左轉去置物櫃←',
                text = '左轉去置物櫃←'
            ),
            MessageTemplateAction(
                label = '右轉去黑板→',
                text ='右轉去黑板→'
            )
        ]
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_book(self, event):
        text = event.message.text
        return text == '調查書'
    def on_enter_book(self, event):
        title = '調查書'
        text = '書好像破了。'
        url = 'https://i.imgur.com/bVB4dDl.png'
        btn = [
            MessageTemplateAction(
                label = '返回書桌',
                text = '返回書桌'
            )
        ]
        send_button_message(event.reply_token, title, text, btn, url)
    def back_to_pic3(self, event):
        text = event.message.text
        return text.lower() == '返回書桌'


##############
    def is_going_to_pic4(self,event):
        text = event.message.text
        return text == '左轉去置物櫃←' or text == '返回置物櫃' or text=='右轉去置物櫃→'
    def on_enter_pic4(self, event):
        title = '我的書包呢？🎒'
        text = '要做什麼？'
        url = 'https://i.imgur.com/mppphHJ.png'
        btn = [
            MessageTemplateAction(
                label = '調查橘色箱子🥸',
                text ='調查橘色箱子'
            ),
            MessageTemplateAction(
                label = '左轉去教室←',
                text = '左轉去教室←'
            ),
            MessageTemplateAction(
                label = '右轉去書桌→',
                text ='右轉去書桌→'
            )
        ]
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_box(self, event):
        text = event.message.text
        return text == '調查橘色箱子'
    def on_enter_box(self, event):
        title = '調查橘色箱子'
        text = '箱子外好像貼著什麼。'
        url = 'https://i.imgur.com/Ipkm2hc.png'
        btn = [
            MessageTemplateAction(
                label = '輸入密碼',
                text='輸入密碼'
            ),
            MessageTemplateAction(
                label = '返回置物櫃',
                text = '返回置物櫃'
            )
        ]
        send_button_message(event.reply_token, title, text, btn, url)
    def back_to_pic4(self, event):
        text = event.message.text
        return text.lower() == '返回置物櫃'
    def is_going_to_check_box(self,event):
        text = event.message.text
        return text.lower() == '輸入密碼'
    def on_enter_check_box(self,event):
        send_text_message(event.reply_token, '請輸入密碼，或按下「返回置物櫃」回去😗')

    def back_to_check_box(self, event):
        text = event.message.text
        if text!='6928' and text!='返回置物櫃':
            send_text_message(event.reply_token, '密碼錯誤！請重新輸入密碼，或按下「返回置物櫃」回去😗')
            return True
        return False
    def is_going_to_box_pen(self,event):
        text = event.message.text
        return text=='6928'
    def on_enter_box_pen(self,event):
        text=event.message.text
        title='橘色箱子打開了😮'
        text1 = '裡面有一些鉛筆。✏️'
        url = 'https://i.imgur.com/dsHL6du.png'
        btn = [
            MessageTemplateAction(
                label = '返回置物櫃',
                text = '返回置物櫃'
            )
             ]
        send_button_message(event.reply_token, title, text1, btn, url)


    