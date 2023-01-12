import re
import time
from threading import Thread
from datetime import datetime
import schedule
import asyncio

import telegram  # pip install python-telegram-bot --upgrade
from telegram.ext import Updater, MessageHandler, Filters

import filename_set
import av_img_video_url
import watchlist
import avdbs_crawling

''' version 23.1.5.18'''

'''
*bold*
_italic_
`inline monospaced text`
'''

#텔레그램 봇
myToken = '5831801489:AAHvEw74bp6zz1mhbNCsAGu9JmtVifG0AWY'
telbot = telegram.Bot(token=myToken)
myBotName = "fc2rss_alarm_bot"
updater = Updater(myToken, use_context=True)

my_user_id = '1706601591'
group_id_trash = '-1001547828770'
group_id_avdbs = '-1001870842558'

klistTxtFile = 'av_list_keyword_rss.txt'
newsKlistTxtFile = 'news_keywords.txt'

#그냥 채팅 전체 읽음
def get_message(bot, update): 
    if bot.channel_post is not None : tp = "channel_post"   #채널일 경우
    elif bot.message is not None : tp = "message"           #그룹일 경우
    elif bot.edited_channel_post is not None  : return      #봇이 채널에 에딧한 메세지일 경우
    elif bot.edited_message is not None  : return      # 채널 -> 댓글 -> 그룹일 경우?ㅁ
    else : print(bot)

    chat_type = bot[tp]['chat']['type'] 
    msgFrom =""
    # print("채널타입 : " + chat_type)
    if chat_type == 'private' or chat_type == 'channel': # 개인채팅, 채널일 경우
        user_id = bot[tp]['chat']['id']
        print("유저id : " + str(user_id))
    elif  chat_type == 'supergroup':
        # print(bot[tp])
        if bot[tp]['sender_chat'] is not None:
            msgFrom = bot[tp]['sender_chat']['title']
            msgFromId = bot[tp]['sender_chat']['id']

            print("from : " + msgFrom + " " + str(msgFromId), end=" -> ")
        else: msgFrom = ""
        msgTo = bot[tp]['chat']['title']
        msgToId = bot[tp]['chat']['id']
        print("to : " + msgTo + " " + str(msgToId))

    if msgFrom == 'AvRssTorrent' : get_avrssbot_text(bot[tp], update); return 
    if msgFrom == 'Fc2RssTorrent': get_fc2rssbot_text(bot[tp], update); return

    news_group = ['🦔한국뉴스_그룹', '🦔해외뉴스_그룹', '🦔코인뉴스_그룹', '🦔사회경제 이슈_그룹']
    if msgTo in news_group  :  resend_with_hashtag(bot[tp],update); return 

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
        if bot[tp]['sender_chat'] is not None:
            msgFrom = bot[tp]['sender_chat']['title']
            msgFromId = bot[tp]['sender_chat']['id']
            print("from : " + msgFrom + " " + str(msgFromId), end=" -> ")
        else: msgFrom = ""
        msgTo = bot[tp]['chat']['title']
        msgToId = bot[tp]['chat']['id']
        print("to : " + msgTo + " " + str(msgToId))

    chat_id = bot[tp]['chat']['id']
    msg = bot[tp]['text'].split('@')[0]    # / 제외하고, 대문자로 변환
    message_id = bot[tp]['message_id']

    print("get command : " + msg)

    global COMMAND
    if chat_type == 'private': # 개인챗에 메시지 전송
        telbot.send_chat_action(chat_id=user_id, action=telegram.ChatAction.TYPING)
        helpmsg = "키워드 알림 적용 채널, 그룹\n\
            \[ [AvRss](https://t.me/+4F1MKUjlKKQ2NWE1) ]  \[ [Fc2Rss](https://t.me/+x-HRQ8PpKI9iZTZl) ]\n\
            사용가능한 명령어\n\
            */kadd* \[keyword] : 키워드 등록\n\
            */klist*           : 키워드 리스트\n\
            */kdel* \[keyword]  : 키워드 삭제\n\
            !!! 띄어쓰기 포함 X. 키워드는 단어 단위로 입력해주세요. !!!\n\n\
            */getinfo* \[품번]   : 품번 상세정보\n\
            ex) abc-123, fc2-ppv-123456  \n\n\
            */feedback* \[내용] : 문의사항, 건의사항\n\
            */help* 도움말\n\
            \[ [에딥톡방](https://t.me/+A1HoasQqHMEzY2U1) ]\n\
            "
        if msg.upper().find("/KADD") != -1 :
            try:
                kadd = bot[tp]['text'].split(" ")[1]
                print("kadd : " + kadd)
                chk = watchlist.add_keyword(str(user_id), kadd, klistTxtFile)
                if chk == 1: telbot.send_message(chat_id = user_id, text = kadd + " 키워드 추가 완료")
                else : telbot.send_message(chat_id = user_id, text = kadd + " 키워드 추가 실패 또는 목록에 이미 있음")
            except Exception as e:
                print(e)
                telbot.send_message(chat_id = user_id, text = "알림을 등록할 키워드를 입력하세요\nex) /kadd [키워드]")
            return
        elif msg.upper() == "/KLIST":
            klist = watchlist.get_querys('av_list_keyword_rss.txt', user_id=user_id)
            txt =""
            for key in klist: txt += key.split(" ")[1] +", "
            telbot.send_message(chat_id = user_id, text = "키워드 리스트\n" + txt)
            return
        elif msg.upper().find("/KDEL") != -1:
            try:
                if bot[tp]['text'].upper() == "/KDEL": telbot.send_message(chat_id = user_id, text = "삭제할 키워드를 입력하세요\nex) /kdel [키워드] ")
                else: 
                    kdel = bot[tp]['text'].split(" ")[1]
                    print("kdel : " + kdel)
                    chk = watchlist.del_keyword(str(user_id), kdel, klistTxtFile)
                    if chk == 1: telbot.send_message(chat_id = user_id , text = kdel + " 키워드 삭제 완료")
                    else : telbot.send_message(chat_id = user_id , text = kdel + " 키워드 삭제 실패 또는 목록에 없음")
            except Exception as e:
                print(e)
                telbot.send_message(chat_id = user_id, text = "삭제할 키워드를 입력하세요\nex) /kdel [키워드] ")
            return
        elif msg.upper() in ["/KBACKUP","/NEWSKBACKUP"]:
            if msg.upper() == "/KBACKUP": txtFile = klistTxtFile
            elif msg.upper() == "/NEWSKBACKUP": txtFile = newsKlistTxtFile

            klist = watchlist.get_querys(txtFile)
            txt = ""
            for k in klist: 
                txtTmp = txt + k +"\n"
                if len(txtTmp) > 1000: telbot.send_message(chat_id = my_user_id, text = txt) ; txt = "" ; time.sleep(4) #1천자 넘으면 일단 전송
                else: txt+=k +"\n"; txtTmp=""
            telbot.send_message(chat_id = my_user_id, text = txt) ; time.sleep(4)#나머지 전송

        elif msg.upper().find("/GETINFO") != -1:
            if bot[tp]['text'].upper() == "/GETINFO" : telbot.send_message(chat_id = user_id, text = "품번을 입력해주세요\n ex) /getinfo abc-123 또는 /getinfo fc2-ppv-123456 ")
            else:
                getinfo = " ".join(bot[tp]['text'].split(" ")[1:])
                print("getinfo : " + getinfo)
                try:
                    get_pumInfo(getinfo, str(user_id))
                except Exception as e:
                    print(e)
                    telbot.send_message(chat_id=user_id, txt=getinfo + " 조회 실패")

        elif msg.upper().find("/FEEDBACK") != -1:
            txtfile = "habot_feedback.txt"
            
            try:
                if bot[tp]['text'].upper() == "/FEEDBACK" :
                    telbot.send_message(chat_id = user_id, text = "내용을 입력해주세요")
                else:
                    feedback = " ".join(bot[tp]['text'].split(" ")[1:])
                    print('feedback : ' + feedback)
                    with open(txtfile, 'a', encoding = 'UTF-8') as f:          
                        f.write(str(user_id) + " " +feedback + "\n")
                    telbot.send_message(chat_id = user_id, text = "피드백 감사합니다.^-^")
                    time.sleep(4)
                    telbot.send_message(chat_id = my_user_id, text = str(user_id) + " : " +feedback)
                    
                    
            except Exception as e:
                print(e)
                telbot.send_message(chat_id = user_id, text = "피드백을 전송하는데 실패했어요 ㅠㅅㅠ\n내용 : "+feedback)

        elif msg.upper() == "/HELP":
            telbot.send_message(chat_id = user_id, text = helpmsg,parse_mode='Markdown' , disable_web_page_preview=True)
            return
        else :
            telbot.send_message(chat_id = user_id, text = helpmsg,parse_mode='Markdown' , disable_web_page_preview=True)    
            return                                 

        try : telbot.delete_message(chat_id= user_id, message_id=message_id)
        except Exception: pass

    elif bot[tp]['text'].find('@') == 0 :
        return 
    elif bot[tp]['text'].split('@')[1].split(' ')[0] != myBotName :
        print(bot[tp]['text'].split('@')[1].split(' ')[0] + " : 날 부른게 아닌거 같아요")
        return
    elif chat_type =='supergroup':
        telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        if bot[tp]['text'].upper() == ("/GETINFO@"+myBotName.upper()) : 
            telbot.send_message(chat_id = chat_id,reply_to_message_id=message_id, text = "품번을 입력해주세요\n ex) /getinfo abc-123 또는 /getinfo fc2-ppv-123456 ")
        else: 
            pumnum = " ".join(bot[tp]['text'].split(" ")[1:]) 
            try:
                get_pumInfo(pumnum, chat_id=str(chat_id), message_id=message_id)
            except Exception as e:
                    print(e)
                    telbot.send_message(chat_id=chat_id, reply_to_message_id=message_id, txt=pumnum + " 조회 실패")

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
        elif title.find("加勒比") != -1 : pumnum = "carib-"+pumnum.split("-")[0]+"-"+pumnum.split("-")[1] #加勒比

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
        elif title.find("Kin8tengoku") !=-1 : 
            for i, t in enumerate(title.split(" ")):
                if t=="Kin8tengoku": pumnum = "kin8-"+title.split(" ")[i+2] #[HD/720p] Kin8tengoku 金8天国 3659 小柄ボディー可愛いナタちゃんのお
            
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
    highlight=""
    if createDate != "-":
        diffDate = datetime.now() - datetime.strptime(createDate, "%Y-%m-%d") # 날짜차이 계산
        if diffDate.days <= 7 : highlight="`"

    uncPumnum = filename_set.pumnum_check(pumnum)
    if uncPumnum.find("carib") != -1 or uncPumnum.find("1pon") != -1 or uncPumnum.find("10mu") != -1 or uncPumnum.find("paco") != -1 : 
        dburl=f"https://db.msin.jp/search/movie?str={uncPumnum}"
    else : dburl=f"https://db.msin.jp/jp.search/movie?str={pumnum}"

    missavPumnum = "-".join(pumnum.split("-")[1:])
    txt = "[.](" +str(thumb1)+ ") `" + str(pumnum.upper()) + "` #"+str(pumnum.upper().replace("_","\_").replace("-","\_")) +"\n"\
        + "\[ [trailer]("+str(trailer)+") ]  "+\
        "\[ [evojav]("+f"https://evojav.pro/en/?s={pumnum}) ]  "+\
        "\[ [missav]("+f"https://missav.com/ko/search/{missavPumnum}"+") ]  "+\
        "\[ [avdbs]("+f"https://www.avdbs.com/menu/search.php?kwd={pumnum}&seq=214407610&tab=2) ]  "+\
        "\[ [javdb]("+f"https://javdb.com/search?q={pumnum}&f=all) ]  "+\
        "\[ [dbmsin]("+dburl+") ]  "+\
        "\[ [sukebei](" +f"https://sukebei.nyaa.si/view/{sukebeiNum}" +") ]  "+\
        "\[ [torrent]("+str(torrentLink)+") ]\n\n"\
        + str(actor) + " " + str(writer) + " " +highlight+ str(createDate) +highlight+ " *" + str(fileSize) + "*\n"\
        + str(translatedTitle)  +"\n"
    mgn = "🧲`magnet:?xt=urn:btih:" + str(infoHash) +"`"

    #키워드 알림
    qs = watchlist.find_keyword_lines(pumnum + " " + txt, klistTxtFile) 

    banedKey = [bk for bk in qs if "!" in bk] # 금지 키워드 목록
    if banedKey != [] : #하나라도 존재하면 그냥 종료
        telbot.delete_message(chat_id=chat_id, message_id=message_id)
        print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n"); 
        return 

    telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    telbot.send_message(text=txt, parse_mode='Markdown', chat_id=chat_id)
    telbot.send_message(text=mgn, chat_id=chat_id, parse_mode='Markdown')
    telbot.delete_message(chat_id=chat_id, message_id=message_id)
    time.sleep(4)

    if qs != [] :
        for q in qs: 
            telbot.send_message(chat_id= q.split(" ")[0], text="⏰ 키워드 : `" + q.split(" ")[1] + "` → `" + str(pumnum.upper().replace("_","\_")) +'` #'+str(pumnum.upper().replace(" ","\_").replace("-","\_"))+'\n\[ [AvRssTorrent](https://t.me/+4F1MKUjlKKQ2NWE1) ]  \[ [신작&순위](https://t.me/+NhDP-cnW7KA3NGM1) ]', parse_mode = 'Markdown', disable_web_page_preview=True)
            time.sleep(4) # 1분에 20개 이상 보내면 에러뜸

    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")
    
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
    else: 
        print(pumAndTitle)
        return
        
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
    highlight=""
    if createDate != "-":
        diffDate = datetime.now() - datetime.strptime(createDate, "%Y-%m-%d") # 날짜차이 계산
        if diffDate.days <= 7 : highlight="`"
    
    txt = "[.](" +f"https://db.msin.jp/images/cover/fc2/fc2-ppv-{pumnum}.jpg"+ ") `FC2PPV " + str(pumnum) + "` #FC2PPV\_"+str(pumnum) +"\n"\
        + "\[ [trailer]("+f"https://db.msin.jp/sampleplay?id=fc2-ppv-{pumnum}"+") ]  "+\
        "\[ [evojav]("+f"https://evojav.pro/en/?s={pumnum}"+") ]  "+\
        "\[ [missav]("+f"https://missav.com/ko/FC2-PPV-{pumnum}"+") ]  "+\
        "\[ [dbmsin]("+f"https://db.msin.jp/search/movie?str={pumnum}"+") ]  "+\
        "\[ [sukebei](" +f"https://sukebei.nyaa.si/view/{sukebeiNum}" +") ]  "+\
        "\[ [torrent]("+torrentLink+") ]\n\n"\
        + str(actor) + " " + str(writer) + " " +highlight+ str(createDate) +highlight+ " **" + str(fileSize) + "**\n"\
        + translatedTitle 
    mgn = "🧲`magnet:?xt=urn:btih:" + str(infoHash) +"`"

    #키워드 알림
    qs = watchlist.find_keyword_lines(txt,klistTxtFile) 

    banedKey = [bk for bk in qs if "!" in bk] # 금지 키워드 목록
    if banedKey != [] : #하나라도 존재하면 그냥 종료
        telbot.delete_message(chat_id=chat_id, message_id=message_id)
        print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n"); 
        return 

    telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    telbot.send_message(text=txt, parse_mode='Markdown', chat_id=chat_id)
    telbot.send_message(text=mgn, chat_id=chat_id, parse_mode='Markdown')
    telbot.delete_message(chat_id=chat_id, message_id=message_id)
    time.sleep(4)
    
    if qs != [] :
        for q in qs: 
            telbot.send_message(chat_id= q.split(" ")[0], text="⏰ 키워드 : `" + q.split(" ")[1] + "` → `" + str(pumnum) + "` #FC2PPV\_" + str(pumnum)+" \n\[ [Fc2RssTorrent](https://t.me/+x-HRQ8PpKI9iZTZl) ]  \[ [신작&순위](https://t.me/+NhDP-cnW7KA3NGM1) ]", parse_mode = 'Markdown', disable_web_page_preview=True)
            time.sleep(4) # 1분에 20개 이상 보내면 에러뜸
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")
    
    return

def get_pumInfo(pumnum, chat_id, message_id=None):
    '''
    pumnum : qwer-1234 또는 fc2ppv 123456, fc2-ppv-123456
    '''
    

    telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

    pumnum = filename_set.pumnum_check(pumnum) #fc2-ppv-12345
    title, writer, actor, createDate = filename_set.get_pumInfo_dbmsin_static(pumnum)
    highlight=""
    if createDate != "-":
        diffDate = datetime.now() - datetime.strptime(createDate, "%Y-%m-%d") # 날짜차이 계산
        if diffDate.days <= 7 : highlight="`"
    if title != "-": 
        title = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥]"," ", title) #특수문자 제거
        title = filename_set.replaceTxt(filename_set.translater(title)) #수정
    title = title.replace("_","\\_")
    thumb = av_img_video_url.makeImageURL(pumnum)
    if isinstance(thumb, list): thumb = thumb[1]
    trailer = av_img_video_url.makeVideoURL(pumnum)
    
    if pumnum.find("fc2") != -1 or pumnum.find("carib") != -1 or pumnum.find("1pon") != -1 or pumnum.find("10mu") != -1 or pumnum.find("paco") != -1 : 
        dburl=f"https://db.msin.jp/search/movie?str={pumnum}"
    else : dburl=f"https://db.msin.jp/jp.search/movie?str={pumnum}"
    missavPumnum = "-".join(pumnum.replace("fc2ppv ","fc2-ppv-").split("-")[1:])
    if pumnum.lower().find("fc2") != -1: pumnum = "fc2ppv "+pumnum.replace(" ","-").split("-")[-1]

    telbot.send_message(chat_id=chat_id, reply_to_message_id=message_id,
                        text="[.]("+str(thumb)+") `" + pumnum.upper() +  "` #" +pumnum.upper().replace("_","\_").replace(" ","\_").replace("-","\_") + "\n\n" +
                        "\[ [javdb](https://javdb.com/search?q="+pumnum+"&f=all) ]  "+
                        "\[ [avdbs](https://www.avdbs.com/menu/search.php?kwd="+pumnum.replace("fc2ppv ","")+"&seq=214407610&tab=2) ]  "+
                        "\[ [evojav](https://evojav.pro/en/?s="+pumnum+") ]  "+
                        "\[ [missav](https://missav.com/ko/search/"+missavPumnum+") ]  "+
                        "\[ [trailer]("+str(trailer)+") ]  "+
                        "\[ [dbmsin]("+ dburl +") ]\n\n"+
                        writer+" "+actor+" "+highlight+createDate+highlight+"\n"+ title
                        ,parse_mode='Markdown' )
    time.sleep(4)

from news_tagger import Keywords
def resend_with_hashtag(bot, update):
    chat_id = bot['chat']['id']
    msg = bot['text'].upper()
    message_id = bot['message_id']

    print(bot)


    # tagKewords = Keywords()
    # txt = tagKewords.tag_keywords(msg)
    # telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    # telbot.send_message(chat_id=chat_id, text=txt)
    # telbot.delete_message(chat_id=chat_id, message_id=message_id)
    # time.sleep(4)




async def int2imoji(num : int):

    res = ""

    if num == 0: res = "0️⃣"
    elif num == 1: res = "1️⃣"
    elif num == 2: res = "2️⃣"
    elif num == 3: res = "3️⃣"
    elif num == 4: res = "4️⃣"
    elif num == 5: res = "5️⃣"
    elif num == 6: res = "6️⃣"
    elif num == 7: res = "7️⃣"
    elif num == 8: res = "8️⃣"
    elif num == 9: res = "9️⃣"

    return res

async def ForTeleReplaceTxt(txt : str):
    txt = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥(\s)(\[)(\])]", "", txt)
    return txt.replace("[","|").replace("]","| ")

from avdbs_crawling import oldList
avdbsBoardUrl = "https://www.avdbs.com/board/"
async def get_avdbs_crawling(chat_id):
    print("ㅡㅡㅡㅡㅡㅡㅡㅡget_avdbs_crawlingㅡㅡㅡㅡㅡㅡㅡㅡ")
    newContents = await avdbs_crawling.get_avdbs_whole_board_asyn()
    if newContents == [] : print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ"); return #할거 없으면 그냥 종료

    #content : [num,thumb,boardType,adult,date,beforeTime,writer,lvl,view,recom,good,title,contentTxt]
    #           0   1     2         3     4    5          6      7   8    9     10   11    12
    for content in newContents[::-1]:
        try:
            thumb, adult, view, recom, good = "-","-","-","-","-"
            if content[1] is not None : thumb = content[1]
            if content[3] is not None : adult = "🔞"
            if content[8] is not None : view = content[8]
            if content[9] is not None : recom = content[9]
            if content[10] is not None : good = content[10]

            boardUrl = avdbsBoardUrl + content[0]

            writer = await ForTeleReplaceTxt(content[6])
            title = await ForTeleReplaceTxt(content[11])
            contentTxt = await ForTeleReplaceTxt(content[12])

            lvl10 = await int2imoji(int(int(content[7]) / 10))
            lvl1 = await int2imoji(int(content[7]) % 10)

            txt= "[.]("+thumb+")   📣  *AVDBS New 게시글 알림*  📣\n\n"+\
                "📂게시판 : ["+ content[2] + "]("+boardUrl+") | "  + adult+"\n"+\
                "🕓 : "+content[4] + " | " + content[5] + "\n"+\
                "🖋 : " + writer + " | LV : " + lvl10 + lvl1 + "\n\n"+\
                "👀 : " + view + " | 💬 : " + recom + " | 👍 : " + good + "\n"+\
                "📍제목 : ["+ title +"]("+boardUrl+")" + "\n\n"+\
                contentTxt

            #키워드 알림
            try:
                qs = await watchlist.find_keyword_lines_asyn(txt, klistTxtFile) 
            except Exception as e:
                print("get_avdbs_crawling - find keword error : ", end="")
                print(e)

            banedKey = [bk for bk in qs if "!" in bk] # 금지 키워드 목록
            if banedKey != [] : #하나라도 존재하면 
                oldList.append(content[0]) # 목록에 그냥 넣어버리고 패스
                continue 

            telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            telbot.send_message(chat_id=chat_id, text=txt, parse_mode='Markdown')
            oldList.append(content[0]) #전송 성공하면 목록에 저장
            time.sleep(4)
        except Exception as e:
            print("get_avdbs_crawling - content send fail : ", end="")
            print(e)
        
        try:
            if qs != [] :
                for q in qs: 
                    print("chat_id : " + str(q.split(" ")[0]), end=" | ")
                    print("키워드 : " + q.split(" ")[1])
                    telbot.send_message(chat_id= q.split(" ")[0], text="⏰ 키워드 : `" + q.split(" ")[1] + "` → \[ [에딥톡방](https://t.me/c/1870842558/1) ]", parse_mode = 'Markdown', disable_web_page_preview=True)
                    time.sleep(4) # 1분에 20개 이상 보내면 에러뜸
        except Exception as e:
            print("get_avdbs_crawling - keword send error : ", end="")
            print(e)
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")

async def backup_klist(chat_id:str, txtFile:str):
    klist = watchlist.get_querys(txtFile)
    txt = ""
    for k in klist: 
        txtTmp = txt + k +","
        if len(txtTmp) > 1000: telbot.send_message(chat_id = chat_id, text = txt) ; txt = "" ; time.sleep(4) #1천자 넘으면 일단 전송
        else: txt+=k +","; txtTmp=""
    telbot.send_message(chat_id = chat_id, text = txt)
    await asyncio.sleep(4)#나머지 전송

def alarmi():
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print("스케쥴 에러 : ", end="")
            print(e)
            
schedule.every(10).minutes.do(lambda:asyncio.run(get_avdbs_crawling(group_id_avdbs))) 
schedule.every().day.at("00:00").do(lambda:asyncio.run(backup_klist(group_id_trash, newsKlistTxtFile))) 

#일단 한번 에딥 크롤링 시작
try:  asyncio.run(get_avdbs_crawling(group_id_avdbs))
except Exception as e:
    print("get_avdbs_crawling error : ", end="")
    print(e)

print("쓰레딩이이잉")
telbot.sendMessage(chat_id=group_id_trash, text=("rss봇 실행됨"))

try :
    # 스레드로 while문 따로 돌림
    t = Thread(target=alarmi, daemon=True)
    t.start()    
except Exception as e:  
    print("스레드 생성 실패 : " , end="")             
    print(e)

try:
    '''rssbot'''
    # 메시지 받아오는 곳
    message_handler = MessageHandler(Filters.text & (~Filters.command), get_message)
    updater.dispatcher.add_handler(message_handler)

    message_handler = MessageHandler(Filters.command, get_command)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling(timeout=5)
    updater.idle()
    
except Exception as e:               # 에러 발생시 예외 발생
    print("텔레그램 봇 에러 : ", end="")
    print(e)