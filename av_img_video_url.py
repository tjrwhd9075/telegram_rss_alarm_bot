
import urllib.request
from av_series import AvSeries

headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/53.36'
} 
def purifyPumnum(pumnum):
    '''
    품번(adf 2123 또는 asf-1234 형태일것) -> maker 와 num 으로 분리
    '''
    splitID = pumnum.replace(" ","-").split('-')
    splitID[0]
    [maker, num] = [splitID[0].lower().strip(), splitID[1].strip()]

    if maker == "carib": num = splitID[1].strip() + "-" + splitID[2].strip()   # carib-11111-111   
    if maker == "fc2ppv": maker = "fc2-ppv"; num = splitID[-1].strip() # fc2-ppv 12345
    if maker == "fc2": maker = "fc2-ppv"; num = splitID[-1].strip()
    replaceItem = { 'kssis': 'ssis', 'kcawd': 'cawd'}

    for key in replaceItem.keys():
        if maker == key:
            maker = replaceItem[key]

    return [maker, num]

def makeImageURL(pumnum):
    '''
    return -> [url1, url2] / 0 (없음)
    '''
    [maker, num] = purifyPumnum(pumnum)
    print(maker, num, end=" ")
    maker = check_and_encode_for_url(maker)
    num = check_and_encode_for_url(num)

    avseries = AvSeries()
    series_dict = avseries.get_json()

    for key in series_dict['DBMSIN_IMG']:
        if maker in series_dict['DBMSIN_IMG'][key]:
            url = 'https://db.msin.jp/jp.images/cover/'+key+'/'+maker.upper()+'-'+num+'.jpg'
            
            print(key, url) 
            return url
            
    for key in series_dict['DBMSIN_UNCEN_IMG']:
        if maker in series_dict['DBMSIN_UNCEN_IMG'][key]:
            url = 'https://db.msin.jp/images/cover/'+key+'/'+maker.lower()+'-'+num+'.jpg'
            
            print(key, url) 
            return url
            
    if len(maker) > 2: #3글자 이상일때
        if maker[0:3].isdigit() is False : #앞에 숫자가 없으면
            digitMaker = [s for s in series_dict['DBMSIN_NUM_AMA_IMG'] if maker.upper() in s] #숫자 찾아내기
            if digitMaker != []: 
                url = 'https://db.msin.jp/jp.images/cover/MGS/'+digitMaker[0].upper()+'-'+num+'.jpg'
                
                req = urllib.request.Request(url=url, headers=headers)
                res = urllib.request.urlopen(req).geturl()
                if res != "https://db.msin.jp/404": print(digitMaker[0], url); return url
    
    for key in series_dict['DBMSIN_AMA_IMG']: # 앞에 숫자 있든 없든..
        if maker in series_dict['DBMSIN_AMA_IMG'][key]:
            if key == 'FANZA': url = 'https://db.msin.jp/jp.images/cover/'+key+'/'+maker.lower()+num+'.jpg' #scute
            else : url = 'https://db.msin.jp/jp.images/cover/'+key+'/'+maker.upper()+'-'+num+'.jpg' #229scute
            
            req = urllib.request.Request(url=url, headers=headers)
            res = urllib.request.urlopen(req).geturl()
            if res != "https://db.msin.jp/404": print(key, url); return url
            
            if maker[0:3].isdigit() :  #229scute 일경우
                url = 'https://db.msin.jp/jp.images/cover/FANZA/'+maker[3:].lower()+num+'.jpg'
                
                req = urllib.request.Request(url=url, headers=headers)
                res = urllib.request.urlopen(req).geturl()
                if res != "https://db.msin.jp/404": print(key, url); return url
            else : #scute 일경우 -> 앞에 숫자 알아내서 붙이기,
                digitMaker = [s for s in series_dict['DBMSIN_NUM_AMA_IMG'] if maker.upper() in s]
                if digitMaker != []: 
                    url = 'https://db.msin.jp/jp.images/cover/MGS/'+digitMaker[0].upper()+'-'+num+'.jpg'
                    
                    req = urllib.request.Request(url=url, headers=headers)
                    res = urllib.request.urlopen(req).geturl()
                    if res != "https://db.msin.jp/404": print(digitMaker[0], url); return url
        
        if key == '':
            url = 'https://db.msin.jp/jp.images/cover/MGS/'+maker.upper()+'-'+num+'.jpg'
            
            req = urllib.request.Request(url=url, headers=headers)
            res = urllib.request.urlopen(req).geturl()
            if res != "https://db.msin.jp/404":  print(key, url); return url

    for key in series_dict['PRESTIGE_ITEMS']:
        if maker in series_dict['PRESTIGE_ITEMS'][key] : 
            url = [f'https://image.mgstage.com/images/'+key+'/'+maker+'/'+num+'/pb_e_'+maker+'-'+num+'.jpg',  #신작?
               f'https://www.prestige-av.com/api/media/goods/'+key+'/'+maker+'/'+num+'/pb_'+maker+'-'+num+'.jpg']
                        

            print(key, url)
            return url

    for key in series_dict['ALL_ITEMS']:

        #소문자, 대문자
        if maker.lower() in series_dict['ALL_ITEMS'][key] or maker.upper() in series_dict['ALL_ITEMS'][key]:
            url = [f'https://pics.dmm.co.jp/mono/movie/adult/'+key+maker+num+'/'+key+maker+num+'pl.jpg',
                    f'https://pics.r18.com/digital/video/'+key+maker+num.zfill(5)+'/'+key+maker+num.zfill(5)+'pl.jpg']

            req = urllib.request.Request(url=url[0], headers=headers)
            res1 = urllib.request.urlopen(req).geturl()
            if res1.find("now_printing") == -1: print(key, url); return url[0]
            req = urllib.request.Request(url=url[1], headers=headers)
            res2 = urllib.request.urlopen(req).geturl()
            if res2.find("now_printing") == -1: print(key, url); return url[1]
        
        #나머지 전부
        if key=='':
            url = [f'https://pics.dmm.co.jp/mono/movie/adult/'+maker+num+'/'+maker+num+'pl.jpg',  
                   f'https://pics.r18.com/digital/video/'+maker+num.zfill(5)+'/'+maker+num.zfill(5)+'pl.jpg']
     
            req = urllib.request.Request(url=url[0], headers=headers)
            res1 = urllib.request.urlopen(req).geturl()
            if res1.find("now_printing") == -1: print(key, url); return url[0]
            req = urllib.request.Request(url=url[1], headers=headers)
            res2 = urllib.request.urlopen(req).geturl()
            if res2.find("now_printing") == -1: print(key, url); return url[1]
        
    print("img url 없음")
    return 0

def makeVideoURL(pumnum):
    '''return -> url / 0 (없음)'''
    [maker, num] = purifyPumnum(pumnum)
    maker = check_and_encode_for_url(maker)
    num = check_and_encode_for_url(num)
    
    avseries = AvSeries()
    series_dict = avseries.get_json()

    if ('heyzo' or '1pondo' or 'pacopaco' or 'carib' or '10musume') in maker:
        return 0
    elif ('fc2') in maker:
        return f'https://adult.contents.fc2.com/embed/{num}'

    for key in series_dict['PRESTIGE_ITEMS']:
        if maker in series_dict['PRESTIGE_ITEMS'][key]:
            url = f'https://www.prestige-av.com/api/media/movie/'+maker.upper()+'-'+num+'.mp4'
            # print(key, url)  
            
            return url
            
    for key in series_dict['AMA']:
        if maker in series_dict['AMA'][key]:
            url = 'https://sample.mgstage.com/sample/'+key+'/'+maker+'/'+num+'/'+maker+'-'+num+'_sample.mp4'
            # print(key, url)  
            
            return url
    
    for key in series_dict['ALL_ITEMS']: 
        if maker[0:3].isdigit() is True: maker = maker[3:] #품번앞에 숫자가 붙어있는지 확인
        
        chk = False

        if maker in series_dict['ALL_ITEMS'][key]:
            # print(key, url)  
            chk = True
        elif key == '':
            # print(key, url)  
            chk = True
        
        if chk == True:
            try: #url 살아잇으면 zfill(3)
                newID = key+maker+num.zfill(3)
                firstLetter = newID[0]
                threeLetter = newID[0:3]
                url = 'https://cc3001.dmm.co.jp/litevideo/freepv/'+firstLetter+'/'+threeLetter+'/'+newID+'/'+newID+'_dmb_w.mp4'
                
                res = urllib.request.urlopen(url) 
                return url
            except: #죽어있으면 zfill(5)
                newID = key+maker+num.zfill(5)
                firstLetter = newID[0]
                threeLetter = newID[0:3]
                url = 'https://cc3001.dmm.co.jp/litevideo/freepv/'+firstLetter+'/'+threeLetter+'/'+newID+'/'+newID+'_dmb_w.mp4'
                
                return url
    print("video url 없음")
    return 0


import urllib.parse

def check_and_encode_for_url(txt):
    return urllib.parse.quote(txt)

if __name__ == "__main__":
    url = "한글/샘플"
    res = check_and_encode_for_url(url)
    print(res)

    print(urllib.parse.unquote(res))