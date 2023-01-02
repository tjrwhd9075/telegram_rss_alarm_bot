
from cmath import exp, nan
from os import close, name
from re import S
from threading import Thread, excepthook
import re

import os
import sys
from pprint import pprint
import asyncio
import requests
import time
from requests.models import DEFAULT_REDIRECT_LIMIT
import schedule
import datetime as dt
import traceback
import zipfile
from zipfile import ZipFile
from PIL import Image


import numpy as np
import mplfinance
import pandas as pd
from numpy.lib.polynomial import polysub
from pandas.core import tools
import FinanceDataReader as fdr #pip install finance-datareader --upgrade
from FinanceDataReader import data 
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

import matplotlib.pyplot as plt
from matplotlib import interactive, rc
import matplotlib.font_manager as fm
import plotly
from plotly import plot, subplots
import plotly.offline as plty
import plotly.graph_objs as pltygo
import matplotlib as mpl
from matplotlib.colors import rgb2hex

import ccxt
from ccxt.binance import binance
import pyupbit

import telegram as tel  # pip install python-telegram-bot --upgrade
from telegram import chat
import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import naver_weather
import naver_news
import watchlist
import aoaposition
import stockchart as sc
import nikedraw
import filename_set
import lotto
import av_img_video_url
import process_kill

plotly.__version__

version = "사용법은 /help\n\
        \n\[version]\
        \n 1.1.5 ha 추세전환 알림 차트에 기준선 추가, 고래포지션 수정 \
        \n\n[알람봇 메인채널](t.me/ha_alarm_feedback)\
        \n\n[채팅방](t.me/signalmaker_chat) : 명령어 사용가능!\
        \n\n[HA 추세전환 알림 한국, 미국 주식](t.me/ha_alarm_korea)\
        \n\n[HA 1일, 4시간 추세전환 알림 코인](t.me/ha_alarm)\
        \n\n[HA 1시간 추세전환 알림 코인](t.me/ha_alarm_1h_coin)\
        \n\n[HA 30분 추세전환 알림 코인](t.me/ha_alarm_30min_coin)\
        \n\n[바이낸스 비트코인 종합시그널](t.me/ha_alarm_binance)\
        \n\n[앤톡 새글 알리미](t.me/antok_alarm) : : 명령어 사용가능!\
        \n\n[네이버 뉴스 알리미](t.me/naver_news_alarm) : 뉴스 추가 명령어 가능!\
        \n\n[klay-aklay 비율 알리미](t.me/kak_ratio_alarm)\
        \n\n\[버그] 비오는 날..\
        "
updateText = "업데이트 완료 : " + version

'''
**bold**
__italic__
--underline--
~~strikethrough~~
[hyperlink](https://google.com)
[user mention](tg://user?id=12345)
`inline monospaced text`
```block monospaced text```
||spoiler||
'''

textHelp = "\n / 를 입력하고 명령어를 선택하세요. \
            \n 또는 메시지 입력란 오른편에 / 버튼을 누르세요."

myApikey = "hOpHmrM35aqoqakISj0m7PAy42bDLXBmhXIrOsvadPBU6bW8Gtin0ggp7UnzFg9f"
mySecretkey = "rJp7j47DyzzvqRhaa9ExusnxrcPSF2I6Aa1B6bNvjlzxv3VP7fs3sl3cMNvSbEdU"

#텔레그램 봇
myToken = '1811197670:AAFaSU2l8pKxT6tDA3tOl2Tpue-OiNC1Af0'
telbot = tel.Bot(token=myToken)
myBotName = "alarm_haBot"
updater = Updater(myToken, use_context=True)

myToken2 = '5831801489:AAHvEw74bp6zz1mhbNCsAGu9JmtVifG0AWY'  # fc2rss
telbot2 = tel.Bot(token=myToken2) # fc2rss
myBotName2 = "fc2rss_alarmBot"

channel_id_feedback = "@ha_alarm_feedback"  # alarm 메인채널
channel_id_binance = "@ha_alarm_binance"  # 시그널메이커 바이낸스 채널
channel_id_korea = "@ha_alarm_korea"  # 한국미국 주식 채널
channel_id_30min_coin = "@ha_alarm_30min_coin"  # 30분봉
channel_id_1h_coin = "@ha_alarm_1h_coin"   # 1시간봉
channel_id_day_coin = "@ha_alarm"      # 1일봉, 4시간봉
channel_id_kak = "@k_ak_ratio"
channel_id_av = '-1001635569220'
channel_id_hitomi = "-1001882150211"

group_id_naver_news = '-1001173681896'
group_id_kak = '-1001589291000'
group_id_trash = '-1001547828770'
group_id_hitomi = "-1001686267660"


image = "jusik.png"
msgOn = 1 # 1일때 메시지 켜짐, 0일때 메시지 꺼짐
runtest = 0 # 0일때 코인 실행 꺼짐, 1일때 코인 실행
run_ko = 0 # 0일때 한국 실행 꺼짐 1일때 실행
run_us = 0 # 0일때 미국 실행 꺼짐 1일때 실행

global krx, sp500, nasdaq, nyse
krx, sp500, nasdaq, nyse = None, None, None, None
def get_stock_list():
    global krx, sp500, nasdaq, nyse
    krx = fdr.StockListing('KRX')
    # 미국 주식 목록
    sp500 = fdr.StockListing('S&P500')
    nasdaq = fdr.StockListing('NASDAQ')
    nyse = fdr.StockListing('NYSE')
# 코드 찾기 어려울 경우를 위해 code찾기 만들기
def codefind(name, country):
    ''' country : "krx", "us "'''
    global krx, sp500, nasdaq, nyse
    if krx is None : get_stock_list()

    if country == "krx" :
        search = list(krx['Name'])
        for i in range(len(krx)):
            if (search[i]==name):
                return krx['Symbol'][i]
    elif country == "us" :
        search = list(sp500['Name'])
        search2 = list(nasdaq['Symbol'])
        search3 = list(nyse['Symbol'])
        for i in range(len(sp500)):
            if (search[i]==name):
                return sp500['Symbol'][i]
        for i in range(len(nasdaq)):
            if (search2[i]==name):
                return nasdaq['Name'][i]
        for i in range(len(nyse)):
            if (search3[i]==name):
                return nyse['Name'][i] 
    return 0
def namefind(symbol):
    global krx, sp500, nasdaq, nyse
    if krx == [] : get_stock_list()

    search = list(sp500['Symbol'])
    search2 = list(nasdaq['Symbol'])
    search3 = list(nyse['Symbol'])
    for i in range(len(sp500)):
        if (search[i]==symbol):
            return sp500['Name'][i]
    for i in range(len(nasdaq)):
        if (search2[i]==symbol):
            return nasdaq['Name'][i]
    for i in range(len(nyse)):
        if (search3[i]==symbol):
            return nyse['Name'][i] 
    return 0


# 캔들차트 그리기
def plot_candle_chart(df, title):  
    
    adp = [mplfinance.make_addplot(df["ema"], color='green')]  # 지수이평선
    adp2 = [mplfinance.make_addplot(df["kijun"], color='gray')]
    fig = mplfinance.plot(df, type='candle', style='charles', mav=(20),  
                    title=title, ylabel='price', show_nontrading=False,
                    savefig='jusik.png',
                    addplot=adp + adp2,
                    block=False
                    )

# 캔들차트 그리기
def plot_candle_chart2(df, title):  
    # 한글 출력용 폰트 지정
    font_name = fm.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    
    adp1 = [mplfinance.make_addplot(df["bolUpper"], color='red')]  # 이평선
    adp2 = [mplfinance.make_addplot(df["20ma"], color='yellow')]  # 이평선
    adp3 = [mplfinance.make_addplot(df["bolLower"], color='blue')]  # 이평선
    fig = mplfinance.plot(df, type='candle', style='charles', mav=(20),
                    title=title, ylabel='price', show_nontrading=False,
                    savefig='jusik.png',
                    addplot= adp1 + adp2 +adp3,
                    block=False
                    )

# 캔들차트 그리기
def plot_candle_chart_ichimoku(df, title):  
    
    adp1 = [mplfinance.make_addplot(df["kijun"], color='gray')]  # 기준선
    adp2 = [mplfinance.make_addplot(df["tenkan"], color='red')]  # 전환선
    adp3 = [mplfinance.make_addplot(df["senkouSpanA"], color='green')]  # 선행A
    adp4 = [mplfinance.make_addplot(df["senkouSpanB"], color='green')]  # 선행B
    fig = mplfinance.plot(df, type='candle', style='charles',
                    title=title, ylabel='price', show_nontrading=False,
                    savefig='jusik.png',
                    addplot= adp1 + adp2 +adp3+adp4,
                    block=False,
                    fill_between = dict(y1=df['senkouSpanA'].values, y2=df['senkouSpanB'].values, color='#f2ad73', alpha=0.20)
                    )

def plot_candle_chart_jisu(df, name):
    '''
    ks11, kq11, dji, ixic, us500
    '''

    if name.upper() == "KS11": title = "KOSPI"
    elif name.upper() == "KQ11": title = "KOSDAQ"
    elif name.upper() == "DJI": title = "DOWJONES"
    elif name.upper() == "IXIC": title = "NASDAQ"
    elif name.upper() == "US500" : title = "S&P500"
    else: title = name.upper()

    if df["close"].iloc[-1]-df["close"].iloc[-2] > 0:
        txt = title+" now : "+str(format(round(df["close"].iloc[-1],2),','))\
             + " (+"+  str(round(df["close"].iloc[-1]-df["close"].iloc[-2],2))\
             +" +" + str(round((df["close"].iloc[-1]/df["close"].iloc[-2]-1)*100,2)) + "%)"
    elif df["close"].iloc[-1]-df["close"].iloc[-2] < 0:
        txt = title+" now : "+str(format(round(df["close"].iloc[-1],2),','))\
             + " ("+  str(round(df["close"].iloc[-1]-df["close"].iloc[-2],2))\
             +" " + str(round((df["close"].iloc[-1]/df["close"].iloc[-2]-1)*100,2)) + "%)"

    fig = mplfinance.plot(df, type='candle', style='charles', mav=(20,60,120),  
                    title=(txt), ylabel='price', show_nontrading=False,
                    savefig='jusik.png',
                    block=False
                    )

############# 텔레그램 봇 #######################
global korea; korea =0
global usa; usa =0

# 맨처음 메뉴버튼
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

# 이후 버튼 누를때 다음 생성되는 버튼들
def build_button(text_list, callback_header = "") : # make button list
    button_list = []
    text_header = callback_header
    
    if callback_header != "" : # 비어있는게 아니라면
        text_header += ","   # 제목 + 콤마 붙임

    for text in text_list :
        button_list.append(InlineKeyboardButton(text, callback_data=text_header + text))

    return button_list

# rss봇이 보낸 메시지 처리
def get_avrssbot_text(bot, update):
    chat_id = bot['chat']['id']
    message_id = bot['message_id']
    msg = bot['text']

    if msg.find("https://sukebei.nyaa.si/download/") == -1 : return #rss 피드가 아니면 종료
    print("ㅡㅡㅡㅡㅡㅡ get_avrssbot_text ㅡㅡㅡㅡㅡㅡ" )

    msg = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥(\s)(\n)(\t)(\r)(#)(.)(\-)(|)(:)(/)]", " ", msg)
    title = msg.split(" | ")[1]
    titleList = title.split(" ")
    pumnum = ""
    for m in titleList: 
        if m.find("-") != -1 : #품번이 존재하면
            if m.find("]") != -1: pumnum=m.split("]")[-1]; break #띄어쓰기 안된 품번 asdf]ssis-123
            else: pumnum=m; break 
    if pumnum == "" : #품번이 없으면 삭제 후 종료
        telbot.delete_message(chat_id=chat_id, message_id=message_id); 
        print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")
        return
    
    sukebeiNum = msg.split(" | ")[0].split("#")[-1]
    title = msg.split(" | ")[1].split("-")[1].split(" ")[1:]
    title = ''.join(title)
    fileSize = msg.split(" | ")[2]
    infoHash = msg.split(" | ")[4].split("\n")[0]
    torrentLink = msg.split(" | ")[4].split("\n")[-1]
    
    print('sukebeiNum : ' + str(sukebeiNum), end=" | ") ; print('pumnum : ' + str(pumnum))
    print('title : ' + str(title))
    print('fileSize : ' + str(fileSize), end=" | ") ; print('infoHash : ' + str(infoHash))
    print('torrentLink : ' + str(torrentLink))

    translatedTitle = filename_set.replaceTxt(filename_set.translater(title))

    #avdbslink = 'https://www.avdbs.com/menu/dvd.php?dvd_idx=' + pum['data-idx']
    thumb = av_img_video_url.makeImageURL(pumnum)
    if isinstance(thumb, list) :
        thumb1 = thumb[0]
        thumb2 = thumb[1]
    else: thumb1 = thumb

    trailer = av_img_video_url.makeVideoURL(pumnum)

    txt = "[.](" +thumb1+ ") " + str(pumnum) + " #"+str(pumnum.replace("-","\_")) +"\n"\
        + "\[[javdb]("+f"https://javdb.com/search?q={pumnum}&f=all)]   \[[미리보기]("+trailer+")]   \[[evojav]("+f"https://evojav.pro/en/?s={pumnum}"+")]   \[[avdbs]("+f"https://www.avdbs.com/menu/dvd.php?dvd_idx={pumnum}"+")]   \[[dbmsin]("+f"https://db.msin.jp/jp.search/movie?str={pumnum}"+")]   \[[sukebei](" +f"https://sukebei.nyaa.si/view/{sukebeiNum}" +")]   \[[torrent]("+torrentLink+")]\n\n"\
        + translatedTitle  +"\n"\
        + fileSize
    mgn = 'magnet:?xt=urn:btih:' + str(infoHash)

    telbot2.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    telbot2.send_message(text=txt, parse_mode='Markdown', chat_id=chat_id)
    telbot2.send_message(text=mgn, chat_id=chat_id)
    telbot.delete_message(chat_id=chat_id, message_id=message_id)
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")
    time.sleep(4)
    
def get_fc2rssbot_text(bot, update):
    
    chat_id = bot['chat']['id']
    message_id = bot['message_id']
    msg = bot['text']

    if msg.find("https://sukebei.nyaa.si/download/") == -1 : return #rss 피드가 아니면 종료
    print("ㅡㅡㅡㅡㅡㅡ get_fc2rssbot_text ㅡㅡㅡㅡㅡㅡ" )

    '''
    한글, 영어, 한자, 일본어, 숫자 모두 매칭되는 regex
    [a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥]
    ^ : not
    '''

    msg = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥(\s)(\n)(\t)(\r)(#)(.)(\-)(|)(:)(/)]", " ", msg)
    # print(msg.split(" | ")[1])
    sukebeiNum = msg.split(" | ")[0].split("#")[-1]

    if msg.split(" | ")[1].find("FC2PPV ") != -1 : # FC2PPV 123456
        pumnum = msg.split(" | ")[1].split("FC2PPV ")[1].split(" ")[0]
        title = msg.split(" | ")[1].split("FC2PPV ")[1].split(" ")[1:]
    elif msg.split(" | ")[1].find("FC2PPV-") != -1 : # FC2PPV-123456
        pumnum = msg.split(" | ")[1].split("FC2PPV-")[1].split(" ")[0]
        title = msg.split(" | ")[1].split("FC2PPV-")[1].split(" ")[1:]
    elif msg.split(" | ")[1].find("FC2 PPV ") != -1 : # FC2 PPV 123456
        pumnum = msg.split(" | ")[1].split("FC2 PPV ")[1].split(" ")[0]
        title = msg.split(" | ")[1].split("FC2 PPV ")[1].split(" ")[1:]
    elif msg.split(" | ")[1].find("FC2-PPV-") != -1 : # FC2-PPV-123456
        pumnum = msg.split(" | ")[1].split("FC2-PPV-")[1].split(" ")[0]
        title = msg.split(" | ")[1].split("FC2-PPV-")[1].split(" ")[1:]
    else: # FC2-PPV-123456
        print(msg.split(" | ")[1])
        pumnum = msg.split(" | ")[1].split("-")[2].split(" ")[0]
        title = msg.split(" | ")[1].split("-")[2].split(" ")[1:]
    title = ''.join(title)
    fileSize = msg.split(" | ")[2]
    infoHash = msg.split(" | ")[4].split("\n")[0]
    torrentLink = msg.split(" | ")[4].split("\n")[-1]
    
    print('sukebeiNum : ' + str(sukebeiNum), end=" | ") ; print('pumnum : ' + str(pumnum))
    print('title : ' + str(title))
    print('fileSize : ' + str(fileSize), end=" | ") ; print('infoHash : ' + str(infoHash))
    print('torrentLink : ' + str(torrentLink))

    translatedTitle = filename_set.replaceTxt(filename_set.translater(title))
    try:
        writer, actor, createDate = filename_set.get_pumInfo_fc2_test(pumnum, 'rssbot') 
    except Exception as e:
        print(e)
        writer, actor, createDate = "-", "-", "-"
    # https://db.msin.jp/search/movie?str=3158020

    txt = "[.](" +f"https://db.msin.jp/images/cover/fc2/fc2-ppv-{pumnum}.jpg"+ ") FC2PPV " + str(pumnum) + " #FC2PPV\_"+str(pumnum) +"\n"\
        + " \[[미리보기]("+f"https://db.msin.jp/sampleplay?id=fc2-ppv-{pumnum}"+")]   \[[evojav]("+f"https://evojav.pro/en/?s={pumnum}"+")]   \[[dbmsin]("+f"https://db.msin.jp/search/movie?str={pumnum}"+")]   \[[sukebei](" +f"https://sukebei.nyaa.si/view/{sukebeiNum}" +")]   \[[torrent]("+torrentLink+")]\n\n"\
        + writer + " " + actor + " " + createDate+ " " + fileSize +"\n"\
        + translatedTitle 
    mgn = 'magnet:?xt=urn:btih:' + str(infoHash)
    telbot2.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    telbot2.send_message(text=txt, parse_mode='Markdown', chat_id=chat_id)
    telbot2.send_message(text=mgn, chat_id=chat_id)
    telbot.delete_message(chat_id=chat_id, message_id=message_id)
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")
    return


COMMAND = ''
EXCHANGE =''
SELLECT = ''
#그냥 채팅 전체 읽음
def get_name(bot, update): 
    if bot.channel_post is not None : tp = "channel_post"   #채널일 경우
    elif bot.message is not None : tp = "message"           #그룹일 경우
    elif bot.edited_channel_post is not None  : return      #봇이 채널에 에딧한 메세지일 경우
    elif bot.edited_message is not None  : return      # 채널 -> 댓글 -> 그룹일 경우?ㅁ
    # elif bot['message']['from']
    else : print(bot)
    # print(bot)

    chat_type = bot[tp]['chat']['type'] 
    # print("채널타입 : " + chat_type)
    if chat_type == 'private' or chat_type == 'channel': # 개인채팅, 채널일 경우
        user_id = bot[tp]['chat']['id']
        print("유저id : " + str(user_id))
    elif  chat_type == 'supergroup':
        # print(bot[tp])
        if bot[tp]['sender_chat'] is not None:
            msgFrom = bot[tp]['sender_chat']['title']
            print("from : " + msgFrom, end=" -> ")
        else: msgFrom = ""
        msgTo = bot[tp]['chat']['title']
        print("to : " + msgTo)

    if msgFrom == 'AvRssTorrent' : get_avrssbot_text(bot[tp], update); return 
    if msgFrom == 'Fc2RssTorrent': get_fc2rssbot_text(bot[tp], update); return
    
    chat_id = bot[tp]['chat']['id']
    msg = bot[tp]['text'].upper()
    message_id = bot[tp]['message_id']

    print("get_name  " + msg)

    global COMMAND
    global EXCHANGE
    global SELLECT

    telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

    if msg == "취소" or msg == "CANCEL":
        telbot.send_message(chat_id=chat_id, text = '취소되었습니다.', reply_markup=ReplyKeyboardRemove())
        SELLECT = ''
        COMMAND = ''
        EXCHANGE = ''
        try :telbot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception:pass
        return

    if COMMAND == "/SHOWCHART": 
        if codefind(msg.lower().capitalize(), "us") != 0 : # 미국종목 이름름 검색 결과
            telbot.send_message(chat_id=chat_id, text = codefind(msg.lower().capitalize(), "us") + " : 검색되었습니다. 차트를 불러옵니다")
            df = fetch_jusik(codefind(msg.lower().capitalize(), "us"), "us", 120)
        elif namefind(msg) != 0: # 미국티커 검색 결과
            print(namefind(msg))
            telbot.send_message(chat_id=chat_id, text = namefind(msg) + " : 검색되었습니다. 차트를 불러옵니다")
            df = fetch_jusik(msg, "us", 120)
        elif codefind(msg, "krx") != 0: # 한국종목이름 검색 결과
            telbot.send_message(chat_id=chat_id, text = msg + "(" + codefind(msg, "krx") + ") : 검색되었습니다. 차트를 불러옵니다")
            df = fetch_jusik(msg, "krx", 120)
        else:
            telbot.send_message(chat_id=chat_id, text = msg + " : 검색되지 않는 종목명입니다.")
            return 

        telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        df = Macd(df)
        df = BolingerBand(df)
        df = Rsi(df)
        df = Ema(df)
        df = Heiken_ashi(df)
        df = ichimoku(df)
        txt = signal_maker(df)
        temp = ""
        for t in txt:
            if str(type(t)) == "<class 'int'>":
                if t > 0 :
                    temp = temp + "\n❤️ " + str(t) + ". 〰️매수 우위"
                elif t < 0 :
                    temp = temp + "\n💙 " + str(-t) + ". 〰️매도 우위"
                else :
                    temp = temp + "\n⚠️ " + str(t) + ". 〰️중립" 
            else:
                temp = temp + t + "\n"

        display_all_signal(df, msg, "1day")
        telbot.send_photo(chat_id=chat_id, photo=open('fig1.png', 'rb'))
        telbot.send_photo(chat_id=chat_id, photo=open('fig2.png', 'rb'))
        telbot.send_photo(chat_id=chat_id, photo=open('fig3.png', 'rb'), caption="💲💲 "+ msg + " 1일봉 💲💲\n" +temp)  
    elif COMMAND == "/STOCKCHART":
        if EXCHANGE=="" and codefind(msg.lower().capitalize(), "us") != 0 : # 미국종목 이름 검색 결과
            reply_keyboard = [["candle", "detail"],["PnF", "HA","cancel"]]
            telbot.send_message(chat_id=chat_id, text = codefind(msg.lower().capitalize(), "us") + " : 검색되었습니다. 차트 타입을 선택해주세요",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
            EXCHANGE = msg
            return
        elif EXCHANGE=="" and namefind(msg) != 0: # 미국티커 검색 결과
            print(namefind(msg))
            reply_keyboard = [["candle", "detail"],["PnF", "HA","cancel"]]
            telbot.send_message(chat_id=chat_id, text = namefind(msg) + " : 검색되었습니다. 차트 타입을 선택해주세요",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
            EXCHANGE = msg
            return

        elif EXCHANGE != "": # 티커입력 -> 차트타입 선택 ->
            sc.get_stockchart(EXCHANGE,msg)
            telbot.send_photo(chat_id=chat_id, photo=open('sc.png', 'rb'), reply_markup=ReplyKeyboardRemove())

        else:
            telbot.send_message(chat_id=chat_id, text = msg + " : 검색되지 않는 종목명입니다.")
            return 
    
    elif COMMAND == "/BTC" or COMMAND == "/ETH":    
        # 취소 버튼
        if msg == ("CANCEL"):
            telbot.send_message(text="취소하였습니다.",chat_id=chat_id, reply_markup=ReplyKeyboardRemove() )
            telbot.delete_message(chat_id=chat_id, message_id=message_id)
        
        elif msg == ("STOCKCHART"): #STOCKCHART : BTC , STOCKCHART. : ETH
            reply_keyboard = [["candle", "detail"],["PnF", "HA","cancel"]]
            telbot.send_message(text="차트 타입을 선택해주세요",
                                        chat_id=chat_id,
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
            telbot.delete_message(chat_id= chat_id, message_id= message_id)
            EXCHANGE = msg
            return
        elif msg == ("BINANCE") or msg == ("UPBIT"): # 비트코인
            reply_keyboard = [["1m", "5m", "15m", "30m"],["1h", "4h", "1d","cancel"]]
            telbot.send_message(text="봉을 선택해주세요.",
                                        chat_id=chat_id,
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
            telbot.delete_message(chat_id= chat_id, message_id= message_id)
            EXCHANGE = msg
            return
        elif msg == ("BINANCE.") or msg == ("UPBIT."): # 이더리움
            # reply_keyboard = [["1m", "5m", "15m", "30m"],["1h", "4h", "1d","cancel"]]
            reply_keyboard = [["1m", "5m", "15m", "30m"],["1h", "4h", "1d","cancel"]]
            telbot.send_message(text="봉을 선택해 주세요.",
                                        chat_id= chat_id,
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
            telbot.delete_message(chat_id= chat_id, message_id= message_id)
            EXCHANGE = msg
            return
        elif COMMAND != '' and EXCHANGE == 'STOCKCHART':
            coin = ""
            if COMMAND == "/BTC" : coin = "$BTCUSD"
            elif COMMAND == "/ETH" : coin = "$ETHUSD"
            sc.get_stockchart(coin,msg)
            telbot.send_photo(chat_id=chat_id, photo=open('sc.png', 'rb'), reply_markup=ReplyKeyboardRemove())

        elif COMMAND != '' and EXCHANGE != '':  # 코인 선택 -> 거래소 선택 -> msg = 'INTERVAL'
            interval = msg.lower()
            print(interval)
            count = 100
            if EXCHANGE == "BINANCE" : # 비트 바이낸스 선택
                coin = "BTC/USDT"
                df = ichimoku(Heiken_ashi(Ema(Rsi(BolingerBand(Macd(fetch_ohlcvs(coin, interval, count)))))))
            elif EXCHANGE == "BINANCE." : # 이더 바이낸스 선택
                coin = "ETH/USDT"
                df = ichimoku(Heiken_ashi(Ema(Rsi(BolingerBand(Macd(fetch_ohlcvs(coin, interval, count)))))))
            elif EXCHANGE == "UPBIT": # 비트 업비트 선택
                coin = "KRW-BTC"
                if interval == '1m' : interval = "minute1"
                elif interval == '5m' : interval = "minute5"
                elif interval == '15m' : interval = "minute15"
                elif interval == '30m' : interval = "minute30"
                elif interval == '1h' : interval = "minute60"
                elif interval == '4h' : interval = "minute240"
                elif interval == '1d' : interval = "1day"
                df = ichimoku(Heiken_ashi(Ema(Rsi(BolingerBand(Macd(pyupbit.get_ohlcv(coin, interval, count)))))))
            elif EXCHANGE == "UPBIT." : # 이더 업비트 선택
                coin = "KRW-BTC"
                if interval == '1m' : interval = "minute1"
                elif interval == '5m' : interval = "minute5"
                elif interval == '15m' : interval = "minute15"
                elif interval == '30m' : interval = "minute30"
                elif interval == '1h' : interval = "minute60"
                elif interval == '4h' : interval = "minute240"
                elif interval == '1d' : interval = "1day"
                coin = "KRW-ETH"
                df = ichimoku(Heiken_ashi(Ema(Rsi(BolingerBand(Macd(pyupbit.get_ohlcv(coin, interval, count)))))))

            txt = signal_maker(df)
            temp = ""
            for t in txt:
                if str(type(t)) == "<class 'int'>":
                    if t > 0 : temp = temp + "\n❤️ " + str(t) + ". 〰️매수 우위"
                    elif t < 0 : temp = temp + "\n💙 " + str(-t) + ". 〰️매도 우위"
                    else : temp = temp + "\n⚠️ " + str(t) + ". 〰️중립" 
                else: temp = temp + t + "\n"

            display_all_signal(df, coin, interval)
            telbot.send_photo(chat_id=chat_id, photo=open('fig1.png', 'rb'))
            telbot.send_photo(chat_id=chat_id, photo=open('fig2.png', 'rb'))                        
            telbot.send_photo(chat_id=chat_id, photo=open('fig3.png', 'rb'),
                            caption="💲💲 "+ EXCHANGE + " "+ COMMAND[1:] +" " + interval +" 💲💲\n" +temp , reply_markup=ReplyKeyboardRemove())     
    elif COMMAND == "/KLAYTN":
        telbot.send_message(text="지원하지 않습니다",  chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
       
    ############### 기타
    elif COMMAND == "/FUN":
        if msg == "로또 번호 추첨":
            telbot.send_message(text="원하는 갯수를 입력하세요(숫자만)", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return 
        elif SELLECT == "로또 번호 추첨":
            EXCHANGE = int(msg) #로또 갯수
            telbot.send_message(text="쉼표(,)로 구분해서 필수번호(+), 제외번호(-)를 입력하세요.\n\
            없으면 0 입력   ex) +4,-11,+45", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = "로또 번호 추첨2"
            return
        elif SELLECT == "로또 번호 추첨2":
            txt = ""
            if msg == "0":
                for i in range(EXCHANGE):
                    lot = lotto.main()
                    txt += ', '.join(str(e) for e in lot) + '\n'
                
            else:
                inex = msg.split(',')
                inc =[]
                exc =[]
                for num in inex:
                    if num[0] == '+': inc.append(int(num[1:]))
                    elif num[0] == '-': exc.append(int(num[1:]))

                for i in range(EXCHANGE):
                    lot = lotto.main(include=inc, exclude=exc)
                    txt += ', '.join(str(e) for e in lot) + '\n'

            telbot.send_message(text=txt, chat_id=chat_id, reply_markup=ReplyKeyboardRemove())

        elif msg == "오늘내일 날씨":
            telbot.send_message(text="도시명을 입력해주세요", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return 
        elif msg == "1주일 내 비소식":
            telbot.send_message(text="도시명을 입력해주세요", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return 
        elif msg == "한강 수온 체크":
            telbot.send_message(text="🌊 현재 한강 수온 🌡 "+naver_weather.temperature()+ "\n\n"+ naver_weather.wise_saying()+"\n[한강수온](https://hangang.life/)",parse_mode="Markdown", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg == "김프" :
            dfBi = fetch_ohlcvs('BTC/USDT', '1d', 2)
            dfUp = pyupbit.get_ohlcv('KRW-BTC', 'day', 2)
            usd2krw = fetch_jisu('usd/krw',10)
            biWon = dfBi['close'].iloc[-1]*usd2krw['close'].iloc[-1]
            kimpWon = dfUp['close'].iloc[-1] - biWon
            kimpPer = (dfUp['close'].iloc[-1]/biWon - 1)*100

            telbot.send_message(text="[[ 비트코인 김프 ]]\
                                    \n\n업비트 현재가 : " + str(format(round(dfUp['close'].iloc[-1]),",")) + "₩\
                                    \n바이낸스 현재가 : " + str(format(round(dfBi['close'].iloc[-1],2),',')) + "$\
                                    \n\t\t = " + str(format(round(biWon),',')) +"₩"
                                    + "\n\n김프 : " + str(format(round(kimpWon),',')) +"₩ ("+ str(format(round(kimpPer,2),',')) + "%)"
                                    ,  chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg == "나이키 드로우":
            nikedraw.get_nike()
            # telbot.send_message(text="지원하지않습니다",  chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            #     global aoaLastTime
            #     global aoaLastPosi
                
            #     txtList = asyncio.run(aoaposition.Whales_Position())
            #     aoaLastPosi = txtList[1]
            #     aoaLastTime = txtList[3]
                
            #     for i in range(len(txtList)):
            #         if txtList[i] == "LONG" : txtList[i] = "Long🔴"
            #         elif txtList[i] == "SHORT" : txtList[i] = "Short🔵"
            #         elif txtList[i] == "-" : txtList[i] = "없음😴"

            #     txt = "[고래 포지션 알림]\
            #             \n\n1️⃣ " + txtList[0] + " : " + txtList[1] + "\n24시간 변동 : " + txtList[2] +" BTC\n" + txtList[3] +\
            #             "\n\n2️⃣ " + txtList[4] + " : " + txtList[5] + "\n24시간 변동 : " + txtList[6] +" BTC\n" + txtList[7] +\
            #             "\n\n3️⃣ " + txtList[8] + " : " + txtList[9] + "\n24시간 변동 : " + txtList[10] +" BTC\n" + txtList[11] +\
            #             "\n\nhttps://sigbtc.pro/\
            #             \nhttps://kimpya.site/apps/leaderboard.php"

            #     telbot.send_message(text= txt,  chat_id=chat_id, reply_markup=ReplyKeyboardRemove(), disable_web_page_preview=True)

        elif SELLECT == "오늘내일 날씨":
            txt = naver_weather.search(msg)
            print(txt)
            telbot.send_message(text=txt, chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif SELLECT == "1주일 내 비소식":
            txt = naver_weather.rainday(msg)
            print(txt)
            telbot.send_message(text=txt, chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        
    ################ HA
    elif COMMAND == "/HA":
        if msg == "HA 알림추가":
            print('목록에 추가할 종목의 이름 or 티커를 입력해주세요')
            telbot.send_message(text='목록에 추가할 종목의 이름 or 티커를 입력해주세요', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return
        elif msg == "HA 목록삭제":
            print('목록에서 삭제할 종목의 이름 or 티커를 입력해주세요')
            telbot.send_message(text='목록에서 삭제할 종목의 이름 or 티커를 입력해주세요', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())  
            SELLECT = msg
            return
        elif msg == "HA 알림목록":
            print("ha 관심 목록 조회")
            fileKo = 'korea_watchlist.txt'
            fileMi = 'usa_watchlist.txt'

            querysKo = watchlist.get_querys(fileKo)
            txt1 = "<한국종목>\n"
            for query in querysKo:
                txt1 = txt1 + query + ", "
            querysMi = watchlist.get_querys(fileMi)
            txt2 = "<미국종목>\n"
            for query in querysMi:
                txt2 = txt2 + query + ", "

            telbot.send_message(text="[HA 관심 목록]\n\n" + txt1 + "\n" + txt2, chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        
        elif SELLECT == "HA 목록삭제":
            if codefind(msg, "krx") != 0 :
                fileHa = 'korea_watchlist.txt'
            elif  namefind(msg) != 0 :
                fileHa = 'usa_watchlist.txt'
            else:
                print(msg + ' : 한국, 미국 종목 DB에 없습니다.')
                telbot.send_message(text=msg[6:] + ' : 한국, 미국 종목 DB에 없습니다.', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
                return 

            rst = watchlist.del_query(msg, fileHa) 
            if rst == 0 : 
                print(msg + ' : HA 목록에 없습니다')
                telbot.send_message(text=msg + ' : HA 목록에 없습니다', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            elif rst == 1 :
                print(msg + ' : HA 목록에서 삭제했습니다.')
                telbot.send_message(text=msg + ' : HA 목록에서 삭제했습니다.', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        
        elif msg == "한국실행":
            asyncio.run(krx_bs_check())
            telbot.send_message(text="실행되었습니다",chat_id=chat_id,reply_markup=ReplyKeyboardRemove())

        elif msg == "미국실행":
            asyncio.run(us_bs_check())
            telbot.send_message(text="실행되었습니다",chat_id=chat_id,reply_markup=ReplyKeyboardRemove())
        
        elif SELLECT == "HA 알림추가":
            if codefind(msg, "krx") != 0 :
                fileHa = 'korea_watchlist.txt'
            elif  namefind(msg) != 0 :
                fileHa = 'usa_watchlist.txt'
                name = namefind(msg)
            else:
                print(msg + ' : 한국, 미국 종목 DB에 없습니다.')
                telbot.send_message(text=msg + ' : 한국, 미국 종목 DB에 없습니다.', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
                return 

            rst = watchlist.add_query(msg, fileHa)  
            if rst == 0 : 
                print(msg + ' : 이미 HA 목록에 있습니다')
                telbot.send_message(text=msg + ' : 이미 HA 목록에 있습니다.', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            elif rst == 1 :
                if namefind(msg) != 0 : # 미국종목이면
                    print(msg + " ("+ name + ') : HA 목록에 추가되었습니다.')
                    telbot.send_message(text=msg+ " ("+ name + ') : HA 목록에 추가되었습니다.', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
                else : # 한국종목이면
                    telbot.send_message(text=msg + ' : HA 목록에 추가되었습니다.', chat_id=chat_id, reply_markup=ReplyKeyboardRemove())

    ############## 뉴스
    elif COMMAND == "/NEWS":
        if msg == "뉴스추가":
            telbot.send_message(text="추가할 검색어를 입력해주세요", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return
        elif msg == "뉴스삭제":
            telbot.send_message(text="삭제할 검색어를 입력해주세요", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return
        elif msg == "뉴스검색":
            telbot.send_message(text="뉴스 검색어를 입력해주세요", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return
        elif msg == "뉴스목록":
            querys = naver_news.get_querys()
            txt = ""
            for query in querys:
                txt = txt + query + ", "
            telbot.send_message(text="[뉴스 검색어 목록]\n\n" + txt, chat_id=chat_id, reply_markup=ReplyKeyboardRemove())

        elif SELLECT == "뉴스추가":
            rst = naver_news.add_query(msg)
            if rst == 1:
                telbot.send_message(text=msg + " : 뉴스 검색어 목록에 추가했습니다." , chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            elif rst == 0:
                telbot.send_message(text=msg + " : 뉴스 검색어 목록에 있습니다." , chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif SELLECT == "뉴스삭제":
            rst = naver_news.del_query(msg)
            if rst == 1:
                telbot.send_message(text=msg + " : 뉴스 검색어 목록에서 삭제했습니다." , chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            elif rst == 0:
                telbot.send_message(text=msg + " : 뉴스 검색어 목록에 없습니다." , chat_id=chat_id, reply_markup=ReplyKeyboardRemove())  
        elif SELLECT == "뉴스검색":
            if bot[tp]['chat']['username'] != 'naver_news_alarm':
                telbot.send_message(text="해당 방에는 [@naver_news_alarm] 봇이 없습니다.\
                                        \n봇을 초대하시거나 또는 [네이버 뉴스 알리미](t.me/naver_news_alarm) 에서 사용하세요",chat_id=chat_id, parse_mode='Markdown',disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
                return
            naver_news.get_send_link(msg, telbot2, chat_id)
        
    ############## 지수
    elif COMMAND == "/JISU":
        if msg == "전부" :
            plot_candle_chart_jisu(fetch_jisu('ks11',300),'ks11')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'))
            plot_candle_chart_jisu(fetch_jisu('kq11',300),'kq11')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'))
            plot_candle_chart_jisu(fetch_jisu('dji',300),'dji')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'))
            plot_candle_chart_jisu(fetch_jisu('ixic',300),'ixic')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'))
            plot_candle_chart_jisu(fetch_jisu('US500',300),'US500')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())
        elif msg == "코스피":
            plot_candle_chart_jisu(fetch_jisu('ks11',300),'ks11')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())
        elif msg == "코스닥":
            plot_candle_chart_jisu(fetch_jisu('kq11',300),'kq11')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())
        elif msg == "나스닥":
            plot_candle_chart_jisu(fetch_jisu('ixic',300),'ixic')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())
        elif msg == "다우존스":
            plot_candle_chart_jisu(fetch_jisu('dji',300),'dji')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())
        elif msg == "S&P500":
            plot_candle_chart_jisu(fetch_jisu('US500',300),'US500')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())
        elif msg == "환율":
            plot_candle_chart_jisu(fetch_jisu('usd/krw',300),'usd/krw')
            telbot.send_photo(chat_id=chat_id, photo=open('jusik.png', 'rb'), reply_markup=ReplyKeyboardRemove())
    
    ############# AV
    elif COMMAND == "/AV1":
        if msg == 'FC2 판매자 작품정리':
            telbot.send_message(text="판매자명을 입력하세요", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return 
        elif SELLECT == "FC2 판매자 작품정리":
            try :
                telbot.send_message(text=msg + "정리중... ", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
                filename_set.get_all_pumnum(msg)
                telbot.send_message(text=msg + "정리완료", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            except Exception as e:
                print(e)
                telbot.send_message(text=msg + " 정리실패", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())

        elif msg == '파일명정리':
            try:
                telbot.send_message(text="파일명 정리중", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
                filename_set.rename_file()
                telbot.send_message(text="파일명 정리완료", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            except Exception as e:
                print(e)
                telbot.send_message(chat_id=chat_id, text="파일명정리 실패",reply_markup=ReplyKeyboardRemove())
        
        elif msg == 'DAY순위' or msg == 'WEEK순위' or msg == 'MONTH순위':
            get_rank(msg, chat_id)
            telbot.send_message(text=msg + " 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg == 'AMA신작' or msg == 'UNCEN신작' or msg == 'CENS신작':
            get_new_release(msg, chat_id)
            telbot.send_message(text=msg + " 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg == '신작전체':
            telbot.send_message(text=msg + " 가져오는 중.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            get_new_release('AMA신작',chat_id)
            get_new_release('UNCEN신작',chat_id)
            get_new_release('CENS신작',chat_id)
            telbot.send_message(text=msg + " 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg == '순위전체':
            telbot.send_message(text=msg + " 가져오는 중.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            get_rank('MONTH순위',chat_id)
            get_rank('WEEK순위',chat_id)
            get_rank('DAY순위',chat_id)
            telbot.send_message(text=msg + " 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg == '전부실행':
            telbot.send_message(text=msg + " 가져오는 중.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            get_rank('MONTH순위',chat_id)
            get_rank('WEEK순위',chat_id)
            get_rank('DAY순위',chat_id)
            get_new_release('AMA신작',chat_id)
            get_new_release('UNCEN신작',chat_id)
            get_new_release('CENS신작',chat_id)
            telbot.send_message(text=msg + " 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())

        elif msg.lower() == 'avdbs week':
            get_avdbs_rank(msg,group_id_trash)
            telbot.send_message(text=msg + " 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg.lower() == 'avdbs month':
            get_avdbs_rank(msg,group_id_trash)
            telbot.send_message(text=msg + " 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg.lower() == 'avdbs year':
            get_avdbs_rank(msg,group_id_trash)
            telbot.send_message(text=msg + " 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg.lower() == 'avdbs all':
            get_avdbs_rank(msg,group_id_trash)
            telbot.send_message(text=msg + " 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg.lower() == 'avdbs whole':
            telbot.send_message(text=msg + " 가져오는 중.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            get_avdbs_rank('avdbs all',group_id_trash)
            get_avdbs_rank('avdbs year',group_id_trash)
            get_avdbs_rank('avdbs month',group_id_trash)
            get_avdbs_rank('avdbs week',group_id_trash)
            telbot.send_message(text=msg + " 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        
        elif msg.lower() == 'upload' :
            telbot.send_message(text="파일을 업로드합니다.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            chk = hitomi_folder_upload(group_id_hitomi)
            telbot.send_message(text="업로드 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            
        elif msg.lower() == 'remove':
            filePath = "C:\\Users\\seokjong_2\\Desktop\\hitomi_downloader_GUI\\hitomi_downloaded"
            telbot.send_message(text=str(len(os.listdir(filePath)))+"개 파일을 삭제합니다.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())

            if os.path.exists(filePath):
                for file in os.scandir(filePath):
                    path = os.path.getsize(file.path)
                    file_size, size_name = convert_size(path)
                    if size_name == "MB" and file_size >= 50 : #50mb 이상이면 스킵
                        telbot.send_message(chat_id=chat_id, text="파일 용량 > 50mb")
                    else:
                        os.remove(file.path)
                telbot.send_message(text="파일 삭제 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            else:
                telbot.send_message(text="폴더가 없습니다.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())

        elif msg.lower() == 'hitomi' :
            telbot.send_message(text="링크 또는 품번을 입력하세요.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg.lower()
            return 
        elif SELLECT == "hitomi":
            telbot.send_message(text="hitomi 작품 찾는중.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            pumnum, chk = get_hitomi(msg.lower(), group_id_hitomi)
            if chk == 1 : 
                telbot.send_message(text="hitomi 작품 찾기 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
                return
            elif chk == 0 : 
                telbot.send_message(chat_id=chat_id, text="작품 찾기 실패", reply_markup=ReplyKeyboardRemove())
        
        elif msg.lower() == 'hitomi writer' :
            telbot.send_message(text="'#writer 작가명' 또는 링크를 입력하세요.\n그룹일 경우 '#group 그룹명' 또는 링크를 입력하세요", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg.lower()
            return 
        elif SELLECT == "hitomi writer":
            telbot.send_message(text="hitomi 작품 찾는중.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            get_all_hitomi_writer(msg.lower(), channel_id_hitomi)
            telbot.send_message(text="hitomi 작품 찾기 완료.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            
        elif msg.lower() == 'h today':
            telbot.send_message(text="hitomi 일간 순위를 가져옵니다.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            get_hitomi_rank(group_id_hitomi, "today")
            telbot.send_message(text="hitomi 일간 순위 완료", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg.lower() == 'h week':
            telbot.send_message(text="hitomi 주간 순위를 가져옵니다.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            get_hitomi_rank(group_id_hitomi, "week")
            telbot.send_message(text="hitomi 주간 순위 완료", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg.lower() == 'h month':
            telbot.send_message(text="hitomi 월간 순위를 가져옵니다.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            get_hitomi_rank(group_id_hitomi, "month")
            telbot.send_message(text="hitomi 월간 순위 완료", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        elif msg.lower() == 'h year':
            telbot.send_message(text="hitomi 연간 순위를 가져옵니다.", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            get_hitomi_rank(group_id_hitomi, "year")
            telbot.send_message(text="hitomi 연간 순위 완료", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())

    elif COMMAND == "/AV":
        if msg == "릴 확인":
            telbot.send_message(text="품번을 입력하세요", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
            SELLECT = msg
            return 
            
        elif SELLECT == "릴 확인":
            try :
                telbot.send_message(text=msg + " 확인중", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
                rel = filename_set.get_streaming_url_from_evojav(msg) # 없으면 '검색결과없음' , 있으면 [pumtitle(0), pumlink(1), pumthumb(2), streamlink(3)]
                print(rel)
                if rel == "검색결과없음":
                    telbot.send_message(text=msg + " " + rel, chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
                else :
                    title = filename_set.replaceTxt(filename_set.translater(rel[0]))
                    txt = "[.]("+rel[2]+") ["+msg +"]("+rel[1]+") "
                    print(txt)
                    tmprel=rel[3:]
                    print(len(tmprel))
                    for i in range(int(len(tmprel)/2)): 
                        print(i)
                        txt += "[스트리밍"+str(i+1)+"](https:"+tmprel[i*2]+") "+"[미리보기"+str(i+1)+"]("+tmprel[2*i+1]+") "    
                        
                    txt += "\n\n" +\
                         "[ [javdb](https://javdb.com/search?q="+msg+"&f=all) ]" +\
                         " [ [avdbs](https://www.avdbs.com/menu/search.php?kwd="+msg+"&seq=214407610&tab=2) ]"+\
                         " [ [evojav](https://evojav.pro/en/?s="+msg+") ]\n\n"+\
                         title
                    print(txt)

                    telbot.send_message(text=txt, chat_id=chat_id, parse_mode = 'Markdown')
            except Exception as e:
                print(e)
                telbot.send_message(text=msg + " 확인 실패", chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
        
        try :telbot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception:pass

    SELLECT = ''
    COMMAND = ''
    EXCHANGE = ''

# 명령어만 읽음
def get_command(bot, update):
    if bot.channel_post is not None : tp = "channel_post"   #채널일 경우
    elif bot.message is not None : tp = "message"           #그룹일 경우
    elif bot.edited_channel_post is not None  : return      #봇이 채널에 에딧한 메세지일 경우
    else : print(bot)

    # print(bot)
    chat_type = bot[tp]['chat']['type'] 
    print("채널타입 : " + chat_type)
    if chat_type == 'private' or chat_type == 'channel': # 개인채팅, 채널일 경우
        user_id = bot[tp]['chat']['id']
        print("유저id : " + str(user_id))
    elif chat_type == 'supergroup':
        if bot[tp]['from'] is not None :
            user_id = bot[tp]['from']['id']
            print("유저id : " + str(user_id))

    chat_id = bot[tp]['chat']['id']
    msg = bot[tp]['text'].split('@')[0].upper()    # / 제외하고, 대문자로 변환
    message_id = bot[tp]['message_id']

    print("get command : " + msg)

    telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

    global COMMAND
    if chat_type == 'private': # 개인챗에 메시지 전송
        helpmsg = "사용 가능한 명령어\n \
            /kadd keyword : 알림 키워드 등록\n \
            /klist : 알림 키워드 리스트\n \
            /kdel keyword : 알림 키워드 삭제\n \
            !띄어쓰기는 인식하지 않습니다.\
            /help 도움말\n \
            [신작&순위 채널](https://t.me/+Y7PSYJPViXFiZTY1) [채팅방](https://t.me/+LO4cGaU8g1JmNjA1)"
        if msg.find("/KADD") != -1 :
            try:
                kadd = bot[tp]['text'].split(" ")[1]
                print("kadd : " + kadd)
                chk = watchlist.add_keyword(str(user_id), kadd, 'av_list_keyword.txt')
                if chk == 1: telbot.send_message(chat_id = user_id, text = kadd + " 키워드 추가 완료")
                else : telbot.send_message(chat_id = user_id, text = kadd + " 키워드 추가 실패 또는 목록에 이미 있음")
            except Exception as e:
                print(e)
                telbot.send_message(chat_id = user_id, text = "명령어 뒤에 키워드를 입력하세요")
            return
        elif msg == "/KLIST":
            klist = watchlist.get_querys('av_list_keyword.txt')
            txt =""
            for key in klist: txt += key.split(" ")[1] +", "
            telbot.send_message(chat_id = user_id, text = "키워드 리스트\n" + txt)
            return
        elif msg.find("/KDEL") != -1:
            try:
                kdel = bot[tp]['text'].split(" ")[1]
                print("kdel : " + kdel)
                chk = watchlist.del_keyword(str(user_id), kdel, 'av_list_keyword.txt')
                if chk == 1: telbot.send_message(chat_id = user_id , text = kdel + " 키워드 삭제 완료")
                else : telbot.send_message(chat_id = user_id , text = kdel + " 키워드 삭제 실패 또는 목록에 없음")
            except Exception as e:
                print(e)
                telbot.send_message(chat_id = user_id, text = "명령어 뒤에 키워드를 입력하세요")
            return
        elif msg == "/HELP":
            telbot.send_message(chat_id = user_id, text = helpmsg,parse_mode='Markdown' )
            return
        else :
            telbot.send_message(chat_id = user_id, text = helpmsg,parse_mode='Markdown' )    
            return                                 

    elif bot[tp]['text'].find('@') == 0 :
        return 0
    elif bot[tp]['text'].split('@')[1] != myBotName :
        print(bot[tp]['text'].split('@')[1] + " : 날 부른게 아닌거 같아요")
        return

    elif msg == "/BTC":
        reply_keyboard = [['binance', 'upbit'],['stockchart', 'cancel']]
        telbot.send_message(text = msg + " 선택됨. 거래소를 선택하세요.", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'), chat_id=chat_id)
    elif msg == "/ETH":
        reply_keyboard = [['binance.', 'upbit.'],['stockchart', 'cancel']]
        telbot.send_message(text = msg + " 선택됨. 거래소를 선택하세요.", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'), chat_id=chat_id)
    elif msg == "/KLAYTN":
        reply_keyboard = [['KLAY', 'KSP', 'KAI', 'sKAI'],['KFI', 'aKLAY','HOUSE'],['ALL','취소']]
        telbot.send_message(text="메뉴를 선택해 주세요.",
                            chat_id=chat_id,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
    
    elif msg == "/STOCKCHART":
        telbot.send_message(text = "입력하세요 : 미국주식티커\
                                    \n(대소문자 상관X)",chat_id=chat_id)
    elif msg == "/SHOWCHART": 
         telbot.send_message(text = "한국주식 이름 or 미국주식 티커를 입력하세요.\
                                    \n(띄어쓰기 조심, 대소문자 상관X)",chat_id=chat_id)
    
    elif msg == "/JISU":
        reply_keyboard = [['코스피','코스닥'],['나스닥','다우존스'],['S&P500','환율'],['전부'],['취소']]
        telbot.send_message(text="보고 싶은 차트를 선택해 주세요.",
                            chat_id=chat_id,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
    elif msg == "/NEWS":
        reply_keyboard = [['뉴스추가','뉴스삭제'],['뉴스검색','뉴스목록'],['취소']]
        telbot.send_message(text="메뉴를 선택해 주세요.",
                            chat_id=chat_id,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
    elif msg == "/HA":
        reply_keyboard = [['HA 알림추가','HA 목록삭제'],['HA 알림목록'],['한국실행', '미국실행'],['취소']]
        telbot.send_message(text="메뉴를 선택해 주세요.",
                            chat_id=chat_id,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
    
    elif msg == "/FUN":
        # reply_keyboard = [['오늘내일 날씨', '1주일 내 비소식'],['김프', '고래 포지션'],['한강 수온 체크'],['취소']]
        reply_keyboard = [['로또 번호 추첨'],['오늘내일 날씨', '1주일 내 비소식'],['김프','한강 수온 체크'],['나이키 드로우','취소']]
        telbot.send_message(text="메뉴를 선택해 주세요.",
                            chat_id=chat_id,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
    elif msg == "/AV":
        reply_keyboard = [['릴 확인'],['취소']]
        telbot.send_message(text="메뉴를 선택해 주세요.",
                            chat_id=chat_id,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
    elif msg == "/AV1":
        reply_keyboard = [['FC2 판매자 작품정리','파일명정리'],['Day순위','Week순위','Month순위'],['AMA신작','UNCEN신작','CENS신작'],['순위전체','신작전체','전부실행'],['avdbs week','avdbs month','avdbs year','avdbs all','avdbs whole'],['hitomi', 'hitomi writer','upload','remove'],["H today","H week","H month","H year"],['취소']]
        telbot.send_message(text="메뉴를 선택해 주세요.",
                            chat_id=chat_id,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='what the fox say?'))
    elif msg == "/SHUTDOWN":
        telbot.send_message(text="프로그램 종료.",chat_id=chat_id)
        process_kill.kill_process("python")
    

    elif msg == "/HELP":
        telbot.send_message(text = "* 검색방법 *\n" + textHelp,chat_id=chat_id)
    else :
        try: 
            update.bot.edit_message_text(text=msg + " : 잘못된 명령어입니다.\n" +textHelp, chat_id=chat_id, message_id=message_id)
            return
        except Exception : pass

    COMMAND = msg
    try : telbot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception: pass

def get_new_release(msg,chat_id):
    try:
        telbot.send_message(chat_id=chat_id, text=msg+ " 가져오는중",reply_markup=ReplyKeyboardRemove())
        pumdf = filename_set.get_new_release(msg[:-2].lower()) # [index  views(0) pumnum(1) pumlink(2) pumthumb(3) pumtitle(4) date(5) rank(6)]
        
        txtfile = 'av_list_new.txt'
        # 기존 데이터 불러오기
        with open(txtfile, 'rt', encoding = 'UTF-8') as f:
            oldtxt = f.read().splitlines() 

        df2str = ''
        for idx, pum in pumdf.iterrows():
            if pum[6] == 0 : # 새로 등장한 녀석이면
                df2str += str(idx) + " (new) [" + pum[1] + "]("+pum[2]+") " + str(pum[0]) + " views " + str(dt.datetime.strftime(pum[5],"%Y-%m-%d")) +"\n"
            elif idx < pum[6] : # 순위가 올라가면
                df2str += str(idx) + " ("+ str(int(pum[6]-idx)) + "↑) [" + pum[1] + "]("+pum[2]+") " + str(pum[0]) + " views " + str(dt.datetime.strftime(pum[5],"%Y-%m-%d")) +"\n"
            elif idx > pum[6] : # 순위가 내려가면
                df2str += str(idx) + " ("+ str(int(idx - pum[6])) + "↓) [" + pum[1] + "]("+pum[2]+") " + str(pum[0]) + " views " + str(dt.datetime.strftime(pum[5],"%Y-%m-%d")) +"\n"
            else: # 순위변동 없으면
                df2str += str(idx) + " [" + pum[1] + "]("+pum[2]+") " + str(pum[0]) + " views " + str(dt.datetime.strftime(pum[5],"%Y-%m-%d")) +"\n"

            # df2str += str(idx) + " [" + pum[1] + "]("+pum[2]+") " + str(pum[0]) + " views " + dt.datetime.strftime(pum[5],"%Y-%m-%d") +"\n"
            
            if idx % 50 == 0 : #50번째마다 출력
                print(df2str)
                telbot.send_message(chat_id=chat_id, text="※ "+msg+" / 품번 / 조회수 ※\n\n" + df2str,parse_mode='Markdown',disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
                df2str = ''

            # 새로운 데이터 입력
            if pum[1] not in oldtxt: #중복검사
                title = filename_set.replaceTxt(filename_set.translater(pum[4]))
                title = title.replace("_","\\_")
                pumnum = pum[1].replace("_","\\_")
                trailer = av_img_video_url.makeVideoURL(pum[1])
                telbot.send_message(chat_id=channel_id_av, 
                                    text="[.]("+pum[3]+") " + pumnum +  " #" +pumnum.replace(" ","\\_").replace("-","\\_") + "\n\n" +
                                    "[ [javdb](https://javdb.com/search?q="+pumnum+"&f=all) ]"+
                                    "  [ [avdbs](https://www.avdbs.com/menu/search.php?kwd="+pumnum+"&seq=214407610&tab=2) ]"+
                                    "  [ [evojav](https://evojav.pro/en/?s="+pumnum+") ]"+
                                    "  [ [supjav]("+pum[2]+") ]" +
                                    "  [ [trailer]("+str(trailer)+")]\n\n"+
                                    title+"\n\n"
                                    "#"+ str(idx) + "위 #"+msg + " "+ str(dt.datetime.strftime(pum[5],"%Y-%m-%d")) + " " + str(pum[0]) + " views"
                                    ,parse_mode='Markdown' )
                with open(txtfile, 'a', encoding = 'UTF-8') as f:          
                    f.write(pum[1] + "\n")

                time.sleep(4) # 1분에 20개 이상 보내면 에러뜸

                chk = watchlist.find_keyword_line(pumnum + " " + title,'av_list_keyword.txt') 
                if chk != 0 :
                    telbot.send_message(chat_id= chk.split(" ")[0], text="키워드 : " + chk.split(" ")[1] + " → " + pumnum +' [신작&순위 채널](https://t.me/+Y7PSYJPViXFiZTY1)', parse_mode = 'Markdown')
                    time.sleep(1) # 1분에 20개 이상 보내면 에러뜸
                

        print(df2str) #나머지 출력
        telbot.send_message(chat_id=chat_id, text="※ "+msg+" / 품번 / 조회수 ※\n\n" + df2str,parse_mode='Markdown',disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
    
    except Exception as e:
        print("get_new_release : ")
        print(e)
        print(traceback.format_exc())
        telbot.send_message(chat_id=chat_id, text="신작 가져오기 실패",reply_markup=ReplyKeyboardRemove())

def get_rank(msg, chat_id):
    try:
        telbot.send_message(chat_id=chat_id, text=msg+ " 가져오는중",reply_markup=ReplyKeyboardRemove())
        pumdf = filename_set.get_popular(msg[:-2].lower()) # [index period(0) views(1) pumnum(2) pumlink(3) rank(4) pumthumb(5) pumtitle(6) date(7)]

        txtfile = 'av_list_new.txt'
        # 기존 데이터 불러오기
        with open(txtfile, 'rt', encoding = 'UTF-8') as f:
            oldtxt = f.read().splitlines() 

        df2str = ''
        for idx, pum in pumdf.iterrows():
            ok = False
            if pum[4] == 0 : # 새로 등장한 녀석이면
                df2str += str(idx) + " (new) [" + pum[2] + "]("+pum[3]+") " + str(pum[1]) + " views " + str(dt.datetime.strftime(pum[7],"%Y-%m-%d")) +"\n"
                if int(idx) <= 10 : #10위 안에 들면
                    ok = True
                    updown = "(new)"
            elif idx < pum[4] : # 순위가 올라가면
                df2str += str(idx) + " ("+ str(pum[4]-idx) + "↑) [" + pum[2] + "]("+pum[3]+") " + str(pum[1]) + " views " + str(dt.datetime.strftime(pum[7],"%Y-%m-%d")) +"\n"
                if int(idx) <= 10 : #10위 안에 들면
                    ok = True
                    updown = "("+ str(pum[4]-idx) + "↑)"
            elif idx > pum[4] : # 순위가 내려가면
                df2str += str(idx) + " ("+ str(idx - pum[4]) + "↓) [" + pum[2] + "]("+pum[3]+") " + str(pum[1]) + " views " + str(dt.datetime.strftime(pum[7],"%Y-%m-%d")) +"\n"
            else: # 순위변동 없으면
                df2str += str(idx) + " [" + pum[2] + "]("+pum[3]+") " + str(pum[1]) + " views " + str(dt.datetime.strftime(pum[7],"%Y-%m-%d")) +"\n"
            
            # 새로운 데이터 입력
            if pum[2] not in oldtxt: #중복검사
                title = filename_set.replaceTxt(filename_set.translater(pum[6]))
                title = title.replace("_","\\_")
                pumnum = pum[2].replace("_","\\_")
                trailer = av_img_video_url.makeVideoURL(pum[2])
                telbot.send_message(chat_id=channel_id_av, 
                                    text="[.]("+pum[5]+") " + pumnum + " #" +pumnum.replace(" ","\\_").replace("-","\\_") + "\n\n" +
                                    "\[ [javdb](https://javdb.com/search?q="+pumnum+"&f=all) ]"+
                                    "  \[ [avdbs](https://www.avdbs.com/menu/search.php?kwd="+pumnum+"&seq=214407610&tab=2) ]"+
                                    "  \[ [evojav](https://evojav.pro/en/?s="+pumnum+") ]"+
                                    "  \[ [supjav]("+pum[3]+") ]"+
                                    "  \[ [trailer]("+str(trailer)+")]\n\n"+
                                    title+"\n\n" 
                                    "#"+str(idx)+"위 (new) #"+msg+ " "+ str(dt.datetime.strftime(pum[7],"%Y-%m-%d")) + " " + str(pum[1]) + " views"
                                    ,parse_mode='Markdown' )
                with open(txtfile, 'a', encoding = 'UTF-8') as f:          
                    f.write(pum[2] + "\n")

                time.sleep(4) # 1분에 20개 이상 보내면 에러뜸

                chk = watchlist.find_keyword_line(pumnum + " " + title,'av_list_keyword.txt') 
                if chk != 0 :
                    telbot.send_message(chat_id= chk.split(" ")[0], text="키워드 : " + chk.split(" ")[1] + " → " + pumnum +' [신작&순위 채널](https://t.me/+Y7PSYJPViXFiZTY1)', parse_mode = 'Markdown')
                    time.sleep(1) # 1분에 20개 이상 보내면 에러뜸
                

            elif ok is True :
                title = filename_set.replaceTxt(filename_set.translater(pum[6]))
                title = title.replace("_","\\_")
                pumnum = pum[2].replace("_","\\_")
                trailer = av_img_video_url.makeVideoURL(pum[2])
                telbot.send_message(chat_id=channel_id_av, 
                                    text="[.]("+pum[5]+") " + pumnum + " #" +pumnum.replace(" ","\\_").replace("-","\\_") + "\n\n" +
                                    "\[ [javdb](https://javdb.com/search?q="+pumnum+"&f=all) ]"+
                                    "  \[ [avdbs](https://www.avdbs.com/menu/search.php?kwd="+pumnum+"&seq=214407610&tab=2) ]"+
                                    "  \[ [evojav](https://evojav.pro/en/?s="+pumnum+") ]"+
                                    "  \[ [supjav]("+pum[3]+") ]" +
                                    "  \[ [trailer]("+str(trailer)+")]\n\n"+
                                    title+"\n\n" 
                                    "#"+str(idx)  + "위 "+updown+ " #"+ msg + " "+ str(dt.datetime.strftime(pum[7],"%Y-%m-%d")) + " " + str(pum[1]) + " views"
                                    ,parse_mode='Markdown' )
                time.sleep(4) # 1분에 20개 이상 보내면 에러뜸

                chk = watchlist.find_keyword_line(pumnum + " " + title,'av_list_keyword.txt') 
                if chk != 0 :
                    telbot.send_message(chat_id= chk.split(" ")[0], text= "키워드 : " + chk.split(" ")[1] + " → " + pumnum +' [신작&순위 채널](https://t.me/+Y7PSYJPViXFiZTY1)', parse_mode = 'Markdown')
                    time.sleep(1) # 1분에 20개 이상 보내면 에러뜸
                
        print(df2str)
        telbot.send_message(chat_id=chat_id, text="※ "+msg+" / 품번 / 조회수 ※\n\n" + df2str,parse_mode='Markdown',disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        print("get_rank : ")
        print(e)
        print(traceback.format_exc())
        telbot.send_message(chat_id=chat_id, text="순위 가져오기 실패",reply_markup=ReplyKeyboardRemove())

def get_avdbs_rank(msg, chat_id):
    try:
        telbot.send_message(chat_id=chat_id, text=msg+ " 가져오는중",reply_markup=ReplyKeyboardRemove())
        pumdf = filename_set.get_avdbs_rank(msg.split(" ")[1].lower()) 
        # [index ,period(0),rank(1),pumnum(2),actor(3),title(4),date(5),avdbslink(6),thumb1(7),thumb2(8),trailer(9),up(10),down(11),oldrank(12)]

        txtfile = 'avdbs_list.txt'
        # 기존 데이터 불러오기
        with open(txtfile, 'rt', encoding = 'UTF-8') as f:
            oldtxt = f.read().splitlines() 

        df2str = ''
        for idx, pum in pumdf.iterrows():
            # print(pum[2])
            ok = False
            if pum[12] == 0 : # 새로 등장한 녀석이면
                df2str += str(idx) + " (new) [" + pum[2] + "](https://evojav.pro/en/?s="+pum[2]+") " + str(pum[10]) + " up " + str(dt.datetime.strftime(pum[5],"%Y-%m-%d")) +"\n"
                if int(idx) <= 15 : #15위 안에 들면
                    ok = True
                    updown = "(new)"
            elif idx < pum[12] : # 순위가 올라가면
                df2str += str(idx) + " ("+ str(pum[12]-idx) + "↑) [" + pum[2] + "](https://evojav.pro/en/?s="+pum[2]+") " + str(pum[10]) + " up " + str(dt.datetime.strftime(pum[5],"%Y-%m-%d")) +"\n"
                if int(idx) <= 15 : #15위 안에 들면
                    ok = True
                    updown = "("+ str(pum[12]-idx) + "↑)"
            elif idx > pum[12] : # 순위가 내려가면
                df2str += str(idx) + " ("+ str(idx - pum[12]) + "↓) [" + pum[2] + "](https://evojav.pro/en/?s="+pum[2]+") " + str(pum[10]) + " up " + str(dt.datetime.strftime(pum[5],"%Y-%m-%d")) +"\n"
            else: # 순위변동 없으면
                df2str += str(idx) + " [" + pum[2] + "](https://evojav.pro/en/?s="+pum[2]+") " + str(pum[10]) + " up " + str(dt.datetime.strftime(pum[5],"%Y-%m-%d")) +"\n"
            
            # 새로운 데이터 입력
            if pum[2] not in oldtxt: #중복검사
                title = filename_set.replaceTxt(str(pum[4]))
                title = title.replace("_","\\_")
                pumnum = pum[2].replace("_","\\_")
                actor = filename_set.replaceTxt(str(pum[3]))
                # print(pum[2])
                # print(title)
                # print(actor)
                telbot.send_message(chat_id=channel_id_av, 
                                    text="[.]("+pum[7]+")[.]("+pum[8]+") " + pumnum + " #" +pumnum.replace(" ","\\_").replace("-","\\_") + "\n\n" +
                                    "[ [javdb](https://javdb.com/search?q="+pumnum+"&f=all) ]"+
                                    "  [ [avdbs](https://www.avdbs.com/menu/search.php?kwd="+pumnum+"&seq=214407610&tab=2) ]"+
                                    "  [ [evojav](https://evojav.pro/en/?s="+pumnum+") ]"+
                                    "  [ [trailer]("+str(pum[9])+")]\n\n"+
                                    actor + "\n" + title+"\n\n" 
                                    "#"+str(idx)+"위 (new) #"+msg.replace(" ","\\_")+ " "+ str(dt.datetime.strftime(pum[5],"%Y-%m-%d")) + " " + str(pum[10]) + " up"
                                    ,parse_mode='Markdown' )
                with open(txtfile, 'a', encoding = 'UTF-8') as f:          
                    f.write(pum[2] + "\n")

                time.sleep(4) # 1분에 20개 이상 보내면 에러뜸

                chk = watchlist.find_keyword_line(pumnum + " " + title,'av_list_keyword.txt') 
                if chk != 0 :
                    telbot.send_message(chat_id= chk.split(" ")[0], text="키워드 : " + chk.split(" ")[1] + " → " + pumnum +' [신작&순위 채널](https://t.me/+Y7PSYJPViXFiZTY1)', parse_mode = 'Markdown')
                    time.sleep(1) # 1분에 20개 이상 보내면 에러뜸
                
            elif ok is True :
                title = filename_set.replaceTxt(str(pum[4]))
                title = title.replace("_","\\_")
                pumnum = pum[2].replace("_","\\_")
                actor = filename_set.replaceTxt(str(pum[3]))
                # print(pumnum)
                # print(title)
                # print(actor)
                telbot.send_message(chat_id=channel_id_av, 
                                    text="[.]("+pum[7]+")[.]("+pum[8]+") " + pumnum + " #" +pumnum.replace(" ","\\_").replace("-","\\_") + "\n\n" +
                                    "[ [javdb](https://javdb.com/search?q="+pumnum+"&f=all) ]"+
                                    "  [ [avdbs](https://www.avdbs.com/menu/search.php?kwd="+pumnum+"&seq=214407610&tab=2) ]"+
                                    "  [ [evojav](https://evojav.pro/en/?s="+pumnum+") ]"+
                                    "  [ [trailer]("+str(pum[9])+")]\n\n"+
                                    actor + "\n" + title+"\n\n"+
                                    "#"+str(idx)  + "위 "+updown+ " #"+ msg.replace(" ","\\_") + " "+ str(dt.datetime.strftime(pum[5],"%Y-%m-%d")) + " " + str(pum[10]) + " up"
                                    ,parse_mode='Markdown' )
                time.sleep(4) # 1분에 20개 이상 보내면 에러뜸

                chk = watchlist.find_keyword_line(pumnum + " " + title,'av_list_keyword.txt') 
                if chk != 0 :
                    telbot.send_message(chat_id= chk.split(" ")[0], text= "키워드 : " + chk.split(" ")[1] + " → " + pumnum +' [신작&순위 채널](https://t.me/+Y7PSYJPViXFiZTY1)', parse_mode = 'Markdown')
                    time.sleep(1) # 1분에 20개 이상 보내면 에러뜸
                
        print(df2str)
        telbot.send_message(chat_id=chat_id, text="※ "+msg.upper()+" / 품번 / UP ※\n\n" + df2str,parse_mode='Markdown',disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        print("get_avdbs_rank : ")
        print(e)
        print(traceback.format_exc())
        telbot.send_message(chat_id=chat_id, text="순위 가져오기 실패",reply_markup=ReplyKeyboardRemove())

async def get_all():
    get_rank('MONTH순위',group_id_trash)
    get_rank('WEEK순위',group_id_trash)
    get_rank('DAY순위',group_id_trash)
    get_new_release('AMA신작',group_id_trash)
    get_new_release('UNCEN신작',group_id_trash)
    get_new_release('CENS신작',group_id_trash)
    telbot.send_message(text="완료.", chat_id=group_id_trash, reply_markup=ReplyKeyboardRemove())

def get_hitomi(link, chat_id):
    filename_set.run_hitomi_downloader() #히토미 프로그램 실행
    if link.find("https://hitomi.la/") == -1 : # 링크가 아니라 품번일 경우
        pumnum = link
        link = f"https://hitomi.la/galleries/{link}.html"
    else:
        pumnum = link.split("-")[-1].split(".")[0]

    filename_set.clipboard_copy(link) 

    return pumnum, hitomi_zip_upload_to_telegram(pumnum,chat_id)

def remove_hitomi(pumnum):
    '''
    return 0 # 삭제실패
    return 1 # 삭제성공
    '''
    filePath = "C:\\Users\\seokjong_2\\Desktop\\hitomi_downloader_GUI\\hitomi_downloaded"
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            if file.path.split("(")[-1].split(")")[0] == pumnum:
                file_size, size_name = convert_size(os.path.getsize(file.path))
                if size_name == "MB" and file_size >= 50 : #50mb 이상이면 스킵
                    print("파일 용량 > 50mb")
                else:
                    os.remove(file.path)
                    print('Remove File') 
                return 1 # 삭제성공
    else:
        print('Directory Not Found')
        return 0 # 삭제실패
    return 0 # 삭제실패

def get_all_hitomi_writer(link, chat_id):
    filename_set.run_hitomi_downloader() #히토미 프로그램 실행

    if link.find("#writer ") != -1 : # 작가명일 경우
        l = link.replace("#writer ", "")
        link = f"https://hitomi.la/artist/{l}-korean.html"
    elif link.find("#group ") != -1: #그룹명일 경우
        l = link.replace("#group ", "")
        link = f"https://hitomi.la/group/{l}-korean.html"
    elif link.find("https://hitomi.la/") : pass # url일 경우
    else : pass #나머지도 그냥 패스 어짜피 결과 안나옴

    writer, pumtitles, pumlinks = filename_set.get_all_hitomi_writer(link)

    txt = "#히토미 작가 : #" +writer+ " [링크](" + link +") \n\n"

    i = 0
    for pumtitle, pumlink in zip(pumtitles, pumlinks):
        pumnum = pumlink.split("-")[-1].split(".")[0]
        if (pumlink.find("…") or pumlink.find("...")) != -1 :
            txt += pumtitle.replace("["," ").replace("]"," ").replace("("," ").replace(")"," ").replace("*"," ").replace("-"," ").replace("_"," ")\
                    +"\n"+pumlink +" (#I"+pumnum+")\n\n" 
        else:
            txt += "["+pumtitle.replace("["," ").replace("]"," ").replace("("," ").replace(")"," ").replace("*"," ").replace("-"," ").replace("_"," ")\
                    +"]("+pumlink+") (#I"+pumnum+")\n\n"
        i += 1
        if i % 10 == 0 : #10개 채워지면 출력
            telbot.send_message(chat_id=chat_id, text=txt, parse_mode='Markdown' )
            txt =""
        filename_set.clipboard_copy(pumlink) #히토미 클립보드 자동 다운로드
        print("|", end="")
        time.sleep(1)
    if i % 10 != 0: #나머지 출력
        telbot.send_message(chat_id=chat_id, text=txt, parse_mode='Markdown' )
        txt =""
    print("/")

    #파일 업로드
    zippath = "C:\\Users\\seokjong_2\\Desktop\\hitomi_downloader_GUI\\hitomi_downloaded"
    telbot.send_message(chat_id=group_id_trash, text="총 : " + str(len(pumtitles)) + "개")
    k=1
    for pumtitle, pumlink in zip(pumtitles, pumlinks):
        pumnum = pumlink.split("-")[-1].split(".")[0]
        
        j=1
        while(j==1):
            current_list = os.listdir(zippath)
            for i in current_list: 
                filenum = i.split("(#I")[-1].split(")")[0]
                if pumnum == filenum :
                    path = os.path.join(zippath, i) # 현재 경로의 모든객체의 전체경로
                    if path.endswith('zip') : #zip 파일일 경우
                        print(str(k), end=". ")
                        check_file_size_stable(path)
                        file_size, size_name = convert_size(os.path.getsize(path))

                        thumbNames = []
                        thumbnails = []
                        with ZipFile(path, 'r') as zipObj:
                            zip_namelist = zipObj.namelist()

                            if len(zip_namelist) <= 10 : cnt = len(zip_namelist)
                            else : cnt = 4

                            for l in range(0, cnt):
                                zipObj.extract(zip_namelist[l], zippath)
                                check_file_size_stable(os.path.join(zippath, zip_namelist[l]))

                                if zip_namelist[l].endswith('webp'): #webp -> png 변환
                                    try:
                                        img = Image.open(os.path.join(zippath, zip_namelist[l])).convert('RGB') 
                                        img.save(os.path.join(zippath, zip_namelist[l].replace('webp','jpg')), 'jpeg')
                                        img.close()
                                        check_file_size_stable(os.path.join(zippath, zip_namelist[l]).replace('webp','jpg'))
                                        thumbNames.append(zip_namelist[l])
                                        thumbNames[l] = zip_namelist[l].replace('webp','jpg')
                                        thumbnails.append(telegram.InputMediaPhoto(open(os.path.join(zippath, thumbNames[l]),'rb')))
                                    except:
                                        print(zip_namelist[l] + " 변환 실패", end=" / / ")
                                os.remove(os.path.join(zippath, zip_namelist[l])) #webp 삭제

                        try:
                            telbot.send_media_group(chat_id=group_id_hitomi, media=thumbnails, timeout=1000)
                        except telegram.error.RetryAfter as e:
                            print(e)
                            print(60)
                            time.sleep(60)
                            telbot.send_media_group(chat_id=group_id_hitomi, media=thumbnails, timeout=1000)
                        except Exception as e:
                            print(e)

                        if size_name == "MB" and file_size >= 50 : #50mb 이상이면 스킵
                            print(str(file_size) + size_name, end=" > 50MB ")
                            try:
                                telbot.send_message(chat_id=group_id_hitomi,text=i + "\n>50mb : "+ str(file_size) + size_name)
                            except telegram.error.RetryAfter as e:
                                print(e)
                                time.sleep(60)
                                telbot.send_message(chat_id=group_id_hitomi,text=i + "\n>50mb : "+ str(file_size) + size_name)
                            except Exception as e:
                                print(e)
                            j=0

                            print("미리보기 삭제", end=' ')
                            for thumb in thumbNames: os.remove(os.path.join(zippath, thumb))
                            print("완료")
                            break 
                        else:
                            print("파일 로딩", end=" → ")
                            alzip = open(path , 'rb')
                            try: 
                                print("업로드",end=" → ")
                                try:
                                    telbot.send_document(chat_id=group_id_hitomi, document=alzip, filename=i, caption=i, timeout=1000)
                                except telegram.error.RetryAfter as e:
                                    print(e)
                                    print(60)
                                    time.sleep(60)
                                    telbot.send_document(chat_id=group_id_hitomi, document=alzip, filename=i, caption=i, timeout=1000)
                                print("완료", end=" → ")
                                print("삭제", end=' ')
                                alzip.close()
                                os.remove(path)
                            except: 
                                print("업로드 실패")
                                try:
                                    telbot.send_message(chat_id=group_id_hitomi,text=i + "\n파일전송 실패 : " + str(file_size) + size_name)
                                except telegram.error.RetryAfter as e:
                                    print(e)
                                    time.sleep(60)
                                    telbot.send_message(chat_id=group_id_hitomi,text=i + "\n파일전송 실패 : " + str(file_size) + size_name)
                                alzip.close()
                            j=0
                        
                        print("미리보기 삭제", end=' ')
                        for thumb in thumbNames: os.remove(os.path.join(zippath, thumb))
                        print("완료")
        k+=1
        txt=""
    return i

def hitomi_zip_upload_to_telegram(pumnum, chat_id):
    '''
    return 0 #폴더안에 아무것도 없음
    return 1 #파일전송 완료
    '''
    zippath = "C:\\Users\\seokjong_2\\Desktop\\hitomi_downloader_GUI\\hitomi_downloaded"
    time.sleep(10)
    k=1
    while(k==1):
        current_list = os.listdir(zippath)
        for i in current_list: 
            if i.split("(#I")[-1].split(")")[0] == pumnum: #폴더안에 해당하는 작품이 있으면
                path = os.path.join(zippath, i) # 현재 경로의 모든객체의 전체경로
                if path.endswith('zip') : #zip 파일일 경우
                    print(i.split("(#I")[-1].split(")")[0], end=" → ")
                    check_file_size_stable(path)
                    file_size, size_name = convert_size(os.path.getsize(path))
                    thumbNames = []
                    thumbnails = []
                    with ZipFile(path, 'r') as zipObj:
                        zip_namelist = zipObj.namelist()

                        if len(zip_namelist) <= 10 : cnt = len(zip_namelist)
                        else : cnt = 4

                        for l in range(0, cnt):
                            zipObj.extract(zip_namelist[l], zippath)   
                            check_file_size_stable(os.path.join(zippath, zip_namelist[l]))                             

                            if zip_namelist[l].endswith('webp'): #webp -> png 변환
                                try: 
                                    img = Image.open(os.path.join(zippath, zip_namelist[l])).convert('RGB') 
                                    img.save(os.path.join(zippath, zip_namelist[l].replace('webp','jpg')), 'jpeg')
                                    img.close()
                                    check_file_size_stable(os.path.join(zippath, zip_namelist[l].replace('webp','jpg')))
                                    thumbNames.append(zip_namelist[l])
                                    thumbNames[l] = zip_namelist[l].replace('webp','jpg')
                                    thumbnails.append(telegram.InputMediaPhoto(open(os.path.join(zippath, thumbNames[l]),'rb')))
                                except:
                                    print(zip_namelist[l] + " 변환 실패", end=" / / ")
                            os.remove(os.path.join(zippath, zip_namelist[l])) #webp 삭제
                    try:
                        telbot.send_media_group(chat_id=chat_id, media=thumbnails, timeout=1000)
                    except telegram.error.RetryAfter as e:
                        print(e)
                        time.sleep(60)
                        telbot.send_media_group(chat_id=chat_id, media=thumbnails, timeout=1000)
                    except Exception as e:
                        print(e)

                    if size_name == "MB" and file_size >= 50 : #50mb 이상이면 스킵
                        telbot.send_message(chat_id=chat_id, text="파일 용량 > 50mb")
                        print(str(file_size)+size_name)
                    else:
                        print("파일 로딩",end=" → ")
                        alzip = open(path , 'rb')
                        try: 
                            print("업로드",end=" → ")
                            try:
                                telbot.send_document(chat_id=chat_id, document=alzip, filename=i, caption=i, timeout=1000)
                            except telegram.error.RetryAfter as e:
                                print(e)
                                time.sleep(60)
                                telbot.send_document(chat_id=chat_id, document=alzip, filename=i, caption=i, timeout=1000)
                            print("완료")
                        except Exception as e:
                            print("실패")
                            print(e)                             
                            telbot.send_message(chat_id=chat_id,text="파일 전송 실패 : "+ i + "\n"+ str(file_size) + size_name)
                        alzip.close()
                    for thumb in thumbNames: os.remove(os.path.join(zippath, thumb)) #미리보기 삭제
                    return 1
            
def hitomi_writer_zip_upload_to_telegram(cnt, chat_id):
    '''cnt : 갯수'''

    zippath = "C:\\Users\\seokjong_2\\Desktop\\hitomi_downloader_GUI\\hitomi_downloaded"

    k = 1
    while(k==1):
        current_list = os.listdir(zippath)			# 경로의 모든 객체들
        if len(current_list) == cnt: #갯수가 맞으면
            for i in current_list: 
                path = os.path.join(zippath, i) 			# 현재 경로의 모든객체의 전체경로
                if os.path.isdir(path):  #폴더(압축안된)가 있으면 다시 처음으로
                    # time.sleep(4)
                    k=1
                    break
                k=0 #while 탈출
        else: #갯수가 다르면 다시 처음으로
            # time.sleep(1)
            pass

    print("총 " + str(len(current_list)) + "개")
    j=1
    for i in current_list: 
        print(i + " " + i.split("(#I")[-1].split(")")[0], end=" → ")
        path = os.path.join(zippath, i)
        file_size, size_name = convert_size(os.path.getsize(path))
        if size_name == "MB" and file_size >= 50 : #50mb 이상이면 스킵
            print(str(file_size)+size_name)
        else:
            print("파일 로딩",end=" → ")
            alzip = open(path , 'rb')
            try: 
                print("업로드",end=" → ")
                telbot.send_document(chat_id=chat_id, document=alzip, filename=i, caption=i, timeout=1000)
                print("완료")
                time.sleep(4)
            except: 
                print("실패")
                telbot.send_message(chat_id=chat_id,text="파일 전송 실패 : "+ i + "\n"+ str(file_size) + size_name)
            alzip.close() 
            j += 1

def hitomi_folder_upload(chat_id):
    '''
    return 0 #폴더안에 아무것도 없음
    return len(current_list) #파일전송 완료. 파일 갯수 반환
    '''
    zippath = "C:\\Users\\seokjong_2\\Desktop\\hitomi_downloader_GUI\\hitomi_downloaded"
    current_list = os.listdir(zippath)
    print(current_list)
    if len(current_list) == 0: return 0 #폴더안에 아무것도 없음
    else:
        print("총 " + str(len(current_list)) + "개")
        telbot.send_message(chat_id=group_id_trash, text="총 : " + str(len(current_list)) + "개")

        today = dt.datetime.now()

        fileListTxt = "#upload" + " #D"+today.strftime('%y%m%d') + "\n\n"
        fileListTxtTmp = ""
        for filename in current_list:
            fileListTxtTmp = fileListTxt + filename.replace(".zip","") + "\n\n"
            if len(fileListTxtTmp) >= 1000: #1천자 넘으면 잘라서 전송
                telbot.send_message(chat_id=channel_id_hitomi, text=fileListTxt)
                fileListTxt =""
            else :
                fileListTxt += filename.replace(".zip","") + "\n\n"
            fileListTxtTmp =""
        telbot.send_message(chat_id=channel_id_hitomi, text=fileListTxt)

        j=1
        for i in current_list: 
            path = os.path.join(zippath, i) # 현재 경로의 모든객체의 전체경로
            if path.endswith("zip"): # zip 파일일 경우
                print(str(j), end=". ")
                file_size, size_name = convert_size(os.path.getsize(path))
                thumbNames = []
                thumbnails = []
                with ZipFile(path, 'r') as zipObj:
                    zip_namelist = zipObj.namelist()

                    if len(zip_namelist) <= 10 : cnt = len(zip_namelist)
                    else : cnt = 4

                    for l in range(0, cnt):
                        zipObj.extract(zip_namelist[l], zippath)
                        check_file_size_stable(os.path.join(zippath, zip_namelist[l]))

                        if zip_namelist[l].endswith('webp'): #webp -> png 변환
                            try:
                                img = Image.open(os.path.join(zippath, zip_namelist[l])).convert('RGB') 
                                img.save(os.path.join(zippath, zip_namelist[l].replace('webp','jpg')), 'jpeg')
                                img.close()
                                check_file_size_stable(os.path.join(zippath, zip_namelist[l]).replace('webp','jpg'))
                                thumbNames.append(zip_namelist[l])
                                thumbNames[l] = zip_namelist[l].replace('webp','jpg')
                                thumbnails.append(telegram.InputMediaPhoto(open(os.path.join(zippath, thumbNames[l]),'rb')))
                            except:
                                print(zip_namelist[l] + " 변환 실패", end=" / / ")
                        os.remove(os.path.join(zippath, zip_namelist[l])) #webp 삭제

                try:
                    telbot.send_media_group(chat_id=chat_id, media=thumbnails, timeout=1000)    
                except telegram.error.RetryAfter as e:
                    print(e)
                    print(60)
                    time.sleep(60) 
                    telbot.send_media_group(chat_id=chat_id, media=thumbnails, timeout=1000)
                except Exception as e:
                    print(e)    

                if size_name == "MB" and file_size >= 50 : #50mb 이상이면 스킵
                    print(str(file_size)+size_name, end=" ")
                    try:
                        telbot.send_message(chat_id=chat_id,text=i + "\n>50mb : "+ str(file_size) + size_name)
                    except telegram.error.RetryAfter as e:
                        print(e)
                        time.sleep(60)
                        telbot.send_message(chat_id=chat_id,text=i + "\n>50mb : "+ str(file_size) + size_name)
                    except Exception as e:
                        print(e)  

                else:
                    print("파일 로딩", end=' -> ')
                    alzip = open(path , 'rb')
                    try: 
                        print("업로드", end=' -> ')
                        try:
                            telbot.send_document(chat_id=chat_id, document=alzip, filename=i, caption=i, timeout=1000)
                        except telegram.error.RetryAfter as e:
                            print(e)
                            print(60)
                            time.sleep(60)
                            telbot.send_document(chat_id=chat_id, document=alzip, filename=i, caption=i, timeout=1000)
                        print("완료", end=" → ")
                        print("삭제", end=' ')
                        alzip.close()
                        os.remove(path) #zip 파일 삭제
                    except Exception as e: 
                        print("업로드 실패 ")
                        print(e)
                        try:
                            telbot.send_message(chat_id=chat_id,text="파일 업로드 실패 : "+ i + "\n"+ str(file_size) + size_name)
                        except telegram.error.RetryAfter as e:
                            print(e)
                            time.sleep(60)
                            telbot.send_message(chat_id=chat_id,text="파일 업로드 실패 : "+ i + "\n"+ str(file_size) + size_name)
                        alzip.close()

                print("썸네일삭제", end=" ")
                for thumb in thumbNames: os.remove(os.path.join(zippath, thumb)) #미리보기 삭제
                print("완료")
                j += 1

        return len(current_list)

def get_hitomi_rank(chat_id, period):
    '''
    period : today, week, month, year
    '''
    pumtitles, pumwriters, pumlinks, ranks = filename_set.get_hitomi_rank(period)

    # 1. 일단다운로드
    print("hitomi " + period + " rank download...", end=" ")
    for pumlink in pumlinks:
        filename_set.clipboard_copy(pumlink)
        time.sleep(1)
    print("complete")

    # 2. zip파일 있는지 확인
    # 3. 업로드
    zippath = "C:\\Users\\seokjong_2\\Desktop\\hitomi_downloader_GUI\\hitomi_downloaded"
    today = dt.datetime.now()

    print("today  " + today.strftime('%y%m%d'))
    
    print("총 : " + str(len(pumtitles)) +"개")
    telbot.send_message(chat_id=group_id_trash, text="총 : " + str(len(pumtitles)) + "개")

    rankListTxt = "#"+period + " #순위" + " #D"+today.strftime('%y%m%d') + "\n\n"
    for pumtitle, pumwriter, rank, pumlink in zip(pumtitles, pumwriters, ranks, pumlinks):
        pumnum = pumlink.split("-")[-1].split(".")[0]
        rankListTxt += str(rank) + "."
        if len(pumwriter.split(","))>=2: #작가 2명이상
            for w in pumwriter.split(","):
                rankListTxt += " [#" +w +"]"
        else: #작가 1명
            rankListTxt += " [#" + pumwriter +"]"
        
        rankListTxt += " " + pumtitle + " (#I"+pumnum+")\n\n"

        
    telbot.send_message(chat_id=channel_id_hitomi, text=rankListTxt)

    k=1
    for pumtitle, pumwriter, pumlink, rank in zip(pumtitles, pumwriters, pumlinks, ranks):
        pumnum = pumlink.split("-")[-1].split(".")[0]
        
        if len(pumwriter.split(","))>=2: #작가 2명이상
            txt = "#"+ period + " #순위 #"+str(rank)+"위 " + "#D"+today.strftime('%y%m%d') + "\n"
            for w in pumwriter.split(","):
                txt += " \[#" +w +"]"
        else: #작가 1명
            txt = "#"+ period + " #순위 #"+str(rank)+"위 " +"#D"+today.strftime('%y%m%d')+"\n\[#" +pumwriter +"]"

        if (pumlink.find("…") or pumlink.find("...")) == -1 : #링크에 ...이 없을경우
            txt += "\n["+pumtitle.replace("["," ").replace("]"," ").replace("("," ").replace(")"," ").replace("*"," ").replace("-"," ").replace("_"," ")+\
                    "]("+pumlink+")" +" (#I"+pumnum+")" 
        else: txt += "\n"+pumtitle.replace("["," ").replace("]"," ").replace("("," ").replace(")"," ").replace("*"," ").replace("-"," ").replace("_"," ")+\
                    "\n"+pumlink +" (#I"+pumnum+")" 
        
        
        
        j=1
        while(j==1):
            current_list = os.listdir(zippath)
            for i in current_list: 
                filenum = i.split("(#I")[-1].split(")")[0]
                if pumnum == filenum :
                    path = os.path.join(zippath, i) # 현재 경로의 모든객체의 전체경로
                    if path.endswith('zip') : #zip 파일일 경우
                        print(str(k), end=". ")
                        check_file_size_stable(path)
                        file_size, size_name = convert_size(os.path.getsize(path))

                        thumbNames = []
                        thumbnails = []
                        with ZipFile(path, 'r') as zipObj:
                            zip_namelist = zipObj.namelist()

                            if len(zip_namelist) <= 10 : cnt = len(zip_namelist)
                            else : cnt = 4

                            for l in range(0, cnt):
                                zipObj.extract(zip_namelist[l], zippath)
                                check_file_size_stable(os.path.join(zippath, zip_namelist[l]))

                                if zip_namelist[l].endswith('webp'): #webp -> png 변환
                                    try:
                                        img = Image.open(os.path.join(zippath, zip_namelist[l])).convert('RGB') 
                                        img.save(os.path.join(zippath, zip_namelist[l].replace('webp','jpg')), 'jpeg')
                                        img.close()
                                        check_file_size_stable(os.path.join(zippath, zip_namelist[l].replace('webp','jpg')))
                                        thumbNames.append(zip_namelist[l])
                                        thumbNames[l] = zip_namelist[l].replace('webp','jpg')
                                        thumbnails.append(telegram.InputMediaPhoto(open(os.path.join(zippath, thumbNames[l]),'rb')))
                                    except:
                                        print(zip_namelist[l] + " 변환 실패", end=" / / ")
                                os.remove(os.path.join(zippath, zip_namelist[l])) #webp 삭제

                        try:
                            telbot.send_media_group(chat_id=chat_id, media=thumbnails, timeout=1000)
                        except telegram.error.RetryAfter as e:
                            print(e)
                            time.sleep(60)
                            telbot.send_media_group(chat_id=chat_id, media=thumbnails, timeout=1000)
                        except Exception as e:
                            print(e)

                        if size_name == "MB" and file_size >= 50 : #50mb 이상이면 스킵
                            print(str(file_size) + size_name, end=" → ")
                            try:
                                telbot.send_message(chat_id=chat_id,text=txt + "\n>50mb : "+ str(file_size) + size_name, parse_mode='Markdown')
                            except telegram.error.RetryAfter as e:
                                print(e)
                                time.sleep(60)
                                telbot.send_message(chat_id=chat_id,text=txt + "\n>50mb : "+ str(file_size) + size_name, parse_mode='Markdown')
                            except Exception as e:
                                print(e)

                            j=0
                            print("미리보기 삭제", end=' ')
                            for thumb in thumbNames:
                                os.remove(os.path.join(zippath, thumb))
                            print("완료")
                            break 
                        else:
                            print("파일 로딩", end=" → ")
                            alzip = open(path , 'rb')
                            try: 
                                print("업로드",end=" → ")
                                try:
                                    telbot.send_document(chat_id=chat_id, document=alzip, filename=i, caption=txt, timeout=1000, parse_mode='Markdown')
                                except telegram.error.RetryAfter as e:
                                    print(e)
                                    time.sleep(60)
                                    telbot.send_document(chat_id=chat_id, document=alzip, filename=i, caption=txt, timeout=1000, parse_mode='Markdown')
                                print("완료", end=" → ")
                                print("파일삭제", end=' ')
                                alzip.close()
                                os.remove(path)
                            except: 
                                try:
                                    telbot.send_message(chat_id=chat_id,text=txt + "\n파일전송 실패 : " + str(file_size) + size_name, parse_mode='Markdown')
                                except telegram.error.RetryAfter as e:
                                    print(e)
                                    time.sleep(60)    
                                    telbot.send_message(chat_id=chat_id,text=txt + "\n파일전송 실패 : " + str(file_size) + size_name, parse_mode='Markdown')
                                print("실패")
                                alzip.close()
                            
                            j=0
                        
                        print("썸네일삭제", end=" ")
                        for thumb in thumbNames:
                            os.remove(os.path.join(zippath, thumb))
                        print("완료")
        k+=1




# 파일 용량 단위 변환
def convert_size(size_bytes):
    '''
    return 용량(float), 단위(str)
    '''
    import math
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return s, size_name[i]

# 파일 용량 변하지 않는지 확인
def check_file_size_stable(filePath):
    print(os.path.basename(filePath), end = " : ")

    t=1
    while(t==1):
        file_size, size_name = convert_size(os.path.getsize(filePath))
        print(str(file_size)+size_name, end="")
        time.sleep(1)
        file_size1, size_name1 = convert_size(os.path.getsize(filePath))
        # print(str(file_size1)+size_name1, end=" ")
        if file_size == file_size1 : t=0    #파일 크기가 같으면 종료 
        else: print(" → ", end="")          #다르면 아직 변환중인 파일
    print(" // ", end= "")
    return 1

# 바이낸스 정보 , 선물 설정
def bnc():
    binance = ccxt.binance({
        'apiKey': myApikey,
        'secret': mySecretkey,
        'enableRateLimit': True,
        'options': { 
        'defaultType': 'future'                # 선물거래
        }
    })
    return binance   

# 바이낸스 딕셔너리 데이터를 데이터 프레임으로 변환
def dic2df(dic):
    df = pd.DataFrame(dic, columns = ['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    return df

# 과거 데이터 호출
def fetch_ohlcvs(coin='BTC/USDT', timeframe='1d', limit=30):
    binance = bnc()
    ohlcv = binance.fetch_ohlcv(symbol=coin, timeframe=timeframe, limit=limit)   #데이터 불러오기  
                                        # 시간간격 :'1m','3m','5m','15m','30m','1h','2h','4h','6h','8h','12h','1d','3d','1w','1M'
    return dic2df(ohlcv)   # 딕셔너리를 데이터프레임으로 변환

def fetch_jusik(name, country, count):
    ''' country : krx, us'''
    today = dt.date.today()
    delta = dt.timedelta(days=count)    # count 봉 전부터
    past = today-delta

    if name == "BRK/B": name = "BRK-B"

    if country == "krx":
        df = fdr.DataReader(codefind(name, "krx"), past, today)
    elif country == "us":
        # df = fdr.DataReader(name, past, today)
        try:
            df = pdr.get_data_yahoo(name, past, today)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            df = fdr.DataReader(name, past, today)
            

    df.rename(columns = {'Open' : 'open', "Close" : "close", "High" : "high", "Low":"low"}, inplace = True)
    return df

def fetch_jisu(name, count):
    '''
    ks11, kq11, dji, ixic, us500, usd/krw
    '''
    today = dt.date.today()
    delta = dt.timedelta(days=count)    # count 봉 전부터
    past = today-delta
 
    df = fdr.DataReader(name, past, today)

    df.rename(columns = {'Open' : 'open', "Close" : "close", "High" : "high", "Low":"low"}, inplace = True)

    return df

def Ema(df, span=8):
    '''ema 지수이평선 '''
    df["ema"] = df["close"].ewm(span=span, adjust=False).mean()
    return df

def BolingerBand(df, n=20, k=2):
    '''
    20ma, bolUpper, bolLower
    '''
    df['20ma'] = df['close'].rolling(window=n).mean()  
    df['bolUpper'] = df['close'].rolling(window=n).mean() + k* df['close'].rolling(window=n).std()
    df['bolLower'] = df['close'].rolling(window=n).mean() - k* df['close'].rolling(window=n).std()
    return df

def Heiken_ashi(df):
    ''' 
    캔들 시가, 종가 : open, close
    HA캔들 시가, 종가, 고가, 저가 : Open, Close, High, Low
    '''
    df_HA = df
    df_HA['Open'] = df['open']

    # HA 종가 = (현재캔들)(시가+종가+저가+고가)/4
    df_HA["Close"] = (df["open"]+df["high"]+df["low"]+df["close"])/4 
    for i in range(df_HA.shape[0]):  
        if i > 0: 
            # HA 시가 = (이전 HA 시가+ 이전 HA 종가)/2
            df_HA.loc[df_HA.index[i],"Open"] = (df_HA["Open"][i-1] + df_HA["Close"][i-1])/2   
            # HA 고가 = 최대(캔들고가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"High"] = max(df["high"][i],df_HA["Open"][i],df_HA["Close"][i])
            # HA 저가 = 최소(캔들저가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"Low"] = min(df["low"][i],df_HA["Open"][i],df_HA["Close"][i]) 

    return df_HA    

def Rsi(df, period=14):
    ''' rsi, lin30, line70 '''
    dfRSI = df
    dfRSI['U'] = np.where(dfRSI.diff(1)['close'] > 0, dfRSI.diff(1)['close'], 0)  # df.diff(1) : 기준일 종가 - 전일 종가, 0보다 크면 증가분을, 아니면 0을 넣음
    dfRSI['D'] = np.where(dfRSI.diff(1)['close'] < 0, dfRSI.diff(1)['close']*(-1), 0) # 기준일 종가 - 전일 종가, 0보다 작으면 감소분을, 아니면 0을 넣음
    dfRSI['AU'] = dfRSI['U'].rolling(window=period).mean() # period=14 동안의 U의 (이동)평균
    dfRSI['AD'] = dfRSI['D'].rolling(window=period).mean() # period=14 동안의 D의 (이동)평균
    df['rsi'] = dfRSI['AU'] / (dfRSI['AD']+dfRSI['AU']) * 100
    df['line30'] = 30
    df['line70'] = 70
    return df

def Macd(df, short=12, long=26, signal=9):
    ''' macd, macdSignal, macdOsc'''
    df['macd']=df['close'].ewm( span=short, min_periods= long-1, adjust=False).mean() - df['close'].ewm( span=long, min_periods=long-1, adjust=False).mean()
    df['macdSignal'] = df['macd'].ewm( span = signal, min_periods=signal-1, adjust=False).mean()
    df['macdOsc'] = df["macd"] - df['macdSignal']
    return df

def ichimoku(df):
    '''
    tenkan, kijun, senkouSpanA, senkouSpanB, chikouSpan
    '''
    high_prices = df['high']
    close_prices = df['close']
    low_prices = df['low']
    dates = df.index
    
    nine_period_high =  df['high'].rolling(window=9).max()
    nine_period_low = df['low'].rolling(window=9).min()
    df['tenkan'] = (nine_period_high + nine_period_low) /2  #전환선
    
    period26_high = high_prices.rolling(window=26).max()
    period26_low = low_prices.rolling(window=26).min()
    df['kijun'] = (period26_high + period26_low) / 2    #기준선
    
    df['senkouSpanA'] = ((df['tenkan'] + df['kijun']) / 2).shift(26)  #선행스팬A
    
    period52_high = high_prices.rolling(window=52).max()
    period52_low = low_prices.rolling(window=52).min()
    df['senkouSpanB'] = ((period52_high + period52_low) / 2).shift(26)   #선행스팬B
    
    df['chikouSpan'] = close_prices.shift(-26)    #후행스팬

    return df

#  - 봉 -> 해당봉의 모든 지표 표시
def display_all_signal(df, name, interval):
    # df.dropna(inplace=True)         # Na 값 있는 행은 지움

    df = df.rename_axis("Date").reset_index()
    # print(df.head)
    if name == "KRW-BTC" or name == "KRW-ETH" or name == "BTC/USDT" or name == "ETH/USDT":
        df['Date'] = df['Date'].apply(lambda x : dt.datetime.strftime(x, '%y-%m-%d %H:%M')) # Datetime to str
    else:
        df['Date'] = df['Date'].apply(lambda x : dt.datetime.strftime(x, '%y-%m-%d')) # Datetime to str
    df_date = df['Date']
    

    ha = pltygo.Candlestick(x=df_date,
                        open=df['Open'],high=df['High'],
                        low=df['Low'], close=df['Close'],
                        name = 'HA',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
    ema = pltygo.Scatter(x=df_date, y=df['ema'], name="8ema", mode='lines', line=dict(color="green", width=0.8))

    macd = pltygo.Scatter( x=df_date, y=df['macd'],  mode='lines',name="MACD") 
    signal = pltygo.Scatter( x=df_date, y=df['macdSignal'], mode='lines', name="Signal") 
    oscillator = pltygo.Bar( x=df_date, y=df['macdOsc'], name="oscillator") 

    rsi = pltygo.Scatter(x=df_date, y=df['rsi'],  mode='lines',name="RSI")
    line30 = pltygo.Scatter(x=df_date, y=df['line30'], name="30", mode='lines',
                            line=dict(color='firebrick', width=0.5))
    line70 = pltygo.Scatter(x=df_date, y=df['line70'], name="70", mode='lines',
                            line=dict(color='royalblue', width=0.5))

    # ichimoku
    kijun = pltygo.Scatter(x=df_date, y=df['kijun'], name="kijun",  mode='lines', line=dict(color='gray', width=2))
    tenkan = pltygo.Scatter(x=df_date, y=df['tenkan'], name="tenkan",  mode='lines',line=dict(color='red', width=2))
    senkouSpanA = pltygo.Scatter(x=df_date, y=df['senkouSpanA'], name="spanA",  mode='lines',line=dict(color='rgba(167, 59, 206, 0.9)', width=0.8),fill=None)#'tonexty',fillcolor ='rgba(235, 233, 102, 0.5)'
    senkouSpanB = pltygo.Scatter(x=df_date, y=df['senkouSpanB'], name="spanB",  mode='lines',line=dict(color='green', width=0.8),fill='tonexty',fillcolor ='rgba(111, 236, 203, 0.5)')


    ohlc = pltygo.Candlestick(x=df_date,
                        open=df['open'],high=df['high'],
                        low=df['low'], close=df['close'],
                        name = 'OHLC',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
    bolUp = pltygo.Scatter(x=df_date, y=df['bolUpper'], name="bolUpper",  mode='lines', line=dict(color='black', width=1))
    bolLow = pltygo.Scatter(x=df_date, y=df['bolLower'], name="bolLower",  mode='lines',line=dict(color='black', width=1))
    ma20 = pltygo.Scatter(x=df_date, y=df['20ma'], name="20ma",  mode='lines',line=dict(color='orange', width=0.8))
    vol = pltygo.Bar(x=df_date, y=df['Volume'], name="vol")

    # OHLC,일목 차트
    fig1 = subplots.make_subplots(rows=1, cols=1, shared_xaxes=True,
                                subplot_titles=('ichimoku Chart, kijun : '+str(format(round(df['kijun'].iloc[-1],2),','))))       # row : 행 , col : 열

    # HA 차트 + 20ma 8ema
    fig2 = subplots.make_subplots(rows=2, cols=1, vertical_spacing=0.05,
                                row_width=[1,3], shared_xaxes=True,
                                subplot_titles=('Heiken Ashi, close : '+str(format(round(df['close'].iloc[-1],2),',')),"volume"))       # row : 행 , col : 열

    # OHLC,볼밴 + RSI + MACD 차트
    fig3 = subplots.make_subplots(rows=2, cols=1, vertical_spacing=0.05,
                                row_width=[1,1], shared_xaxes=True, 
                                subplot_titles=('RSI : '+str(round(df['rsi'].iloc[-1],2)), 'MACD' ))       # row : 행 , col : 열
    
    # fig1

    setIchimoku = [ohlc, senkouSpanA, senkouSpanB, kijun]
    for ichi in setIchimoku: 
        fig1.add_trace(ichi, 1,1)
    
    fig1.update_xaxes(rangeslider_thickness = 0, nticks = 5, type='category')     # 스크롤바 두께
    fig1.update_layout(title_text=name+ " " + interval +" chart", showlegend=False)
    fig1.update_yaxes(side="right", nticks =10)
    fig1.update_layout(legend=dict(yanchor="top", y=1, xanchor="left", x=0))
    fig1.write_image("fig1.png")

    # fig2

    setHa = [ha, ma20, ema]
    for ha in setHa: 
        fig2.add_trace(ha, 1,1)
    
    fig2.add_trace(vol, 2,1)
    
    fig2.update_xaxes(rangeslider_thickness = 0, nticks = 5, type='category')     # 스크롤바 두께
    fig2.update_layout(title_text=name+ " " + interval +" chart", showlegend=False)
    fig2.update_yaxes(side="right", nticks =10)
    # fig2.update_layout(legend=dict(yanchor="top", y=1, xanchor="left", x=0))
    fig2.write_image("fig2.png")

    # fig3 
    setRsi = [rsi, line30, line70]
    for rsi in setRsi: 
        fig3.add_trace(rsi, 1,1)

    setMacd = [macd, signal, oscillator]
    for macd in setMacd: 
        fig3.add_trace(macd, 2,1) 

    fig3.update_xaxes(rangeslider_thickness = 0, nticks = 5, type='category')     # 스크롤바 두께
    fig3.update_layout(title_text=name+ " " + interval +" chart", showlegend=False)
    fig3.update_yaxes(side="right")
    # fig3.update_layout(legend=dict(yanchor="top", y=1, xanchor="left", x=0))
    fig3.write_image("fig3.png")

#  - 지표 -> 모든 봉의 해당 지표 값 표시
def display_all_interval(dfSet,intervalSet, name ,signal):
    '''
    signal : 'ohlc', 'ha', 'macd', 'rsi', 
    '''

    if signal == 'ohlc':
        fig = subplots.make_subplots(rows=len(intervalSet), cols=1, 
                                vertical_spacing=0.05,
                                subplot_titles=intervalSet)
        for i in range(len(intervalSet)):
            dfSet[i].dropna(inplace=True)
            ohlc = pltygo.Candlestick(x=dfSet[i].index,
                        open=dfSet[i]['open'],high=dfSet[i]['high'],
                        low=dfSet[i]['low'], close=dfSet[i]['close'],
                        name =intervalSet[i]+ 'OHLC',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
            fig.add_trace(ohlc, i+1,1) 
            
    if signal == 'ha':
        fig = subplots.make_subplots(rows=len(intervalSet), cols=1, 
                                vertical_spacing=0.05,
                                subplot_titles=intervalSet, )
        for i in range(len(intervalSet)):
            dfSet[i] = Heiken_ashi(dfSet[i])
            dfSet[i].dropna(inplace=True)
            ha = pltygo.Candlestick(x=dfSet[i].index,
                        open=dfSet[i]['Open'],high=dfSet[i]['High'],
                        low=dfSet[i]['Low'], close=dfSet[i]['Close'],
                        name = intervalSet[i]+'HA',
                        increasing={'line': {'color': 'firebrick'}},
                        decreasing={'line': {'color': 'royalblue'}},
                        )
            fig.add_trace(ha, i+1,1) 
    
    if signal == 'macd':
        fig = subplots.make_subplots(rows=int(len(intervalSet)/2), cols=2, 
                                vertical_spacing=0.05,
                                subplot_titles=intervalSet)

        for i in range(len(intervalSet)):
            dfSet[i] = Macd(dfSet[i])
            dfSet[i].dropna(inplace=True)

            macd = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['macd'],
                                    marker=dict(color='red')) 
            macdSignal = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['macdSignal'], marker=dict(color='blue')) 
            oscillator = pltygo.Bar( x=dfSet[i].index, y=dfSet[i]['macdOsc']) 

            setMacd = [macd, macdSignal, oscillator]
            if i%2 == 0: # 짝수번일때 0,2,4
                for macd in setMacd: 
                    fig.add_trace(macd, int(i/2)+1,1)
            else:
                for macd in setMacd: 
                    fig.add_trace(macd, int(i/2)+1,2)

    if signal == 'rsi':
        fig = subplots.make_subplots(rows=int(len(intervalSet)/2), cols=2, 
                                vertical_spacing=0.05,
                                subplot_titles=intervalSet)

        for i in range(len(intervalSet)):
            dfSet[i] = Rsi(dfSet[i])
            dfSet[i].dropna(inplace=True)

            rsi = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['rsi'], marker=dict(color='black')) 
            line30 = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['line30'], marker=dict(color='blue')) 
            line70 = pltygo.Scatter( x=dfSet[i].index, y=dfSet[i]['line70'], marker=dict(color='red')) 

            setRsi = [rsi, line30, line70]
            if i%2 == 0: # 짝수번일때 0,2,4
                for rsi in setRsi: 
                    fig.add_trace(rsi, int(i/2)+1,1)
            else:
                for rsi in setRsi: 
                    fig.add_trace(rsi, int(i/2)+1,2)

    fig.update_xaxes(rangeslider_thickness = 0)     # 스크롤바 두께
    fig.update_layout(title_text=name+ " " + signal +" chart")
    if signal == 'ha' or signal == 'ohlc':
        fig.update_annotations(yshift=-20,xshift=300)
    else:
        fig.update_annotations(yshift=-20,xshift=-160)    # 서브차트 제목 위치
    fig.update_layout(showlegend=False)             # 범례 안보이게
    fig.write_image("fig3.png")
        
# 시그널 메이커
def signal_maker(df):
    buyCnt = 0
    sellCnt= 0
    txt = []
    # 1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟
    ### macdㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
   
    # 매수	
    if df['macd'].iloc[-1] > df['macdSignal'].iloc[-1] :  # macd > sign
        if df['macd'].iloc[-2] < df['macdSignal'].iloc[-2] : # 1봉전 macd < sign
            txt.append("\n❤️3. 〰️MACD > signal : 골든크로스🔀")
            buyCnt += 3
        elif df['macd'].iloc[-2] < df['macd'].iloc[-1]:   # 1봉전 macd < 0봉전 macd
            txt.append("\n❤️1. 〰️MACD > signal : 정배열↗️")
            buyCnt += 1
        elif  df['macd'].iloc[-2] > df['macd'].iloc[-1]:
            txt.append("\n⚠️0. 〰️MACD > signal : 정배열 조정↗️↘️")
        
    # 매도
    elif df['macd'].iloc[-1] < df['macdSignal'].iloc[-1]:
        if df['macd'].iloc[-2] > df['macdSignal'].iloc[-2]:
            txt.append("\n💙3. 〰️MACD < signal : 데드크로스🔀")
            sellCnt -= 3
        elif df['macd'].iloc[-2] > df['macd'].iloc[-1]:
            txt.append("\n💙1. 〰️MACD < signal : 역배열↘️")
            sellCnt -= 1
        elif df['macd'].iloc[-2] < df['macd'].iloc[-1]:
            txt.append("\n⚠️0. 〰️MACD < signal : 역배열 반등↘️↗️ ")
    
    # ## macd oscㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['macdOsc'].iloc[-2] < df['macdOsc'].iloc[-1] : # 1봉전 < 0봉전
        if df['macdOsc'].iloc[-3] > df['macdOsc'].iloc[-2] : # 2봉전 > 1봉전
            txt.append("❤️3. 〰️MACD OSC : 반등↘️↗️ ")
            buyCnt += 3
        elif df['macdOsc'].iloc[-1] > 0 and df['macdOsc'].iloc[-2] < 0 : 
            txt.append("❤️3. 〰️MACD OSC : ↗️0️⃣↗️ 돌파")
            buyCnt += 3
        else :
            txt.append("❤️1. 〰️MACD OSC : 상승↗️")
            buyCnt += 1

    elif df['macdOsc'].iloc[-2] > df['macdOsc'].iloc[-1] :
        if df['macdOsc'].iloc[-3] < df['macdOsc'].iloc[-2] :
            txt.append("💙3. 〰️MACD OSC : 조정↗️↘️")
            sellCnt -= 3
        elif df['macdOsc'].iloc[-2] < 0 and df['macdOsc'].iloc[-1] > 0 :
            txt.append("💙3. 〰️MACD OSC : ↘️0️⃣↘️ 돌파")
            sellCnt -= 3
        else:
            txt.append("💙1. 〰️MACD OSC : 하락↘️")
            sellCnt -= 1

    # ## rsiㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

    if df['rsi'].iloc[-2] < 31 and df['rsi'].iloc[-2] < df['rsi'].iloc[-1]:
        txt.append("❤️3. 〰️RSI : ↘️30선↗️ 반등")
        buyCnt += 3
    elif df['rsi'].iloc[-2] > 69 and df['rsi'].iloc[-2] > df['rsi'].iloc[-1]:
        txt.append("💙3. 〰️RSI : ↗️70선↘️ 조정")
        sellCnt -= 3
    elif df['rsi'].iloc[-1] < 31 :
        txt.append("❤️2. 〰️RSI : 30⬇️")
        buyCnt += 2
    elif df['rsi'].iloc[-1] > 69 :
        txt.append("💙2. 〰️RSI : 70⬆️")
        sellCnt -= 2
    else:
        txt.append("⚠️0. 〰️30 < RSI < 70")

    # ## Heiken ashiㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['Open'].iloc[-1] < df['Close'].iloc[-1]:
        if df['Open'].iloc[-2] > df['Close'].iloc[-2]:
            txt.append("❤️3. 〰️HA : 양봉전환↘️↗️ ")
            buyCnt += 3
        else:
            txt.append("❤️1. 〰️HA : 양봉↗️  ")
            buyCnt += 1
    elif df['Open'].iloc[-1] > df['Close'].iloc[-1]:
        if df['Open'].iloc[-2] < df['Close'].iloc[-2]:
            txt.append("💙3.  〰️HA : 음봉전환↗️↘️ ")
            sellCnt -= 3
        else:
            txt.append("💙1. 〰️HA : 음봉↘️")
            sellCnt -= 1

    # ## 볼린저밴드ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['close'].iloc[-2] < df['bolLower'].iloc[-2] and df['open'].iloc[-1] < df['close'].iloc[-1]:
        txt.append("❤️3. 〰️BB : ↘️하한↗️ 반등")
        buyCnt += 3
    elif df['close'].iloc[-2] > df['bolUpper'].iloc[-2] and df['open'].iloc[-1] > df['close'].iloc[-1]:
        txt.append("💙3. 〰️BB : ↗️상한↘️ 조정")
        sellCnt -= 3
    elif df['close'].iloc[-1] < df['bolLower'].iloc[-1] :
        txt.append("❤️2. 〰️BB하한 ⬇️")
        buyCnt += 2
    elif df['close'].iloc[-1] > df['bolUpper'].iloc[-1] :
        txt.append("💙2. 〰️BB상한 ⬆️")
        sellCnt -= 2
    elif df['20ma'].iloc[-1] < df['close'].iloc[-1] < df['bolUpper'].iloc[-1]:
        txt.append("❤️1. 〰️BB상한 > 종가 > 20ma : ↗️구간")
        buyCnt += 1
    elif df['bolLower'].iloc[-1] < df['close'].iloc[-1] < df['20ma'].iloc[-1]:
        txt.append("💙1. 〰️BB하한 < 종가 < 20ma : ↘️구간")
        sellCnt -= 1

    # ## 이동평균선 8ema, 20maㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['ema'].iloc[-1] > df['20ma'].iloc[-1] :
        if df['ema'].iloc[-2] < df['20ma'].iloc[-2]:
            txt.append("❤️3. 〰️20ma < 8ema : 골든크로스🔀")
            buyCnt += 3
        elif df['ema'].iloc[-2] < df['ema'].iloc[-1] and df['20ma'].iloc[-2] < df['20ma'].iloc[-1]:
            txt.append("❤️1. 〰️20ma < 8ema : 정배열 ↗️")
            buyCnt += 1
        else :
            txt.append("⚠️0. 〰️20ma < 8ema : 정배열 조정↗️↘️")
    elif df['ema'].iloc[-1] < df['20ma'].iloc[-1] :
        if df['ema'].iloc[-2] > df['20ma'].iloc[-2]:
            txt.append("💙3. 〰️20ma > 8ema : 데드크로스🔀")
            sellCnt -=3
        elif df['ema'].iloc[-2] > df['ema'].iloc[-1] and df['20ma'].iloc[-2] > df['20ma'].iloc[-1]:
            txt.append("💙1. 〰️20ma > 8ema : 역배열↘️")
            sellCnt -= 1
        else :
            txt.append("⚠️0. 〰️20ma > 8ema : 역배열 반등↘️↗️")
    
    ## 일목기준표
    if df['close'].iloc[-2] > df['kijun'].iloc[-2] and df['close'].iloc[-1] < df['kijun'].iloc[-1]:
        txt.append("💙3. 〰️일목 : 기준선 하향돌파⬇️")
        sellCnt -= 3
    elif df['close'].iloc[-2] < df['kijun'].iloc[-2] and df['close'].iloc[-1] > df['kijun'].iloc[-1]:
        txt.append("❤️3. 〰️일목 : 기준선 상향돌파⬆️")
        buyCnt += 3 
    elif df['senkouSpanB'].iloc[-1] > df['close'].iloc[-1] : # 선행스팬 아래
        if df['kijun'].iloc[-1] < df['tenkan'].iloc[-1] : # 기준 < 전환
            txt.append("💙2. 〰️일목 : 선행B⬇️ 저항구간")
            sellCnt -= 2
        elif df['kijun'].iloc[-1] > df['tenkan'].iloc[-1] : # 기준 > 전환
            txt.append("💙1. 〰️ 일목 : 선행B⬇️ 하락구간↘️")
            sellCnt -= 1
    elif df['senkouSpanB'].iloc[-1] < df['close'].iloc[-1] : # 선행스팬 위
        if df['kijun'].iloc[-1] < df['tenkan'].iloc[-1] : # 기준 < 전환
            txt.append("❤️1. 〰️일목 : 선행B⬆️ 상승구간↗️")
            buyCnt += 1
        elif df['kijun'].iloc[-1] > df['tenkan'].iloc[-1] : # 기준 > 전환
            txt.append("❤️2. 〰️일목 : 선행B⬆️ 지지구간")
            buyCnt += 2

    txt.append(buyCnt + sellCnt)
    return txt

# 시그널 메이커 시간 비교
async def signal_maker_time():
    coin = "BTC/USDT"
    count = 100
    intervalSet = ['1m','5m', '15m', '30m', '1h', '4h', '1d']
    plus = 0
    minus = 0
    plusIntervalSet = []
    minusIntervalSet = []
    close = 0

    rsiSet = {}
    bbSet ={}

    telbot.send_chat_action(chat_id=channel_id_binance, action=telegram.ChatAction.TYPING)
    for interval in intervalSet:    
        df = ichimoku(Heiken_ashi(Ema(Rsi(BolingerBand(Macd(fetch_ohlcvs(coin, interval, count)))))))
        txt = signal_maker(df)

        if txt[-1] > 5: #매수 시그널
            plus += 1
            temp = ""
            for t in txt:
                if str(type(t)) == "<class 'int'>":
                    if t > 0 :  temp = temp + "\n❤️ " + str(t) + ". 〰️매수 우위"
                    elif t < 0 : temp = temp + "\n💙 " + str(-t) + ". 〰️매도 우위"
                    else : temp = temp + "\n⚠️ " + str(t) + ". 〰️중립" 
                else: temp = temp + t + "\n"
            temp = "💲💲 binance "+ coin +" " + interval +" 💲💲\n"+ temp
            plusIntervalSet.append(temp)
        elif txt[-1] <-5: #매도 시그널
            minus += 1
            temp = ""
            for t in txt:
                if str(type(t)) == "<class 'int'>":
                    if t > 0 : temp = temp + "\n❤️ " + str(t) + ". 〰️매수 우위"
                    elif t < 0 : temp = temp + "\n💙 " + str(-t) + ". 〰️매도 우위"
                    else : temp = temp + "\n⚠️ " + str(t) + ". 〰️중립" 
                else: temp = temp + t + "\n"
            temp = "💲💲 binance "+ coin +" " + interval +" 💲💲\n"+ temp
            minusIntervalSet.append(temp)
        
        # rsi
        if df['rsi'].iloc[-1] < 31:
            rsiSet[interval] =df['rsi'].iloc[-1]
        elif df['rsi'].iloc[-1] > 69:
            rsiSet[interval] =df['rsi'].iloc[-1]
        
        # BB
        close = df['close'].iloc[-1]
        if df['bolUpper'].iloc[-1] < df['high'].iloc[-1] :
            if df['bolUpper'].iloc[-1] < df['close'].iloc[-1] :
                bbSet[interval] =df['bolUpper'].iloc[-1]
            else:
                bbSet[interval] =df['bolUpper'].iloc[-1]
        elif df['bolLower'].iloc[-1] > df['low'].iloc[-1] :
            if df['bolLower'].iloc[-1] > df['close'].iloc[-1] :
                bbSet[interval] =df['bolLower'].iloc[-1]
            else:
                bbSet[interval] =df['bolLower'].iloc[-1]
    
    if plus >= 4 : # 매수시그널이 더 많을때
        for txt in plusIntervalSet:
            telbot.sendMessage(text=txt, chat_id=channel_id_binance)
    elif minus >= 4 : # 매도시그널이 더 많을때
        for txt in minusIntervalSet:
            telbot.sendMessage(text=txt, chat_id=channel_id_binance)
    
    if len(rsiSet) >=5:  # rsi <31 해당하는게 5개 이상있으면
        txtr="❗️❗️ RSI ❗️❗️\n"
        for key in rsiSet:
            txtr = txtr + (key + " : " + str(round(rsiSet[key],2)) + "\n")
        telbot.sendMessage(text=txtr, chat_id=channel_id_binance)
    
    if len(bbSet) >=5:  # BB 초과, 미만 5개 이상있으면
        txtbb ="❗️❗️ BB ❗️❗️ / close : " + str(format(round(close,2),',')) +"\n"
        for key in bbSet:
            txtbb = txtbb + (key + " : " + str(format(round(bbSet[key],2),',')) + "\n")
        telbot.sendMessage(text=txtbb, chat_id=channel_id_binance)
    
    
    ############## 5분마다 실행할 코드들 ############################

    
    naver_news.send_new_links(telbot2, group_id_naver_news)

# 5분에 한번씩 실행
# schedule.every().hour.at("04:45").do(lambda:asyncio.run(signal_maker_time()))
# schedule.every().hour.at("09:45").do(lambda:asyncio.run(signal_maker_time()))
# schedule.every().hour.at("14:45").do(lambda:asyncio.run(signal_maker_time()))



def heiken_ashi_coin(country, coin='BTC/USDT', interval='1d', count=60):
    if country == "binance":
        df = fetch_ohlcvs(coin, interval, count)
    elif country == "upbit":
        df = pyupbit.get_ohlcv(coin, interval, count)
    df_HA = df

    df_HA["Open"] = df["open"]       # 캔들 시가
    df_HA["Close"] = df["close"]     # 캔들 종가

    # HA 종가 = (현재캔들)(시가+종가+저가+고가)/4
    df_HA["close"] = (df["open"]+df["high"]+df["low"]+df["close"])/4 
    for i in range(df_HA.shape[0]):  
        if i > 0: 
            # HA 시가 = (이전 HA 시가+ 이전 HA 종가)/2
            df_HA.loc[df_HA.index[i],"open"] = (df_HA["open"][i-1] + df_HA["close"][i-1])/2   
            # HA 고가 = 최대(캔들고가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"high"] = max(df["high"][i],df_HA["open"][i],df_HA["close"][i])
            # HA 저가 = 최소(캔들저가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"low"] = min(df["low"][i],df_HA["open"][i],df_HA["close"][i]) 
    # 20일 이동평균
    df_HA["ma"] = df["Close"].rolling(window=20).mean()
    # 8일 지수이동평균
    df_HA["ema"] = df["Close"].ewm(span=8, adjust=False).mean()

    period26_high = df["high"].rolling(window=26).max()
    period26_low = df["low"].rolling(window=26).min()
    df_HA['kijun'] = (period26_high + period26_low) / 2    #기준선

    # df_HA = df_HA.fillna(0) # NA 값을 0으로
    return df_HA       

def heiken_ashi_jusik(token, region, count):
    today = dt.date.today()
    delta = dt.timedelta(days=count)    # count 봉 전부터
    past = today-delta
    if region == "krx":
        df = fdr.DataReader(codefind(token, "krx"), past, today)
    if region == "us":
        df = fdr.DataReader(token, past, today)
    
    df_HA = df
    df_HA["open"] = df["Open"]
    df_HA["close"] = df["Close"]
    df_HA["low"] = df["Low"]
    df_HA["high"] = df["High"]
    df_HA["Ropen"] = df["Open"]       # 캔들 시가
    df_HA["Rclose"] = df["Close"]     # 캔들 종가

    # HA 종가 = (현재캔들)(시가+종가+저가+고가)/4
    df_HA["close"] = (df["Open"]+df["High"]+df["Low"]+df["Close"])/4 
    for i in range(df_HA.shape[0]):  
        if i > 0: 
            # HA 시가 = (이전 HA 시가+ 이전 HA 종가)/2
            df_HA.loc[df_HA.index[i],"open"] = (df_HA["open"][i-1] + df_HA["close"][i-1])/2   
            # HA 고가 = 최대(캔들고가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"high"] = max(df["High"][i],df_HA["open"][i],df_HA["close"][i])
            # HA 저가 = 최소(캔들저가, HA시가, HA종가)
            df_HA.loc[df_HA.index[i],"low"] = min(df["Low"][i],df_HA["open"][i],df_HA["close"][i]) 
    # 20일 이동평균
    df_HA["ma"] = df["Close"].rolling(window=20).mean()
    # 8일 지수이동평균
    df_HA["ema"] = df["Close"].ewm(span=8, adjust=False).mean()

    period26_high = df["High"].rolling(window=26).max()
    period26_low = df["Low"].rolling(window=26).min()
    df_HA['kijun'] = (period26_high + period26_low) / 2    #기준선

    # df_HA = df_HA.fillna(0) # NA 값을 0으로
    return df_HA       

# rsi반등신호, MACD저점반등신호, HA전환신호, 5일고점돌파신호, 기준선 돌파신호
def signal_maker2(df):
    buyCnt = 0
    txt = []
    # 1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟
    
    # ## Heiken ashiㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['Open'].iloc[-1] < df['Close'].iloc[-1]:  # 오늘 양봉
        if df['Open'].iloc[-2] > df['Close'].iloc[-2]: # 어제 음봉
            txt.append("❤️. 〰️HA : 양봉전환↘️↗️ ")
            buyCnt += 1    

    # ## macd oscㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['macdOsc'].iloc[-2] < 0 and df['macdOsc'].iloc[-2] < df['macdOsc'].iloc[-1] : # 0 이하, 1봉전 < 0봉전
        if df['macdOsc'].iloc[-3] > df['macdOsc'].iloc[-2] : # 2봉전 > 1봉전
            txt.append("❤️. 〰️MACD OSC : 저점반등↘️↗️ ")
            buyCnt += 1
    elif df['macdOsc'].iloc[-2] < df['macdOsc'].iloc[-1] and df['macdOsc'].iloc[-3] > df['macdOsc'].iloc[-2] : # 아무대나 반등하는 곳
        txt.append("🟡. 〰️MACD OSC : 그냥반등↘️↗️ ")
        buyCnt += 0

    # 5일 최고점 돌파ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['high'].iloc[-1] > df['high'].iloc[-2] and df['high'].iloc[-1] > df['high'].iloc[-3] and df['high'].iloc[-1] > df['high'].iloc[-4] and df['high'].iloc[-1] > df['high'].iloc[-5] and df['high'].iloc[-1] > df['high'].iloc[-6]:
        if df['close'].iloc[-1] > df['open'].iloc[-1]: # 5일 최고점, 양봉일때
            txt.append("❤️. 〰️5일 최고점 돌파")
            buyCnt += 1

    ## 일목기준표
    if df['close'].iloc[-2] < df['kijun'].iloc[-2] and df['close'].iloc[-1] > df['kijun'].iloc[-1]:
        txt.append("❤️. 〰️일목 : 기준선 상향돌파⬆️")
        buyCnt += 1 

    # ## rsiㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    if df['rsi'].iloc[-2] < 31 and df['rsi'].iloc[-2] < df['rsi'].iloc[-1]:
        txt.append("❤️. 〰️RSI : ↘️30이하↗️ 반등")
        buyCnt += 1
    elif df['rsi'].iloc[-1] < 31 :
        txt.append("❤️. 〰️RSI : 30이하⬇️")
        buyCnt += 1
    
    txt.append(buyCnt)
    return txt

async def buy_signal(token, interval, df_HA, channel_id=None):
    telbot.send_chat_action(chat_id=channel_id, action=telegram.ChatAction.TYPING)
    # ha음봉(ha_open > ha_close) -> ha양봉(ha_open < ha_close)  # 양전
    if df_HA["open"].iloc[-2] > df_HA["close"].iloc[-2] and df_HA["open"].iloc[-1] < df_HA["close"].iloc[-1] :
        # 8ema < 20ma   # 하락추세중 추세반전
        if df_HA["ema"].iloc[-1] < df_HA["ma"].iloc[-1]:
            # 8ema < ha_close  :  100% 매수
            if df_HA["ema"].iloc[-1] < df_HA["close"].iloc[-1]:
                plot_candle_chart(df_HA, token)
                if namefind(token) != 0:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                    caption=namefind(token) + " ("+token+")\n" + interval + " 양봉전환 : 100% 매수\n\
                                            close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
                else :
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                        caption=token + " " + interval + " 양봉전환 : 100% 매수\n\
                                                close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
                return 100
            # 8ema > ha_close  :  50% 매수
            if df_HA["ema"].iloc[-1] > df_HA["close"].iloc[-1]:
                plot_candle_chart(df_HA, token)
                if namefind(token) != 0:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                    caption=namefind(token) + " ("+token+")\n" + interval + " 양봉전환 : 50% 매수\n\
                                            close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
                else :
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                        caption=token + " " + interval + " 양봉전환 : 50% 매수\n\
                                                close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
                return 50
        # 8ema > 20ma   # 상승추세중 불타기 추세반전
        if df_HA["ema"].iloc[-1] > df_HA["ma"].iloc[-1]:
            plot_candle_chart(df_HA, token)
            if namefind(token) != 0:
                telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                caption=namefind(token) + " ("+token+")\n" + interval + " 양봉전환 : 10% 매수\n\
                                        close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
            else :
                telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                    caption=token + " " + interval + " 양봉전환 : 10% 매수\n\
                                            close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
            return 10
    time.sleep(1)
    return 0

async def sell_signal(token, interval, df_HA, channel_id=None):
    telbot.send_chat_action(chat_id=channel_id, action=telegram.ChatAction.TYPING)
    # ha양봉(ha_open < ha_close) -> ha양봉(ha_open < ha_close)  # 양봉연속
    if df_HA["open"].iloc[-2] < df_HA["close"].iloc[-2] and df_HA["open"].iloc[-1] < df_HA["close"].iloc[-1]:
        # ha양봉 and 캔들양봉 : 10% 매도
        if df_HA["Open"].iloc[-1] < df_HA["Close"].iloc[-1]:
            # post_message(tokenCoin, channel, token + " " + interval + " 양봉연속 : 10% 매도")
            return 10
    # ha양봉(ha_open < ha_close) -> ha음봉(ha_open > ha_close)  # 음봉전환 : 전량매도
    if df_HA["open"].iloc[-2] < df_HA["close"].iloc[-2] and df_HA["open"].iloc[-1] > df_HA["close"].iloc[-1]:
        # 아직 상승추세
        if df_HA["ema"].iloc[-1] > df_HA["ma"].iloc[-1] :
            # 작은 낙폭
            if df_HA["close"].iloc[-1] > df_HA["ema"].iloc[-1] :
                plot_candle_chart(df_HA, token)
                if namefind(token) != 0:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                    caption=namefind(token)+" (" + token + ")\n"
                                    + interval + " 음봉전환 : 50% 매도\n\
                                    close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
                else:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                        caption=token + " " + interval + " 음봉전환 : 50% 매도\n\
                                                close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
                return 50
            # 큰 낙폭    
            if df_HA["close"].iloc[-1] < df_HA["ema"].iloc[-1] :
                plot_candle_chart(df_HA, token)
                if namefind(token) != 0:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                    caption=namefind(token)+" (" + token + ")\n"
                                    + interval + " 음봉전환 : 80% 매도\n\
                                    close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
                else:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                    caption=token + " " + interval + " 음봉전환 : 80% 매도\n\
                                            close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
                return 80
            # 떡락
            if df_HA["close"].iloc[-1] < df_HA["ma"].iloc[-1] :
                plot_candle_chart(df_HA, token)
                if namefind(token) != 0:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                    caption=namefind(token)+" (" + token + ")\n"
                                    + interval + " 음봉전환 : 100% 매도\n\
                                    close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
                else:
                    telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                        caption=token + " " + interval + " 음봉전환 : 100% 매도\n\
                                                close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
                return 100
        # 하락추세
        if df_HA["ema"].iloc[-1] < df_HA["ma"].iloc[-1] :
            plot_candle_chart(df_HA, token)
            if namefind(token) != 0:
                telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                caption=namefind(token)+" (" + token + ")\n"
                                + interval + " 음봉전환 : 100% 매도\n\
                                close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
            else:
                telbot.send_photo(chat_id=channel_id, photo=open(image, 'rb'), 
                                    caption=token + " " + interval + " 음봉전환 : 100% 매도\n\
                                            close : " + str(format(round(df_HA["Close"].iloc[-1],2),',')) +\
                                            "\nkijun : " + str(format(round(df_HA["kijun"].iloc[-1],2),','))
                                                )  # 사진보내기
            return 100
    time.sleep(1)
    return 0
    # (1봉전) 8ema > 20ma and (현재) 8ema < 20ma  : 전량매도

####################### jusik ##########################

count = 120
async def krx_ha_check():
    #     jongmok = watchlist.get_querys('korea_watchlist.txt')
    #     for token in jongmok: # krx
    #         print(token)
    #         df_HA = heiken_ashi_jusik(token, "krx", count)
    #         await buy_signal(token, "day", df_HA, channel_id=channel_id_korea)
    #         await sell_signal(token, "day", df_HA, channel_id=channel_id_korea)
        
    # # 매일 정해진 시간에
    # schedule.every().day.at("15:00").do(lambda:asyncio.run(krx_ha_check()))
    # schedule.every().day.at("08:30").do(lambda:asyncio.run(krx_ha_check()))
    # # asyncio.run(krx_ha_check())
    a=1

async def us_ha_check():
    #     jongmok2 = watchlist.get_querys('usa_watchlist.txt')        
    #     for token in jongmok2: #us
    #         print(token)
    #         df_HA = heiken_ashi_jusik(token, "us", count)
    #         await buy_signal(token, "day", df_HA, channel_id=channel_id_korea)
    #         await sell_signal(token, "day", df_HA, channel_id=channel_id_korea)
    # # 매일 정해진 시간에
    # schedule.every().day.at("10:00").do(lambda:asyncio.run(us_ha_check())) 
    # schedule.every().day.at("20:00").do(lambda:asyncio.run(us_ha_check()))
    # # asyncio.run(us_ha_check())
    a=2

async def krx_bs_check():
    jongmok = watchlist.get_querys('korea_watchlist.txt')
    for token in jongmok: # krx
        print(token)

        try:
            df = fetch_jusik(token, "krx", 120)
            df = Macd(df)
            df = BolingerBand(df)
            df = Rsi(df)
            df = Ema(df)
            df = Heiken_ashi(df)
            df = ichimoku(df)
            txt = signal_maker2(df)

            temp = ""
            for t in txt:
                if str(type(t)) == "<class 'int'>":
                    temp = temp + "\n총점 : ❤️ " + str(t)
                else:
                    temp = temp + t + "\n"

            if txt[0] == "❤️. 〰️MACD OSC : 저점반등↘️↗️ " or txt[0] == "❤️. 〰️HA : 양봉전환↘️↗️ ":
                display_all_signal(df, token, "1day")

                percent = ((df['close'].iloc[-1] / df['close'].iloc[-2]) -1) * 100

                telbot.send_photo(chat_id=channel_id_korea, photo=open('fig1.png', 'rb'))
                telbot.send_photo(chat_id=channel_id_korea, photo=open('fig2.png', 'rb'))
                telbot.send_photo(chat_id=channel_id_korea, photo=open('fig3.png', 'rb'), 
                                    caption="💲💲 "+ token + " 1일봉\n" + 
                                            "종가 : " + str(round(df['close'].iloc[-1],0)) + "원 ( " + str(round(percent,2)) + "% )💲💲\n"
                                             + temp)  
                time.sleep(5)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            telbot.sendMessage(chat_id=channel_id_korea, text=(token + "데이터 불러오기 실패"))

# 매일 정해진 시간에
# schedule.every().day.at("15:00").do(lambda:asyncio.run(krx_bs_check()))
# schedule.every().day.at("08:50").do(lambda:asyncio.run(krx_bs_check()))
# asyncio.run(krx_bs_check())

async def us_bs_check():
    jongmok2 = watchlist.get_querys('usa_watchlist.txt')        
    for token in jongmok2: #us
        print(token)
        
        try:
            df = fetch_jusik(token, "us", 120)
            # print(df.head())
            df = Macd(df)
            df = BolingerBand(df)
            df = Rsi(df)
            df = Ema(df)
            df = Heiken_ashi(df)
            df = ichimoku(df)
            txt = signal_maker2(df)

            temp = ""
            for t in txt:
                if str(type(t)) == "<class 'int'>":
                    temp = temp + "\n총점 : ❤️ " + str(t)
                else:
                    temp = temp + t + "\n"

            percent = ((df['close'].iloc[-1] / df['close'].iloc[-2]) -1) * 100

            if token == 'BRK.B':
                token == 'BRK/B'

            if txt[0] == "❤️. 〰️MACD OSC : 저점반등↘️↗️ " or txt[0] == "🟡. 〰️MACD OSC : 그냥반등↘️↗️":
                sc.get_stockchart(token,"DETAIL")
                telbot.send_photo(chat_id=channel_id_korea, photo=open('sc.png', 'rb'), 
                                    caption="💲💲 "+ token + " 1일봉\n" + 
                                            "종가 : " + str(round(df['close'].iloc[-1],2)) + "$ ( " + str(round(percent,2)) + "% ) 💲💲\n" 
                                            +temp)
            elif txt[0] == "❤️. 〰️HA : 양봉전환↘️↗️ " :
                display_all_signal(df, token, "1day")
                sc.get_stockchart(token,"HA")
                telbot.send_photo(chat_id=channel_id_korea, photo=open('sc.png', 'rb'))
                # display_all_signal(df, token, "1day")
                # telbot.send_photo(chat_id=channel_id_korea, photo=open('fig1.png', 'rb'))
                telbot.send_photo(chat_id=channel_id_korea, photo=open('fig2.png', 'rb'), 
                                            caption="💲💲 "+ token + " 1일봉\n" + 
                                                    "종가 : " + str(round(df['close'].iloc[-1],2)) + "$ ( " + str(round(percent,2)) + "% ) 💲💲\n"
                                                    +temp)
                # telbot.send_photo(chat_id=channel_id_korea, photo=open('fig3.png', 'rb'), caption="💲💲 "+ token + " 1일봉 💲💲\n" +temp)  
        except Exception as e:
            print(e)
            telbot.sendMessage(chat_id=channel_id_korea, text=(token + "데이터 불러오기 실패"))

# 매일 정해진 시간에
# schedule.every().day.at("17:00").do(lambda:asyncio.run(us_bs_check())) 
# asyncio.run(us_bs_check())

 
########### upbit ####################
coin = "KRW-BTC"
coin2 = "KRW-ETH"

# 30분봉
async def coin_ha_check_30min():
    interval_30 = "minute30"
    #비트
    df_HA_h = heiken_ashi_coin("upbit",coin, interval_30, count)
    await buy_signal(coin, interval_30, df_HA_h, channel_id=channel_id_30min_coin)
    await sell_signal(coin, interval_30, df_HA_h, channel_id=channel_id_30min_coin)
    #이더
    df_HA_h2 = heiken_ashi_coin("upbit",coin2, interval_30, count)
    await buy_signal(coin2, interval_30, df_HA_h2, channel_id=channel_id_30min_coin)
    await sell_signal(coin2, interval_30, df_HA_h2, channel_id=channel_id_30min_coin)

# 30분봉에 한번씩 실행
# schedule.every().hour.at(":28").do(lambda:asyncio.run(coin_ha_check_30min()))
# schedule.every().hour.at(":58").do(lambda:asyncio.run(coin_ha_check_30min()))

# 60분봉
async def coin_ha_check_60min():
    interval_60 = "minute60"
    #비트
    df_HA_h = heiken_ashi_coin("upbit",coin, interval_60, count)
    await buy_signal(coin, interval_60, df_HA_h, channel_id=channel_id_1h_coin)
    await sell_signal(coin, interval_60, df_HA_h, channel_id=channel_id_1h_coin)
    #이더
    df_HA_h2 = heiken_ashi_coin("upbit",coin2, interval_60, count)
    await buy_signal(coin2, interval_60, df_HA_h2, channel_id=channel_id_1h_coin)
    await sell_signal(coin2, interval_60, df_HA_h2, channel_id=channel_id_1h_coin)

# 60분에 한번씩 실행
# schedule.every().hour.at(":59").do(lambda:asyncio.run(coin_ha_check_60min()))

# 4시간봉
async def coin_ha_check_240min():
    interval_240 = "minute240"
    #비트
    df_HA_h = heiken_ashi_coin("upbit",coin, interval_240, count)
    await buy_signal(coin, interval_240, df_HA_h, channel_id=channel_id_day_coin)
    await sell_signal(coin, interval_240, df_HA_h, channel_id=channel_id_day_coin)
    #이더
    df_HA_h2 = heiken_ashi_coin("upbit",coin2, interval_240, count)
    await buy_signal(coin2, interval_240, df_HA_h2, channel_id=channel_id_day_coin)
    await sell_signal(coin2, interval_240, df_HA_h2, channel_id=channel_id_day_coin)
# 4시간에 한번씩 실행
# schedule.every().day.at("23:57").do(lambda:asyncio.run(coin_ha_check_240min()))
# schedule.every().day.at("03:57").do(lambda:asyncio.run(coin_ha_check_240min()))
# schedule.every().day.at("07:57").do(lambda:asyncio.run(coin_ha_check_240min()))
# schedule.every().day.at("11:57").do(lambda:asyncio.run(coin_ha_check_240min()))
# schedule.every().day.at("15:57").do(lambda:asyncio.run(coin_ha_check_240min()))
# schedule.every().day.at("19:57").do(lambda:asyncio.run(coin_ha_check_240min()))

 # 1일봉
async def coin_ha_check_day():
    interval_day = "day"
    #비트
    df_HA_d = heiken_ashi_coin("upbit",coin, interval_day, count)
    await buy_signal(coin, interval_day, df_HA_d, channel_id=channel_id_day_coin)
    await sell_signal(coin, interval_day, df_HA_d, channel_id=channel_id_day_coin)
    #이더
    df_HA_h2 = heiken_ashi_coin("upbit",coin2, interval_day, count)
    await buy_signal(coin2, interval_day, df_HA_h2, channel_id=channel_id_day_coin)
    await sell_signal(coin2, interval_day, df_HA_h2, channel_id=channel_id_day_coin)
    # 날씨 알림!!
    telbot.sendMessage(text=naver_weather.rainday("순천"), chat_id=channel_id_feedback)    
# schedule.every().day.at("08:50").do(lambda:asyncio.run(coin_ha_check_day()))

############## binance ####################

btc = 'BTC/USDT'
eth = 'ETH/USDT'

# 30분봉
async def binance_ha_check_30min():
    interval_30 = "30m"
    #비트
    df_HA_h = heiken_ashi_coin("binance",btc, interval_30, count)
    await buy_signal(btc, interval_30, df_HA_h, channel_id=channel_id_30min_coin)
    await sell_signal(btc, interval_30, df_HA_h, channel_id=channel_id_30min_coin)
    #이더
    df_HA_h2 = heiken_ashi_coin("binance",eth, interval_30, count)
    await buy_signal(eth, interval_30, df_HA_h2, channel_id=channel_id_30min_coin)
    await sell_signal(eth, interval_30, df_HA_h2, channel_id=channel_id_30min_coin)

# 30분봉에 한번씩 실행
# schedule.every().hour.at(":28").do(lambda:asyncio.run(binance_ha_check_30min()))
# schedule.every().hour.at(":58").do(lambda:asyncio.run(binance_ha_check_30min()))

# 60분봉
async def binance_ha_check_60min():
    interval_60 = "1h"
    #비트
    df_HA_h = heiken_ashi_coin("binance",btc, interval_60, count)
    await buy_signal(btc, interval_60, df_HA_h, channel_id=channel_id_1h_coin)
    await sell_signal(btc, interval_60, df_HA_h, channel_id=channel_id_1h_coin)
    #이더
    df_HA_h2 = heiken_ashi_coin("binance",eth, interval_60, count)
    await buy_signal(eth, interval_60, df_HA_h2, channel_id=channel_id_1h_coin)
    await sell_signal(eth, interval_60, df_HA_h2, channel_id=channel_id_1h_coin)
# 60분에 한번씩 실행
# schedule.every().hour.at(":57").do(lambda:asyncio.run(binance_ha_check_60min()))

# 4시간봉
async def binance_ha_check_240min():
    interval_240 = "4h"
    #비트
    df_HA_h = heiken_ashi_coin("binance",btc, interval_240, count)
    await buy_signal(btc, interval_240, df_HA_h, channel_id=channel_id_day_coin)
    await sell_signal(btc, interval_240, df_HA_h, channel_id=channel_id_day_coin)
    #이더
    df_HA_h2 = heiken_ashi_coin("binance",eth, interval_240, count)
    await buy_signal(eth, interval_240, df_HA_h2, channel_id=channel_id_day_coin)
    await sell_signal(eth, interval_240, df_HA_h2, channel_id=channel_id_day_coin)
# 4시간에 한번씩 실행
# schedule.every().day.at("23:55").do(lambda:asyncio.run(binance_ha_check_240min()))
# schedule.every().day.at("03:55").do(lambda:asyncio.run(binance_ha_check_240min()))
# schedule.every().day.at("07:55").do(lambda:asyncio.run(binance_ha_check_240min()))
# schedule.every().day.at("11:55").do(lambda:asyncio.run(binance_ha_check_240min()))
# schedule.every().day.at("15:55").do(lambda:asyncio.run(binance_ha_check_240min()))
# schedule.every().day.at("19:55").do(lambda:asyncio.run(binance_ha_check_240min()))

# 1일봉
async def binance_ha_check_day():
    interval_day = "1d"
    #비트
    df_HA_d = heiken_ashi_coin("binance",btc, interval_day, count)
    await buy_signal(btc, interval_day, df_HA_d, channel_id=channel_id_day_coin)
    await sell_signal(btc, interval_day, df_HA_d, channel_id=channel_id_day_coin)
    #이더
    df_HA_h2 = heiken_ashi_coin("binance",eth, interval_day, count)
    await buy_signal(eth, interval_day, df_HA_h2, channel_id=channel_id_day_coin)
    await sell_signal(eth, interval_day, df_HA_h2, channel_id=channel_id_day_coin)
# schedule.every().day.at("23:55").do(lambda:asyncio.run(binance_ha_check_day()))

################## 앤톡새글알리미 #################################
import antok_alarmi
# schedule.every(2).minutes.do(lambda:asyncio.run(antok_alarmi.send_new()))


async def get_avdbs_rank_week():
    get_avdbs_rank('avdbs week',group_id_trash)

async def get_avdbs_rank_month():
    get_avdbs_rank('avdbs month',group_id_trash)

async def get_hitomi_today_rank():
    telbot.send_message(chat_id=group_id_trash, text="hitomi today rank...",reply_markup=ReplyKeyboardRemove())
    get_hitomi_rank(group_id_hitomi, "today")
    telbot.send_message(chat_id=group_id_trash, text="hitomi today rank complete",reply_markup=ReplyKeyboardRemove())
    



schedule.every().day.at("15:00").do(lambda:asyncio.run(krx_bs_check()))
schedule.every().day.at("15:15").do(lambda:asyncio.run(us_bs_check())) 


schedule.every().day.at("21:30").do(lambda:asyncio.run(get_avdbs_rank_month()))
schedule.every().day.at("21:45").do(lambda:asyncio.run(get_avdbs_rank_week()))
schedule.every().day.at("22:00").do(lambda:asyncio.run(get_all()))
# schedule.every().day.at("23:00").do(lambda:asyncio.run(get_hitomi_today_rank()))


def alarmi():
    print("쓰레딩이이잉")
    telbot.sendMessage(chat_id=group_id_trash, text=("ha봇 실행됨"))
    while True:
        try:
            schedule.run_pending()

        except Exception as e:   # 에러 발생시 예외 발생
            print(e)
            print("\n스레드 에러발생!!\n")
            # telbot.sendMessage(chat_id=channel_id_feedback, text=(e)) # 메세지 보내기
            # telbot.sendMessage(chat_id=channel_id_feedback, text=("스레드 에러발생!")) # 메세지 보내기

try :
    # 스레드로 while문 따로 돌림
    t = Thread(target=alarmi, daemon=True)
    t.start()


    '''haBot'''
    # 메시지 받아오는 곳
    message_handler = MessageHandler(Filters.text & (~Filters.command), get_name)
    updater.dispatcher.add_handler(message_handler)
    # 명령어 받아오는 곳
    message_handler2 = MessageHandler(Filters.command, get_command)
    updater.dispatcher.add_handler(message_handler2)
    # 봇이 보낸 메시지
    # updater.dispatcher.add_handler(CallbackQueryHandler(callback_get))
    # updater.dispatcher.add_handler(MessageHandler(Filters.forwarded_from(username="fc2rsstorrent"), get_fc2rssbot_text))
    # updater.dispatcher.add_handler(MessageHandler(Filters.via_bot(username="alarm_haBot"), get_habot_text))
    
    updater.start_polling(timeout=5)
    updater.idle()
    
except Exception as e:               # 에러 발생시 예외 발생
    print(e)
    # telbot.sendMessage(chat_id=channel_id_feedback, text=(e)) # 메세지 보내기
    # telbot.sendMessage(chat_id=channel_id_feedback, text=("에러 발생!")) # 메세지 보내기







# 해야할 것
'''
stockchart
1. 종목 재무관련 정보 크롤링
https://stockcharts.com/freecharts/symbolsummary.html?sym=aapl
'''

'''
# 이미지 여러장 묶어서 보내기
photo_list = []
for i in range(len(os.walk("./코로나이미지").__next__()[2])): # 이미지 파일 개수만큼 for문 돌리기
    photo_list.append(telegram.InputMediaPhoto(open("./코로나이미지/{}.png".format(i), "rb")))
bot.sendMediaGroup(chat_id=id, media=photo_list)
'''