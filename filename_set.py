

from cProfile import label
from mmap import PAGESIZE
from pprint import pprint
from unittest import result
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
from matplotlib.pyplot import title
from numpy import setxor1d
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from pprint import pprint
import requests
import random
from sqlalchemy import column
import undetected_chromedriver as uc
import traceback

from sympy import EX
from zmq import EVENT_CLOSED

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("start-maximized")
chrome_options.add_argument('headless')    # 창 띄우지 X
chrome_options.add_argument('disable-gpu')  # gpu 사용 X
chrome_options.add_argument('no-sandbox')
chrome_options.add_argument("single-process")
chrome_options.add_argument("disable-dev-shm-usage")
chrome_options.add_argument("--disableWarnings")
chrome_options.add_argument('--log-level=1')   # 에러메시지 안뜨게?
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36")

import os
import chromedriver_autoinstaller as AutoChrome
import shutil

def chromedriver_update():
    chrome_ver = AutoChrome.get_chrome_version().split('.')[0]
    print(f'최신 크롬 버전은 {chrome_ver}입니다.')

    current_list = os.listdir(os.getcwd()) 			# 현재 경로의 모든 객체들
    chrome_list = []
    for i in current_list:
        path = os.path.join(os.getcwd(), i) 			# 현재 경로의 모든객체의 전체경로
        if os.path.isdir(path): 				# 그 경로가 폴더인지 확인
            if 'chromedriver.exe' in os.listdir(path): 		# 폴더면 안에 chromedriver.exe가 있는지 확인
                chrome_list.append(i) 				# 있는경우 chrome_list에 추가
                print(f'현재 크롬 버전은 {chrome_ver}입니다.')

    old_version = list(set(chrome_list)-set([chrome_ver])) 	# 그중에 최신버전은 제외

    for i in old_version:
        path = os.path.join(os.getcwd(),i) 			# 구버전이 있는 폴더의 경로 
        shutil.rmtree(path) 					# 그 경로 삭제

    if not chrome_ver in current_list: 				# 최신버전 폴더가 현재 경로에 없으면
        AutoChrome.install(True) 				# 크롬드라이버 설치
        print('크롬 버전을 업데이트 합니다')
    else : pass 						# 아니면 무시

def get_chromedriver_path():
    ''' 크롬 버전의 숫자 폴더명 리턴 '''
    chrome_ver = AutoChrome.get_chrome_version().split('.')[0]
    # print(f'현재 크롬 버전은 {chrome_ver}입니다.')

    current_list = os.listdir(os.getcwd()) 			# 현재 경로의 모든 객체들
    chrome_list = []
    for i in current_list:
        path = os.path.join(os.getcwd(), i) 			# 현재 경로의 모든객체의 전체경로
        if os.path.isdir(path): 				# 그 경로가 폴더인지 확인
            if 'chromedriver.exe' in os.listdir(path): 		# 폴더면 안에 chromedriver.exe가 있는지 확인
                return i #크롬 버전의 숫자 폴더명



# https://chromedriver.chromium.org/downloads  크롬드라이버 다운로드 사이트

chrome_path = "./" + get_chromedriver_path() + "/chromedriver"
# path = 'chromedriver'
header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'}


def replaceWriterTxt(txt):
    dic = {
            "変態面接官N":"변Tae면접관N","すいか、":"수박","シロートエキスプレスZ":"시로토익스프레스Z","匿名希望。":"익명희망",
            "ぱすも":"파스모","ちゃおず":"차오즈","ネオペイ":"네오페이","レッドDキング":"레드D킹","ビーストたけし":"비스트타케시",
            "どむどむ":"도무도무","男尊女卑":"남존녀비","白い池":"하얀연못","パスカルF":"파스칼F","ゆず故障":"유자고장",
            "美女革命":"미녀혁명","SG.GK":"SGGK","精いっぱい":"가득히","マン貫ドライチ":"만관도라이치",
            "[超]スタミナ二郎 増し増し":"초스태미나지로증가증가","[超]スタミナ二郎増し増し":"초스태미나지로증가증가",
            "美少女遊記":"미소녀유기","保健室の窓":"보건실창문","[COFFEE]":"COFFEE","超時空夢幻カメコ":"초시공몽환카메코",
            "暗黒王子":"암흑왕자","ハメンタル":"하멘탈","悪徳メンエスオーナー":"악덕멘에스오너","ヤンヤン突け棒":"양양찌르기",
            "北の大地《個人撮影》":"북쪽의대지","東京BUZZハメクション":"도쿄BUZZ하메쿠숀","生生Cちゃんねる":"생생C짱네루",
            "リアリスト":"리어리스트","しゃんぷー博士":"샴푸박사","モモちゃん":"모모짱","マスクde本物素人":"마스크de진짜아마추어",
            "☆無限堂☆":"무한당","エログラム":"에로그램","P活女子":"P활여자","あうとどあ仙人1号":"아우도토아선인1호",
            "ギャラクシィ☆堂":"갤럭시당","アダルト研究所":"성인연구소","ワクチン":"백신","えぽす。":"에포스","ひのまるハメ撮り倶楽部Black":"히노마루POV클럽블랙",
            "BEAST☆OF☆FUCK獣のSEX‼乱交‼中出し‼etc..":"BEASTofFUCK","BEAST☆OF☆FUCK獣のSEX乱交中出しetc":"BEASTofFUCK","BEASTOFFUCK獣のSEX乱交中出しetc":"BEASTofFUCK",
            "◇たすぽ◇":"타스포","はめサムライ[進化]":"하메사무라이진화","車フェラ＋１（時々ハメ）":"차내입으로","素人ハメハメindeep":"아마추어하메하메 in deep",
            "スタジオきぞく":"스튜디오키조쿠","素人良品性活":"아마추어양품성활","ペナス":"페나스","東京濃密空間":"도쿄농밀공간",
            "ゆってぃ＠手コキ隠し撮り":"유레아주무르기Do촬","心斎橋ハードコア":"신사이바시하드코어","秘密基地":"비밀기지","ナンパ":"헌팅",
            "素人0930":"아마추어0930","美尻ちゃんねる":"아름다운엉덩이짱","肛門切痔郎":"항문절치로","はむ！チーズ！":"햄치즈",
            "ひめ学生":"히메학생","素人D1Q":"아마추어D1Q","関西素人ハメ撮り":"간사이아마추어POV","素人坂18":"아마추어언덕18",
            "中出しナックルズα":"7내4정너클a","花村玲奈24歳♡色白♡美容部員":"하나무라_레나 24세 색백미용부원","マスコン":"마스콘",
            "～絶頂快楽～":"절정쾌락","ポコイダーZERO1":"포코이더ZERO1","ピクトグラム":"픽토그램","素人Rendezvous":"아마추어Rendezvous",
            "美〇女遊記":"미소녀유기","アビス":"어비스","ジョブズ":"직업","モナッシー":"모나시","いこか":"이코카","シャーマン1号":"샤먼1호",
            "極楽インコ":"극락잉꼬","じゅうはち":"쥬하치","マロンの秘密":"마론의비밀","インディ":"인디","はめックス":"하메쿠스","下心俊介":"시모신토스케",
            "可愛い素人選抜123":"귀여운아마추어선발123","しろうと仙人":"시로토선인","梨奈の射精動画＠個人撮影":"리나의사정동영상","わいせつ映像":"외설영상",
            "エアペイ":"에어페이","裏垢＠小出のハメ撮り":"뒷면코이데의하메도리","淫行生":"음행생","神出鬼没":"신출귀몰","本物素人しか勝たん！":"진짜아마추어밖에이겼다!",
            "ギャラクシィ堂":"갤럭시당","全日本素人美女":"전일본아마추어미녀","進撃のごろうまる":"진격의고로마루","令和＠コレクション":"레이와컬렉션",
            "素人専門ちゃんねる":"아마추어전문찬네루","イチャラブヘイタ":"이차러브헤이타","一番槍":"이치반","クロスギルド":"크로스길드","美女遊記":"미녀유기",
            "ナナコ７":"나나코7","娘ガチャ":"딸가챠","くらんべり":"쿠란베리","メンヘラコリック(´。)":"멘헤라코릭","100分後にイク兄@フェラパイズリ動画主観中心":"100분후이쿠오빠@페라파이즈리동영상주관중심",
            "北の大地個人撮影":"북쪽대지개인촬영","新KUi":"새로운KUi","久美子むっちり爆乳Hカップ妻":"쿠미코무찌리폭유H컵아내","フルボッキ":"풀복",
            "フェラっ娘！":"입으로딸!","キングDジョー":"킹D조","ファッキングピエロ":"패킹광대","資本主義":"자본주의","マスオダイレクト":"마스오다이렉트",
            "ゆりちゃん調教日記":"유리짱조교일기","援ポリオヤルマーニ":"원폴리오야르마니","マイコのえっちな思い出":"마이코의놀라운추억",
            "モハメドリアリ":"모하메드리아리","まんぴ～す":"만피스","巨乳好きクリエイターMUG":"거유좋아하는제작자Mug","エロ川コナン":"에로강코난","千華繚乱”Next”":"치카요란Next",
            "個撮ｐ活女子とハメ撮り":"개인촬영p활여자와POV","deruデるking":"데루킹","マジックミー車じゃないですよ":"매직미자동차가아닙니다",
            "新章開幕セクロス先生のキメちゃん連続絶頂変態調教日記プラス":"신장개막세크로스선생님의키메짱연속절정변Tae조교일기플러스","ロジャースAPS":"로저스APS",
            "ダグラスマッサージー":"더글라스마사지","ペリカ":"펠리카","東京パパ活くらぶ":"도쿄파파활클럽","あとがない男":"노빠꾸남","とるそー":"토루소","匿名男":"익명남",
            "TOKYO美人倶楽部":"TOKYO미인클럽","まなちゃん個人撮影":"마나짱개인촬영","フェラする女":"페라하는여자","超スタミナ二郎増し増し":"슈퍼스태미나지로증가",
            "独占ちゃん":"독점짱","エレDキング":"엘레D킹","トラスト颯斗":"트러스트후두","暗黒痴女":"암흑치녀","TOKYO美女倶楽部":"TOKYO미녀클럽","お値、うちど〜が":"오아타이우치도가",
            "おかずは素人":"반찬은아마추어","ハメ撮りマスターD":"하메도리마스터D","未性年":"미未성년","©️鏡花水月":"경화수월",
            "探偵オナン":"형사오난","ぷらら":"푸라라","上手い棒♂堕女製造器":"능숙한막대기타녀제조기","オナキンTV":"오나킨TV",
            "はめサムライ進化":"하메사무라이진화","密林":"밀림","デッドボールPORN":"데드볼PORN","チェリーマン":"체리맨",
            "亀頭戦士ガンシャム":"귀두전사건샴","むげんどー":"무겐도","素人大臣":"동인대신","":"","":"","":"","":"","":"","":"","":"","":"","":"",
        
          }

    for key in dic.keys():
        txt = txt.replace(key, dic[key])
    return txt

def replaceTxt(txt):
    dic = {'\\':' ', '/':" ", ":" :" ", "*" :" ", "?" :" ","《":" ","》":" ","<" :" ", ">" :" ", "|" :" ", '"' :" ","●":" ","・":" ","○":" "," ​​":" ","⇒":" ","　":" "," ":""," ":" ","『":" ","』":" ",",":" ","→":" ","\n":" ","」":" ","「":" ","【":" ","】":" ","…":" ","★":" ","·":" ",".":" ","!":" ","‼":"","◯":" ","♡":"","×":" ","☆":" ","❤️":" ",
            "❗️":" ","※":"","〇":""," ️":"","♥️":"","♪":"","[":" ","]":" ","‘":" ","’":" ","~":" ","`":" ","⁉":" ",
            "&lt;":"","&gt;":"",
            "화장실" :"#화장sil ", "로리":"#로Li ","롤리":"#로Li ","선생님":"#선생님 ","오랄":"#페라 ","사까시":"#페라 ","구강 성교":"#페라 #이라마 ","구강성교":"#페라 #이라마 ","페라":"#페라 ","펠라":"#페라 ",
            "절륜":"#절륜 ","NTR":"#NTR ","옆집":"#옆집 ","누나":"#누나 ","난교":"#난교 ","3P":"#3P ","3p":"#3P ","아르바이트":"#아르바이트 ","알바":"#아르바이트 ","일라마치오":"#이라마 치오",
            "매직미러":"#매직미러 ","매직 미러":"#매직미러 ",
            "비서":"#비서 ","OL":"#OL ","회사":"#회사 ","사내":"#사내 ","상사":"#상사 ","부하":"#부하 ","거래처":"#거래처 ","사무실":"#사무실 ","신입":"#신입 ","사원":"#사원 ","직원":"#직원 ","스위트룸":"#스위트룸 ","스위트 룸":"#스위트룸 ",
            "학원":"#학원 ","여자 학교생":"#여고생 ","여자학교생":"#여고생 ","학교":"#학교 ","신입생":"#신입생 ","기숙사":"#기숙사 ",
            "목구멍":"#목구멍 ","이라마":"#이라마 ",
            "학생":"#학생 ","여학생":"#여학생 ","대학생":"#대학생 ","여자 대학생":"#여대생 ","여자대학생":"#여대생 ","여 #학생":"#여학생 ","대 #학생":"#대학생 ","여자 대 #학생":"#여대생 ","여자대 #학생":"#여대생 ",
            "주부":"#주부 ","유부녀":"#유Bu녀 ","아줌마":"#아줌마 #미시 ","부인":"#부인 ","가정부":"#가정부 ","가정교사":"#가정교사 ","보육교사":"#보육교사 ","교사":"#교사 ","요가":"#요가 ","오일":"#오일 "," 에스테":" #에스테틱 ","멘에스":"#에스테틱 ","마사지":"#마사지 ","정체사":"#정체사 ","안마사":"#안마사 ","정조대":"#정조대 ",
            "방뇨":"#방뇨 ","빼앗겨":"#빼앗겨 ","DQN":"#DQN ", "츤데레":"#츤데레 ","레2프":"#레2프 ","레 프":"#레2프 ","레x프":"#레2프 ","윤간":"#윤gan ","레깅스":"#레깅스 ", "차내":"#차내 ",
            "키스":"#키스 ","지근거리":"#지근거리 ","버스":"#버스 ","모델":"#모델 ",
            "근친상간":"#근chin상gan ","근친 상간":"#근chin상gan ", "근친":"#근chin상gan ",
            "아내":"#아내 ","동생":"#동생 ","여동생":"#여동생 ","여 #동생":"#여동생 ","언니":"#언니 ","의붓":"#의붓 ","아버지":"#아버지 ", "시아버지":"#시아버지 ","아빠":"#아빠 ", "어머니":"#어머니 ","엄마":"#엄마 ", "딸":"#딸 ","아들":"#아들 ","조카":"#조카 ","며느리":"#며느리 ","처남":"#처남 ",
            "7내4정":"#7내4정 ","질내사정":"#7내4정 ","질 내 사정":"#7내4정 ","질 내 사 정":"#7내4정 ","질내 사정":"#7내4정 ","질싸":"#7내4정 ", "질 사":"#7내4정 ","질 정액 샷":"#7내4정 ","나마나카다시":"생 #7내4정 ","생질컴샷":"생 #7내4정 ","질쿰샷":"#7내4정 ","질 쿰 샷":"#7내4정 ","중출":"#7내4정 ","크림피":"#7내4정 ","크림 파이":"#7내4정 ","크림파이":"#7내4정 ",
            "얼굴사정":"#얼4 ","얼굴 사정":"#얼4 ","부카케":"#부카케 #얼4 ","안면사정":"#부카케 #얼4 ","안면 사정":"#부카케 #얼4 ",
            "병원":"#병원 ","동정":"#동정 ","엉덩이":"#엉덩이 ","파이 빵":"#파이빵 ","파이빵":"#파이빵 ","치한":"#치한 ","치하철":"#지하철 ",
            " 애널":" #애널 ","항문":"#항문 #애널 ", "아날":"#애널 ","아나르":"#애널 ",
            "강제":"#강je #레2프 ","레×프":"#레2프 ", "강간":"#강gan ", "레이프":"#레2프 ",
            "커플":"#커플 ","수영복":"#수영복 ","수영장":"#수영장 ","강사":"#강사 ",
            "소꿉친구":"#소꿉친구 ","남자친구":"#남자친구 ","여자친구":"#여자친구 ","친구":"#친구 ","구속":"#구속 ",
            "치매":"#치한 ","강도":"#강도 ","사채":"#사채 ","빚":"#빚 ","협박":"#협박 ",
            "데뷔":"#데뷔 ","DEBUT":"#데뷔 ","Debut":"#데뷔 ",
            "임신":"#임신 ","헌팅":"#헌팅 ","난파":"#난파 ","남파":"#난파 ","자취방":"#자취방 ","데이트":"#데이트 ",
            "코스프레":"#코스프레 ","풍속":"#풍속 ","야근":"#야근 ","실사화":"#실사화 #만화원작 ","여대생":"#여대생 ","슬로우":"#슬로우 ","슬로피스톤":"#슬로우 피스톤","슬로섹":"#슬로우 섹","슬로 피스톤":"#슬로우 피스톤","아저씨":"#아저씨 ","쓰레기방":"#쓰레기방 ",
            "밀실":"#밀실 ","농밀":"#농밀 ","불륜":"#불륜 ","관장":"#관장 ","애인":"#애인 ","변태":"변Tae","자매":"#자매 ","가족":"#가족 ","흑인":"#흑인 ","실금":"#실금 ","유카타":"#유카타 ",
            "미니스카트":"#미니스커트 ","미니 스카트":"#미니스커트 ","미니스커트":"#미니스커트 ","미니 스커트":"#미니스커트 ","스커트":"#스커트 ","원피스":"#원피s","스타킹":"#스타킹 ","남매":"#남매 ",
            "스마타":"#스마타 #비비기 ","비비기":"#비비기 #스마타 ","코기":"#코기 ","코키":"#코기 ","허벅지":"#허벅지 ","가랑이":"#가랑이 ","사타구니":"#사타구니 ","침입":"#침입 ","이불속":"#이불속 ","이불 속":"#이불속 ","이불안":"#이불속 ","이불 안":"#이불속 ",
            "시골":"#시골 ","최음":"#최음 ","수면":"#수면 ","수면간":"#수면간 ","수면제":"#수면je ", "만취":"#만취 ","만취간":"#만취간 ",
            "최면":"#최면 ", "미약":"#미약 ","춘약":"#미약 ","도촬":"#Do촬 ","몰카":"#Mol카 ","몰래 촬영":"#Mol카 ","몰래 카메라":"#Mol카 ","몰래카메라":"#Mol카 ","몰래":"#몰래 ","미용사":"#미용사 ","미용실":"#미용실 ","미장원":"#미용실 ",
            "메이드":"#메이드 ","봉사":"#봉사 ", "이웃":"#이웃 ", "이웃집":"#이웃집 ","중년":"#중년 ","호텔":" #호텔 ","러브호텔":"러브 #호텔 ","러브호":"러브 #호텔","러브 호":"러브 #호텔 ", "부부":"#부부 ", "야외":"#야외 ","옥외":"#야외 ",
            "로션":"#로션 ","보지":"보ji","오줌":"#5줌 ", "젖꼭지":"#젖꼭ji ","교복":"#교Bok ","육변기":"#6변Gi ","변기":"#변Gi ","얼굴노출":"#얼공 ","노출":"#노출 ","거유":"#거유 ","폭유":"#폭유 ","자위":"#자wi ","오나니":"#오나니 ",
            "캠핑":"#캠핑 ","텐트":"#텐트 ","고쿤":"#고쿤 #입4 ","입내 사정":"#입4 ","과외":"#과외 ","금욕":"#금욕 ","모유":"#모유 ","고정":"#고정 ","바이브":"#바이브 ",
            "경련":"#경련 ","오르가즘":"#오르가즘 ","절정":"#절정 ","트랜스":"#트랜스 ",
            "레즈":"#레즈 ","개인 사격":"#개인촬영 ","개인 촬영":"#개인촬영 ","개 촬영":"#개인촬영 ","풍속":"#풍속 ","소프":"#소프 ","노브라":"#노브라 ","노팬티":"#노팬티 ","노 브라":"#노브라 ","노 팬티":"#노팬티 ","처녀":"#처녀 ","남편":"#남편 ","삼촌":"#삼촌 ","승무원":"#승무원 ",
            "아이돌":"#아이돌 ","감금":"#감금 ","쓰레기실":"#쓰레기방 ","동거":"#동거 ","무방비":"#무방비 ","기름":"#오일 ","JD":"#JD ","혼욕":"#혼욕 ","포티오":"#포르치오 ","포르치오":"#포르치오 ","포르티오":"#포르치오 ",
            "유출":"#Yu출 ","여고생":"#여고생 ","가출":"#가출 ","셀카":"#셀카 ","숨겨진 촬영":"#Do촬","숨겨진촬영":"#Do촬 ","목욕":"#목Yok ","사장":"#사장 ",
            "E컵":"#E컵 ","E 컵":"#E컵 ","E-컵":"#E컵 ","Ecup":"#E컵 ","E cup":"#E컵 ",
            "G컵":"#G컵 ","G 컵":"#G컵 ","G-컵":"#G컵 ","Gcup":"#G컵 ","G cup":"#G컵 ",
            "F컵":"#F컵 ","F 컵":"#F컵 ","F-컵":"#F컵 ","Fcup":"#F컵 ","F cup":"#F컵 ",
            "H컵":"#H컵 ","H 컵":"#H컵 ","H-컵":"#H컵 ","Hcup":"#H컵 ","H cup":"#H컵 ",
            "I컵":"#I컵 ","I 컵":"#I컵 ","I-컵":"#I컵 ","Icup":"#I컵 ","I cup":"#I컵 ",
            "J컵":"#J컵 ","J 컵":"#J컵 ","J-컵":"#J컵 ","Jcup":"#J컵 ","J cup":"#J컵 ",
            "온천":"#온천 ","남탕":"#남탕 ",
            "간호":"#간호 ","간호사":"#간호사 ","#간호 사":"#간호사 ",
            "유혹":"#유혹 ","상담":"#상담 ","모니터링":"#모니터링 ","건방진":"#건방진 ","성노예":"#성노예 ","노예":"#노예 ","선배":"#선배 ",
            "나카다시":"#나카다시 ","바니":"#바니걸 ","바니걸":"#바니걸 ","여관":"#여관 ","멘션":"#멘션 ","편의점":"#편의점 ","점원":"#점원 ","점장":"#점장 ","전화":"#전화 ",
            "비키니":"#비키니 ","무수정":"#무수정 ","동창회":"#동창회 ","야구부":"#야구부 ","테니스부":"#테니스부 ","축구부":"#축구부 ","배구부":"#배구부 ","카우걸":"#카우걸 #기승위 ","기승위":"#기승위 #카우걸 ",
            "그라비아":"#그라비아 ","동아리":"#동아리 ","조카":"#조카 ","세후레":"#세후레 ","아첨약":"#미약 ","능욕":"#능Yok ","무단취소":"#무단취소 ","무단 취소":"#무단취소 ",
            "성욕몬스터":"#성욕몬스터 ","성욕 몬스터":"#성욕몬스터 ","동창":"#동창 ","역전":"#역전 ","출장":"#출장 ","경멸":"#경멸 ","같은방":"#같은방 ","같은 방":"#같은방 ","부재중":"#부재중 ","선술집":"#선술집 ","아나운서":"#아나운서 ",
            "고기 오나호":"#6변Gi","도 M":"#도M ","드 M":"#도M ","마조":"#마조 ","조교":"#조교 ","조련":"#조교 ","판치라":"#판치라 ","치녀":"#치녀 ","세뇌":"#세뇌 ","동료":"#동료 ","여행":"#여행 ","싫어하는":"#싫어하는 ","파이즈리":"#파이즈리 ",
            "슬렌더":"#슬렌더 ","욕구불만":"욕9 불만","욕구 불만":"욕9 불만","변소":"#변so ","커닐링구스":"#커닐링구스 ","2구멍":"#2구멍 ","2 구멍":"#2구멍 ",
            "배빵":"#배빵 ","음뇨":"#음뇨 ",
            "합숙":"#합숙 ","트레이닝":"#트레이닝 ","자지":"자ji ","도서관":"#도서관 ",
            "네카페":"#네카페","넷카페":"#네카페","V#OL":"VOL","전철":"#전철 ","주차장":"#주차장 ","자동차":"#자동차 ",

            "# #":"#","##":"#","   ":" ","  ":" ","#_":"#"}

    for key in dic.keys():
        txt = txt.replace(key, dic[key])

    return txt
  
import googletrans
def gtranslate():
    translator = googletrans.Translator()
    
    for filename in os.listdir(file_path): #현재 위치 (.) 의 파일을 모두 가져온다
        name, ext = os.path.splitext(filename)
        print("파일명 : " + name + ", 확장자 : " + ext) 

        sname = name.split(" ")

        if sname[0].upper() == "FC2-PPV":
            named = " ".join(sname[2:]) #품번을 제외한 제목
            pum = " ".join(sname[:2])
        else:
            named = " ".join(sname[1:]) #품번을 제외한 제목
            pum = sname[0]

        if named != None : #제목이 없는지 확인
            newName = translator.translate(named, dest='ko') #번역
            newName = replaceTxt(newName.text) #수정
            newName = pum +" " + newName + ext
        else :
            newName = pum + ext

        print("새파일명 : " + newName)

        file_oldname = os.path.join(file_path,filename)
        file_newname = os.path.join(file_path,newName)
        os.renames(file_oldname, file_newname) 
        print(" 파일명 수정 완료!\n\n")

import os
import sys
import urllib.request
import json
from google.cloud import translate_v2 as translate

def papago(txt):
    try:
        client_id = "CDWEGWm1AGvUFyq3Sw1J" # 개발자센터에서 발급받은 Client ID 값
        client_secret = "9uXJT9Qo6i" # 개발자센터에서 발급받은 Client Secret 값
        encText = urllib.parse.quote(txt)

        try:
            translator = googletrans.Translator()
            source = translator.detect(txt).lang
        except Exception as e:
            print("papago detect lang : " )
            # print(e)
            print(traceback.format_exc())
            source = "en"

        data = f"source="+source+"&target=ko&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        try:
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        except Exception as e:
            print("papago request : " )
            # print(e)
            print(traceback.format_exc())
            return ""
        
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read().decode('utf-8')
            result = json.loads(response_body)
            # print('번역결과 : ',result['message']['result']['translatedText'])
            return result['message']['result']['translatedText']
        else:
            print("Error Code:" + rescode)
            return ""
    except Exception as e:
        print("papago : " )
        # print(e)
        print(traceback.format_exc())
        return ""

def google_cloud_trans(txt):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'cedar-gearbox-355116-cdb9d479a26d.json'
    try:
        client = translate.Client()
        result = client.translate(txt, target_language='ko')
        return result['translatedText']
    except Exception as e:
        print("google_cloud_trans : " )
        # print(e)
        print(traceback.format_exc())
        return ""

def google_cloud_trans_tgl(txt, tgl):
    ''' tgl : ko, ja, en, ... '''
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'cedar-gearbox-355116-cdb9d479a26d.json'
    try:
        client = translate.Client()
        result = client.translate(txt, target_language=tgl)
        return result['translatedText']
    except Exception as e:
        print("google_cloud_trans_tgl : ")
        # print(e)
        print(traceback.format_exc())
        return ""

def google_trans_free(txt):
    translator = googletrans.Translator()
    try:
        return translator.translate(txt, src='auto',dest='ko').text
    except Exception as e:
        print("google_trans_free : ")
        print(e)
        print(traceback.format_exc())
        return ""

def translater(txt):
    txt = replaceTxt(txt)
    # result = google_cloud_trans(txt)
    # if result == 0 : 
    #     print("구글 클라우드 번역 실패")
    result = papago(txt)
    if result == "" :
        print("파파고 번역 실패")
        result = google_trans_free(txt)
    if result == "": result = txt
    # result = txt
    return result


avdbs = "https://www.avdbs.com/"
def get_pumInfo(pumnum):
    
    url = f'https://www.avdbs.com/menu/search.php?kwd={pumnum}&seq=214581737&tab=2'
    # driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(3) 

    source = driver.page_source
    soup = bs(source, 'html.parser')

    #로그인
    chk = soup.select('#contants > ul.page_tab > li.tab_2.on > a > span')[0].get_text()
    # print(chk)
    if chk == '(-1)':
        login = soup.select('#srch-bar > div.hdr_menu > ul > li:nth-child(1) > a')[0]['href']
        login = avdbs + login
        # print(login)
        driver.get(login)
        user_id = 'tjrwhd9075'
        user_pwd = 'ysj7953!'
        driver.find_element(By.ID,'member_uid').send_keys(user_id)
        driver.find_element(By.ID,'member_pwd').send_keys(user_pwd)
        driver.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/button[1]').click()

        time.sleep(3)
        
        driver.get(url)
        time.sleep(3)
        source = driver.page_source
        soup = bs(source, 'html.parser')

    time.sleep(5)

    try : 
        pum = soup.select("#contants > ul.container > li.page.page_2 > div > ul > li > div > div.dscr > p.title > a.lnk_dvd_dtl")[0]
        # print(pum)         
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        pum = soup.select("#contants > ul.container > li.page.page_2 > div > ul > li:nth-child(1) > div > div.dscr > p.title > a.lnk_dvd_dtl")[0]
        
        # print(pum) 


    pumlink = avdbs + pum['href']
    print(pumlink)
    pumtitle = replaceTxt(pum.get_text())
    print(pumtitle)

    url = pumlink
    driver.get(url)
    time.sleep(3)

    source = driver.page_source
    soup = bs(source, 'html.parser')

    try : 
        pumactor = soup.select("#ranking_tab1 > div.profile_view_top > div.path_row > ul > li:nth-child(2) > h1 > a > span:nth-child(2) > span:nth-child(3)")[0].get_text()
        print(pumactor)
        pumactor =  " [#"+pumactor+"] "
    except Exception as e:
        print(e)
        print("배우 찾기 실패")
        pumactor = " #UnknownActor "

    try :
        pumdate = soup.select("#ranking_tab1 > div.profile_view_top > div.profile_view_inner > div.profile_picture > div > div.profile_detail > p:nth-child(1)")[0].get_text()
        print(pumdate.split(" ")[1])
        pumdate = " ("+pumdate.split(" ")[1]+")"
    except Exception as e:
        print(e)
        print("날짜 찾기 실패")
        pumdate = ""

    pumname = pumactor +pumtitle + pumdate
    # pumname = " ["+pumactor+"] "+" ("+pumdate.split(" ")[1]+")"

    return pumname

from selenium.webdriver.common.keys import Keys
def get_pumInfo_fc2_from_fc2hub(pumnum):
    
    url = f'https://fc2hub.com/'
    # driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,'#content > div > div > div > div > div > form > div > input').send_keys(pumnum)
    driver.find_element(By.CSS_SELECTOR,'#content > div > div > div > div > div > form > div > input').send_keys(Keys.ENTER)
    time.sleep(3)

    source = driver.page_source
    soup = bs(source, 'html.parser')
    try :
        try:
            pumtitle = soup.select_one('h1.card-text.fc2-title').get_text()
            # print(pumtitle)
            print("제목 : "+pumtitle)
            title = translater(pumtitle) #번역
            title = " " + replaceTxt(title) #수정
            print("수정 제목 : " + title)
        except Exception as e :
            print(e)
            print("제목 없음")
            title = " #noneTitle"
        try:
            pumwriter = soup.select_one('div.col-8').next_element.get_text()
            # print(pumwriter)
            pumwriter = " #"+ replaceTxt(pumwriter).replace("   ","_").replace("  ","_").replace(" ","_").replace("#","").replace("-","")
            print("제작자 : "+pumwriter)
        except Exception as e :
            print(e)
            print("제작자 없음")
            pumwriter = " #noneWriter"

    except Exception as e :
            print(e)
            print("검색결과 없음")
            return ""

    pumname = pumwriter + title
    return pumname

def get_pumInfo_fc2_test(pumnum, where=None):
    ''' 
    if where is "rssbot":
        return writer1, actor1, createDate
    else: 
        return pumname = writer1 + actor1 + title + createDate
    '''
    
    url = f'https://db.msin.jp/'
    # driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, 'body > div.modalouter > div > a.close_modal').click() # 18세 확인창
    try:
        driver.find_element(By.CSS_SELECTOR, 'body > ins > div > div:nth-child(1) > span > svg > path').click() #광고창 닫기
    except Exception as e:
        print(e)
        print("광고창 없음")

    time.sleep(3)
    driver.find_element(By.ID, 'mmbtn').click()
    time.sleep(1)
    driver.find_element(By.ID, 'mmbtn').click()
    driver.find_element(By.ID, 'mbox').send_keys(pumnum)
    driver.find_element(By.ID, 'mbox').send_keys(Keys.ENTER)
    time.sleep(3)

    source = driver.page_source
    soup = bs(source, 'html.parser')

    try:
        title = soup.select('#content > div.movie_info_ditail > div.mv_title')[0].get_text()
        print("제목 : "+title)
        
        if where is None:
            title = translater(title) #번역
            title = replaceTxt(title) #수정
            print("수정 제목 : " + title)

    except Exception as e :
        print(e)
        print("제목 없음 ? 검색결과 없음")
        title = "#UnknownTitle"

    try:
        actor = soup.select('#content > div.movie_info_ditail > div.mv_artist')[0].get_text()
        actor = actor.replace("（FC2動画）","")
        print("배우 : "+actor)

        actor1 = translater(actor) #번역
        actor1 = "#"+replaceTxt(actor1).replace(" ","").replace("#","").replace("-","") #수정

        # actor1 = actor1 + " " + actor
        print("수정 배우 :" + actor1)

    except Exception as e :
        print(e)
        print("배우명 없음")
        actor1 = "#UnknownActor"

    try:
        createDate = soup.select('#content > div.movie_info_ditail > div.mv_createDate')[0].get_text()
        createDate = "("+ createDate +")"
        print("날짜 : "+createDate)
    except Exception as e :
        print(e)
        print("날짜 없음")
        createDate = ""
    try :
        writer = soup.select('#content > div.movie_info_ditail > div.mv_writer')[0].get_text()
        print("제작자 : "+writer)
        writer1 = replaceTxt(writer).replace("   ","").replace("  ","").replace(" ","").replace("#","").replace("-","") #수정
        writer1 = "#"+replaceWriterTxt(writer1)
        print("수정 제작자 :" + writer1)

    except Exception as e :
        print(e)
        print("제작자 없음")
        writer1 = "#UnknownWriter"

    if where is None:
        pumname = " "+writer1 + " "+actor1 + " "+title + " "+createDate 
        return pumname
    elif where == "rssbot":
        return writer1, actor1, createDate

def get_pumInfo_fc2(pumnum):
    
    url = f'https://db.msin.jp/jp.search/movie?str={pumnum}'
    # driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, 'body > div.modalouter > div > a.close_modal').click()
    # time.sleep(5)

    source = driver.page_source
    soup = bs(source, 'html.parser')

    try :
        pum = soup.select("#content > a")[0]
        pumlink = pum['href']
        print(pumlink)
    except Exception as e :
            print(e)
            print("검색결과 없음")
            return ""

    url = pumlink
    driver.get(url)
    # time.sleep(5)

    source = driver.page_source
    soup = bs(source, 'html.parser')

    # translator = googletrans.Translator()

    try:
        title = soup.select('#content > div.movie_info_ditail > div.mv_title')[0].get_text()
        print("제목 : "+title)
        
        title = translater(title) #번역
        title = " " + replaceTxt(title) #수정
        print("수정 제목 : " + title)

    except Exception as e :
        print(e)
        print("제목 없음 ? 검색결과 없음")
        title =""

    try:
        actor = soup.select('#content > div.movie_info_ditail > div.mv_artist')[0].get_text()
        actor = actor.replace("（FC2動画）","")
        print("배우 : "+actor)

        actor1 = translater(actor) #번역
        actor1 = " #"+replaceTxt(actor1).replace(" ","_").replace("#","").replace("-","") #수정

        actor1 = actor1 + " " + actor
        print("수정 배우 :" + actor1)

    except Exception as e :
        print(e)
        print("배우명 없음")
        actor1 = ""

    try:
        createDate = soup.select('#content > div.movie_info_ditail > div.mv_createDate')[0].get_text()
        createDate = " ("+ createDate +")"
        print("날짜 : "+createDate)
    except Exception as e :
        print(e)
        print("날짜 없음")
        createDate = ""
    try :
        writer = soup.select('#content > div.movie_info_ditail > div.mv_writer')[0].get_text()
        print("제작자 : "+writer)

        writer1 = translater(writer) #번역
        writer1 = " #"+replaceTxt(writer1).replace("   ","_").replace("  ","_").replace(" ","_").replace("#","").replace("-","") #수정
        writer1 = writer1 + " " + writer
        
        print("수정 제작자 :" + writer1)

    except Exception as e :
        print(e)
        print("제작자 없음")
        writer1 = ""

    pumname = writer1 + actor1 + title + createDate 
    return pumname

def get_pumInfo_ama(pumnum):
    
    url = 'https://db.msin.jp/'
    # driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    # time.sleep(5)

    inputBox = driver.find_element(By.ID,"mbox")
    inputBox.send_keys(pumnum)
    inputBox.submit()

    source = driver.page_source
    soup = bs(source, 'html.parser')
    
    try:
        title = soup.select('#content > div:nth-child(3) > div.mv_title')[0].get_text()
        print("제목 : " + title)
        
        # translator = googletrans.Translator()
        title = translater(title) #번역
        title = " " + replaceTxt(title) #수정
        print("수정 제목 : " + title)
    except Exception as e:
        print(e)
        print("제목 없음 ? 검색결과 없음")
        title =""

    try:
        createDate = soup.select('#content > div:nth-child(3) > div.mv_createDate')[0].get_text()
        createDate = " ("+ createDate +")"
        print("날짜 : " + createDate)
    except Exception as e:
        print(e)
        print("날짜 없음")
        createDate =""


    try:
        actor = soup.select('#content > div:nth-child(3) > div.mv_artist > span > a')[0].get_text()
        print("배우 :" + actor)
        actor = translater(actor) #번역
        actor = " #"+replaceTxt(actor).replace(" ","_").replace("#","").replace("-","") #수정
        print("수정 배우 :" + actor)
    except Exception as e :
        print(e)
        print("배우명 없음")
        actor =""

    newName = actor + title +  createDate
    return newName

def get_pumInfo_ama_from_javdb(pumnum):
    
    url = f'https://javdb.com/search?q={pumnum}&f=all'
    # driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    source = driver.page_source
    soup = bs(source, 'html.parser')

    try :
        pum1 = soup.select('body > section > div > div.movie-list.h.cols-4.vcols-8 > div:nth-child(1)')[0]
        pumtitle1 = pum1.a.select_one('div.video-title').get_text()
        print('pumtitle1 : ' + pumtitle1)
    except :
        # if pumtitle1.find(pumnum.split("-")[-1]) == -1 : # 품번 검색 실패 -> 그냥 종료
        return ""
    pumlink = "https://javdb.com" + pum1.a['href']
    print('pumlink : ' + pumlink)

    driver.get(pumlink)
    source = driver.page_source
    soup = bs(source, 'html.parser')

    puminforms = soup.select('body > section > div > div.video-detail > div.video-meta-panel > div > div:nth-child(2) > nav > div')

    pumdate = ""
    pumactor = ""
    for puminform in puminforms :
        txt = puminform.get_text().replace("\n","").replace(" ","").replace("&nbsp;","")
        # print('puminform : ' + txt)

        
        if txt.find('日期') != -1 : #날짜
            pumdate = " ("+txt.split(":")[-1]+")"
            print('pumdate : ' + pumdate)
        
        if txt.find('演員') != -1 : #배우
            if txt.find('♀') != -1 : #여배우가 있으면 
                pumactor = txt.split(":")[1].split("♀")[0]
                pumactor = " [#"+ translater(pumactor) +"] "
                print('pumactor : ' + pumactor)
        pumtitle1 = " "+replaceTxt(translater(pumtitle1))
    
    newName = str(pumactor) + str(pumtitle1) +  str(pumdate.replace(" ",""))
    return newName



from pathlib import Path
import os
file_path = "I:\\가마우지\\0. 파일명 정리완료"

def rename_file():
    for filename in os.listdir(file_path): #현재 위치 (.) 의 파일을 모두 가져온다
        name, ext = os.path .splitext(filename)
        print("파일명 : " + name + ", 확장자 : " + ext) 

        pumnum = name.split(" ")[0]  # " " 단위로 파일명 분리->품번 추출
        print("품번 : " + pumnum)
        if pumnum.upper() != "FC2-PPV" and pumnum.upper() != "FC2PPV": #fc2 파일 건너뛰기
            try:
                if len(pumnum.split("-")) < 3 :  #ABC 나눠진 파일 확인
                    pumname = get_pumInfo(pumnum)
                else :
                    pumname = get_pumInfo(pumnum[:-2])
                print("작품 제목 : "+pumname)

            except Exception as e:  #아마추어 품번일때
                print(e)
                print("ama : " + pumnum)
                try :
                    if len(pumnum.split("-")) < 3 :  #ABC 나눠진 파일 확인
                        pumname = get_pumInfo_ama_from_javdb(pumnum)
                    else :
                        pumname = get_pumInfo_ama_from_javdb(pumnum[:-2])
                except Exception as e: #검색안되면 스킵
                    print(e)
                    print("fail : " + pumnum)
                    continue
            #파일명 변경
            new_filename = pumnum + pumname + ext
            print("새파일명 : " + new_filename)
                
        elif pumnum.upper() == "FC2-PPV" or pumnum.upper() == "FC2PPV" : #fc2 파일일때
            pumnum = name.split(" ")[1]
            if pumnum[-2] == '_' or pumnum[-2] == '-': # -n 또는 _n 로 나눠진 파일일때
                print("품번 : " + pumnum[:-2])
                pumname = get_pumInfo_fc2_test(pumnum[:-2])
            else:
                print("품번 : " +pumnum)
                pumname = get_pumInfo_fc2_test(pumnum)

            #파일명 변경
            new_filename = "FC2-PPV "+ pumnum + pumname + ext
            print("새파일명 : " + new_filename)
        
        # new_filename=replaceTxt(new_filename)
        # print("수정된 새파일명 : " + new_filename)
        if len(new_filename) > 250 :
            new_filename = new_filename[:250] + ext

        file_oldname = os.path.join(file_path,filename)
        file_newname = os.path.join(file_path,new_filename)
        os.renames(file_oldname, file_newname) 
        print(pumnum + " 파일명 수정 완료!\n\n")    

def get_pumnum_rel(pumnum):
    
    # driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # 릴 확인
    sagalink = f'https://javsaga.ninja/?s={pumnum}'
    driver.get(sagalink)
    # time.sleep(60)
    time.sleep(random.uniform(7,10))
    source = driver.page_source
    soup = bs(source, 'html.parser')

    rst = soup.select('body > div.main > div > div > div.archive-title > h1')[0].get_text()
    # time.sleep(60)
    
    if rst[-3:] == "(0)":
        rel = "X"
    else :
        rel = "O\n" + sagalink
    return rel

def get_rel_chk_javgo(pumnum):
    '''
    찾을 정보 : 날짜, 배우, 제목
    '''
    
    url = f'https://javgo.to/ko/search?keyword={pumnum}'
    # driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(random.uniform(1,5))

    source = driver.page_source
    soup = bs(source, 'html.parser')

    pums = soup.select('#body > div > aside.main > section > div.box-item-list > div')

    for pum in pums:
        if pum.select_one('div.code').get_text().find(pumnum) != -1: #품번이 맞으면
            title = pum.select_one('div.title').get_text()
            title = title.replace(" ","")
            print("title : " + title)
            actor = pum.select_one('div.actress').get_text()
            actor = actor.replace("\n",",").replace(",,,","").replace(",,","")
            if actor == "...":
                actor = 'unknown'
            print("actor : " + actor)
            date = pum.select_one('div.detail-item').next_element.next_element.get_text()
            date = date.replace(" ","").split("\n")[1]
            print("date : " + date)

            return date + "^^" + actor + "^^" + title
    return 0

def get_all_pumnum(writer):
    
    
    url = f'https://db.msin.jp/page/writer?name={writer}'
    # driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    print("url 로딩", end= " / ")
    driver.get(url)
    time.sleep(random.uniform(1,5))

    print("enter 클릭", end= " / ")
    driver.find_element(By.CSS_SELECTOR, 'body > div.modalouter > div > a.close_modal').click()
    print("설정 클릭", end= " / ")
    driver.find_element(By.CSS_SELECTOR, '#cbtn').click()
    # driver.find_element(By.CSS_SELECTOR, 'body > ins > div > div:nth-child(1) > span > svg > path').click()

    # time.sleep(60)
    source = driver.page_source
    soup = bs(source, 'html.parser')
    iframe = soup.select('body > div.lity.lity-opened.lity-iframe > div > div > div > div > iframe')[0]['src']
    print("iframe (설정창)", end= " / ")
    # print(iframe)
    driver.get("https://db.msin.jp"+iframe)
    time.sleep(random.uniform(1,5))
    
    print("설정 상세 클릭", end= " / ")
    driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(15) > label:nth-child(2)').click()
    driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(15) > label:nth-child(4)').click()
    driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(15) > label:nth-child(6)').click()
    driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(15) > label:nth-child(8)').click()
    driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(15) > label:nth-child(10)').click()
    #//////////////////////////////////////////////

    print("url 다시 로딩", end= " / ")
    driver.get(url)
    time.sleep(random.uniform(1,5))
    source = driver.page_source
    soup = bs(source, 'html.parser')
    pgs = soup.select('#content > div.movie_view > div.pagination > div > a')

    pglist = []
    for pg in pgs :
        pglist.append(pg.get_text())

    print(len(pglist))
    if pglist == [] :
        pglist = '1'

    for i in range(1,1+int(pglist[-1])):
        pglink = f'https://db.msin.jp/page/writer?name={writer}&page={i}'
        driver.get(pglink)
        time.sleep(random.uniform(1,5))
        source = driver.page_source
        soup = bs(source, 'html.parser')

        pums = soup.select('#content > div.movie_view_wrap > div > div')
        for pum in pums:
            pumnum = pum.select_one('div.movie_pn').get_text().split("-")[2]
            pumdate = pum.select_one('div.movie_create').get_text()
            pumtitle = pum.select_one('div.movie_title').get_text()
            pumactor = pum.select_one('div.movie_artist').get_text().replace("（FC2動画）","")
            if pumactor == "":
                pumactor = "unknown"
            

            # 릴 확인
            sagalink = f'https://javsaga.ninja/?s={pumnum}'
            driver.get(sagalink)
            # time.sleep(60)
            time.sleep(random.uniform(5,7))
            source = driver.page_source
            soup = bs(source, 'html.parser')

            rst = soup.select('body > div.main > div > div > div.archive-title > h1')[0].get_text()
            # time.sleep(60)
            
            if rst[-3:] == "(0)": #없음
                rel = "X"
                # tmp = get_rel_chk_javgo(pumnum)
                # if tmp == 0:  #진짜없음
                #     rel = "X"
                #     newtxt = pumnum +" "+ writer +" "+ pumdate + " " + pumactor + " " + pumtitle.replace(" ","") + " " + rel
                # else: #찾아보니 있음
                #     rel = "O"
                #     tmp = tmp.split("^^")
                #     newtxt = pumnum +" "+ writer +" "+ tmp[0] + " " + tmp[1] + " " + tmp[2] + " " + rel + " go"
            else : #있음
                rel = "O"
            newtxt = pumnum +" "+ writer +" "+ pumdate + " " + pumactor + " " + pumtitle.replace(" ","") + " " + rel
            
            print(newtxt)

            txtfile = 'fc2.txt'
            # 기존 데이터 불러오기
            with open(txtfile, 'rt', encoding = 'UTF-8') as f:
                oldtxt = f.read().splitlines() 

            # 새로운 데이터 입력
            if newtxt not in oldtxt: #중복검사
                with open(txtfile, 'a', encoding = 'UTF-8') as f:          
                    f.write(newtxt + "\n")
    return 0

def get_all_pumnum_fc2hub(link):
    ''' link : All Videos By '판매자' 여기 링크 가져올것 '''
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options)

    pgnum=1
    while 1:
        url = link+'?page='+str(pgnum)
        pgnum += 1
        
        driver.get(url)
        time.sleep(random.uniform(1,5))
        
        source = driver.page_source
        soup = bs(source, 'html.parser')

        if pgnum == 2: writer = soup.select('#content > div > div > div.col-sm-12.col-md-12.col-xl-10 > div:nth-child(2) > div > div > div.col-md-8 > div > h5')[0].get_text()

        try:
            pums = soup.select('#content > div > div > div.col-sm-12.col-md-12.col-xl-10 > div:nth-child(3) > div')
            # print(pums)
            if pums == [] :
                break
        except:
            break

        for pum in pums:
            pumnum = pum.select_one('h4.card-title').get_text().split("-")[2]
            print(pumnum)
            pumtitle = pum.select_one('p.card-text').get_text()
            print(pumtitle)
            pumthumb = pum.select_one('img.card-img-top')['src']
            print(pumthumb)
        
            # 릴 확인
            sagalink = f'https://javsaga.ninja/?s={pumnum}'
            driver.get(sagalink)
            # time.sleep(60)
            time.sleep(random.uniform(7,10))
            source = driver.page_source
            soup = bs(source, 'html.parser')

            rst = soup.select('body > div.main > div > div > div.archive-title > h1')[0].get_text()
            # time.sleep(60)
            
            if rst[-3:] == "(0)": #없음
                # rel = "X"
                rel = "X"
            else : #있음
                rel = "O"
            
            newtxt = pumnum + "!@#" + writer +"!@#"+ pumtitle + "!@#" + rel
            
            print(newtxt)

            txtfile = 'fc2.txt'
            # 기존 데이터 불러오기
            with open(txtfile, 'rt', encoding = 'UTF-8') as f:
                oldtxt = f.read().splitlines() 

            # 새로운 데이터 입력
            if newtxt not in oldtxt: #중복검사
                with open(txtfile, 'a', encoding = 'UTF-8') as f:          
                    f.write(newtxt + "\n")
    

def get_all_pumnum_uc(writer):
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    url = f'https://db.msin.jp/page/writer?name={writer}'
    driver = uc.Chrome(options=options)
    driver.get(url)
    time.sleep(random.uniform(1,5))
    driver.find_element(By.CSS_SELECTOR, 'body > div.modalouter > div > a.close_modal').click()
    driver.find_element(By.CSS_SELECTOR, '#cbtn').click()
    driver.find_element(By.CSS_SELECTOR, 'body > ins > div > div:nth-child(1) > span > svg > path').click()


    source = driver.page_source
    soup = bs(source, 'html.parser')

    iframe = soup.select('body > div.lity.lity-opened.lity-iframe > div > div > div > div > iframe')[0]['src']
    print(iframe)
    driver.get(iframe)
    time.sleep(random.uniform(1,5))
    
    driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(15) > label:nth-child(2)').click()
    driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(15) > label:nth-child(4)').click()
    driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(15) > label:nth-child(6)').click()
    driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(15) > label:nth-child(8)').click()
    driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(15) > label:nth-child(10)').click()
    #//////////////////////////////////////////////

    driver.get(url)
    time.sleep(random.uniform(1,5))
    source = driver.page_source
    soup = bs(source, 'html.parser')
    pgs = soup.select('#content > div.movie_view > div.pagination > div > a')

    pglist = []
    for pg in pgs :
        pglist.append(pg.get_text())

    print(len(pglist))
    if pglist == [] :
        pglist = '1'

    # for i in range(int(pglist[-1]), 0, -1): #거꾸로
    for i in range(1,1+int(pglist[-1])):
        pglink = f'https://db.msin.jp/page/writer?name={writer}&page={i}'
        driver.get(pglink)
        time.sleep(random.uniform(1,5))
        source = driver.page_source
        soup = bs(source, 'html.parser')

        pums = soup.select('#content > div.movie_view_wrap > div > div')
        for pum in pums:
            pumnum = pum.select_one('div.movie_pn').get_text().split("-")[2]
            pumdate = pum.select_one('div.movie_create').get_text()
            pumtitle = pum.select_one('div.movie_title').get_text()
            pumactor = pum.select_one('div.movie_artist').get_text().replace("（FC2動画）","")
            if pumactor == "":
                pumactor = "unknown"
            

            # 릴 확인
            sagalink = f'https://javsaga.ninja/?s={pumnum}'
            driver.get(sagalink)
            # time.sleep(60)
            time.sleep(random.uniform(7,10))
            source = driver.page_source
            soup = bs(source, 'html.parser')

            rst = soup.select('body > div.main > div > div > div.archive-title > h1')[0].get_text()
            # time.sleep(60)
            
            if rst[-3:] == "(0)": #없음
                rel = "X"
                # tmp = get_rel_chk_javgo(pumnum)
                # if tmp == 0:  #진짜없음
                #     rel = "X"
                #     newtxt = pumnum +" "+ writer +" "+ pumdate + " " + pumactor + " " + pumtitle.replace(" ","") + " " + rel
                # else: #찾아보니 있음
                #     rel = "O"
                #     tmp = tmp.split("^^")
                #     newtxt = pumnum +" "+ writer +" "+ tmp[0] + " " + tmp[1] + " " + tmp[2] + " " + rel + " go"
            else : #있음
                rel = "O"
            newtxt = pumnum +" "+ writer +" "+ pumdate + " " + pumactor + " " + pumtitle.replace(" ","") + " " + rel
            
            print(newtxt)

            txtfile = 'fc2.txt'
            # 기존 데이터 불러오기
            with open(txtfile, 'rt', encoding = 'UTF-8') as f:
                oldtxt = f.read().splitlines() 

            # 새로운 데이터 입력
            if newtxt not in oldtxt: #중복검사
                with open(txtfile, 'a', encoding = 'UTF-8') as f:          
                    f.write(newtxt + "\n")
    return 0

def get_streaming_url_from_evojav(pumnum):
    
    evolink = f'https://evojav.pro/en/?s={pumnum}'
    # driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(evolink)
    time.sleep(random.uniform(5,6))   # 잠깐 휴식
    source = driver.page_source
    soup = bs(source, 'html.parser')

    rst = soup.select('body > div.main > div > div > div.archive-title > h1')[0].get_text()  #검색 결과가 있는지 확인

    if rst[-3:] == "(0)": return "검색결과없음"  # 종료

    pums = soup.select('body > div.main > div > div > div.posts.clearfix > div')
    # print(pums)
    
    for pum in pums:
        # print(pum)
        pumtitle = pum.a['title']
        print(pumtitle)

        if len(pums)==1 and "Chinese Subtitles" in pumtitle : continue  #중국어 자막은 건너띄기, 중국어 자막버전 밖에 없으면 일단 ㄱ
        pumlink = pum.a['href'] 
        pumthumb = pum.select_one('img.thumb')['src']
        print(pumlink)
        print(pumthumb)

        # driver = webdriver.Chrome(chrome_path, options=chrome_options)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(pumlink)
        time.sleep(random.uniform(5,6))   # 잠깐 휴식
        source = driver.page_source
        soup = bs(source, 'html.parser')

        txt = [pumtitle, pumlink, pumthumb]

        # 파트 없을때
        btns = soup.select('body > div.main > div:nth-child(1) > div > div.left > div.btns > div > a')
        part = False
        
        # 파트 있을때
        if btns[0].get_text() == "1": 
            btns = soup.select('body > div.main > div > div.video-wrap > div.left > div.btns.active > div:nth-child(2) > div.cd-server.active > a')
            # print(btns[0].get_text())
            parts = soup.select('body > div.main > div > div.video-wrap > div.left > div.btns.active > div:nth-child(1) > a')
            # print(parts[0].get_text())
            part = True

        for i,btn in enumerate(btns):
            # print(btn.get_text().lower())
            if btn.get_text().lower() == "st" or btn.get_text().lower() == 'streamtape':
                if part is True :
                    for j,part in enumerate(parts) :
                        # print(i, j)
                        #파트 클릭
                        time.sleep(1) 
                        driver.find_element(By.CSS_SELECTOR,f"body > div.main > div > div.video-wrap > div.left > div.btns.active > div:nth-child(1) > a:nth-child({2+j})").click()
                        time.sleep(1)                 
                        #서버 클릭
                        driver.find_element(By.CSS_SELECTOR,f"body > div.main > div > div.video-wrap > div.left > div.btns.active > div:nth-child(2) > div.cd-server.active > a:nth-child({i+1})").click()
                        time.sleep(3)  

                        driver.switch_to.frame(0)
                        driver.switch_to.frame(0)
                        source = driver.page_source
                        soup = bs(source, 'html.parser')

                        streamlink = soup.select_one('div.plyr__video-wrapper').video['src']
                        streamthumb = soup.select_one('div.plyr__video-wrapper').video['poster']
                        print(streamlink)
                        print(streamthumb)
                        txt.append(streamlink)
                        txt.append(streamthumb)
                        driver.switch_to.default_content()
                        
                    driver.quit()
                    
                    # print(txt)
                    return txt

                else :
                    driver.find_element(By.CSS_SELECTOR,f"body > div.main > div > div.video-wrap > div.left > div.btns > div > a:nth-child({i+2})").click()
                    time.sleep(3)

                    driver.switch_to.frame(0)
                    driver.switch_to.frame(0)
                    source = driver.page_source
                    soup = bs(source, 'html.parser')

                    streamlink = soup.select_one('div.plyr__video-wrapper').video['src']
                    streamthumb = soup.select_one('div.plyr__video-wrapper').video['poster']
                    print(streamlink)
                    print(streamthumb)

                    txt.append(streamlink)
                    txt.append(streamthumb)
                    print(txt)
                    
                    driver.quit()
                    return txt

import re
import pandas as pd
from datetime import datetime, timedelta

def get_popular(period):
    '''
    period = day, week, month
    '''
    

    pages = ['1','2','3']

    # pumdf = pd.DataFrame(columns=['period','views','pumnum','pumlink','rank','pumthumb','pumtitle','date'])

    pumdf = pd.read_csv(f"av_list_{period}.csv",header=0, index_col=0)
    pumdf['rank'] = pumdf.index  # 이전 인덱스는 랭크로 이동
    pumdf = pumdf.astype({'rank':'int'})

    # print("저장되어있는 데이터")
    # print(pumdf)

    # supjav
    for page in pages:
        # driver = webdriver.Chrome(chrome_path, options=chrome_options)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        print('\n supjav ' + page)
        suplink = f'https://supjav.com/popular/page/{page}?sort={period}'
        driver.get(suplink)
        time.sleep(random.uniform(7,10))   # 잠깐 휴식
        source = driver.page_source
        soup = bs(source, 'html.parser')

        pums = soup.select('body > div.main > div > div.content > div.posts.clearfix > div')
        
        for pum in pums:
            pumdate = pum.select_one('div.meta').next_element.get_text()
            delta = datetime.now() - datetime.strptime(pumdate, "%Y/%m/%d")

            if period == 'day' and delta.days >= 2 : continue # 일수가 2일 이상 차이나면 스킵
            elif period == 'week' and delta.days >= 8 : continue # 일수가 8일 이상 차이나면 스킵
            elif period == 'month' and delta.days >= 32 : continue # 일수가 32일 이상 차이나면 스킵

            pumlink = pum.a['href']
            pumnum = pum.a['title'].replace("[Reducing Mosaic]","").replace("[Uncensored Leak]","").replace("[Full Version]","").replace("[Chinese Subtitles]","").replace("【SupJAV-Exclusive】","").replace("[English Subtitles]","").replace("[4K]","").replace("   ","").replace("  ","")
            pumthumb = pum.select_one('img.thumb')['data-original']
            pumtitle = pumnum
            if pumnum.find("FC2PPV") != -1 : #fc2ppv 가 포함되어 있으면
                pumnum = " ".join(pumnum.replace("-"," ").split(" ")[0:2])
            elif pumnum.find("S-Cute") != -1 : #S-Cute 가 포함되어 있으면
                pumnum = " ".join(pumnum.split(" ")[0:2])
            elif pumnum.split(" ")[0].find("-") != -1 : # '-' 가 포함되어 있으면 
                pumnum = pumnum.split(" ")[0]
            else : # fc2ppv 도 아니고, 일반 품번도 아닌데 띄어쓰기만 되어있는 작품.
                pumnum = " ".join(pumnum.split(" ")[0:2])
            
            pumtitle = pumtitle.replace(pumnum,"")
            pumviews = int(pum.select_one('span.date').get_text().split(" ")[0])
            
            i = pumdf.index[pumdf['pumnum'] == pumnum].tolist()   # 중복된 품번이 있는 곳의 인덱스 찾기
        
            if i == [] : # 새로운 품번이면 그대로 추가
                tmp = pd.DataFrame(data=[[period,pumviews,pumnum,pumlink,0,pumthumb,pumtitle,pumdate]], columns=['period','views','pumnum','pumlink','rank','pumthumb','pumtitle','date'])
                pumdf = pd.concat([pumdf,tmp])
                # print(pumnum + " new " + str(pumviews))
            else : # 원래 있는거면 
                # print(pumdf.loc[pumdf['pumnum']==pumnum,'pumlink'].tolist()[0])
                if pumdf.loc[pumdf['pumnum']==pumnum,'pumlink'].tolist()[0].find('supjav') != -1 : #링크가 같으면 
                    pumdf.loc[pumdf['pumnum']==pumnum,'views'] = pumviews # 품번이 같은 행의, 뷰 수정
                    # print(pumnum + " re " + str(pumviews))
                else: #링크가 다르면
                    pumdf.loc[pumdf['pumnum']==pumnum,'views'] += pumviews #추가
                    # print(pumnum + " add " + str(pumviews))
        time.sleep(3)
        driver.quit()

    # driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # javsaga
    for page in pages:
        print('\n javsaga ' + page)
        sagalink = f'https://javsaga.ninja/popular/page/{page}?sort={period}'
        driver.get(sagalink)
        time.sleep(random.uniform(7,10))   # 잠깐 휴식
        source = driver.page_source
        soup = bs(source, 'html.parser')

        pums = soup.select('body > div.main > div > div > div.posts.clearfix > div')
              
        for pum in pums:

            pumdate = pum.a.div.span.get_text()
            delta = datetime.now() - datetime.strptime(pumdate, "%Y/%m/%d")

            if period == 'day' and delta.days >= 2 : continue # 일수가 2일 이상 차이나면 스킵
            elif period == 'week' and delta.days >= 8 : continue # 일수가 8일 이상 차이나면 스킵
            elif period == 'month' and delta.days >= 32 : continue # 일수가 32일 이상 차이나면 스킵

            pumlink = pum.a['href']
            pumnum = pum.a.h3.get_text().replace("[Reducing Mosaic]","").replace("[Uncensored Leak]","").replace("[Full Version]","").replace("[Chinese Subtitles]","").replace("【SupJAV-Exclusive】","").replace("[English Subtitles]","").replace("[4K]","").replace("   ","").replace("  ","")
            pumthumb = pum.select_one('img.thumb')['data-original']
            pumtitle = pumnum
            if pumnum.find("FC2PPV") != -1 : #fc2ppv 가 포함되어 있으면
                pumnum = " ".join(pumnum.replace("-"," ").split(" ")[0:2])
            elif pumnum.find("S-Cute") != -1 : #S-Cute 가 포함되어 있으면
                pumnum = " ".join(pumnum.split(" ")[0:2])
            elif pumnum.split(" ")[0].find("-") != -1 : # '-' 가 포함되어 있으면 
                pumnum = pumnum.split(" ")[0]
            else : # fc2ppv 도 아니고, 일반 품번도 아닌데 띄어쓰기만 되어있는 작품.
                pumnum = " ".join(pumnum.split(" ")[0:2])
            pumtitle = pumtitle.replace(pumnum,"")

            pumviews = int(pum.a.div.next_element.next_element.get_text())

            i = pumdf.index[pumdf['pumnum'] == pumnum].tolist()   # 중복된 품번이 있는 곳의 행 찾기

            if i == [] : # 새로운 품번이면 그대로 추가
                tmp = pd.DataFrame(data=[[period,pumviews,pumnum,pumlink,0,pumthumb,pumtitle,pumdate]], columns=['period','views','pumnum','pumlink','rank','pumthumb','pumtitle','date'])
                pumdf = pd.concat([pumdf,tmp])
                # print(pumnum + " new " + str(pumviews))
            else : # 원래 있는거면
                if pumdf.loc[pumdf['pumnum']==pumnum,'pumlink'].tolist()[0].find('javsaga') != -1 : #링크가 같으면 
                    pumdf.loc[pumdf['pumnum']==pumnum,'views'] = pumviews # 품번이 같은 행의, 뷰 수정
                    # print(pumnum + " re " + str(pumviews))
                else: #링크가 다르면
                    pumdf.loc[pumdf['pumnum']==pumnum,'views'] += pumviews # 추가
                    # print(pumnum + " add " + str(pumviews))

    # evojav
    for page in pages:
        print('\n evojav ' + page)
        evolink = f'https://evojav.pro/en/popular/page/{page}/?sort={period}'
        driver.get(evolink)
        time.sleep(random.uniform(7,10))   # 잠깐 휴식
        source = driver.page_source
        soup = bs(source, 'html.parser')

        pums = soup.select('body > div.main > div > div > div.posts.clearfix > div')
              
        for pum in pums:

            pumdate = pum.div.div.next_element.get_text()
            pumdate = datetime.strptime(pumdate, "%Y/%m/%d") # 문자열을 날짜형식으로 변환
            delta = datetime.now() - pumdate

            if period == 'day' and delta.days >= 2 : continue # 일수가 2일 이상 차이나면 스킵
            elif period == 'week' and delta.days >= 8 : continue # 일수가 8일 이상 차이나면 스킵
            elif period == 'month' and delta.days >= 32 : continue # 일수가 32일 이상 차이나면 스킵

            pumlink = pum.a['href']
            pumnum = pum.a['title'].replace("[Reducing Mosaic]","").replace("[Uncensored Leak]","").replace("[Full Version]","").replace("[Chinese Subtitles]","").replace("【SupJAV-Exclusive】","").replace("[English Subtitles]","").replace("[4K]","").replace("   ","").replace("  ","")
            pumthumb = pum.select_one('img.thumb')['data-original']
            pumtitle = pumnum
            if pumnum.find("FC2PPV") != -1 : #fc2ppv 가 포함되어 있으면
                pumnum = " ".join(pumnum.replace("-"," ").split(" ")[0:2])
            elif pumnum.find("S-Cute") != -1 : #S-Cute 가 포함되어 있으면
                pumnum = " ".join(pumnum.split(" ")[0:2])
            elif pumnum.split(" ")[0].find("-") != -1 : # '-' 가 포함되어 있으면 
                pumnum = pumnum.split(" ")[0]
            else : # fc2ppv 도 아니고, 일반 품번도 아닌데 띄어쓰기만 되어있는 작품.
                pumnum = " ".join(pumnum.split(" ")[0:2])
            pumtitle = pumtitle.replace(pumnum,"")
            pumviews = int(pum.div.div.span.get_text().split(" ")[0])

            i = pumdf.index[pumdf['pumnum'] == pumnum].tolist()   # 중복된 품번이 있는 곳의 인덱스 찾기
            if i == [] : # 새로운 품번이면 그대로 추가
                tmp = pd.DataFrame(data=[[period,pumviews,pumnum,pumlink,0,pumthumb,pumtitle,pumdate]], columns=['period','views','pumnum','pumlink','rank','pumthumb','pumtitle','date'])
                pumdf = pd.concat([pumdf,tmp])
            else : # 원래 있는거면
                if pumdf.loc[pumdf['pumnum']==pumnum,'pumlink'].tolist()[0].find('evojav') != -1 : #링크가 같으면 
                    pumdf.loc[pumdf['pumnum']==pumnum,'views'] = pumviews # 품번이 같은 행의, 뷰 수정
                else: # 링크가 다르면
                    pumdf.loc[pumdf['pumnum']==pumnum,'views'] += pumviews #추가

    pumdf['date'] = pd.to_datetime(pumdf['date'], format="%Y/%m/%d")
    
    if period == 'day' : d = 2
    elif period == 'week' : d = 7
    elif period == 'month' : d = 31
    pumdf = pumdf[(pumdf['date']>=(datetime.now()-timedelta(days=d)))]

    # pumdf = pumdf.drop_duplicates(subset=['period','pumnum'], keep='last') # 중복제거
    pumdf = pumdf.sort_values(['period','views'],ascending=False) # 내림차순 정렬
    pumdf = pumdf.reset_index(drop=True) # 인덱스 = 순위
    pumdf.index = pumdf.index +1

    print("새로 저장중")
    pumdf = pumdf[:50]
    pumdf.to_csv(f"av_list_{period}.csv")
    print(pumdf)
    
    return pumdf
    # # 조회수 내림차순 정렬
    # pumlist = sorted(pumlist,reverse=True, key=lambda s: int(re.search(r'(\d+)', s).groups()[0]))

def get_new_release(category):
    '''
    category = 'ama', 'uncen', 'cens'
    '''
    
    # pumdf = pd.DataFrame(columns=['views','pumnum','pumlink','pumthumb','pumtitle','date','rank'])

    pumdf = pd.read_csv(f"av_list_{category}.csv",header=0, index_col=0)
    pumdf['rank'] = pumdf.index  # 이전 인덱스는 랭크로 이동
    pumdf = pumdf.astype({'rank':'int'})

    page = 0
    while(page >= 0):
        page += 1

        print('\n supjav ' + str(page))
        # driver = webdriver.Chrome(chrome_path, options=chrome_options)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        if category == 'ama': 
            cat = 'amateur'
            suplink = f'https://supjav.com/category/{cat}/page/{page}'
        elif category == 'uncen': 
            cat = 'uncensored-jav'
            suplink = f'https://supjav.com/category/{cat}/page/{page}'
        elif category == 'cens': 
            cat = 'censored-jav'
            suplink = f'https://supjav.com/category/{cat}/page/{page}?asgtbndr=1'
        else : 
            print("카테고리 입력이 잘못되었습니다.")
            return 0
        driver.get(suplink)
        time.sleep(random.uniform(7,10))   # 잠깐 휴식
        source = driver.page_source
        soup = bs(source, 'html.parser')

        pums = soup.select('body > div.main > div > div.content > div.posts.clearfix > div')
        
        for pum in pums:
            pumdate = pum.select_one('div.meta').next_element.get_text()
            delta = datetime.now() - datetime.strptime(pumdate, "%Y/%m/%d")

            if delta.days >= 2 : 
                page = -1
                break # 일수가 2일 이상 차이나면 종료

            pumlink = pum.a['href']
            pumthumb = pum.select_one('img.thumb')['data-original']
            pumnum = pum.a['title'].replace("[Reducing Mosaic]","").replace("[Uncensored Leak]","").replace("[Full Version]","").replace("[Chinese Subtitles]","").replace("【SupJAV-Exclusive】","").replace("[English Subtitles]","").replace("[4K]","").replace("   ","").replace("  ","")
            pumtitle = pumnum
            if pumnum.find("FC2PPV") != -1 : #fc2ppv 가 포함되어 있으면
                pumnum = " ".join(pumnum.replace("-"," ").split(" ")[0:2])
            elif pumnum.find("S-Cute") != -1 : #S-Cute 가 포함되어 있으면
                pumnum = " ".join(pumnum.split(" ")[0:2])
            elif pumnum.split(" ")[0].find("-") != -1 : # '-' 가 포함되어 있으면 
                pumnum = pumnum.split(" ")[0]
            else : # fc2ppv 도 아니고, 일반 품번도 아닌데 띄어쓰기만 되어있는 작품.
                pumnum = " ".join(pumnum.split(" ")[0:2])
            pumtitle = pumtitle.replace(pumnum,"")
            pumviews = int(pum.select_one('span.date').get_text().split(" ")[0])
            
            i = pumdf.index[pumdf['pumnum'] == pumnum].tolist()   # 중복된 품번이 있는 곳의 인덱스 찾기
            if i == [] : # 새로운 품번이면 그대로 추가
                tmp = pd.DataFrame(data=[[pumviews,pumnum,pumlink,pumthumb,pumtitle,pumdate]], columns=['views','pumnum','pumlink','pumthumb','pumtitle','date'])
                pumdf = pd.concat([pumdf,tmp])
            else : # 원래 있는거면
                if pumdf.loc[pumdf['pumnum']==pumnum,'pumlink'].tolist()[0].find('supjav') != -1 : #링크가 같으면 
                    pumdf.loc[pumdf['pumnum']==pumnum,'views'] = pumviews # 품번이 같은 행의, 뷰 수정
                else: # 링크가 다르면
                    pumdf.loc[pumdf['pumnum']==pumnum,'views'] += pumviews #추가

        time.sleep(3)
        driver.quit()

    pumdf['date'] = pd.to_datetime(pumdf['date'], format="%Y/%m/%d")
    pumdf = pumdf[(pumdf['date']>=(datetime.now()-timedelta(days=2)))]

    pumdf = pumdf.sort_values(['views'],ascending=False) # 내림차순 정렬
    pumdf = pumdf.reset_index(drop=True) # 인덱스 = 순위
    pumdf.index = pumdf.index +1
    pumdf.fillna(0)

    print("새로 저장중")
    pumdf.to_csv(f"av_list_{category}.csv")
    print(pumdf)
    
    return pumdf

def get_new_release_test(category):
    '''
    category = 'ama', 'uncen', 'cens'
    '''
    pumdf = pd.DataFrame(columns=['views','pumnum','pumlink','pumthumb','pumtitle','date'])
    

    page = 0
    while(page >= 0):
        page += 1

        print('\n supjav ' + str(page))
        # driver = webdriver.Chrome(chrome_path, options=chrome_options)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        if category == 'ama': 
            cat = 'amateur'
            suplink = f'https://supjav.com/category/{cat}/page/{page}'
        elif category == 'uncen': 
            cat = 'uncensored-jav'
            suplink = f'https://supjav.com/category/{cat}/page/{page}'
        elif category == 'cens': 
            cat = 'censored-jav'
            suplink = f'https://supjav.com/category/{cat}/page/{page}?asgtbndr=1'
        else : 
            print("카테고리 입력이 잘못되었습니다.")
            return 0
        driver.get(suplink)
        time.sleep(random.uniform(7,10))   # 잠깐 휴식
        source = driver.page_source
        soup = bs(source, 'html.parser')

        pums = soup.select('body > div.main > div > div.content > div.posts.clearfix > div')
        
        for pum in pums:
            pumdate = pum.select_one('div.meta').next_element.get_text()
            delta = datetime.now() - datetime.strptime(pumdate, "%Y/%m/%d")

            if delta.days >= 2 : 
                page = -1
                break # 일수가 2일 이상 차이나면 종료

            pumlink = pum.a['href']
            pumthumb = pum.select_one('img.thumb')['data-original']
            pumnum = pum.a['title'].replace("[Reducing Mosaic]","").replace("[Uncensored Leak]","").replace("[Full Version]","").replace("[Chinese Subtitles]","").replace("【SupJAV-Exclusive】","").replace("[English Subtitles]","").replace("[4K]","").replace("   ","").replace("  ","")
            pumtitle = pumnum
            if pumnum.find("FC2PPV") != -1 : #fc2ppv 가 포함되어 있으면
                pumnum = " ".join(pumnum.replace("-"," ").split(" ")[0:2])
            elif pumnum.split(" ")[0].find("-") != -1 : # '-' 가 포함되어 있으면 
                pumnum = pumnum.split(" ")[0]
            else : # fc2ppv 도 아니고, 일반 품번도 아닌데 띄어쓰기만 되어있는 작품.
                pumnum = " ".join(pumnum.split(" ")[0:2])
            pumtitle = pumtitle.replace(pumnum,"")


            pumviews = int(pum.select_one('span.date').get_text().split(" ")[0])
            
            tmp = pd.DataFrame(data=[[pumviews,pumnum,pumlink,pumthumb,pumtitle,pumdate]], columns=['views','pumnum','pumlink','pumthumb','pumtitle','date'])
            pumdf = pd.concat([pumdf,tmp])
            print(pumnum + " " + str(pumviews)+ " " + pumdate)

        pumdf['date'] = pd.to_datetime(pumdf['date'], format="%Y/%m/%d")
            
        time.sleep(3)
        driver.quit()

    pumdf = pumdf.sort_values(['views'],ascending=False) # 내림차순 정렬
    pumdf = pumdf.reset_index(drop=True) # 인덱스 = 순위
    pumdf.index = pumdf.index +1
    pumdf.fillna(0)

    print("새로 저장중")
    pumdf.to_csv(f"av_list_{category}.csv")
    print(pumdf)
    
    return pumdf


import av_img_video_url as avurl
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
    # driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    source = driver.page_source
    soup = bs(source, 'html.parser')

    pums = soup.select('#dvd_lst > div > ul > li')
    
    cnt = 0
    for pum in pums :
        pumnum = pum.select_one('span.snum').get_text()
        print(pumnum)
        avdbslink = 'https://www.avdbs.com/menu/dvd.php?dvd_idx=' + pum['data-idx']
        rank = int(pum.select_one('span.rnk_no').get_text().replace("위",""))

        #에딥에서 상세정보
        driver.get(avdbslink)
        time.sleep(5)
        source1 = driver.page_source
        soup1 = bs(source1, 'html.parser')

        try:
            title = soup1.select_one('#title_kr').get_text()
        except:
            title = "Unknown"
        try:
            actor = soup1.select_one('a.cast').get_text().replace("#","")
        except:
            actor = "Unknown"
        date = soup1.select_one('div.profile_detail').next_element.next_element.get_text().split(" ")[-1]
        try:
            up = int(soup1.select_one('span.likecount').get_text().replace(",",""))
            down = int(soup1.select_one('span.dislikecount').get_text())
        except:
            up = 0
            down = 0

        thumb = avurl.makeImageURL(pumnum)
        if isinstance(thumb, list):
            thumb1 = thumb[0]
            thumb2 = thumb[1]
        else: thumb1 = thumb
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

import watchlist
def get_hitomi_rank(period):
    '''
    period : today, week, month, year
    '''
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    txtfile = f'hitomi_{period}_rank.txt'
    

    pgnum = 1
    pumtitles = []
    pumwriters = []
    pumlinks = []
    pumthumbs = []
    pumnums = []
    ranks = []

    for pgnum in range(1,2): # 1 페이지만
        
        if pgnum == 1 : url = f'https://hitomi.la/popular/{period}-korean.html'
        else: url = f'https://hitomi.la/popular/{period}-korean.html?page=' +str(pgnum)
        
        driver.get(url)
        time.sleep(random.uniform(5,10))   # 잠깐 휴식
        source = driver.page_source
        soup = bs(source, 'html.parser')

        pums = soup.select('body > div.container > div.gallery-content > div')

        for n, pum in enumerate(pums):
            pumtitle = pum.select_one('h1.lillie').get_text()            
            try:
                pumwriter_tmp = pum.select_one('div.artist-list').ul.get_text().split("\n") #작가 2명
                pumwriter = ""
                for w in pumwriter_tmp : 
                    if w != "": 
                        if pumwriter == "" : pumwriter += w  #첫번째는 그냥
                        else: pumwriter += ","+w  #두번째부터는 콤마 붙여서
            except: pumwriter="N/A"
            pumlink = "https://hitomi.la"+pum.select_one('a.lillie')['href']
            pumnum = pumlink.split("-")[-1].split(".")[0]
            pumnums.append(pumnum)

            chk = watchlist.find_query_line(pumnum,txtfile) # 몇번째 행에 있는지 확인 (1부터 시작)
            if (chk == -1) or (n+1 < chk) : #목록에 없으면 저장 또는 순위가 상승하면 저장
                
                pumtitles.append(pumtitle)
                pumlinks.append(pumlink)
                pumwriters.append(pumwriter)
                ranks.append(n+1)

    with open(txtfile, 'w', encoding = 'UTF-8') as f: # 'w' : 파일 내용을 새롭게 덮어씀
        for pumnum in pumnums :
            f.write(pumnum + "\n")
            
    return pumtitles, pumwriters, pumlinks, ranks
            

# hitomi writer
def get_all_hitomi_writer(link):
    ''' link : 작가 페이지 '''
    
    # driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    pumtitles = []
    pumlinks = []
    writer = ""
    pgnum=1
    while 1:
        url = link+'?page='+str(pgnum)
        pgnum += 1

        driver.get(url)
        time.sleep(random.uniform(7,10))   # 잠깐 휴식
        source = driver.page_source
        soup = bs(source, 'html.parser')
        try:
            if pgnum == 2: writer = soup.select('#artistname')[0].get_text() #작가 이름은 한번만 저장
            pums = soup.select('body > div.container > div.gallery-content > div')
            if pums == [] : break 
        except: break 
            
        for pum in pums:
            pumtitle = pum.select_one('h1.lillie').get_text()
            print(pumtitle, end=" ")
            pumlink = 'https://hitomi.la/'+pum.select_one('h1.lillie').a['href']
            print(pumlink)
            pumtitles.append(pumtitle)
            pumlinks.append(pumlink)
    print("총 " + str(len(pumtitles))+" 개")
    return writer, pumtitles, pumlinks


from pywinauto.application import Application
from pywinauto import findwindows
import clipboard

def run_hitomi_downloader():

    app=  Application(backend="uia")
    try :
        app.connect(title_re=u".*hitomi_downloader_GUI.*")  
        print("앱연결")
    except :
        app.start("C:\\Users\\seokjong_2\\Desktop\\hitomi_downloader_GUI\\hitomi_downloader_GUI.exe")
        print("앱실행")


def clipboard_copy(link):
    clipboard.copy(link)
    time.sleep(3)

def rename_tweeter_file():
    twtr_folder = "C:\\Users\\seokjong_2\\Desktop\\hitomi_downloader_GUI\\hitomi_downloaded_twitter"
    current_list = os.listdir(twtr_folder)

    for i in current_list:
        twtr_user_folder = os.path.join(twtr_folder, i) # 현재 경로의 모든객체의 전체경로
        if os.path.isdir(twtr_user_folder) :
            twtr_list = os.listdir(twtr_user_folder) #유저 폴더의 자료들
            cnt=0
            for tl in twtr_list:
                if tl.split(" ")[0] != "#트위터":
                    file_oldname = os.path.join(twtr_user_folder, tl) #각 자료의 절대주소
                    file_newname = os.path.join(twtr_user_folder,"#트위터 #" + i + tl)
                    try:
                        os.renames(file_oldname, file_newname) 
                        cnt += 1
                    except: #중복 파일 삭제
                        os.remove(file_oldname)
            print(i  +" 이름 변경완료 " + str(cnt) +"개")


# https://fc2hub.com/seller/16022/ぱおん
# https://db.msin.jp/page/writer?name=ぱおん

rename_tweet = 0
hitomi_on = 0
dbmsin_on = 0
fc2hub_on = 0
rename = 0
avdb = 0
if __name__ == '__main__':
    # chromedriver_update()
    # path = get_chromedriver_path()
    # run_hitomi_downloader()
    # get_hitomi_rank_week()

    if rename_tweet ==1 :
        rename_tweeter_file()
    if hitomi_on == 1:
        get_all_hitomi_writer("https://hitomi.la/artist/quzilax-korean.html")
    if fc2hub_on == 1:
        get_all_pumnum_fc2hub('https://fc2hub.com/seller/1606/%E4%B8%AD%E5%87%BA%E3%81%97%E3%83%8A%E3%83%83%E3%82%AF%E3%83%AB%E3%82%BA%CE%B1')
    if dbmsin_on == 1 :
        writer = 'ぱおん'
        # get_all_pumnum_uc(writer)
        get_all_pumnum(writer)
    if rename == 1 :
        rename_file()
    if avdb == 1:
        get_avdbs_rank('week')

# get_popular('day')
# get_new_release('ama')

























 







# https://goodthings4me.tistory.com/560
'''
import pathlib

## 파일명 변경 함수
def rename_file(filepath, filenames):
    # path = pathlib.Path('.') / 'rename' # pathlib.Path('./rename')과 동일
    path = pathlib.Path(filepath)
    print(path)  # rename
    file_count = len([f for f in path.iterdir()])  # 폴더내 파일수
    file_count_len = len(str(file_count))
    print(f'file_count: {file_count}/nlen: {file_count_len}')

    cnt = 1
    for file in path.iterdir():
        if not file.is_dir():
            # print(file)  # rename/test10.png
            print(file.name)  # test10.png
            # print(file.stem)  # test10
            # print(file.suffix)  # .png
            # print(file.parent)  # remame
            # print()

            directory = file.parent
            file_name_ext = file.name
            file_name = file.stem
            extension = file.suffix
            
            if file.is_file():
                new_filename = filenames + str(cnt).zfill(file_count_len) + extension
                # 숫자 앞에 0 채우기 .zfill(숫자길이)
                file.rename(path / new_filename)
            cnt += 1

    print('-' * 30)
    
    for f in path.iterdir():
        print(f.name)


file_dir = r'D:/rename/sub_rename'
new_filename = 'Anaconda 설치_'

rename_file(file_dir, new_filename)
'''
'''
#파일관리 함수

shutil.copy(a, b)
shutil.move(a, b)
shutil.rmtree(path) # 비어있는 directory만 삭제 가능
os.rename(a, b)
os.remove(f)

os.chdir(d) # change
os.mkdir(d) # make ☆ (이미 존재하면 예외)
os.rmdir(d) # remove
os.getcwd() # 현재 working directory 문자열 리턴
os.listdir(d) # directory 목록
glob.glob(pattern)
os.path.isabs(f) # 절대경로 검사
os.path.abspath(f) # 상대경로 -> 절대경로
os.path.realpath(f)
os.path.exists(f) # 경로 존재 검사 ☆
os.path.isfile(f) # 파일인지 검사
os.path.isdir(f) # directory인지 검사
'''