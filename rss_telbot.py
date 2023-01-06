import re
import time
from threading import Thread
from datetime import datetime

import telegram  # pip install python-telegram-bot --upgrade
from telegram.ext import Updater, MessageHandler, Filters

import filename_set
import av_img_video_url
import watchlist

''' version 23.1.5.18'''

'''
*bold*
_italic_
`inline monospaced text`
'''

#텔레그램 봇
myToken = '5831801489:AAHvEw74bp6zz1mhbNCsAGu9JmtVifG0AWY'
telbot = telegram.Bot(token=myToken)
myBotName = "fc2rss_alarmBot"
updater = Updater(myToken, use_context=True)

my_user_id = '1706601591'
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
    txt = "[.](" +str(thumb1)+ ") `" + str(pumnum.upper().replace("_","\_")) + "` #"+str(pumnum.upper().replace("_","\_").replace("-","\_")) +"\n"\
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
    mgn = "`magnet:?xt=urn:btih:" + str(infoHash) +"`"

    telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    telbot.send_message(text=txt, parse_mode='Markdown', chat_id=chat_id)
    telbot.send_message(text=mgn, chat_id=chat_id, parse_mode='Markdown')
    telbot.delete_message(chat_id=chat_id, message_id=message_id)
    time.sleep(4)

    #키워드 알림
    qs = watchlist.find_keyword_lines(pumnum + " " + txt,'av_list_keyword.txt') 
    if qs != [] :
        for q in qs: telbot.send_message(chat_id= q.split(" ")[0], text="키워드 : " + q.split(" ")[1] + " → " + str(pumnum.upper().replace("_","\_")) +' [Fc2RssTorrent](https://t.me/+Hqirrs4MIUZhOGI1)', parse_mode = 'Markdown')
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
    mgn = "`magnet:?xt=urn:btih:" + str(infoHash) +"`"
    telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    telbot.send_message(text=txt, parse_mode='Markdown', chat_id=chat_id)
    telbot.send_message(text=mgn, chat_id=chat_id, parse_mode='Markdown')
    telbot.delete_message(chat_id=chat_id, message_id=message_id)
    time.sleep(4)

    #키워드 알림
    qs = watchlist.find_keyword_lines(txt,'av_list_keyword.txt') 
    if qs != [] :
        for q in qs: telbot.send_message(chat_id= q.split(" ")[0], text="키워드 : " + q.split(" ")[1] + " → " + str(pumnum.upper().replace("_","\_")) +' [Fc2RssTorrent](https://t.me/+Hqirrs4MIUZhOGI1)', parse_mode = 'Markdown')
        time.sleep(4) # 1분에 20개 이상 보내면 에러뜸
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")
    
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
            print("from : " + msgFrom, end=" -> ")
        else: msgFrom = ""
        msgTo = bot[tp]['chat']['title']
        print("to : " + msgTo)

    chat_id = bot[tp]['chat']['id']
    msg = bot[tp]['text'].split('@')[0].upper()    # / 제외하고, 대문자로 변환
    message_id = bot[tp]['message_id']

    print("get command : " + msg)

    telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

    global COMMAND
    if chat_type == 'private': # 개인챗에 메시지 전송
        helpmsg = "키워드 알림 적용 채널, 그룹\n\
            \[ [신작&순위 채널](https://t.me/+Y7PSYJPViXFiZTY1) ]  \[ [AvRss](https://t.me/+RJU6zonaLrswZWE9) ]  \[ [Fc2Rss](https://t.me/+Hqirrs4MIUZhOGI1) ]\n\
            사용가능한 명령어\n\
            */kadd* \[keyword] : 키워드 등록\n\
            */klist*           : 키워드 리스트\n\
            */kdel* \[keyword]  : 키워드 삭제\n\
            !!! 띄어쓰기 포함 X. 키워드는 단어 단위로 입력해주세요. !!!\n\n\
            */getinfo* \[품번]   : 품번 상세정보\n\
            ex) abc-123, fc2-ppv-123456  \n\n\
            */feedback* \[내용] : 문의사항, 건의사항\n\
            */help* 도움말\n\
            \[ [에딥톡방](https://t.me/+zdk5g1B2caE4Mzk1) ]\n\
            "
        if msg.find("/KADD") != -1 :
            try:
                kadd = bot[tp]['text'].split(" ")[1]
                print("kadd : " + kadd)
                chk = watchlist.add_keyword(str(user_id), kadd, 'av_list_keyword.txt')
                if chk == 1: telbot.send_message(chat_id = user_id, text = kadd + " 키워드 추가 완료")
                else : telbot.send_message(chat_id = user_id, text = kadd + " 키워드 추가 실패 또는 목록에 이미 있음")
            except Exception as e:
                print(e)
                telbot.send_message(chat_id = user_id, text = "알림을 등록할 키워드를 입력하세요\nex) /kadd [키워드]")
            return
        elif msg == "/KLIST":
            klist = watchlist.get_querys(user_id, 'av_list_keyword.txt')
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
                telbot.send_message(chat_id = user_id, text = "삭제할 키워드를 입력하세요\nex) /kdel [키워드] ")
            return

        elif msg.find("/GETINFO") != -1:
            if bot[tp]['text'] == "/getinfo" : telbot.send_message(chat_id = user_id, text = "품번을 입력해주세요\n ex) /getinfo abc-123 또는 /getinfo fc2-ppv-123456 ")
            else:
                getinfo = bot[tp]['text'].replace("/getinfo ","")
                print("getinfo : " + getinfo)
                try:
                    get_pumInfo(getinfo, str(user_id))
                except Exception as e:
                    print(e)
                    telbot.send_message(chat_id=user_id, txt=getinfo + " 조회 실패")

        elif msg.find("/FEEDBACK") != -1:
            txtfile = "habot_feedback.txt"
            feedback = bot[tp]['text'].replace('/feedback ',"")
            print('feedback : ' + feedback)
            try:
                if feedback == "/feedback" :
                    telbot.send_message(chat_id = user_id, text = "내용을 입력해주세요")
                else:
                    with open(txtfile, 'a', encoding = 'UTF-8') as f:          
                        f.write(str(user_id) + " " +feedback + "\n")
                    telbot.send_message(chat_id = my_user_id, text = str(user_id) + " : " +feedback)
                    time.sleep(4)
                telbot.send_message(chat_id = user_id, text = "피드백 감사합니다.^-^\n"+feedback)
            except Exception as e:
                print(e)
                telbot.send_message(chat_id = user_id, text = "피드백을 전송하는데 실패했어요 ㅠㅅㅠ\n내용 : "+feedback)

        elif msg == "/HELP":
            telbot.send_message(chat_id = user_id, text = helpmsg,parse_mode='Markdown' )
            return
        else :
            telbot.send_message(chat_id = user_id, text = helpmsg,parse_mode='Markdown' )    
            return                                 

        try : telbot.delete_message(chat_id= user_id, message_id=message_id)
        except Exception: pass

def get_pumInfo(pumnum, chat_id):
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

    telbot.send_message(chat_id=chat_id, 
                        text="[.]("+str(thumb)+") `" + pumnum.upper().replace("_","\_") +  "` #" +pumnum.upper().replace("_","\_").replace(" ","\_").replace("-","\_") + "\n\n" +
                        "\[ [javdb](https://javdb.com/search?q="+pumnum+"&f=all) ]  "+
                        "\[ [avdbs](https://www.avdbs.com/menu/search.php?kwd="+pumnum.replace("fc2ppv ","")+"&seq=214407610&tab=2) ]  "+
                        "\[ [evojav](https://evojav.pro/en/?s="+pumnum+") ]  "+
                        "\[ [missav](https://missav.com/ko/search/"+missavPumnum+") ]  "+
                        "\[ [trailer]("+str(trailer)+") ]  "+
                        "\[ [dbmsin]("+ dburl +") ]\n\n"+
                        writer+" "+actor+" "+highlight+createDate+highlight+"\n"+ title
                        ,parse_mode='Markdown' )
    time.sleep(4)


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

    message_handler = MessageHandler(Filters.command, get_command)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling(timeout=5)
    updater.idle()
    
except Exception as e:               # 에러 발생시 예외 발생
    print(e)