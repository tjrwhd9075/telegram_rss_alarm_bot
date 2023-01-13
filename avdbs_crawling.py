import urllib.request
from bs4 import BeautifulSoup as bs
import asyncio

avdbsUrl = "https://www.avdbs.com"
avdbsWholeBoardUrl = "https://www.avdbs.com/board/t90"
avdbsPumUrl= 'https://www.avdbs.com/menu/dvd.php?dvd_idx='
avdbsTwitUrl = "https://www.avdbs.com/actor/twit"
avdbsActorUrl = 'https://www.avdbs.com/menu/actor.php?actor_idx='
avdbsActorTwitUrl = 'https://www.avdbs.com/actor/twit?_idx='

# adult_chk=1 로 넣으면 성인인증한것처럼 나온다.
# user_nickname=ddd   로 넣으면 로그인 한것 처럼나온다.
# member_idx=111      의미 없어보이지만 회원시퀀스로 보여진다.
headers = {
        "Cookie":"age=off; adult_chk=1; user_nickname=dd; member_idx= 11;",
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/53.36'
    } 

global oldList
oldList = [] #게시판 번호 저장

async def get_avdbs_whole_board_asyn():
    global oldList
    
    try:
        req = urllib.request.Request(url=avdbsWholeBoardUrl, headers=headers)
        response = urllib.request.urlopen(req)

        getcode = response.getcode()
        if getcode == 200: #정상

            res = response.read().decode('utf-8')
            soup = bs(res,'html.parser')
            contents = soup.select('#contants > div.brd_lst > div > div.lst_wrp > ul.lst.normal, #contants > div.brd_lst > div > div.lst_wrp > ul.lst.hlight')

            newList=[]
            for content in contents:
                #컨텐츠 번호
                num = content.select_one('li.no').get_text().strip()
                if num in oldList: 
                    if len(oldList) >= 100 : oldList[0:50]=[] #너무 쌓이면 목록삭제
                    continue # 이미 목록에 있으면 건너뜀
                else: print(num, end=" | ")
                #컨텐츠 썸네일
                thumb = content.select_one('img.thumb')
                if thumb is not None and thumb['src'].find("ao_lst.jpg") == -1: #19 이상 사진일때 그냥 패스
                    thumb = avdbsUrl+thumb['src']; thumb=thumb.replace("_s","") ; print(thumb, end=" | ")
                else : thumb = None ; print(thumb, end=" | ")
                #컨텐츠 게시판 타입                
                boardType = content.select_one('span.mark').get_text().strip()
                print(boardType, end=" | ")
                #성인여부             
                adult = content.select_one('span.adult_only')
                if adult is not None: adult = adult.get_text().strip()
                else: adult = None
                print(adult, end=" | ")
                #컨텐츠 날짜
                date = content.select_one('li.date').get_text().strip()
                print(date, end=" | ")
                #컨텐츠 작성시간
                beforeTime = content.select_one('span.float-right > span.margin-left-10').get_text().strip()
                print(beforeTime, end=" | ")
                #컨텐츠 작성자
                writer = content.select_one('span.writer').get_text().strip()
                print(writer, end=" | ")
                #컨텐츠 작성자 레벨
                lvl = content.select_one('img.lvl')['src']
                lvl = lvl.split('_')[-1].replace(".gif","")
                print("lvl : "+lvl, end=" | ")
                #컨텐츠 조회수
                view = content.select_one('i.fa.fa-eye')
                if view is not None:
                    view = view.next_sibling.next_sibling.get_text().strip()
                else: view = "0"
                print("view : "+view, end=" | ")
                #컨텐츠 댓글수
                recom = content.select_one('i.margin-left-10.fa.fa-commenting-o')
                if recom is not None:
                    recom = recom.next_sibling.next_sibling.get_text().strip()
                else: recom = "0"
                print("recom : "+recom, end=" | ")
                #컨텐츠 따봉수
                good = content.select_one('i.margin-left-10.fa.fa-thumbs-o-up')
                if good is not None:
                    good = good.next_sibling.next_sibling.get_text().strip()
                else: good = "0"
                print("good : "+good, end="\n")
                #컨텐츠 제목               
                title = content.select_one('h2.title').get_text().strip()
                title = title.replace(boardType, "")
                if adult is not None: title = title.replace(adult,"")
                title = title.replace("  [","[").replace(" [","[")
                print("제목 : "+title, end="\n")
                #컨텐츠내용
                contentTxt = content.select_one('div.dscr').get_text().strip()
                print("내용 : "+contentTxt, end="\n\n")

                newList.append([num,thumb,boardType,adult,date,beforeTime,writer,lvl,view,recom,good,title,contentTxt])
            
            return newList

        else:
            print(str(getcode) + " : avdbs url 에러")
            return []
    except Exception as e:
        print("url open fail")
        print(e)
        return []

global twtOldList
twtOldList = [] #트윗 번호 저장

async def get_avdbs_twit_asyn():
    ''' return [[twitNum, actorIdx, actorUrl, actorNm, twitUrl, twitID, beforeTime, txt, imgUrls, videoUrls], .... ]'''
    global twtOldList
    
    try:
        req = urllib.request.Request(url=avdbsTwitUrl, headers=headers)
        response = urllib.request.urlopen(req)

        getcode = response.getcode()
        if getcode == 200: #정상

            res = response.read().decode('utf-8')
            soup = bs(res,'html.parser')
            contents = soup.select('li.twit_item')

            newList=[]
            for content in contents:
                twitNum, actorIdx, actorUrl, actorNm, twitUrl, twitID, beforeTime, txt, = "-","-","-","-","-","-","-","-"
                imgUrls, videoUrls=[],[]
                try:
                    #컨텐츠 번호
                    twitNum = content.select_one('li.twit_item')['data-twit_id']
                    if twitNum in twtOldList: 
                        if len(twtOldList) >= 100 : twtOldList[0:50]=[] #너무 쌓이면 목록삭제
                        continue # 이미 목록에 있으면 건너뜀
                    else: print(twitNum, end=" | ")
                    #여배우 번호
                    actorIdx = content.select_one('li.twit_item')['data-actor_idx']
                    print(actorIdx, end=" | ")
                    actorUrl = avdbsActorUrl+actorIdx
                    #여배우 이름
                    actorNm = content.select_one('span.actor_nm').get_text().strip()
                    print(actorNm, end=" | ")
                    #트윗url
                    twitUrl = content.select_one('li.twit_item')['data-twit_url']
                    print(twitUrl, end=" | ")
                    #트윗프로필
                    twitPf = content.select_one('div.pf_thumb').a.img['src']
                    print(twitPf, end=" | ")
                    #트윗id
                    twitID = content.select_one('span.twitter_id').get_text().strip()
                    print(twitID, end=" | ")
                    #n분전
                    beforeTime = content.select_one('span.time').get_text().strip()
                    print(beforeTime, end=" | ")
                    #텍스트
                    txt = content.select_one('div.ct_txt').get_text().strip()
                    print(txt)
                    #이미지 또는 비디오
                    media = content.select_one('div.img_box').div
                    imgUrls, videoUrls = [], []
                    if media is not None: 
                        for i, img in enumerate(media.find_all('img')):
                            if img['src'] != '/w2017/img/twitter-play.png':
                                imgUrls.append(img['src'].replace(":small",""))
                                # urllib.request.urlretrieve(img['src'], f"img_{actorIdx}_{i}.jpg")
                        for video in media.find_all('source-tag'):
                            videoUrls.append(video['src'])
                        # if videoUrls != []: urllib.request.urlretrieve(videoUrls[0], f"video_{actorIdx}.mp4")
                    print(imgUrls)
                    print(videoUrls)
                    newList.append([twitNum, actorIdx, actorUrl, actorNm, twitUrl, twitID, beforeTime, txt, imgUrls, videoUrls])

                except Exception as e: print("twit 읽기 실패")
            return newList

        else:
            print(str(getcode) + " : avdbs url 에러")
            return []
    except Exception as e:
        print("url open fail")
        print(e)
        return []


def get_puminfo(pumnum:str):
    ''' return title, actor, date, up, down'''
    req = urllib.request.Request(url=avdbsPumUrl+pumnum, headers=headers)
    response = urllib.request.urlopen(req)
    res = response.read().decode('utf-8')
    soup = bs(res,'html.parser')

    try:
        title = soup.select_one('#title_kr').get_text().strip()
    except:
        title = "Unknown"
    print(title ,end=" | ")
    try:
        actor = soup.select_one('a.cast').get_text().strip().replace("#","")
    except:
        actor = "Unknown"
    print(actor ,end=" | ")
    try:
        date = soup.select_one('div.profile_detail').next_element.next_element.get_text().strip().split(" ")[-1]
    except:
        date = "-"
    print(date ,end=" | ")
    try:
        up = int(soup.select_one('span.likecount').get_text().strip().replace(",",""))
        down = int(soup.select_one('span.dislikecount').get_text().strip())
    except:
        up = 0
        down = 0
    print(up, down ,end=" | ")

    return title, actor, date, up, down
    


# asyncio.run(get_avdbs_whole_board_asyn())
if __name__ == "__main__":
    asyncio.run(get_avdbs_twit_asyn())

    # pumnum = "SSIS-308"
    # get_puminfo(pumnum)