import json
from pprint import pprint

PRESTIGE_ITEMS = {
    'prestige': ['chn','gdl','afs','drc','esk','hrv','yrh','ama','abs','abp','bgn','sga','ppt','pxh','mgt','tus','tre','gwjac','vpc'],
    'kanbi': ['kpb','dtt'],
    'doc': ['cdc','sim','fcp','docp'],
    'onemore': ['onez'],
    'shiroutotv': ['siv'],
    'mbm': ['kum'],
    'projectdiamond': ['prb'],
    'jackson': ['jac','jnt'],
    'gets': ['ggen','gyan','gnab','gzap'],
    'kurofune': ['kfne'],
    'nanpatv': ['npv'],
    'luxutv': ['lxv'],
    'documentv': ['dcv']
}

AMA = {
    'nanpatv' : ["200gana"],
    'hamedori2nd' : ["328hmdnc"],
    'ara' : ["261ara"],
    'luxutv' : ["259luxu"],
    'prestige':["ymym"],
    'shirouto' : ['siro'],
    'scute' : ['229scute']
}

ALL_ITEMS = {
    '1': ['idol','rct','sdmt','nag','gs','atom','sdmua','msfh','svvrt','mist','silkbt','shh','acme','nhdta','sdmf','mogi','stcv',"hunta",'drpt','mgold','votan','noskn','paioh','bkynb','mtall','hunt','sdfk','silku','star','stars','sdjs','sdnm','kmhr','sdth','kuse','sdab','sdmm','danuhd','nyh','zozo','ftht','akdl','silk','silks','sdam','sdde','kire','shn','fsdss','fsvss','nhdtb','svdvd','iesp','piyo','dldss','sun','dandy','rctd','hawa','sw','ienf','gs','hbad','okb','dandan','nhvr','havd','mtvr','iesm','ftdss','okp','oks','svomn','hypn','sdnt','sdmu','nttr','fset','shyn','dvdm','miha'],
    '2': ['ecb','wzen','wpom','ekbe','dfe','wfr','ekw','wpvr','wkd'],  '12': ['bur','lol','imo','scr'], '13': ['gg','gbd','gvg','dsvr','gqe','ovg','yvg','rvg'],
    '17':['mkd'],'18': ['jkzk','mght','sprd','ntrd','spbx','mond'],  '21':['psd'],'24': ['cmd','dyd','dtsl','dfbvr','vdd','ped'],  '30': ['nha','msc','msa'],'33':['dph'],
    '36': ['doks','drop','dkwt','dmow'],  '41':['hodv','om','pjf','ly','pmc'],'42': ['sp'],'41':['kk'],'48':['mdvhj'],'49':['mgdv'],     
    '53':['pdv'],'55': ['davk','tmavntgvr','T28'],'57': ['jksr','mcsr','itsr','bdsr','husr','sgsr'],'60':['xv'],'61':['mds'], '71': ['gas'],    '84': ['mdtm','mkmp','kmvr','umso'], 
    '86': ['axdvd'], '100': ['tv','yen'],'118':['fiv','kkj','aka','giro','yzf'],     '125': ['umd'], '143': ['mom','shm'],     '149': ['rd'],    '171': ['lhtd'], '172': ['xrw'], '189': ['hsf'], '301': ['mbdd'],
    '422': ['kagd'], '433': ['gun','neo'], '436': ['bubb','yas'], '5013': ['tsds'], '504': ['ibw'],'540':['yst','wpe','bcm','tmg'],
    '5443': ['loota'], '5448': ['mwkd'], '5561': ['brth','flvr11','lvid','ftsh','vntg','shmo'], 
    '5581': ['pitv'], '5642': ['bndv','hodv'],'5050':['kkom'],   
    'h_021':['pym'],'h_068':['mxgs'], 'h_890':['mist'], 'h_1337': ['wvr9c'],'h_308':['aoz'],'h_491':['fone','kswp','nebo','ciel','tdmn', 'dori'],
    'h_1368': ['komz'], 'h_254': ['kir','ofku','spz','vnds','doki','mgdn','dmat','udak','nxg','kazk','eih'],
    'h_1248': ['kiwvr'], 'h_1462': ['com','pyu'], 'h_706': ['anda','coch','gredb','prbyb','sbmo','sprbd','thnib','ppmn'],
    'h_1580':['och'],'h_900':['diy'],'h_259':['vnds'],'h_244': ['saba','supa'], 'h_1575': ['sgkx'], 'h_1256': ['tpvr','tprm'], 'h_1127': ['vovs','gopj','vosf','vosm'],
    'h_1116': ['cafuku','cami','casmani','cafr','capi','cabe','caca'], 'h_019': ['aczd','acz','kck'],'h_305':['bagbd'],
    'h_1100': ['hzgb','hzgd','hzhb'], 'h_1000': ['spye'], 'h_1001': ['oyaj'], 'h_1160': ['meko','mhar'],'h_1605':["stsk"],
    'h_1231': ['ss'], 'h_1300': ['mtes'],'h_1352':['knmd'], 'h_1628':['sat'], 'h_1534':['grmo'],'h_127':['ysn'],
    'h_1422':['semg'],'h_1435': ['clo','bth'], 'h_1573': ['ftuj'], 'h_1577': ['favkh','fbcpv'], 'h_496': ['dogd'],'h_213':['ageom'],
    'h_697':['sexy'],'h_918':['tad'],'h_574': ['iqpa'], 'h_1569': ['nkkvr'], 'h_086': ['hthd','xmom','fera','keed','jrze','jura','mesu','nuka','abba','cvdx','toen','zeaa','iqqq','hima','ferax','iga','kaad','hone'],
    'h_1002': ['jgaho'], 'h_1386': ['dinm'], 'h_1492': ['siror'], 'h_1587': ['ein'], 'h_720': ['zex'],'h_1613':['bdda'],
    'h_1416': ['ad'], 'h_1563': ['mol'], 'h_094': ['ktra'], 'h_796': ['san','much'],'h_1609':['spivr'],'h_1615':['beaf'],
    'h_458': ['hsm'], 'h_1304': ['tg'], 'h_1526': ['pm'], 'h_1342': ['nsm'], 'h_1440': ['fgan'],'h_1639':['wpsl'],
    'h_1060':['vsed'],'h_967':['asw'],'h_1594': ['spro'], 'h_1096': ['bdsm'], 'h_113': ['bbacos','cb','ek','kpp','spo','sw','syk','sy','izm'],
    'h_1664':['pes','kir','nxg','nxgs','ofku'],'h_1165': ['goju'], 'h_1553': ['ftvr'], 'h_1560': ['shind'],'h_452':["tmcy"],'h_1068':['ftom'],'h_422':['sero'],
    'h_175':['dnty'],'h_1345': ['gnax'], 'h_1558': ['csdx'], 'h_1593': ['cubex','fanq','fanx','papak'], 'h_172': ['hmgl','hmnf'], 'h_1631': ['krs'],
    'h_173': ['ghmt','giro','ghkr','gtrl','ryoj','tbb','thp'], 'h_1454':['smdy'], 'h_1359':['swdf'],'h_066':['fabs',"fax"],
    'h_189': ['cha','milf','pc','tsm','uta','vio'], 'h_237': ['emot','find','ambi','ambs','clot','hdka','nacr','nacx','zmar'],
    'h_897': ['nmk','hict'], 'h_101': ['gs'], 'h_227': ['jukf'], 'h_1324': ['skmj'], 'h_1240': ['milk'],'h_1112':['nubi'],
    'h_1472': ['hmdnv','erofv','hmvf','stvf','instv'], 'h_1378': ['arso'], 'h_580': ['tms'], 'h_1533': ['can'], 'h_1321': ['pydvr'],'h_1133':['gogo','pais','pako','honb'],
    'h_1155': ['crvr'], 'h_910': ['VRTM'], 'h_921': ['^hj$'], 'h_346': ['rebd'], 'h_1495': ['bank'],'h_1596':['gns'],
    '': [] # zfill(3)
}
DBMSIN_IMG = {
    'MGS' : ["abw"] # https://db.msin.jp/jp.images/cover/MGS/ABW-312.jpg
}

# MGS 품번에는 숫자가 없는데, 링크에는 숫자가 있는것 / 앞에 숫자 알아내기
DBMSIN_NUM_AMA_IMG =[
    '290VSED','342PIH','020GG','109IDOL','203SEXY','220SILK','481ACZD','016HEZ','050KK','420HHL','026JKZK','099KKJ','360TAD','014DIY','278GZAP','223ECB','168RS','052VNDS','107SDMT','052PES','052OFKU','052NXGS','052NXG','052KIR','118RCT','110FSET','107STARS','298GOGO','223WPSL','001HMGL','169MDS','420STH','224DYD','263EMOT','224CMD','336DTT','225YSN','223WZEN','298PAIS','077GBD','324SRTD','271GS','390JNT','326KFNE','446KHOM','554SPIVR','107MSFH','563PPZ','390JAC','112SVVRT','224DTSL','201FONE','298PAKO','201CIEL','201DORI','002HODV','336KNB','595CHNYM','118RCTD','278GNAB','435MFC','300MAAN','480FRIN','277DCV','300NTK','259LUXU','230ORECO','726ANKK','702NOSKN','558KRS','520SSK','223EKBE','043PYM','278GIRO','005AOZ','352KNMD','107SDMUA','026MOND','109IENE','116SHH','307SHIC','1073DSVR','258DTSG','116ACME','336KBI','116NHDTA','107MOGI','336ASI','534IND','107SDMF','336ASI','003T28','201TDMN'
    ]
# matching = [s for s in DBMSIN_NUM_AMA_IMG if "베리" in s] 
# print(matching) #리스트

DBMSIN_UNCEN_IMG = {
    'heyzo' : ["heyzo"],
    'h4610' : ["h4610"],
    'paco' : ["paco"],          
    'carib' : ["carib"],
    "10mu" : ["10mu"],
    'fc2':["fc2-ppv"],
    '1pon':["1pon"]    
}

DBMSIN_AMA_IMG ={
    'FANZA' : ['iptd','skho','hhl','pchn','tkwa','hoi','spay','60xv','sth','frin',"scute","pow","sqb","hmdnc","oreco","ankk",'ssk','mgmr'], #https://db.msin.jp/jp.images/cover/FANZA/scute1306.jpg
    'MGS' : ["229scute",'bkynb'],#https://db.msin.jp/jp.images/cover/MGS/229SCUTE-1288.jpg
    'GIGA':["thp","ghov","gigp","spsa"], #https://db.msin.jp/jp.images/cover/GIGA/THP-96.jpg
    "" : [] #MGS 기타등등
}

# 각 딕셔너리를 하나의 리스트에 담는다.
dict_list = {
    'ALL_ITEMS':ALL_ITEMS,
    'AMA':AMA,
    'DBMSIN_AMA_IMG': DBMSIN_AMA_IMG,
    'DBMSIN_IMG': DBMSIN_IMG, 
    'DBMSIN_NUM_AMA_IMG': DBMSIN_NUM_AMA_IMG, 
    'DBMSIN_UNCEN_IMG': DBMSIN_UNCEN_IMG, 
    'PRESTIGE_ITEMS':PRESTIGE_ITEMS
}

class AvSeries():
    def __init__(self) -> None:
        self.file = 'av_series_list.txt'
        self.av_series_list = None
        if self.av_series_list == None: self.av_series_list = self.get_json(self.file)
    

    def save_default(self, data, file=None):
        if file is None : file = self.file
        with open(file, 'w') as f:
            json.dump(data, f)

    def get_json(self, file=None):
        if file is None : file = self.file

        if self.av_series_list == None : self.save_default(dict_list)
        else: self.save_json()
        # json 형식으로 파일 불러오기
        with open(file, 'r') as f:
            try: self.av_series_list = json.load(f)
            except : self.av_series_list = self.save_default(dict_list)
            return self.av_series_list

    def save_json(self, file=None):
        if file is None : file = self.file
        # json 형식으로 파일 저장
        with open(file, 'w') as f:
            json.dump(self.av_series_list, f)

    def add(self, key1, key2, value, file=None):
        '''
        dict={
            'ALL_ITEMS':avurl.ALL_ITEMS,
            'AMA':avurl.AMA,
            'DBMSIN_AMA_IMG': avurl.DBMSIN_AMA_IMG,
            'DBMSIN_IMG': avurl.DBMSIN_IMG, 
            'DBMSIN_NUM_AMA_IMG': avurl.DBMSIN_NUM_AMA_IMG, 
            'DBMSIN_UNCEN_IMG': avurl.DBMSIN_UNCEN_IMG, 
            'PRESTIGE_ITEMS':avurl.PRESTIGE_ITEMS
        }
        '''
        if file is None : file = self.file
        self.av_series_list = self.get_json(file)
        
        if key1 not in self.av_series_list:
            self.av_series_list[key1] = {}

        if key2 not in self.av_series_list[key1]:
            self.av_series_list[key1][key2] = []

        if value not in self.av_series_list[key1][key2]:
            self.av_series_list[key1][key2].append(value)
            self.save_json(file)
        

    def delete(self, key1, key2, value ,file=None):
        if file is None : file = self.file

        self.av_series_list = self.get_json()
        if key1 in self.av_series_list:
            if key2 in self.av_series_list[key1] :
                if value in self.av_series_list[key1][key2]:
                    self.av_series_list[key1][key2] = self.av_series_list[key1][key2].remove(value)
                    self.save_json(file)

                else: print(f"delet - can't find {value} in av_series_list['{key1}']['{key2}']")
            else: print(f"delet - can't find '{key2}' in av_series_list['{key1}']")
        else: print(f"delet - can't find '{key1}' in av_series_list")

if __name__ == "__main__":
    avSeries = AvSeries()
    avSeries.add('DBMSIN_AMA_IMG','a','asdf')   
    pprint(avSeries.get_json(),width=100, compact=True)

