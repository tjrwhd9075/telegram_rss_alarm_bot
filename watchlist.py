import aiofile

async def read_file_asyn(filename):
    async with aiofile.AIOFile(filename, 'r', encoding = 'UTF-8') as f:
        contents = await f.read()
        contents = contents.split("\n")
        return contents



def get_querys(file, user_id=None):
    '''
    user_id is None -> return [전체쿼리] 
    user_id is not None -> return [유저에 해당하는 쿼리]
    '''
    with open(file, 'r', encoding = 'UTF-8') as f:
        querys = f.read().splitlines() 

    if user_id is None: #전체 쿼리 리턴
        return querys
    else: #유저id에 해당하는 라인만 리턴
        qs=[]
        for q in querys:
            if str(q.split(" ")[0]) == str(user_id):
                qs.append(q)

    return qs


async def get_querys_asyn(file, user_id=None):
    '''
    user_id is None -> return [전체쿼리] 
    user_id is not None -> return [유저에 해당하는 쿼리]
    '''

    querys = await read_file_asyn(file)

    if user_id is None: #전체 쿼리 리턴
        return querys
    else: #유저id에 해당하는 라인만 리턴
        qs=[]
        for q in querys:
            if str(q.split(" ")[0]) == str(user_id):
                qs.append(q)

    return qs

def find_query_line(txt, file):
    '''
    return T -> 행번호
    return F -> -1
    '''
    i = 0
    querys = get_querys(file)

    for i, query in enumerate(querys):
        if query == txt : return i # 몇번째 줄인지 리턴
    return -1

def del_query(name, file):
    '''
    return -> 0 (fail 목록에 없음) / 1 (true 삭제 완료)
    '''
    if find_query_line(name, file) < 0: #목록에 없습니다
        return 0

    else : #목록에 있습니다. 삭제합니다
        with open(file,'rt', encoding = 'UTF-8') as f: 
            querys=f.read().splitlines()

        querys.sort()

        with open(file,'w', encoding = 'UTF-8') as f: 
            for query in querys: 
                if query != name: # 같으면 건너뜀
                    f.write(query + '\n')
        return 1

def add_query(name, file):
    '''
    return -> 0 (fail 이미 목록에 있음) / 1 (true 추가 완료)
    '''
    querys = get_querys(file)
    for query in querys:
        if query == name : # 목록에 있습니다
            return 0 # 저장안하고 종료

    with open(file, 'a', encoding = 'UTF-8') as f:         # 목록에 없습니다. 추가합니다.")
        f.write(name + "\n") 
        return 1 # 저장함




#----------------------------------------------------------------------------------------------



def add_keyword(user_id, keyword, file):
    '''
    return -> 0 (fail 이미 목록에 있음) / 1 (true 추가 완료)
    '''
    user_id = str(user_id)
    querys = get_querys(file, user_id=user_id)
    for query in querys:
        if query == (user_id + " " + keyword) : # 목록에 있습니다
            return 0 # 저장안하고 종료

    with open(file, 'a', encoding = 'UTF-8') as f:         # 목록에 없습니다. 추가합니다.")
        f.write("\n"+user_id + " " + keyword) 
        return 1 # 저장함

def del_keyword(user_id, keyword, file):
    '''
    return -> 0 (fail 목록에 없음) / 1 (true 삭제 완료)
    '''
    txt = user_id + " " + keyword
    
    if find_query_line(txt, file) < 0: #목록에 없습니다
        return 0

    else : #목록에 있습니다. 삭제합니다
        with open(file,'rt', encoding = 'UTF-8') as f: 
            querys=f.read().splitlines()

        querys.sort()

        with open(file,'w', encoding = 'UTF-8') as f: #전부 저장하는데
            for query in querys: 
                if query != txt: # 삭제할 것과 같으면 건너뜀
                    f.write(query + '\n')
        return 1

def find_keyword_line(txt, file):
    '''
    찾으면 -> "user_id" + " " + "keyword"
    없으면 -> 0
    '''
    querys = get_querys(file)

    for query in querys:
        if query!="" and txt.find(query.split(" ")[1]) != -1 : #키워드와 같은 문자열이 존재하면
            return query
    return 0

def find_keyword_lines(txt, file):
    '''
    찾으면 -> list["user_id" + " " + "keyword", ...]
    없으면 -> []
    '''
    querys = get_querys(file)

    qs=[]
    for query in querys:
        if query!="" and txt.find(query.split(" ")[1]) != -1 : #키워드와 같은 문자열이 존재하면
            qs.append(query)
    return qs

async def find_keyword_lines_asyn(txt, file):
    '''
    찾으면 -> list["user_id" + " " + "keyword", ...]
    없으면 -> []
    '''
    try: 
        querys = await get_querys_asyn(file)
    except Exception as e:
            print("find_keyword_lines_asyn - get_querys_asyn error : ", end="")
            print(e)
    qs=[]
    try:
        for query in querys:
            if txt.find(query.split(" ")[1]) != -1 : #키워드와 같은 문자열이 존재하면
                qs.append(query)
    except Exception as e:
            print("find_keyword_lines_asyn - find same keyword error : ", end="")
            print(e)
    return qs
    
