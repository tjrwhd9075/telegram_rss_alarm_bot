
import urllib.request
import json
import time

import googletrans
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
            print(e)
            # print(traceback.format_exc())
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
            print(e)
            # print(traceback.format_exc())
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
        print(e)
        # print(traceback.format_exc())
        return ""

def google_trans_free(txt):
    translator = googletrans.Translator()
    try:
        return translator.translate(txt, src='auto',dest='ko').text
    except Exception as e:
        print("google_trans_free : ")
        print(e)
        # print(traceback.format_exc())
        return ""

def translater(txt):
    txt = replaceTxt(txt)
    result = papago(txt)
    if result == "" :
        print("파파고 번역 실패")
        result = google_trans_free(txt)
    if result == "": result = txt
    # result = txt
    return result

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







