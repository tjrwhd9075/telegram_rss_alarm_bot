
def get_querys(user_id, file):
    with open(file, 'r', encoding = 'UTF-8') as f:
        querys = f.read().splitlines() 

    qs=[]
    for q in querys:
        if str(q.split(" ")[0]) == str(user_id):
            qs.append(q)

    return qs

def find_query_line(name, file):
    '''
    return T -> 행번호
    return F -> -1
    '''
    i = 0
    querys = get_querys(file)

    for query in querys:
        i = i+1
        if query == name :
            return i
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
    keyword = keyword.upper()
    querys = get_querys(file)
    for query in querys:
        if query == (user_id + " " + keyword) : # 목록에 있습니다
            return 0 # 저장안하고 종료

    with open(file, 'a', encoding = 'UTF-8') as f:         # 목록에 없습니다. 추가합니다.")
        f.write(user_id + " " + keyword + "\n") 
        return 1 # 저장함

def del_keyword(user_id, keyword, file):
    '''
    return -> 0 (fail 목록에 없음) / 1 (true 삭제 완료)
    '''
    keyword = keyword.upper()
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
        if txt.find(query.split(" ")[1]) != -1 : #키워드와 같은 문자열이 존재하면
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
        if txt.find(query.split(" ")[1]) != -1 : #키워드와 같은 문자열이 존재하면
            qs.append(query)
    return qs