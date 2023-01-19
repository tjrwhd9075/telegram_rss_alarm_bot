import urllib.request
from bs4 import BeautifulSoup as bs
import asyncio
import pandas as pd

import av_img_video_url as avurl

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
            contents = soup.find_all('li', class_='twit_item')
            # contents = soup.select('ul > li.twit_item')

            newList=[]
            for content in contents:
                # print(content)
                try:
                    twitNum, actorIdx, actorUrl, actorNm, twitUrl, twitID, beforeTime, txt = "-","-","-","-","-","-","-","-"
                    imgUrls, videoUrls=[],[]
                    #컨텐츠 번호
                    twitNum = content['data-twit_id']
                    if twitNum in twtOldList: 
                        if len(twtOldList) >= 200 : twtOldList[0:100]=[] #너무 쌓이면 목록삭제
                        continue # 이미 목록에 있으면 건너뜀
                    # else: print(twitNum, end=" | ")
                    #트윗url
                    twitUrl = content['data-twit_url']
                    # print(twitUrl, end=" | ")
                    #트윗프로필
                    twitPf = content.select_one('div.pf_thumb').a.img['src']
                    # print(twitPf, end=" | ")
                    #트윗id
                    twitID = content.select_one('span.twitter_id').get_text().strip()
                    # print(twitID, end=" | ")

                    #여배우 번호
                    actorIdx = content['data-actor_idx']
                    # print(actorIdx, end=" | ")
                    #avdbs 여배우 url
                    actorUrl = avdbsActorUrl+actorIdx
                    # print(actorUrl, end=" | ")
                    #여배우 이름
                    actorNm = content.select_one('span.actor_nm').get_text().strip()
                    # print(actorNm, end=" | ")
                    
                    #n분전
                    beforeTime = content.select_one('span.time').get_text().strip()
                    # print(beforeTime, end=" | ")
                    #텍스트
                    txt = content.select_one('div.ct_txt').get_text().strip()
                    # print(txt)
                    #이미지 또는 비디오
                    mediaP = content.select_one('div.img_box')
                    media = content.select_one('div.img_box').div
                    imgUrls, videoUrls = [], []
                    if media is not None: 
                        for i, img in enumerate(mediaP.find_all('img')):
                            if img['src'] != '/w2017/img/twitter-play.png':
                                imgUrls.append(img['src'].replace(":small",""))
                                # urllib.request.urlretrieve(img['src'], f"img_{actorIdx}_{i}.jpg")
                        for video in mediaP.find_all('source-tag'):
                            videoUrls.append(video['src'])
                        # if videoUrls != []: urllib.request.urlretrieve(videoUrls[0], f"video_{actorIdx}.mp4")
                    # print(imgUrls)
                    # print(videoUrls)
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
    
def get_avdbs_rank(period):
    '''
    period : week, month, year, all
    '''
    # pumdf = pd.DataFrame(columns=['period','rank','pumnum','actor','title','date','avdbslink','thumb','up','down','oldrank'])

    pumdf = pd.read_csv(f"av_list_avdbs_{period}.csv",header=0, index_col=0)
    pumdf['oldrank'] = pumdf.index  # 이전 인덱스는 랭크로 이동
    pumdf = pumdf.astype({'oldrank':'int'})
    pumdf['rank'] = 50
    
    #에딥 랭킹
    
    url = f'https://www.avdbs.com/menu/dvd_ranking.php?tab={period}'
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    res = response.read().decode('utf-8')
    soup = bs(res,'html.parser')

    pums = soup.find('ul', class_='lst').find_all('li')
    
    cnt = 0
    for pum in pums :
        pumnum = pum.select_one('span.snum').get_text().strip()
        print(pumnum)
        avdbslink = 'https://www.avdbs.com/menu/dvd.php?dvd_idx=' + pum['data-idx']
        rank = int(pum.select_one('span.rnk_no').get_text().replace("위",""))

        #에딥에서 상세정보
        title, actor, date, up, down = get_puminfo(pum['data-idx'])
        if title == "": title = pum.select_one('a.title').get_text().strip(); print(title)

        thumb = avurl.makeImageURL(pumnum)
        if isinstance(thumb, list):
            thumb1 = thumb[0]
            thumb2 = thumb[1]
        else: thumb1 = thumb; thumb2="-"
        trailer = avurl.makeVideoURL(pumnum)

        i = pumdf.index[pumdf['pumnum'] == pumnum].tolist()   # 중복된 품번이 있는 곳의 인덱스 찾기
        if i == [] : # 새로운 품번이면 그대로 추가
            tmp = pd.DataFrame(data=[[period,rank,pumnum,actor,title,date,avdbslink,thumb1,thumb2,trailer,up,down,0]], columns=['period','rank','pumnum','actor','title','date','avdbslink','thumb1','thumb2','trailer','up','down','oldrank'])
            pumdf = pd.concat([pumdf,tmp])
        else:
            pumdf.loc[pumdf['pumnum']==pumnum,'rank'] = rank # 품번이 같은 행의, 랭크 수정
            pumdf.loc[pumdf['pumnum']==pumnum,'up'] = up # 품번이 같은 행의, up 수정
            pumdf.loc[pumdf['pumnum']==pumnum,'down'] = down # 품번이 같은 행의, down 수정

        cnt=cnt+1
        if cnt == 30: break
    
    pumdf['date'] = pd.to_datetime(pumdf['date'], format="%Y/%m/%d")
    pumdf = pumdf.sort_values(['period','rank'],ascending=True) # 오름차순 정렬
    pumdf = pumdf.reset_index(drop=True) # 인덱스 = 순위
    pumdf.index = pumdf.index +1
    # pumdf['rank'] = 0

    print("새로 저장중")
    pumdf = pumdf[:30]
    pumdf.to_csv(f"av_list_avdbs_{period}.csv")
    print(pumdf)
    
    return pumdf

# asyncio.run(get_avdbs_whole_board_asyn())
if __name__ == "__main__":
    # asyncio.run(get_avdbs_twit_asyn())
    get_avdbs_rank("week")

    # pumnum = "SSIS-308"
    # get_puminfo(pumnum)