'''
>> class Keywords
>> class Tagger
'''
import requests
import urllib.request,json
from bs4 import BeautifulSoup as bs

class Keywords():
    ''' 키워드는 대문자만 취급함 '''
    def __init__(self, keywordsTxtFile=None) -> None:

        if keywordsTxtFile is None: 
            self.keywordsTxtFile = "news_keywords.txt"
        else : self.keywordsTxtFile = keywordsTxtFile
        
        self.keywords = self.get_keywords(self.keywordsTxtFile)
    
    def get_keywords(self, keywordsTxtFile=None):
        if keywordsTxtFile is None: keywordsTxtFile=self.keywordsTxtFile

        with open(keywordsTxtFile, 'r+', encoding = 'UTF-8') as f:
            keywords = f.read().split(",").sort()
        return keywords

    def add_keyword(self, keyword:str, keywordsTxtFile=None) -> bool:
        if keywordsTxtFile is None: keywordsTxtFile=self.keywordsTxtFile

        keywords = self.get_keywords(keywordsTxtFile)
        if keyword.upper() in keywords : return False # 목록에 있습니다 저장안하고 종료

        with open(keywordsTxtFile, 'a+', encoding = 'UTF-8') as f: # 목록에 없습니다. 추가합니다.")
            f.write(keyword.upper()+",") 
            self.del_keyword("")
            return True # 저장함

    def add_keywords(self, keywordL:list, keywordsTxtFile=None) -> list:
        if keywordsTxtFile is None: keywordsTxtFile=self.keywordsTxtFile

        keywords = self.get_keywords(keywordsTxtFile)
        added = []
        for kl in keywordL:
            if kl.upper() not in keywords : 
                with open(keywordsTxtFile, 'a+', encoding = 'UTF-8') as f: # 목록에 없습니다. 추가합니다.")
                    f.write(kl.upper()+",") 
                    added.append(kl.upper())
        self.del_keyword("")
        return added # 저장한 키워드 목록 반환
    
    def del_keyword(self, keyword, keywordsTxtFile=None) -> bool:
        ''' del_keyword("") -> 중복제거, 공백문자 제거'''
        if keywordsTxtFile is None: keywordsTxtFile=self.keywordsTxtFile
        keywords = self.get_keywords(keywordsTxtFile)

        if keyword.upper() not in keywords and keyword != "": return False # 목록에 없습니다 종료
        
        with open(keywordsTxtFile, 'w+', encoding = 'UTF-8') as f: # 목록에 있습니다 삭제
            keywords = [x for x in keywords if x != keyword.upper()]
            for kw in list(set(keywords)): f.write(kw.upper()+",") 
            return True # 저장함

    def tag_keywords(self, text: str) -> str:
        text = text.upper()
        hashtag_list = [word.replace("#","").replace("_"," ") for word in text.split() if word.startswith("#")]
        self.add_keywords(hashtag_list)

        for keyword in self.get_keywords():
            if keyword != "" and keyword in text :
                to = '#'+keyword.replace(" ","_")+" "
                text = text.replace(keyword, to)
        self.del_keyword("")
        return text.replace("##","#").replace("###","#")


class News:
    def __init__(self) -> None:
        self.url = None
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' 
                }

    def get_news(self, url: str) -> str:
        self.url = url
        response = requests.get(url, self.headers)
        soup = bs(response.text, 'html.parser')
        news_text = soup.get_text().strip().replace("\n","")
        return self.keywords.tag_keywords(news_text)


#테스트
if __name__ == "__main__":
    keywords = Keywords()

    print(keywords.add_keywords(["Apple","TSLA","MsfT"]))
    print(keywords.get_keywords())

    txt = "제목 : 테슬라, #중국 에서 가격 인하...3개월래 2번째 * #연합인포맥스 * #CNN 은 “테슬라(TSLA)가 중국에서 수요 부진 속에서 판매를 촉진하기 위해 3개월래 두 번째 가격인하를 단행했다”고 보도했다.   “6일(금) 테슬라가 중국에서 생산되는 모델3와 Y의 가격을 인하했다”고 전했다.   이와 관련해 “모델 3와 Y의 시작가는 각각 13.5% 인하된 229,900위안, 10% 인하된 259,900위안이다”고 설명했다.   이어 “‘22년 10월 24일(월) 두 모델에 대해 각각 9.4%씩 가격을 인하한 이후 두 번째인 것이다. 과거 2년 동안 테슬라는 가격을 인상한 바있다”고 덧붙였다.   이에 6일 테슬라의 그레이스 타오 부회장은 “테슬라의 이번 가격인하는 동사의 대단한 엔지니어링 혁신이 뒷받침한다”고 본인의 웨이보 계정에 글을 게재했다.   또한 “당사는 국가(중국)가 경제 발전 촉진을 원함에 따라 현실적인 행동으로 응답해준 것이다”고 덧붙였다."

    print(keywords.tag_keywords(txt))
    print(keywords.get_keywords())



'''
1. 텍스트를 받아온다.
2. 해시태그를 단다.
    - 단어를 비교한다.
3. 텍스트를 리턴한다.

r : 읽기 모드, 파일 없으면 Error
r+: 읽기 또는 쓰기모드, 파일 없으면 Error
w : 쓰기 모드, 파일 없으면 새로 만든다.
w+ : 읽기 또는 쓰기 모드, 파일 없으면 새로 만든다.
a : 파일 추가(FP가 파일의 끝으로 이동)로 쓰기 모드, 파일 없으면 새로 만든다.
a+ : 읽기 또는 파일 추가 모드, 파일 없으면 만든다.
'''

        