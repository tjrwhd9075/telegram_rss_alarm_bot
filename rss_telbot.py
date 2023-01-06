import re
import time
from threading import Thread

import telegram  # pip install python-telegram-bot --upgrade
from telegram import chat
from telegram.ext import Updater, MessageHandler, Filters

import filename_set
import av_img_video_url

''' version 23.1.5.18'''

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

    pumnumTmp = re.sub(r"[^a-zA-Z0-9(\-)(\_)]", "?", title) # 숫자랑 영어, '-' 빼고 전부 제거
    pumnumTmpList = pumnumTmp.split("?")
    pumnum = ""
    for p in pumnumTmpList: 
        if p.find("-") != -1 : pumnum=p; break #품번이 존재하면
    
    try:
        if title.find("カリビアンコム") != -1 and title.find("-CARIB") == -1  : pumnum = "carib-"+pumnum # 010323-001-CARIB カリビアンコム , カリビアンコム 102517-525
        elif title.find("Caribbeancom") != -1 : pumnum = "carib-"+pumnum # [Uncensored] Caribbeancom 010323-001 旅館の生き残りに賭ける美人女将 , (UNCENSORED )Caribbeancom 加勒比 010323-001
        elif title.find("-carib-1080p") != -1 : pumnum = "carib-"+pumnum.split("-")[0]+"-"+pumnum.split("-")[1] ## 010423-001-carib-1080p-進撃の青山 ～欲求不満で止まらない～青山はな
        elif title.find("-CARIB ") != -1 : pumnum = "carib-"+pumnum.split("-")[0]+"-"+pumnum.split("-")[1] #010423-001-CARIB

        elif title.find('HEYZO') != -1 and pumnum=="": # [HD/720p] HEYZO 2951 おしゃぶり上手なギャルのカラダを余すところなくいただきました！ – 羽月まい 
            for i,p in enumerate(pumnumTmpList) : 
                if p == "HEYZO" : pumnum = p + "-" + pumnumTmpList[i+1] ; break
        elif title.find('heyzo') != -1 and title.find('hd') != -1:  # heyzo_hd_2951_full-おしゃぶり上手なギャルのカラダを余すところなくいただきました 
            for i,p in enumerate(pumnumTmpList):
                if p == "heyzo" : pumnum = p + "-" + pumnumTmpList[i+2] ; break
        elif title.find('Heyzo') != -1 :  # [Heyzo] [2946] [uncen] [2022] エッチ大好きなさとみちゃん～もまれすぎてオッパイが大きくなってきちゃいました～
            for i,p in enumerate(pumnumTmpList):
                if p == "Heyzo" : pumnum = p + "-" + pumnumTmpList[i+6] ; break
        
        elif title.find("-1pon-1080p") != -1 or title.find("-1PON") != -1:  # 010423_001-1pon-1080p-高級ソープへようこそ 安室なみ, 010323_001-1PON
            for i, p in enumerate(pumnumTmpList):
                if p.find("1pon") != -1 : pumnum = "1pon-" + pumnumTmpList[i-1] + "_" + p.split("-")[0] ; break
                elif p.find("1PON") != -1 : pumnum = "1pon-" + pumnumTmpList[i-1] + "_" + p.split("-")[0] ; break

        elif title.find("-10mu-1080p") != -1 or title.find("-10MU") != -1:  # 010423_01-10mu-1080p-秘蔵マンコセレクション 〜あおいのおまんこ見てください
            for i, p in enumerate(pumnumTmpList):
                if p.find("10mu") != -1 : pumnum = "10mu-" + pumnumTmpList[i-1] + "_" + p.split("-")[0] ; break
                elif p.find("10MU") != -1 : pumnum = "10mu-" + pumnumTmpList[i-1] + "_" + p.split("-")[0] ; break   # 010323_01-10MU      

        elif title.find("-paco-1080p") != -1 :  # 010423_771-paco-1080p-人妻マンコ図鑑 149
            for i, p in enumerate(pumnumTmpList):
                if p.find("paco") != -1 : pumnum = "paco-" + pumnumTmpList[i-1] + "_" + p.split("-")[0] ; break

        elif title.find("H4610-") !=-1 and title.find("HD-") != -1: pumnum = pumnum.split("-")[0] + "-" + pumnum.split("-")[1] #H4610-gol211-FHD-綺麗な肌全身で感じまくって
        elif title.find("kin8-") !=-1 and title.find("HD-") != -1: pumnum = pumnum.split("-")[0] + "-" + pumnum.split("-")[1] # kin8-3656-FHD-2022

    except : pass

    if pumnum == "" or pumnum == "-" : #품번이 없으면 삭제 후 종료
        telbot.delete_message(chat_id=chat_id, message_id=message_id); 
        print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")
        return
    
    sukebeiNum = msg.split(" | ")[0].split("#")[-1]
    title = msg.split(" | ")[1]
    fileSize = msg.split(" | ")[2]
    infoHash = msg.split(" | ")[4].split("\n")[0]
    torrentLink = msg.split(" | ")[4].split("\n")[-1]
    
    print('sukebeiNum : ' + str(sukebeiNum), end=" | ") ; print('pumnum : ' + str(pumnum))
    print('title : ' + str(title))
    print('fileSize : ' + str(fileSize), end=" | ") ; print('infoHash : ' + str(infoHash))
    print('torrentLink : ' + str(torrentLink))

    translatedTitle = filename_set.replaceTxt(filename_set.translater(title))

    trailer = av_img_video_url.makeVideoURL(pumnum)
    thumb = av_img_video_url.makeImageURL(pumnum)
    if isinstance(thumb, list) :
        thumb1 = thumb[0]
        thumb2 = thumb[1]
    else: thumb1 = thumb

    

    title, writer, actor, createDate = filename_set.get_pumInfo_dbmsin_static(pumnum)

    uncPumnum = filename_set.pumnum_check(pumnum)
    if uncPumnum.find("carib") != -1 or uncPumnum.find("1pon") != -1 or uncPumnum.find("10mu") != -1 or uncPumnum.find("paco") != -1 : 
        dburl=f"https://db.msin.jp/search/movie?str={uncPumnum}"
    else : dburl=f"https://db.msin.jp/jp.search/movie?str={pumnum}"

    missavPumnum = "-".join(pumnum.split("-")[1:])
    txt = "[.](" +str(thumb1)+ ") " + str(pumnum.upper().replace("_","\_")) + " #"+str(pumnum.upper().replace("_","\_").replace("-","\_")) +"\n"\
        + "[ [trailer]("+str(trailer)+") ]  \
        \[ [evojav]("+f"https://evojav.pro/en/?s={pumnum}) ]  \
        \[ [missav]("+f"https://missav.com/ko/search/{missavPumnum}"+") ]  \
        \[ [avdbs]("+f"https://www.avdbs.com/menu/search.php?kwd={pumnum}&seq=214407610&tab=2) ]  \
        \[ [javdb]("+f"https://javdb.com/search?q={pumnum}&f=all) ]  \
        \[ [dbmsin]("+dburl+") ]  \
        \[ [sukebei](" +f"https://sukebei.nyaa.si/view/{sukebeiNum}" +") ]  \
        \[ [torrent]("+str(torrentLink)+") ]\n\n"\
        + str(actor) + " " + str(writer) + " " + str(createDate) + " *" + str(fileSize) + "*\n"\
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
    
    pumAndTitle = msg.split(" | ")[1].upper()
    if pumAndTitle.find("FC2PPV ") != -1 : # FC2PPV 123456
        pumnum = pumAndTitle.split("FC2PPV ")[1].split(" ")[0]
        title = pumAndTitle.split("FC2PPV ")[1].split(" ")[1:]
    elif pumAndTitle.find("FC2PPV-") != -1 : # FC2PPV-123456
        pumnum = pumAndTitle.split("FC2PPV-")[1].split(" ")[0]
        title = pumAndTitle.split("FC2PPV-")[1].split(" ")[1:]
    elif pumAndTitle.find("FC2 PPV ") != -1 : # FC2 PPV 123456
        pumnum = pumAndTitle.split("FC2 PPV ")[1].split(" ")[0]
        title = pumAndTitle.split("FC2 PPV ")[1].split(" ")[1:]
    elif pumAndTitle.find("FC2-PPV-") != -1 : # FC2-PPV-123456
        pumnum = pumAndTitle.split("FC2-PPV-")[1].split(" ")[0]
        title = pumAndTitle.split("FC2-PPV-")[1].split(" ")[1:]
    else: # FC2-PPV-123456
        print(pumAndTitle)
        pumnum = pumAndTitle.split("-")[2].split(" ")[0]
        title = pumAndTitle.split("-")[2].split(" ")[1:]
    title = ''.join(title)
    fileSize = msg.split(" | ")[2]
    infoHash = msg.split(" | ")[4].split("\n")[0]
    torrentLink = msg.split(" | ")[4].split("\n")[-1]
    
    print('sukebeiNum : ' + str(sukebeiNum), end=" | ") ; print('pumnum : ' + str(pumnum))
    print('title : ' + str(title))
    print('fileSize : ' + str(fileSize), end=" | ") ; print('infoHash : ' + str(infoHash))
    print('torrentLink : ' + str(torrentLink))

    translatedTitle = filename_set.replaceTxt(filename_set.translater(title))
    title, writer, actor, createDate = filename_set.get_pumInfo_dbmsin_static("fc2-ppv-"+str(pumnum))
    
    txt = "[.](" +f"https://db.msin.jp/images/cover/fc2/fc2-ppv-{pumnum}.jpg"+ ") FC2PPV " + str(pumnum) + " #FC2PPV\_"+str(pumnum) +"\n"\
        + " \[ [trailer]("+f"https://db.msin.jp/sampleplay?id=fc2-ppv-{pumnum}"+") ]  \
            \[ [evojav]("+f"https://evojav.pro/en/?s={pumnum}"+") ]  \
            \[ [missav]("+f"https://missav.com/ko/FC2-PPV-{pumnum}"+") ]  \
            \[ [dbmsin]("+f"https://db.msin.jp/search/movie?str={pumnum}"+") ]  \
            \[ [sukebei](" +f"https://sukebei.nyaa.si/view/{sukebeiNum}" +") ]  \
            \[ [torrent]("+torrentLink+") ]\n\n"\
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