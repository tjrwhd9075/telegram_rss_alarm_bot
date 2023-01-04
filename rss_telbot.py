import re
import time
from threading import Thread

import telegram  # pip install python-telegram-bot --upgrade
from telegram import chat
from telegram.ext import Updater, MessageHandler, Filters

import filename_set
import av_img_video_url

''' version 23.1.3.20'''

#텔레그램 봇
myToken = '5831801489:AAHvEw74bp6zz1mhbNCsAGu9JmtVifG0AWY'
telbot = telegram.Bot(token=myToken)
myBotName = "fc2rss_alarmBot"
updater = Updater(myToken, use_context=True)

group_id_trash = '-1001547828770'

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
    
    try:
        if titleList[0] == "カリビアンコム": pumnum = "carib-"+pumnum
        elif titleList[0] == "heyzo" and titleList[1] == "hd" : pumnum = titleList[0] + "-" + titleList[2]
        elif titleList[2] == "Heyzo" and titleList[3] == " " and titleList[4] == " " : pumnum = titleList[2] + "-" + titleList[5] #  Heyzo   2946  [uncen] [2022] エッチ大好きなさとみちゃん～もまれすぎてオッパイが大きくなってきちゃいました～ - 石川さと 1080p
        elif titleList[0].find("-carib-1080p") != -1: pumnum = "carib-"+titleList[0].split("-")[0]+"_"+titleList[0].split("-")[1] # 010423-001-carib-1080p-進撃の青山 ～欲求不満で止まらない～青山はな
        elif titleList[1].find("-1pon-1080p") != -1: pumnum = "1pon-"+titleList[0]+"_"+titleList[1].split("-")[0] # 010423 001-1pon-1080p-高級ソープへようこそ 安室なみ
        elif titleList[1].find("-1PON") != -1: pumnum = "1pon-"+titleList[0]+"_"+titleList[1].split("-")[0]
        elif titleList[1].find("-10mu-1080p") != -1: pumnum = "10mu-"+titleList[0]+"_"+titleList[1].split("-")[0] # 010423 01-10mu-1080p-秘蔵マンコセレクション
        elif titleList[1].find("-paco-1080p") != -1: pumnum = "paco-"+titleList[0]+"_"+titleList[1].split("-")[0] # 010423 771-paco-1080p-人妻マンコ図鑑 149
        elif titleList[0].find("H4610-") !=-1 and titleList[0].find("HD-") != -1: pumnum = titleList[0].split("-")[0] + "-" + titleList[0].split("-")[1] #H4610-gol211-FHD-綺麗な肌全身で感じまくって
    except : pass

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

    thumb = av_img_video_url.makeImageURL(pumnum)
    if isinstance(thumb, list) :
        thumb1 = thumb[0]
        thumb2 = thumb[1]
    else: thumb1 = thumb

    trailer = av_img_video_url.makeVideoURL(pumnum)

    title, writer, actor, createDate = filename_set.get_pumInfo_dbmsin_static(pumnum)

    txt = "[.](" +str(thumb1)+ ") " + str(pumnum.replace("_","\_")) + " #"+str(pumnum.replace("-","\_")) +"\n"\
        + "\[[javdb]("+f"https://javdb.com/search?q={pumnum}&f=all)]   \[[미리보기]("+str(trailer)+")]   \[[evojav]("+f"https://evojav.pro/en/?s={pumnum})]   \[[avdbs]("+f"https://www.avdbs.com/menu/search.php?kwd={pumnum}&seq=214407610&tab=2)]   \[[dbmsin]("+f"https://db.msin.jp/jp.search/movie?str={pumnum}"+")]   \[[sukebei](" +f"https://sukebei.nyaa.si/view/{sukebeiNum}" +")]   \[[torrent]("+str(torrentLink)+")]\n\n"\
        + str(actor) + " " + str(writer) + " " + str(createDate) + " **" + str(fileSize) + "**\n"\
        + str(translatedTitle)  +"\n"
    mgn = 'magnet:?xt=urn:btih:' + str(infoHash)

    telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    telbot.send_message(text=txt, parse_mode='Markdown', chat_id=chat_id)
    telbot.send_message(text=mgn, chat_id=chat_id)
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
    title, writer, actor, createDate = filename_set.get_pumInfo_dbmsin_static(pumnum)
    
    txt = "[.](" +f"https://db.msin.jp/images/cover/fc2/fc2-ppv-{pumnum}.jpg"+ ") FC2PPV " + str(pumnum) + " #FC2PPV\_"+str(pumnum) +"\n"\
        + " \[[미리보기]("+f"https://db.msin.jp/sampleplay?id=fc2-ppv-{pumnum}"+")]   \[[evojav]("+f"https://evojav.pro/en/?s={pumnum}"+")]   \[[dbmsin]("+f"https://db.msin.jp/search/movie?str={pumnum}"+")]   \[[sukebei](" +f"https://sukebei.nyaa.si/view/{sukebeiNum}" +")]   \[[torrent]("+torrentLink+")]\n\n"\
        + str(actor) + " " + str(writer) + " " + str(createDate) + " **" + str(fileSize) + "**\n"\
        + translatedTitle 
    mgn = 'magnet:?xt=urn:btih:' + str(infoHash)
    telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    telbot.send_message(text=txt, parse_mode='Markdown', chat_id=chat_id)
    telbot.send_message(text=mgn, chat_id=chat_id)
    telbot.delete_message(chat_id=chat_id, message_id=message_id)
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")
    time.sleep(4)
    return

#그냥 채팅 전체 읽음
def get_message(bot, update): 
    if bot.channel_post is not None : tp = "channel_post"   #채널일 경우
    elif bot.message is not None : tp = "message"           #그룹일 경우
    elif bot.edited_channel_post is not None  : return      #봇이 채널에 에딧한 메세지일 경우
    elif bot.edited_message is not None  : return      # 채널 -> 댓글 -> 그룹일 경우?ㅁ
    else : print(bot)

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




def alarmi():
    print("쓰레딩이이잉")
    telbot.sendMessage(chat_id=group_id_trash, text=("rss봇 실행됨"))
    while True:

        pass

try :
    # 스레드로 while문 따로 돌림
    t = Thread(target=alarmi, daemon=True)
    t.start()

    '''rssbot'''
    # 메시지 받아오는 곳
    message_handler = MessageHandler(Filters.text & (~Filters.command), get_message)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling(timeout=5)
    updater.idle()
    
except Exception as e:               # 에러 발생시 예외 발생
    print(e)