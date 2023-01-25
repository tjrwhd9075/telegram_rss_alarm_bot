
import urllib.request
from urllib import parse
import json
import re

import googletrans
from bs4 import BeautifulSoup as bs


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
            "亀頭戦士ガンシャム":"귀두전사건샴","むげんどー":"무겐도","素人大臣":"동인대신","お値うちどが":"오치우치도가",
            "シン錦糸町ハメ撮りサークル":"신긴시초POV서클","PINX汁自慢の男優さん募集中":"PINX즙자랑의남배우모집중",
            "アヘピース":"아헤피스","ジャコモカサノヴァ":"자코모카사노바","西日本ハメ撮り横丁":"서일본POV요코초","まるきゅう商事":"마루큐상사",
            "":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"",
        
          }

    for key in dic.keys():
        txt = txt.replace(key, dic[key])
    return txt

def replaceTxt(txt):
    dic = {'\\':' ', '/':" ", ":" :" ", "*" :" ", "?" :" ","《":" ","》":" ","<" :" ", ">" :" ", "|" :" ", '"' :" ","●":" ","・":" ","○":" "," ​​":" ","⇒":" ","　":" "," ":""," ":" ","『":" ","』":" ",",":" ","→":" ","\n":" ","」":" ","「":" ","【":" ","】":" ","…":" ","★":" ","·":" ",".":" ","!":" ","‼":"","◯":" ","♡":"","×":" ","☆":" ","❤️":" ",
            "❗️":" ","※":"","〇":""," ️":"","♥️":"","♪":"","[":" ","]":" ","‘":" ","’":" ","~":" ","`":" ","⁉":" ",
            "&lt;":"","&gt;":"",
            "화장실" :"#화장sil ", "로리":"#로Li ","롤리":"#로Li ","선생님":"#선생님 ","오랄":"#페라 ","사까시":"#페라 ","구강 성교":"#페라 #이라마 ","구강성교":"#페라 #이라마 ","일라마치오":"#이라마 치오","페라":"#페라 ","펠라":"#페라 ","목구멍":"#목구멍 ","이라마":"#이라마 ",
            "절륜":"#절륜 ","조루":"#조루 ","NTR":"#NTR ","옆집":"#옆집 ","누나":"#누나 ","난교":"#난교 ","3P":"#3P ","3p":"#3P ","아르바이트":"#아르바이트 ","알바":"#아르바이트 ",
            "매직미러":"#매직미러 ","매직 미러":"#매직미러 ","마술 거울":"#매직미러 ","마술거울":"#매직미러 ","마법의 거울":"#매직미러 ",
            "비서":"#비서 ","OL":"#OL ","회사":"#회사 ","사내":"#사내 ","상사":"#상사 ","부하":"#부하 ","거래처":"#거래처 ","사무실":"#사무실 ","신입":"#신입 ","사원":"#사원 ","직원":"#직원 ","스위트룸":"#스위트룸 ","스위트 룸":"#스위트룸 ",
            "학원":"#학원 ","여자 학교생":"#여고생 ","여자학교생":"#여고생 ","학교":"#학교 ","신입생":"#신입생 ","기숙사":"#기숙사 ",
            "학생":"#학생 ","여학생":"#여학생 ","대학생":"#대학생 ","여자 대학생":"#여대생 ","여자대학생":"#여대생 ","여 #학생":"#여학생 ","대 #학생":"#대학생 ","여자 대 #학생":"#여대생 ","여자대 #학생":"#여대생 ",
            "주부":"#주부 ","유부녀":"#유Bu녀 ","기혼 여성":"#유Bu녀 ","기혼여성":"#유Bu녀 ","아줌마":"#아줌마 #미시 ","부인":"#부인 ","가정부":"#가정부 ","가정교사":"#가정교사 ","보육교사":"#보육교사 ","교사":"#교사 ","요가":"#요가 ","오일":"#오일 "," 에스테":" #에스테틱 ","멘에스":"#에스테틱 ","마사지":"#마사지 ","정체사":"#정체사 ","안마사":"#안마사 ","정조대":"#정조대 ",
            "방뇨":"#방뇨 ","빼앗겨":"#빼앗겨 ","DQN":"#DQN ", "츤데레":"#츤데레 ","레2프":"#레2프 ","레 프":"#레2프 ","레x프":"#레2프 ","윤간":"#윤gan ","레깅스":"#레깅스 ", "차내":"#차내 ",
            "키스":"#키스 ","지근거리":"#지근거리 ","버스":"#버스 ","모델":"#모델 ",
            "근친상간":"#근chin상gan ","근친 상간":"#근chin상gan ", "근친":"#근chin상gan ",
            "아내":"#아내 ","동생":"#동생 ","여동생":"#여동생 ","여 #동생":"#여동생 ","언니":"#언니 ","의붓":"#의붓 ","아버지":"#아버지 ", "시아버지":"#시아버지 ","아빠":"#아빠 ", "어머니":"#어머니 ","엄마":"#엄마 ", "딸":"#딸 ","아들":"#아들 ","조카":"#조카 ","며느리":"#며느리 ","매형":"#매형 ","처제":"#처제 ","처남":"#처남 ","남편":"#남편 ","삼촌":"#삼촌 ",
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
            "경련":"#경련 ","오르가즘":"#오르가즘 ","절정":"#절정 ","트랜스":"#트랜스 ","조수":"#조수 ","시오후키":"#시오후키 ",
            "레즈":"#레즈 ","개인 사격":"#개인촬영 ","개인 촬영":"#개인촬영 ","개 촬영":"#개인촬영 ","풍속":"#풍속 ","소프":"#소프 ","노브라":"#노브라 ","노팬티":"#노팬티 ","노 브라":"#노브라 ","노 팬티":"#노팬티 ","처녀":"#처녀 ","승무원":"#승무원 ",
            "아이돌":"#아이돌 ","감금":"#감금 ","쓰레기실":"#쓰레기방 ","동거":"#동거 ","무방비":"#무방비 ","기름":"#오일 ","JD":"#JD ","혼욕":"#혼욕 ","포티오":"#포르치오 ","포르치오":"#포르치오 ","포르티오":"#포르치오 ",
            "유출":"#Yu출 ","여고생":"#여고생 ","가출":"#가출 ","셀카":"#셀카 ","숨겨진 촬영":"#Do촬","숨겨진촬영":"#Do촬 ","목욕":"#목Yok ","욕실":"#욕실 ","사장":"#사장 ",
            "E컵":"#E컵 ","E 컵":"#E컵 ","E-컵":"#E컵 ","Ecup":"#E컵 ","E cup":"#E컵 ",
            "G컵":"#G컵 ","G 컵":"#G컵 ","G-컵":"#G컵 ","Gcup":"#G컵 ","G cup":"#G컵 ",
            "F컵":"#F컵 ","F 컵":"#F컵 ","F-컵":"#F컵 ","Fcup":"#F컵 ","F cup":"#F컵 ",
            "H컵":"#H컵 ","H 컵":"#H컵 ","H-컵":"#H컵 ","Hcup":"#H컵 ","H cup":"#H컵 ",
            "I컵":"#I컵 ","I 컵":"#I컵 ","I-컵":"#I컵 ","Icup":"#I컵 ","I cup":"#I컵 ",
            "J컵":"#J컵 ","J 컵":"#J컵 ","J-컵":"#J컵 ","Jcup":"#J컵 ","J cup":"#J컵 ",
            "온천":"#온천 ","남탕":"#남탕 ",
            "간호":"#간호 ","간호사":"#간호사 ","#간호 사":"#간호사 ","배달원":"#배달원 ",
            "유혹":"#유혹 ","상담":"#상담 ","모니터링":"#모니터링 ","건방진":"#건방진 ","성노예":"#성노예 ","노예":"#노예 ","선배":"#선배 ",
            "나카다시":"#나카다시 ","바니":"#바니걸 ","바니걸":"#바니걸 ","여관":"#여관 ","멘션":"#멘션 ","편의점":"#편의점 ","점원":"#점원 ","점장":"#점장 ","전화":"#전화 ",
            "비키니":"#비키니 ","무수정":"#무수정 ","동창회":"#동창회 ","야구부":"#야구부 ","테니스부":"#테니스부 ","축구부":"#축구부 ","배구부":"#배구부 ","카우걸":"#카우걸 #기승위 ","기승위":"#기승위 #카우걸 ",
            "그라비아":"#그라비아 ","동아리":"#동아리 ","세후레":"#세후레 ","아첨약":"#미약 ","능욕":"#능Yok ","무단취소":"#무단취소 ","무단 취소":"#무단취소 ",
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
  
def papago(txt):
    try:
        client_id = "CDWEGWm1AGvUFyq3Sw1J" # 개발자센터에서 발급받은 Client ID 값
        client_secret = "9uXJT9Qo6i" # 개발자센터에서 발급받은 Client Secret 값
        encText = urllib.parse.quote(txt)

        try:
            translator = googletrans.Translator()
            source = translator.detect(txt).lang
        except Exception as e:
            print("papago detect lang 실패: " + txt, end="" )
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
            print("papago request 실패: " , end="")
            print(e)
            # print(traceback.format_exc())
            return txt
        
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read().decode('utf-8')
            result = json.loads(response_body)
            # print('번역결과 : ',result['message']['result']['translatedText'])
            return result['message']['result']['translatedText']
        else:
            print("Error Code:" + rescode)
            return txt
    except Exception as e:
        print("papago 번역실패 : " + txt , end="")
        print(e)
        # print(traceback.format_exc())
        return txt

def google_trans_free_old(txt):
    translator = googletrans.Translator()
    try:
        return translator.translate(txt, src='auto',dest='ko').text
    except Exception as e:
        print("google_trans_free 번역실패: ")
        print(e)
        # print(traceback.format_exc())
        return txt

def google_trans_free(txt):
    translator = googletrans.Translator()

    txtList = txt.split(" ")
    result = ""
    for t in txtList:
        if t!="":
            try:
                result+= translator.translate(t, src='auto',dest='ko').text +" "
            except Exception as e:
                print("google_trans_free 번역실패: " + t, end=" ")
                print(e)
                result+=""
    return result


def translater(txt):
    txt = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥]"," ", txt) #특수문자 제거
    # txt = replaceTxt(txt)
    
    result = google_trans_free(txt)
    source =""
    if result != "":
        try:
            translator = googletrans.Translator()
            source = translator.detect(result).lang
        except Exception as e:
            print("translater detect lang 실패: ", end="" )
            print(e)
            # print(traceback.format_exc())

        if source != "ko": result = papago(result) 

    return result

def pumnum_check(pumnum):
    pumnum = pumnum.lower()
    if pumnum.find("scute") != -1: pumnum = pumnum.split(" ")[0] #229SCUTE-1288 Mayu -> 229SCUTE-1288
    elif pumnum.find("caribbeancom ") != -1: pumnum = pumnum.replace("caribbeancom ","carib-") #Caribbeancom 010323-001 -> carib-010323-001
    elif pumnum.find("-carib") != -1: pumnum = "carib-"+pumnum.replace("-carib","") #010323-001-CARIB -> -> carib-010323-001
    elif pumnum.find("1pondo") != -1: pumnum = pumnum.replace("1pondo ","1pon-") #1Pondo 010323_001 -> 1pon-010323_001
    elif pumnum.find("-1pon") != -1: pumnum = "1pon-"+pumnum.replace("-1pon","")# 010323_001-1PON
    elif pumnum.find("10musume") != -1: pumnum = pumnum.replace("10musume ","10mu-") #10musume 010323_01 -> 10mu-010323_01
    elif pumnum.find("pacopacomama ") != -1: pumnum = pumnum.replace("pacopacomama ","paco-") #Pacopacomama 010323_770 -> paco-010323_770
    elif pumnum.find("pacopacomama-") != -1: pumnum = pumnum.replace("pacopacomama-","paco-") #Pacopacomama-010323_770 -> paco-010323_770
    elif pumnum.find("fc2ppv ") != -1 : pumnum = pumnum.replace("fc2ppv ", "fc2-ppv-")
    elif pumnum.find("fc2ppv-") != -1 : pumnum = pumnum.replace("fc2ppv-", "fc2-ppv-")
    elif pumnum.find("fc2-ppv ") != -1 : pumnum = pumnum.replace("fc2-ppv ", "fc2-ppv-")
    elif pumnum.find("heyzo ") != -1 : pumnum = pumnum.replace("heyzo ", "heyzo-")

    return pumnum

def get_pumInfo_dbmsin_static(pumnum):
    '''
    # pumnum : 국내 -> asd-1234 , 해외(fc2) -> fc2-ppv-123456
    국내 https://db.msin.jp/jp.search/movie?str={}
    해외 https://db.msin.jp/search/movie?str={}

    # return puminfo = {"title":"-","writer":"-","actor":"-","createDate":"-","thumb":"-"}
    '''
    puminfo = {"title":"-","writer":"-","actor":"-","createDate":"-","thumb":"-"}


    avfc2=""
    pumnum = pumnum_check(pumnum)
    
    if pumnum.find("fc2") != -1 or pumnum.find("carib") != -1 or pumnum.find("10mu") != -1 or pumnum.find("paco") != -1 or pumnum.find("1pon") != -1 or pumnum.find("heyzo") != -1: 
        url = f'https://db.msin.jp/search/movie?str=' + parse.quote(pumnum); avfc2="fc2"
    else :
        url = f"https://db.msin.jp/jp.search/movie?str=" + parse.quote(pumnum); avfc2="av"

    headers = {
        "Cookie":"age=off",
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/53.36'
    } 
    
    try:
        req = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(req).read().decode('utf-8')
        soup = bs(response,'html.parser')
    except Exception as e:
        print("get_pumInfo_dbmsin_static - url open fail : ",end=""); print(e)
        print(puminfo)
        return puminfo
    
    try:
        if soup.select_one("#content > p:nth-child(4)").get_text().strip() == "No Resutls": 
            if pumnum[0:3].isdigit() is True:  #품번앞에 숫자가 붙어있는지 확인, 숫자 떼고 한번더 써치
                pumnum = pumnum[3:]
                try:
                    url = f"https://db.msin.jp/jp.search/movie?str=" + parse.quote(pumnum)
                    req = urllib.request.Request(url=url, headers=headers)
                    response = urllib.request.urlopen(req).read().decode('utf-8')
                    soup = bs(response,'html.parser')
                except Exception as e:
                    print("get_pumInfo_dbmsin_static - url open fail : ",end=""); print(e)
                    print(puminfo)
                    return puminfo
            else:
                print("get_pumInfo_dbmsin_static - dbmsin 검색결과 없음 : ")
                print(puminfo)
                return puminfo
    except: pass

    try: #여러개 검색되는 경우 한번더
        href = soup.select_one("#content > div:nth-child(4) > div > div:nth-child(1) > div.movie_ditail > div.movie_title > a")['href']
        print("https://db.msin.jp"+href[2:])
        url = "https://db.msin.jp"+href[2:]
        req = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(req).read().decode('utf-8')
        soup = bs(response,'html.parser')
    except: pass

    if avfc2 == "fc2": print(str(pumnum), end=" ")
    elif avfc2 == "av": print(str(pumnum), end=" ")

    try: 
        title=soup.select_one("div.mv_title").get_text().strip()
        title = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥]"," ", title) #특수문자 제거
        title = replaceTxt(translater(title)) #수정
        puminfo['title']=title
    except Exception as e : puminfo['title']="-"

    try: 
        writer = "-"
        if soup.select_one("div.mv_writer") is not None : writer=soup.select_one("div.mv_writer").get_text().strip()
        elif soup.select_one("div.mv_series") is not None : writer=soup.select_one("div.mv_series").get_text().strip()
        elif soup.select_one("div.mv_label") is not None : writer=soup.select_one("div.mv_label").get_text().strip()

        if writer != "-":
            if avfc2=="fc2": 
                writer = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥]","", replaceWriterTxt(writer)) #특수문자 제거
            elif avfc2=="av": 
                writer = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥]","", writer) #특수문자 제거
            writer = "#"+translater(writer).replace(" ","")+" "
        puminfo['writer']=writer
    except Exception as e : puminfo['writer']="-"

    try: 
        actor = soup.select_one("div.mv_artist").get_text().strip()
        actor = actor.replace("（FC2動画）","")
        actor = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥]"," ", actor) #특수문자 제거
        
        if actor.find(" ") != -1 : #여러명인 경우
            actors = actor.split(" ")
            actor = ""
            for at in actors:
                if at != "" and at is not None :
                    actor += "#"+translater(at).replace(" ","").replace("#","").replace("-","")+" "
        else:
            actor = "#"+translater(actor).replace(" ","").replace("#","").replace("-","")+" "
        puminfo['actor']=actor
    except Exception as e : puminfo['actor']="-"

    try: 
        createDate=soup.select_one("div.mv_createDate").get_text().strip()
        puminfo['createDate']=createDate
    except Exception as e : puminfo['createDate']="-"

    try: 
        thumb=soup.select_one("div.mv_coverUrl")
        if thumb is not None: thumb = thumb.get_text().strip()
        else:
            thumb = soup.find("img", class_="movie_img")
            if thumb is not None: 
                if thumb['src'].find("https://db.msin.jp") == -1 and thumb['src'].find("../") != -1 : # ../images/cover/fc2/fc2-ppv-1234568.jpg
                    thumb = thumb['src'].replace("../","https://db.msin.jp/")
                else: thumb = thumb['src']
            else: thumb = "-"

        puminfo['thumb']=thumb
    except Exception as e : puminfo['thumb']="-"
    
    print(puminfo)
    return puminfo

def get_pumInfo_fc2_from_fc2hub_static(pumnum):
    ''' 
    pumnum : 숫자만 
    return fc2info ={'title':'', 'pumnum':'', 'writer':'', 'trailer':'','img':[]}
    '''
    fc2hubUrl = f'https://fc2hub.com/search?kw={pumnum}'
    headers = {
        "Cookie":"age=off",
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/53.36'
    } 
    req = urllib.request.Request(url=fc2hubUrl, headers=headers)

    fc2info ={'title':'', 'pumnum':'', 'writer':'', 'trailer':'','img':[]}
    try: 
        res = urllib.request.urlopen(req)
        # print(res.geturl())
        if res.geturl() == fc2hubUrl : # 검색결과 없음
            print(f"get_pumInfo_fc2_from_fc2hub_static - no reslut {pumnum}")
            return fc2info
        res = res.read().decode('utf-8')
        soup = bs(res,'html.parser')

        pumid = soup.find('h1', class_='card-title fc2-id')
        if pumid is not None :
            pumid = pumid.get_text().strip()
            fc2info['pumnum'] = pumid

        title = soup.find('h1', class_='card-text fc2-title')
        if title is not None :
            title = title.get_text().strip()
            title = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥(\s)]", " ", title)
            title = replaceTxt(translater(title))
            fc2info['title'] = title

        # writer = soup.find('div', class_='col-8')
        writer = soup.select_one('div.col-8')
        if writer is not None :
            writer = writer.get_text().split("\n")
            writer = [w for w in writer if w != ""][0]
            writer = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥]", "", replaceWriterTxt(writer))
            writer = "#"+translater(writer).replace(" ","") +" "
            fc2info['writer'] = writer

        #iframe 씨발꺼
        fc2info['trailer'] = f'https://adult.contents.fc2.com/embed/{pumid.lower().replace("fc2-ppv-","")}'

        imgs = soup.find('div', class_='col des').find_all('a')
        if imgs is not None :
            for img in imgs:
                img = img['href']
                fc2info['img'].append(img)
        print(fc2info)
        return fc2info

    except Exception as e:
        print(f"get_pumInfo_fc2_from_fc2hub_static - urlopen fail : {fc2hubUrl} | ",end=""); print(e)
        return fc2info

def get_pumInfo_from_javdb_static(pumnum):
    ''' return puminfo ={'title':'', 'pumnum':'', 'writer':'','actor:'', 'date':'','trailer':'','img':[]} '''
    url = f'https://javdb.com/search?q={pumnum}&f=all'

    headers = {
        "Cookie":"age=off",
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/53.36'
    } 
    req = urllib.request.Request(url=url, headers=headers)

    puminfo ={'title':'', 'pumnum':'', 'writer':'','actor':'', 'date':'','trailer':'','img':[]}    

    res = urllib.request.urlopen(req)
    res = res.read().decode('utf-8')
    soup = bs(res,'html.parser')

    pums = soup.find_all('div', class_="item")
    for pum in pums:
        pumid = pum.find('div', class_='video-title').find('strong').get_text().strip()
        if pumnum.upper().find(pumid.upper()) != -1 or pumid.upper().find(pumnum.upper()) != -1:
            puminfo['pumnum'] = pumid
            pumlink = "https://javdb.com" + pum.a['href']
            title = pum.a['title']
            title = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥(\s)]", " ", title)
            title = replaceTxt(translater(title))
            puminfo['title']=title
            date = pum.find('div', class_='meta').get_text().strip().replace(" ","")
            puminfo['date']=date

            req1 = urllib.request.Request(url=pumlink, headers=headers)
            res1 = urllib.request.urlopen(req1)
            res1 = res1.read().decode('utf-8')
            soup1 = bs(res1,'html.parser')

            infos = soup1.find_all('div', class_='panel-block')
            for info in infos :
                txt = info.get_text().strip().replace("\n","").replace(" ","").replace("&nbsp;","").replace("\xa0","")

                if txt.find('系列') !=-1: #시리즈
                    writer = txt.split(':')[1]
                    writer = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥]", "", writer)
                    writer = translater(writer)
                    puminfo['writer']="#"+writer+" "
                elif txt.find('片商')!=-1: #시리즈가 없으면 제작사
                    writer = txt.split(':')[1]
                    writer = re.sub(r"[^a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣぁ-ゔァ-ヴー々〆〤一-龥]", "", writer)
                    writer = translater(writer)
                    puminfo['writer']="#"+writer+" "
                
                if txt.find('演員')!=-1: #여배우
                    if txt.find('♀') != -1 : #여배우가 있으면 
                        actor = txt.split(":")[1].split("♀")

                        actortxt=''
                        for act in actor:
                            if act != "" and act!=" ":
                                actortxt += "#"+translater(act)+" "
                        puminfo['actor']=actortxt
            #썸네일
            thumb = soup1.find('div', class_='column column-video-cover')
            if thumb is not None and thumb.a is not None :
                puminfo['img'].append(thumb.a.img['src'])
            #이미지
            imgs = soup1.find('div', class_='tile-images preview-images')
            if imgs is not None and imgs.find_all('a',class_="tile-item") is not None:
                imgs = imgs.find_all('a',class_="tile-item")
                for img in imgs:
                    puminfo['img'].append(img['href'])
            #트레일러
            trailer = soup1.find('source', attrs={'type':'video/mp4'})
            if trailer is not None:
                if trailer['src'][0:2] == "//":  # //asdfasf/asdf 형태일때
                    trailer['src'] = trailer['src'].replace("//", 'https://')
                puminfo['trailer'] = trailer['src']

            print(puminfo)
            return puminfo
    print(puminfo)
    return puminfo



