import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,MessageTemplateAction

from fsm import TocMachine
from utils import send_text_message, send_button_message, send_image_message

load_dotenv()

machine = TocMachine(
    states=['user',
    'pic1', 'door','check_door','success','open',
    'pic2','safe','check_safe','safe_pen','brick',
    'pic3','book',
    'pic4','box','check_box','box_pen'],
    transitions=[
        {'trigger': 'advance', 'source': ['pic2','pic4','user'], 'dest': 'pic1', 'conditions': 'is_going_to_pic1'},
        {'trigger': 'advance', 'source': 'pic1', 'dest': 'door', 'conditions': 'is_going_to_door'},
        {'trigger': 'advance', 'source': 'door', 'dest': 'check_door', 'conditions': 'is_going_to_check_door'},
        {'trigger': 'advance', 'source': 'check_door', 'dest': 'success', 'conditions': 'is_going_to_success'},
        {'trigger': 'advance', 'source': 'check_door', 'dest': 'check_door', 'conditions': 'back_to_check_door'},
        {'trigger': 'advance', 'source':['check_door','door'], 'dest': 'pic1', 'conditions': 'back_to_pic1'},
        {'trigger': 'advance', 'source': 'success', 'dest': 'open', 'conditions': 'is_going_to_open'},

        {'trigger': 'advance', 'source': ['pic1','pic3'], 'dest': 'pic2', 'conditions': 'is_going_to_pic2'},
        {'trigger': 'advance', 'source':['brick','safe','check_safe','safe_pen'], 'dest': 'pic2', 'conditions': 'back_to_pic2'},
        {'trigger': 'advance', 'source': 'pic2', 'dest': 'safe', 'conditions': 'is_going_to_safe'},
        {'trigger': 'advance', 'source': 'pic2', 'dest': 'brick', 'conditions': 'is_going_to_brick'},
        {'trigger': 'advance', 'source': 'safe', 'dest': 'check_safe', 'conditions': 'is_going_to_check_safe'},
        {'trigger': 'advance', 'source': 'check_safe', 'dest': 'check_safe', 'conditions': 'back_to_check_safe'},
        {'trigger': 'advance', 'source': 'check_safe', 'dest': 'safe_pen', 'conditions': 'is_going_to_safe_pen'},

        {'trigger': 'advance', 'source': ['pic2','pic4'], 'dest': 'pic3', 'conditions': 'is_going_to_pic3'},
        {'trigger': 'advance', 'source':'book', 'dest': 'pic3', 'conditions': 'back_to_pic3'},
        {'trigger': 'advance', 'source': 'pic3', 'dest': 'book', 'conditions': 'is_going_to_book'},

        {'trigger': 'advance', 'source': ['pic1','pic3'], 'dest': 'pic4', 'conditions': 'is_going_to_pic4'},
        {'trigger': 'advance', 'source': 'pic4', 'dest': 'box', 'conditions': 'is_going_to_box'},
        {'trigger': 'advance', 'source': 'box', 'dest': 'check_box', 'conditions': 'is_going_to_check_box'},
        {'trigger': 'advance', 'source': 'check_box', 'dest': 'box_pen', 'conditions': 'is_going_to_box_pen'},
        {'trigger': 'advance', 'source': 'check_box', 'dest': 'check_box', 'conditions': 'back_to_check_box'},
        {'trigger': 'advance', 'source':['box','box_pen','check_box'], 'dest': 'pic4', 'conditions': 'back_to_pic4'},
        {'trigger': 'advance', 'source': 'open', 'dest': 'user'},

        {'trigger': 'go_back', 'source': ['user','pic1', 'door','check_door','success','open','pic2','pic3','safe','check_safe','safe_pen','brick','pic3','book','pic4','box','check_box','box_pen'], 'dest': 'user'},
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path='')


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

mode = 0

@app.route('/callback', methods=['POST'])
def webhook_handler():
    global mode
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f'Request body: {body}')
    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue

        print(f'\nFSM STATE: {machine.state}')
        print(f'\nadvance?: {machine.advance(event)}')
        print(f'REQUEST BODY: \n{body}')

        response = machine.advance(event)
        
        if response == False:
            if (machine.state == 'user'):
                send_text_message(event.reply_token, '輸入「開始」來逃出學校！😛😛😛')
            elif (machine.state != 'user') and (event.message.text.lower() == 'end'):
                send_text_message(event.reply_token, '輸入「開始」來逃出學校!😛😛😛')
                machine.go_back()
            elif(machine.state=='pic1'):
                title = '睡午覺起床，發現教室沒人，門也鎖起來了。我想回家啊……😭'
                text = '要做什麼？'
                url = 'https://i.imgur.com/a3PWEUM.png'
                btn = [MessageTemplateAction(label = '調查門',text ='調查門'),
                    MessageTemplateAction(label = '左轉去黑板←',text = '左轉去黑板←'),
                    MessageTemplateAction(label = '右轉去置物櫃→',text ='右轉去置物櫃→')]
                send_button_message(event.reply_token, title, text, btn, url)
            elif(machine.state=='door'):
                title = '門鎖起來了，旁邊有密碼鎖。（……教室以前有裝這種鎖嗎？）'
                text = '要做什麼？'
                url = 'https://i.imgur.com/xR45Jpr.png'
                btn = [MessageTemplateAction(label = '輸入密碼',text='輸入密碼'),
                MessageTemplateAction(label = '返回教室',text = '返回教室'),]
                send_button_message(event.reply_token, title, text, btn, url)
            elif(machine.state=='pic2'):
                title = '黑板下有一些奇怪的東西？？？👀'
                text = '要做什麼？'
                url = 'https://i.imgur.com/R6527gN.png'
                btn = [MessageTemplateAction(label = '調查保險箱',text ='調查保險箱'),
                MessageTemplateAction(label = '調查牆上的方塊',text ='調查牆上的方塊'),
                MessageTemplateAction(label = '左轉去書桌←',text = '左轉去書桌←'),
                MessageTemplateAction(label = '右轉去教室→',text ='右轉去教室→')]
                send_button_message(event.reply_token, title, text, btn, url)
            elif(machine.state=='safe'):
                title = '調查保險箱🤨'
                text = '鎖起來了。'
                url = 'https://i.imgur.com/KMvC7D2.png'
                btn = [MessageTemplateAction(label = '轉動密碼',text='轉動密碼'),
                    MessageTemplateAction(label = '返回黑板',text = '返回黑板')]
                send_button_message(event.reply_token, title, text, btn, url)
            elif(machine.state=='brick'):
                text=event.message.text
                title='調查牆上的方塊'
                text1 = '是誰畫的？'
                url = 'https://i.imgur.com/gPywi5J.png'
                btn = [MessageTemplateAction(label = '返回黑板',text = '返回黑板') ]
                send_button_message(event.reply_token, title, text1, btn, url)
            elif(machine.state=='pic3'):
                title = '已經是放學時間了。'
                text = '桌上有一本書📘'
                url = 'https://i.imgur.com/d9QGwlE.png'
                btn = [
                    MessageTemplateAction(label = '調查書',text ='調查書'),
                    MessageTemplateAction(label = '左轉去置物櫃←',text = '左轉去置物櫃←'),
                    MessageTemplateAction(label = '右轉去黑板→',text ='右轉去黑板→')]
                send_button_message(event.reply_token, title, text, btn, url)
            elif(machine.state=='book'):
                title = '調查書'
                text = '書好像破了。'
                url = 'https://i.imgur.com/bVB4dDl.png'
                btn = [MessageTemplateAction(label = '返回書桌',text = '返回書桌')]
                send_button_message(event.reply_token, title, text, btn, url)
            elif(machine.state=='pic4'):
                title = '我的書包呢？🎒'
                text = '要做什麼？'
                url = 'https://i.imgur.com/mppphHJ.png'
                btn = [MessageTemplateAction(label = '調查橘色箱子🥸',text ='調查橘色箱子'),
                MessageTemplateAction(label = '左轉去教室←',text = '左轉去教室←'),
                MessageTemplateAction(label = '右轉去書桌→',text ='右轉去書桌→')]
                send_button_message(event.reply_token, title, text, btn, url)
            elif(machine.state=='box'):
                title = '調查橘色箱子'
                text = '箱子外好像貼著什麼。'
                url = 'https://i.imgur.com/Ipkm2hc.png'
                btn = [MessageTemplateAction(label = '輸入密碼',text='輸入密碼'),
                    MessageTemplateAction(label = '返回置物櫃',text = '返回置物櫃')]
                send_button_message(event.reply_token, title, text, btn, url)

        
    return 'OK'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return send_file('fsm.png', mimetype='image/png')


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port, debug=True)