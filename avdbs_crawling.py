import urllib.request
from bs4 import BeautifulSoup as bs
import asyncio

avdbsUrl = "https://www.avdbs.com"
avdbsWholeBoardUrl = "https://www.avdbs.com/board/t90"
avdbsBoardUrl = "https://www.avdbs.com/board/"

headers = {
        "Cookie":"age=off",
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
            contents = soup.select('#contants > div.brd_lst > div > div.lst_wrp > ul.lst.normal')

            newList=[]
            for content in contents:
                #컨텐츠 번호
                num = content.select_one('li.no').get_text().strip()
                if num in oldList: 
                    if len(oldList) >= 100 : oldList = oldList[70:] #너무 쌓이면 목록삭제
                    continue # 이미 목록에 있으면 건너뜀
                else: oldList.append(num); num=avdbsBoardUrl+num; print(num, end=" | ")
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

# get_avdbs_whole_board()