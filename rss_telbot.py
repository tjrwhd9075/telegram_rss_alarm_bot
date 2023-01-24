import os
import re
import time
from threading import Thread
from datetime import datetime
import schedule
import asyncio
import aiofile
import urllib.request

import telegram  # pip install python-telegram-bot --upgrade
from telegram.ext import Updater, MessageHandler, Filters

import filename_set
import av_img_video_url
import watchlist
import avdbs_crawling

''' version 23.1.5.18'''

from pytz import timezone
#한국 시간대로 설정
KST = timezone('Asia/Seoul')
current_time = datetime.now()
kst_time = current_time.astimezone(KST)
diff_hour = kst_time.hour - current_time.hour
diff_min = kst_time.minute - current_time.minute
print(current_time)
print(kst_time)


#텔레그램 봇
myToken = '5831801489:AAHvEw74bp6zz1mhbNCsAGu9JmtVifG0AWY'
telbot = telegram.Bot(token=myToken)
myBotName = "fc2rss_alarm_bot"
updater = Updater(myToken, use_context=True)

my_user_id = '1706601591'
group_id_trash = '-1001547828770'
group_id_avdbs = '-1001870842558'
group_id_memo = '-1001651190351'

channel_fc2rss = "-1001831133794"
channel_avrss = "-1001851191415"
channel_id_av = '-1001635569220'

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
    msgFrom =""; msgTo=""
    # print("채널타입 : " + chat_type)
    if chat_type == 'private' or chat_type == 'channel': # 개인채팅, 채널일 경우
        user_id = bot[tp]['chat']['id']
        msgTo = bot[tp]['chat']['title']
        print(f"{msgTo} - 유저id : {user_id}")
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

    # news_group = ['🦔한국뉴스_그룹', '🦔해외뉴스_그룹', '🦔코인뉴스_그룹', '🦔사회경제 이슈_그룹']
    # if msgTo in news_group  :  resend_with_hashtag(bot[tp],update); return 

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
        elif msg.upper() == "/AVDBSRANKBACKUP":
            csvfiles = ['avdbs_list.txt','av_list_avdbs_all.csv','av_list_avdbs_month.csv','av_list_avdbs_year.csv','av_list_avdbs_week.csv']
            for csvfile in csvfiles:
                doc = open(csvfile , 'rb')
                telbot.send_document(chat_id=chat_id, document=doc, filename=csvfile, timeout=1000)
                doc.close()
                time.sleep(4)
            print("avdbs rank 백업 완료")
            telbot.send_message(chat_id=chat_id, text="avdbs rank 백업 완료")
        elif msg.upper().find("/AVDBS") != -1: 
            if bot[tp]['text'].upper() == "/AVDBS": telbot.send_message(chat_id = user_id, text = "기간을 입력하세요.(week, month, year, all)")
            else: 
                period = bot[tp]['text'].split(" ")[1].lower()
                if period in ['week','month','year','all']:
                    get_avdbs_rank("avdbs "+period, group_id_trash)
                    asyncio.run(backup_avdbs(group_id_trash, f'av_list_avdbs_{period}.csv'))
                else: telbot.send_message(chat_id = user_id, text = "잘못된 입력입니다..(week, month, year, all)")

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

    msg = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥(\s)(\n)(\t)(\r)(#)(.)(\-)(_)(|)(:)(/)]", " ", msg)
    title = msg.split(" | ")[1]

    pumnumTmp = re.sub(r"[^a-zA-Z0-9(\-)(\_)]", "?", title) # 숫자랑 영어, '-' 빼고 전부 제거
    pumnumTmpList = pumnumTmp.split("?")        
    pumnum = ""
    for p in pumnumTmpList: 
        if p.find("-") != -1 : pumnum=p; break #품번이 존재하면
    
    try:
        caribs = ['カリビアンコム', 'Caribbeancom', 'carib', 'CARIB', '加勒比']
        if any(carib in title for carib in caribs):
            fpumnum = re.findall(r'\d+[-_]\d+', title) # [숫자_숫자] 또는 [숫자-숫자] 문자열을 찾아냄 
            pumnum = "carib-"+fpumnum[0]

        # if title.find("カリビアンコム") != -1 and title.find("-CARIB") == -1  : pumnum = "carib-"+pumnum # 010323-001-CARIB カリビアンコム , カリビアンコム 102517-525
        # elif title.find("Caribbeancom") != -1 : 
        #     fpumnum = re.findall(r'\d+[-_]\d+', title) # [숫자_숫자] [숫자-숫자] 문자열을 찾아냄 
        #     pumnum = "carib-"+fpumnum[0] # [Uncensored] Caribbeancom 010323-001 旅館の生き残りに賭ける美人女将 , (UNCENSORED )Caribbeancom 加勒比 010323-001
        # elif title.find("-carib-1080p") != -1 : pumnum = "carib-"+pumnum.split("-")[0]+"-"+pumnum.split("-")[1] ## 010423-001-carib-1080p-進撃の青山 ～欲求不満で止まらない～青山はな
        # elif title.find("-CARIB ") != -1 : pumnum = "carib-"+pumnum.split("-")[0]+"-"+pumnum.split("-")[1] #010423-001-CARIB
        # elif title.find("加勒比") != -1 : pumnum = "carib-"+pumnum.split("-")[0]+"-"+pumnum.split("-")[1] #加勒比

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
        elif title.lower().find("paco") != -1 : # pacopacomama-121022_754 イキナリ亀甲縛り 〜鈴木里奈〜
            fpumnum = re.findall(r'\d+[_]\d+', title) 
            pumnum = "paco-"+fpumnum[0]
                
        elif title.find("H4610-") !=-1 and title.find("HD-") != -1: pumnum = pumnum.split("-")[0] + "-" + pumnum.split("-")[1] #H4610-gol211-FHD-綺麗な肌全身で感じまくって
        # elif title.find("kin8-") !=-1 and title.find("HD-") != -1: pumnum = pumnum.split("-")[0] + "-" + pumnum.split("-")[1] # kin8-3656-FHD-2022
        elif title.lower().find("kin8") !=-1 : 
            match = re.search(r'\b\d{4}\b', title) #4자리 숫자 찾기
            if match: pumnum = "kin8-"+str(match.group())
    except:
        pass

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
    res = filename_set.get_pumInfo_dbmsin_static(pumnum)
    title = res['title']
    writer = res['writer']
    actor = res['actor']
    createDate = res['createDate']
    thumb = res['thumb']
    trailer =''

    if writer =="-" and actor=="-" and createDate=="-" : #fc2 제외한 품번들
        res = filename_set.get_pumInfo_from_javdb_static(pumnum)
        writer = res['writer']
        actor = res['actor']
        createDate = res['date']
        trailer = res['trailer']
        if res['img'] != [] : thumb = res['img'][0]

    if thumb == '' or thumb == '-' or thumb is None:
        thumb = av_img_video_url.makeImageURL(pumnum)
        if isinstance(thumb, list) : thumb1 = thumb[0]
        else: thumb1 = thumb
    else : thumb1 = res['thumb']
    if trailer == '' or trailer is None:
        trailer = av_img_video_url.makeVideoURL(pumnum)

    highlight=""
    if createDate != "-" and createDate != "":
        diffDate = datetime.now() - datetime.strptime(createDate, "%Y-%m-%d") # 날짜차이 계산
        if diffDate.days <= 7 : highlight="`"

    uncPumnum = filename_set.pumnum_check(pumnum)
    if uncPumnum.find("carib") != -1 or uncPumnum.find("1pon") != -1 or uncPumnum.find("10mu") != -1 or uncPumnum.find("paco") != -1 : 
        dburl=f"https://db.msin.jp/search/movie?str={uncPumnum}"
    else : dburl=f"https://db.msin.jp/jp.search/movie?str={pumnum}"

    missavPumnum = pumnum.upper().replace("FC2PPV ","FC2-PPV-").replace("10MU-","").replace("PACO-","").replace("1PON-","").replace("CARIB-","")
    txt = "[.](" +str(thumb1)+ ") `" + str(pumnum.upper()) + "` #"+str(pumnum.upper().replace("_","\_").replace("-","\_")) +"\n"\
        "\[ [javdb]("+f"https://javdb.com/search?q={pumnum}&f=all) ]  "+\
        "\[ [trailer]("+str(trailer)+") ]  "+\
        "\[ [avdbs]("+f"https://www.avdbs.com/menu/search.php?kwd={pumnum}&seq=214407610&tab=2) ]  "+\
        "\[ [evojav]("+f"https://evojav.pro/en/?s={pumnum}) ]  "+\
        "\[ [supjav]("+f"https://supjav.com/?s={pumnum}) ]  "+\
        "\[ [missav]("+f"https://missav.com/ko/search/{missavPumnum}"+") ]  "+\
        "\[ [dbmsin]("+dburl+") ]  "+\
        "\[ [sukebei](" +f"https://sukebei.nyaa.si/view/{sukebeiNum}" +") ]  "+\
        "\[ [bt4g](https://kr.bt4g.org/search/"+str(pumnum)+") ]  "+\
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
    telbot.send_message(text=txt, chat_id=channel_avrss, parse_mode='Markdown')
    telbot.send_message(text=mgn, chat_id=channel_avrss, parse_mode='Markdown')
    telbot.delete_message(chat_id=chat_id, message_id=message_id)
    time.sleep(4)

    qs = list(set(qs) - set(banedKey))
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

    pumnum = re.sub(r"[^0-9]", "", pumnum) #숫자를 제외한 문자는 제거
    
    title = ''.join(title)
    fileSize = msg.split(" | ")[2]
    infoHash = msg.split(" | ")[4].split("\n")[0]
    torrentLink = msg.split(" | ")[4].split("\n")[-1]
    
    print('sukebeiNum : ' + str(sukebeiNum), end=" | ") ; print('pumnum : ' + str(pumnum))
    print('title : ' + str(title))
    print('fileSize : ' + str(fileSize), end=" | ") ; print('infoHash : ' + str(infoHash))
    print('torrentLink : ' + str(torrentLink))

    translatedTitle = filename_set.replaceTxt(filename_set.translater(title))
    res = filename_set.get_pumInfo_dbmsin_static("fc2-ppv-"+str(pumnum))
    title = res['title']
    writer = res['writer']
    actor = res['actor']
    createDate = res['createDate']
    thumb = res['thumb']
    trailer = ''

    if writer =="-" and actor =="-" and createDate =="-" : 
        res = filename_set.get_pumInfo_fc2_from_fc2hub_static(pumnum.split("-")[-1])
        writer = res['writer']
        trailer = res['trailer']
        if res['img'] != []: thumb = res['img'][0]

    highlight=""
    if createDate != "-" and createDate != "":
        diffDate = datetime.now() - datetime.strptime(createDate, "%Y-%m-%d") # 날짜차이 계산
        if diffDate.days <= 7 : highlight="`"
    
    if thumb == '-' or thumb is None:
        thumb = f"https://db.msin.jp/images/cover/fc2/fc2-ppv-{pumnum}.jpg"
    if trailer == '' or trailer is None:
        trailer = f"https://adult.contents.fc2.com/embed/{pumnum}"

    txt = "[.](" +thumb+ ") `FC2PPV " + str(pumnum) + "` #FC2PPV\_"+str(pumnum) +"\n"\
        + "\[ [trailer]("+trailer+") ]  "+\
        "\[ [evojav]("+f"https://evojav.pro/en/?s={pumnum}) ]  "+\
        "\[ [supjav]("+f"https://supjav.com/?s={pumnum}) ]  "+\
        "\[ [missav]("+f"https://missav.com/ko/FC2-PPV-{pumnum}) ]  "+\
        "\[ [avdbs](https://www.avdbs.com/menu/search.php?kwd="+pumnum.replace("fc2ppv ","")+"&seq=214407610&tab=2) ]  "\
        "\[ [dbmsin]("+f"https://db.msin.jp/search/movie?str={pumnum}) ]  "+\
        "\[ [sukebei](" +f"https://sukebei.nyaa.si/view/{sukebeiNum}) ]  "+\
        "\[ [bt4g](https://kr.bt4g.org/search/"+str(pumnum)+") ]  "+\
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
    telbot.send_message(text=txt, chat_id=channel_fc2rss, parse_mode='Markdown')
    telbot.send_message(text=mgn, chat_id=channel_fc2rss, parse_mode='Markdown')
    telbot.delete_message(chat_id=chat_id, message_id=message_id)
    time.sleep(4)
    
    qs = list(set(qs) - set(banedKey))
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
    res = filename_set.get_pumInfo_dbmsin_static(pumnum)
    title = res['title']
    writer = res['writer']
    actor = res['actor']
    createDate = res['createDate']
    thumb = res['thumb']
    trailer=''

    if title != "-": 
        title = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥]"," ", title) #특수문자 제거
        title = filename_set.replaceTxt(filename_set.translater(title)) #수정
    else:
        if writer =="-" and actor=="-" and createDate=="-" and pumnum.lower().find('fc2') == -1: #fc2 제외한 품번들
            res = filename_set.get_pumInfo_from_javdb_static(pumnum)
            title = res['title']
            writer = res['writer']
            actor = res['actor']
            createDate = res['date']
            trailer = res['trailer']
            if res['img'] != []: thumb = res['img'][0]
        elif writer =="-" and actor=="-" and createDate=="-" and pumnum.lower().find('fc2') != -1: #fc2 품번
            res = filename_set.get_pumInfo_fc2_from_fc2hub_static(pumnum.split("-")[-1])
            title = res['title']
            writer = res['writer']
            trailer = res['trailer']
            if res['img'] != []: thumb = res['img'][0]

    highlight=""
    if createDate != "-" or createDate != "":
        diffDate = datetime.now() - datetime.strptime(createDate, "%Y-%m-%d") # 날짜차이 계산
        if diffDate.days <= 7 : highlight="`"
    
    title = title.replace("_","\\_")
    if thumb =='' or thumb =='-' or thumb is None:
        thumb = av_img_video_url.makeImageURL(pumnum)
        if isinstance(thumb, list): thumb = thumb[1]
    if trailer =='' or trailer is None:    
        trailer = av_img_video_url.makeVideoURL(pumnum)
    
    if pumnum.find("fc2") != -1 or pumnum.find("carib") != -1 or pumnum.find("1pon") != -1 or pumnum.find("10mu") != -1 or pumnum.find("paco") != -1 : 
        dburl=f"https://db.msin.jp/search/movie?str={pumnum}"
    else : dburl=f"https://db.msin.jp/jp.search/movie?str={pumnum}"
    missavPumnum = pumnum.replace("fc2ppv ","fc2-ppv-")
    if pumnum.lower().find("fc2") != -1: pumnum = "fc2ppv "+pumnum.replace(" ","-").split("-")[-1]

    telbot.send_message(chat_id=chat_id, reply_to_message_id=message_id,
                        text="[.]("+str(thumb)+") `" + pumnum.upper() +  "` #" +pumnum.upper().replace("_","\_").replace(" ","\_").replace("-","\_") + "\n\n" +
                        "\[ [javdb](https://javdb.com/search?q="+pumnum+"&f=all) ]  "+
                        "\[ [trailer]("+str(trailer)+") ]  "+
                        "\[ [avdbs](https://www.avdbs.com/menu/search.php?kwd="+pumnum.replace("fc2ppv ","")+"&seq=214407610&tab=2) ]  "+
                        "\[ [evojav](https://evojav.pro/en/?s="+pumnum+") ]  "+
                        "\[ [supjav]("+f"https://supjav.com/?s={pumnum}) ]  "+
                        "\[ [missav](https://missav.com/ko/search/"+missavPumnum+") ]  "+
                        "\[ [bt4g](https://kr.bt4g.org/search/"+pumnum.replace("fc2ppv ","")+") ]  "+
                        "\[ [dbmsin]("+ dburl +") ]\n\n"+
                        writer+" "+actor+" "+highlight+createDate+highlight+"\n"+ title
                        ,parse_mode='Markdown' )
    time.sleep(4)

from news_tagger import Keywords
def resend_with_hashtag(bot, update):
    chat_id = bot['chat']['id']
    msg = bot['text']
    message_id = bot['message_id'] # 방금 입력받은 메시지의 id
    reply_message_id = bot['reply_to_message']['message_id'] # 답장걸어야 하는 메시지의 id

    if reply_message_id is not None:
        tagKewords = Keywords()

        urls = find_urls(msg)
        for url in urls: msg=msg.replace(url, "")  #메시지에서 url 임시 제거

        txt = tagKewords.tag_keywords(msg)

        for url in urls: txt+="\n"+url #메시지에 다시 url 입력
        txt=txt.replace("\n\n\n","\n").replace("\n\n","\n") #줄간격 너무 떨어져있는거 제거

        telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        telbot.send_message(chat_id=chat_id,reply_to_message_id=reply_message_id, text=txt)
        telbot.delete_message(chat_id=chat_id, message_id=message_id)
        time.sleep(4)

def find_urls(string) -> list:
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return urls


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
    txt = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥(\s)(\[)(\])(\?)(\!))]", "", txt)
    return txt.replace("[","|").replace("]","| ")

# 파일 용량 단위 변환
async def convert_size(size_bytes):
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

from avdbs_crawling import oldList, twtOldList
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
            qs = []
            try:
                qs = await watchlist.find_keyword_lines_asyn(txt, klistTxtFile) 
                
                banedKey = [bk for bk in qs if "!" in bk] # 금지 키워드 목록
                if banedKey != [] : #하나라도 존재하면 
                    oldList.append(content[0]) # 목록에 그냥 넣어버리고 패스
                    continue 
            except Exception as e:
                print("get_avdbs_crawling - find keword error : ", end="")
                print(e)

            

            telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            telbot.send_message(chat_id=chat_id, text=txt, parse_mode='Markdown')
            oldList.append(content[0]) #전송 성공하면 목록에 저장
            await asyncio.sleep(4)

            try:
                qs = list(set(qs) - set(banedKey))
                if qs != [] :
                    for q in qs: 
                        print("chat_id : " + str(q.split(" ")[0]), end=" | ")
                        print("키워드 : " + q.split(" ")[1])
                        telbot.send_message(chat_id= q.split(" ")[0], text="⏰ 키워드 : `" + q.split(" ")[1] + "` → \[ [에딥톡방](https://t.me/c/1870842558/1) ]", parse_mode = 'Markdown', disable_web_page_preview=True)
                        await asyncio.sleep(4) # 1분에 20개 이상 보내면 에러뜸
            except Exception as e:
                print("get_avdbs_crawling - keword send error : ", end="")
                print(e)
        except Exception as e:
            print("get_avdbs_crawling - content send fail : ", end="")
            print(e)
        
        
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")

async def get_avdbs_twit_crawling(chat_id):
    print("ㅡㅡㅡㅡㅡㅡㅡget_avdbs_twit_crawlingㅡㅡㅡㅡㅡㅡㅡ")
    newContents = await avdbs_crawling.get_avdbs_twit_asyn()
    if newContents == [] : print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ"); return #할거 없으면 그냥 종료

    #content : [twitNum, actorIdx, actorUrl, actorNm, twitUrl, twitID, beforeTime, txt, imgUrls, videoUrls]
    #           0       1         2         3        4        5       6           7    8        9     
    for content in newContents[::-1]:
        try:
            twitNum, actorIdx, actorUrl, actorNm = content[0],content[1],content[2],content[3]
            twitUrl, twitID, beforeTime, twitTxt = content[4],content[5],content[6],content[7]
            imgUrls, videoUrls = content[8],content[9] #리스트

            if imgUrls == [] and videoUrls == [] : continue #이미지, 영상 아무것도 없으면 스킵

            twitTxt = await ForTeleReplaceTxt(twitTxt)
            txt=f"\[ [{actorNm}]({actorUrl}) ] [{twitID}]({twitUrl}) | {beforeTime}\n\n"+twitTxt
            print(f"{actorNm} | {actorIdx} | {twitID} | {beforeTime} | {twitTxt}")
            print(imgUrls, videoUrls)

            #키워드 알림
            try:
                qs = await watchlist.find_keyword_lines_asyn(txt, klistTxtFile) 
                banedKey = [bk for bk in qs if bk.find("!") != -1] # 금지 키워드 목록
                if banedKey != [] : #하나라도 존재하면 
                    twtOldList.append(twitNum) # 목록에 그냥 넣어버리고 패스
                    continue 
            except Exception as e:
                print("get_avdbs_twit_crawling - find keword error : ", end="")
                print(e)

            # 이미지, 영상 다운로드 -> 텔레 업로드 -> 삭제
            imgs=[]
            if imgUrls != []:
                for i, img in enumerate(imgUrls):
                    imgfile = f"img_{actorIdx}_{i}.jpg"
                    urllib.request.urlretrieve(img, imgfile)
                    imgs.append(telegram.InputMediaPhoto(open(imgfile,'rb')))
                try:
                    telbot.send_media_group(chat_id=chat_id, reply_to_message_id='1418', media=imgs, timeout=1000)
                    await asyncio.sleep(4)
                    for i, img in enumerate(imgUrls): os.remove(imgfile) #삭제
                except telegram.error.RetryAfter as e:
                    print(e)
                    await asyncio.sleep(60)
                    telbot.send_media_group(chat_id=chat_id, reply_to_message_id='1418', media=imgs, timeout=1000)
                    await asyncio.sleep(4)
                    for i, img in enumerate(imgUrls): os.remove(imgfile) #삭제
                except Exception as e:
                    print("get_avdbs_twit_crawling img send fail : ", end="")
                    print(e)

            if videoUrls != []:
                videofile = f"video_{actorIdx}.mp4"
                urllib.request.urlretrieve(videoUrls[0], videofile)

                if os.path.exists(videofile) :
                    file_size, size_name = await convert_size(os.path.getsize(videofile))
                    if size_name == "MB" and file_size >= 50 : #50mb 이상이면 스킵
                        print("video "+str(file_size) + size_name, end=" > 50MB ")
                    else : 
                        # video = telegram.InputMediaVideo(open(videofile,'rb'))
                        video=open(videofile,'rb')
                        try:
                            telbot.send_video(chat_id=chat_id, reply_to_message_id='1418', video=video, timeout=1000)
                            await asyncio.sleep(4)
                            video.close()
                            os.remove(videofile)
                        except telegram.error.RetryAfter as e:
                            print(e)
                            await asyncio.sleep(60)
                            telbot.send_video(chat_id=chat_id, reply_to_message_id='1418', video=video, timeout=1000)
                            await asyncio.sleep(4)
                            video.close()
                            os.remove(videofile)
                        except Exception as e:
                            print("get_avdbs_twit_crawling video send fail : ", end="")
                            print(e)
                        if not video.closed : video.close()
                    
            telbot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            telbot.send_message(chat_id=chat_id, reply_to_message_id='1418', text=txt, parse_mode='Markdown')
            twtOldList.append(twitNum) #전송 성공하면 목록에 저장
            await asyncio.sleep(4)

            try:
                qs = list(set(qs) - set(banedKey))
                if qs != [] :
                    for q in qs: 
                        print("chat_id : " + str(q.split(" ")[0]), end=" | ")
                        print("키워드 : " + q.split(" ")[1])
                        telbot.send_message(chat_id= q.split(" ")[0], text="⏰ 키워드 : `" + q.split(" ")[1] + "` → \[ [에딥톡방](https://t.me/c/1870842558/1418) ]", parse_mode = 'Markdown', disable_web_page_preview=True)
                        await asyncio.sleep(4) # 1분에 20개 이상 보내면 에러뜸
            except Exception as e:
                print("get_avdbs_twit_crawling - keword send error : ", end="")
                print(e)
        except Exception as e:
            print("get_avdbs_twit_crawling - content send fail : ", end="")
            print(e)
        
    # 잔류하는 이미지, 영상파일 삭제
    mediaFiles = os.listdir(os.getcwd())

    for mf in mediaFiles:
        if mf.endswith("jpg") or mf.endswith("png") or mf.endswith("mp4") :
            try: os.remove(mf); print(f"removed : {mf}")
            except Exception as e:
                print("get_avdbs_twit_crawling - remove media file fail : ",end="")
                print(e)
        
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")

async def backup_klist(chat_id:str):
    txtFile = [klistTxtFile, 'avdbs_list.txt','av_list_avdbs_all.csv','av_list_avdbs_month.csv','av_list_avdbs_year.csv','av_list_avdbs_week.csv' ]

    for tf in txtFile :
        async with aiofile.AIOFile(tf, 'rb') as f:
            data = await f.read()
            try:
                telbot.send_document(chat_id=chat_id, document=data, filename=tf, timeout=1000)
            except Exception as e:
                telbot.send_message(chat_id=chat_id, text=f"backup fail : {tf}")
                print("backup_klist - send doc fail : ", end="")
                print(e)
    print(f"백업 완료")
    telbot.send_message(chat_id=chat_id, text="백업 완료")
    # klist = watchlist.get_querys(txtFile)
    # if txtFile == newsKlistTxtFile : klist=klist[0].split(",")
    # txt = txtFile+ " backup"
    # for k in klist: 
    #     txtTmp = txt + k +","
    #     if len(txtTmp) > 1000: telbot.send_message(chat_id = chat_id, text = txt) ; txt = "" ; time.sleep(4) #1천자 넘으면 일단 전송
    #     else: txt+=k +","; txtTmp=""
    # telbot.send_message(chat_id = chat_id, text = txt)
    # await asyncio.sleep(4)#나머지 전송


async def backup_avdbs(chat_id, file):
    # csvfiles = ['avdbs_list.txt','av_list_avdbs_all.csv','av_list_avdbs_month.csv','av_list_avdbs_year.csv','av_list_avdbs_week.csv']
    # for csvfile in csvfiles:
    async with aiofile.AIOFile(file, 'rb') as f:
        data = await f.read()
        telbot.send_document(chat_id=chat_id, document=data, filename=file, timeout=1000)
        f.close()
    await asyncio.sleep(4)

    async with aiofile.AIOFile('avdbs_list.txt', 'rb') as f:
        data = await f.read()
        telbot.send_document(chat_id=chat_id, document=data, filename='avdbs_list.txt', timeout=1000)
        f.close()
    await asyncio.sleep(4)
    print(f"{file} 백업 완료")
    telbot.send_message(chat_id=chat_id, text=f"{file} 백업 완료")

def get_avdbs_rank(avdbs_period, chat_id):
    ''''
    avdbs_period : "avdbs week", "avdbs month", "avdbs year", "avdbs all"
    '''
    msg=avdbs_period

    reply_to_message_id=""
    if msg.lower().find("week") != -1 : reply_to_message_id = '1305' #에딥톡방-에딥주간순위
    elif msg.lower().find("month") != -1 : reply_to_message_id = '1303' #에딥톡방-에딥월간순위
    elif msg.lower().find("year") != -1 : reply_to_message_id = '1332' #에딥톡방-에딥연간순위
    elif msg.lower().find("all") != -1 : reply_to_message_id = '1334' #에딥톡방-에딥연간순위
    
    try:
        telbot.send_message(chat_id=chat_id, text=msg+ " 가져오는중")
        pumdf = avdbs_crawling.get_avdbs_rank(msg.split(" ")[1].lower()) 
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
                df2str += str(idx) + " (new) [" + pum[2] + "](https://evojav.pro/en/?s="+pum[2]+") " + str(pum[10]) + " up " + str(datetime.strftime(pum[5],"%Y-%m-%d")) +"\n"
                if int(idx) <= 15 : #15위 안에 들면
                    ok = True
                    updown = "(new)"
            elif idx < pum[12] : # 순위가 올라가면
                df2str += str(idx) + " ("+ str(pum[12]-idx) + "↑) [" + pum[2] + "](https://evojav.pro/en/?s="+pum[2]+") " + str(pum[10]) + " up " + str(datetime.strftime(pum[5],"%Y-%m-%d")) +"\n"
                if int(idx) <= 15 : #15위 안에 들면
                    ok = True
                    updown = "("+ str(pum[12]-idx) + "↑)"
            elif idx > pum[12] : # 순위가 내려가면
                df2str += str(idx) + " ("+ str(idx - pum[12]) + "↓) [" + pum[2] + "](https://evojav.pro/en/?s="+pum[2]+") " + str(pum[10]) + " up " + str(datetime.strftime(pum[5],"%Y-%m-%d")) +"\n"
            else: # 순위변동 없으면
                df2str += str(idx) + " [" + pum[2] + "](https://evojav.pro/en/?s="+pum[2]+") " + str(pum[10]) + " up " + str(datetime.strftime(pum[5],"%Y-%m-%d")) +"\n"
            
            highlight=""
            if datetime.strftime(pum[5],"%Y-%m-%d") != "-":
                diffDate = datetime.now() - datetime.strptime(datetime.strftime(pum[5],"%Y-%m-%d"), "%Y-%m-%d") # 날짜차이 계산
                if diffDate.days <= 7 : highlight="`"

            # 새로운 데이터 입력
            if pum[2] not in oldtxt: #중복검사
                title = filename_set.replaceTxt(str(pum[4]))
                title = title.replace("_","\\_")
                pumnum = pum[2].replace("_","\\_")
                actor = filename_set.replaceTxt(str(pum[3]))
                dburl=f"https://db.msin.jp/jp.search/movie?str={pumnum}"

                txt="[.]("+str(pum[7])+") [.]("+str(pum[8])+") `" + pumnum + "` #" +pumnum.replace(" ","\\_").replace("-","\\_") + "\n\n"\
                    "\[ [javdb](https://javdb.com/search?q="+pumnum+"&f=all) ]  "\
                    "\[ [trailer]("+str(pum[9])+") ]  "\
                    "\[ [avdbs](https://www.avdbs.com/menu/search.php?kwd="+pumnum+"&seq=214407610&tab=2) ]  "\
                    "\[ [evojav](https://evojav.pro/en/?s="+pumnum+") ]  "\
                    "\[ [supjav]("+f"https://supjav.com/?s={pumnum}) ]  "+\
                    "\[ [missav](https://missav.com/ko/search/"+pumnum+") ]  "\
                    "\[ [bt4g](https://kr.bt4g.org/search/"+pumnum+") ]  "\
                    "\[ [dbmsin]("+ dburl +") ]\n\n"\
                    "#"+actor.replace(" "," #").replace("("," #").replace(")","") + "\n" + title+"\n\n"\
                    "#"+str(idx)+"위 (new) #"+msg.replace(" ","\\_")+ " "+highlight+ str(datetime.strftime(pum[5],"%Y-%m-%d")) +highlight+ " " + str(pum[10]) + " up"

                qs = watchlist.find_keyword_lines(pumnum + " " + txt,'av_list_keyword.txt') 

                banedKey = [bk for bk in qs if "!" in bk] # 금지 키워드 목록
                if banedKey != [] : #하나라도 존재하면 스킵
                    with open(txtfile, 'a', encoding = 'UTF-8') as f:          
                        f.write(pum[2] + "\n")
                    continue

                telbot.send_message(chat_id=channel_id_av, text=txt,parse_mode='Markdown' )
                if reply_to_message_id != "":
                    time.sleep(4)
                    telbot.send_message(chat_id=group_id_avdbs, reply_to_message_id=reply_to_message_id, text=txt,parse_mode='Markdown' )
                with open(txtfile, 'a', encoding = 'UTF-8') as f:          
                    f.write(pum[2] + "\n")
                time.sleep(4) # 1분에 20개 이상 보내면 에러뜸

                qs = list(set(qs) - set(banedKey))
                #키워드 알림
                if qs != [] :
                    for q in qs: telbot.send_message(chat_id= q.split(" ")[0], text="⏰ 키워드 : `" + q.split(" ")[1] + "` → `" + str(pumnum.upper()) +'` #'+str(pumnum.upper().replace(" ","\_").replace("-","\_"))+' [신작&순위 채널](https://t.me/+Y7PSYJPViXFiZTY1)', parse_mode = 'Markdown', disable_web_page_preview=True); time.sleep(4) # 1분에 20개 이상 보내면 에러뜸
                    
                
            elif ok is True :
                title = filename_set.replaceTxt(str(pum[4]))
                title = title.replace("_","\\_")
                pumnum = pum[2].replace("_","\\_")
                actor = filename_set.replaceTxt(str(pum[3]))
                dburl=f"https://db.msin.jp/jp.search/movie?str={pumnum}"

                txt="[.]("+pum[7]+") [.]("+pum[8]+") `" + pumnum + "` #" +pumnum.replace(" ","\\_").replace("-","\\_") + "\n\n"\
                    "\[ [javdb](https://javdb.com/search?q="+pumnum+"&f=all) ]  "\
                    "\[ [trailer]("+str(pum[9])+") ]  "\
                    "\[ [avdbs](https://www.avdbs.com/menu/search.php?kwd="+pumnum+"&seq=214407610&tab=2) ]  "\
                    "\[ [evojav](https://evojav.pro/en/?s="+pumnum+") ]  "\
                    "\[ [supjav]("+f"https://supjav.com/?s={pumnum}) ]  "+\
                    "\[ [missav](https://missav.com/ko/search/"+pumnum+") ]  "\
                    "\[ [bt4g](https://kr.bt4g.org/search/"+pumnum+") ]  "\
                    "\[ [dbmsin]("+ dburl +") ]\n\n"\
                    "#"+actor.replace(" "," #").replace("("," #").replace(")","") + "\n" + title+"\n\n"\
                    "#"+str(idx)  + "위 "+updown+ " #"+ msg.replace(" ","\\_") + " "+highlight+ str(datetime.strftime(pum[5],"%Y-%m-%d")) +highlight+ " " + str(pum[10]) + " up"

                qs = watchlist.find_keyword_lines(pumnum + " " + txt,'av_list_keyword.txt') 

                banedKey = [bk for bk in qs if "!" in bk] # 금지 키워드 목록
                if banedKey != [] : #하나라도 존재하면 스킵
                    continue

                telbot.send_message(chat_id=channel_id_av, text=txt,parse_mode='Markdown' )
                time.sleep(4) # 1분에 20개 이상 보내면 에러뜸
                if reply_to_message_id != "":
                    telbot.send_message(chat_id=group_id_avdbs, reply_to_message_id=reply_to_message_id, text=txt,parse_mode='Markdown' )
                    time.sleep(4)

                qs = list(set(qs) - set(banedKey))
                #키워드 알림 
                if qs != [] :
                    for q in qs: telbot.send_message(chat_id= q.split(" ")[0], text="⏰ 키워드 : " + q.split(" ")[1] + " → `" + str(pumnum.upper()) +'` #'+str(pumnum.upper().replace(" ","\_").replace("-","\_"))+' [신작&순위 채널](https://t.me/+Y7PSYJPViXFiZTY1)', parse_mode = 'Markdown', disable_web_page_preview=True); time.sleep(4) # 1분에 20개 이상 보내면 에러뜸
                    
                
        print(df2str)
        telbot.send_message(chat_id=chat_id, text="※ "+msg.upper()+" / 품번 / UP ※\n\n" + df2str,parse_mode='Markdown',disable_web_page_preview=True)
    except Exception as e:
        print("get_avdbs_rank : ")
        print(e)
        telbot.send_message(chat_id=chat_id, text="순위 가져오기 실패")

async def get_avdbs_rank_week():
    get_avdbs_rank('avdbs week',group_id_trash)
    await backup_avdbs(group_id_trash,'av_list_avdbs_week.csv')

async def get_avdbs_rank_month():
    get_avdbs_rank('avdbs month',group_id_trash)
    await backup_avdbs(group_id_trash,'av_list_avdbs_month.csv')

global LINKS
LINKS=[]
async def get_twidouga():
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡget_twidougaㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
    links = avdbs_crawling.get_twidouga_rank()
    for link in links :
        try:
            if link not in LINKS: 
                LINKS.append(link)
                telbot.send_video(chat_id=group_id_memo, video=link); time.sleep(3)
                print(link)
            
        except Exception as e:
            print("get_twidouga - send video fail : ",end="")
            print(e)
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
        



def alarmi():
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print("스케쥴 에러 : ", end="")
            print(e)
            
sch_hour = (21 - diff_hour)%24 # 21시 -> 09시 = ??
sch_min30 = (30 + diff_min)%60 # 30분 - 28분 = 2분
sch_min45 = (45 + diff_min)%60 # 30분 - 28분 = 2분
print(f"{sch_hour}:{sch_min30}, {sch_min45}")
schedule.every().day.at(f"{sch_hour}:{sch_min30}").do(lambda:asyncio.run(get_avdbs_rank_month()))
schedule.every().day.at(f"{sch_hour}:{sch_min45}").do(lambda:asyncio.run(get_avdbs_rank_week()))

schedule.every(3).hours.do(lambda:asyncio.run(get_twidouga())) 
schedule.every(10).minutes.do(lambda:asyncio.run(get_avdbs_crawling(group_id_avdbs))) 
schedule.every(15).minutes.do(lambda:asyncio.run(get_avdbs_twit_crawling(group_id_avdbs))) 
schedule.every().day.at("00:00").do(lambda:asyncio.run(backup_klist(group_id_trash))) 

print("쓰레딩이이잉")
telbot.sendMessage(chat_id=group_id_trash, text=("rss봇 실행됨"))

#일단 한번 에딥 크롤링 시작
try:
    telbot.send_message(chat_id=group_id_avdbs, text="ㅡㅡㅡㅡㅡㅡㅡㅡrestartㅡㅡㅡㅡㅡㅡㅡㅡ")  
    asyncio.run(get_avdbs_crawling(group_id_avdbs))
except Exception as e:
    print("get_avdbs_crawling error : ", end="")
    print(e)

#일단 한번 에딥 크롤링 시작
try:
    telbot.send_message(chat_id=group_id_avdbs, reply_to_message_id='1418', text="ㅡㅡㅡㅡㅡㅡㅡㅡrestartㅡㅡㅡㅡㅡㅡㅡㅡ")  
    asyncio.run(get_avdbs_twit_crawling(group_id_avdbs))
except Exception as e:
    print("get_avdbs_twit_crawling error : ", end="")
    print(e)

#일단 한번 에딥 크롤링 시작
try:  
    telbot.send_message(chat_id=group_id_memo, text="ㅡㅡㅡㅡㅡㅡㅡㅡrestartㅡㅡㅡㅡㅡㅡㅡㅡ")
    asyncio.run(get_twidouga())

except Exception as e:
    print("get_avdbs_twit_crawling error : ", end="")
    print(e)    

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