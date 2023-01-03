from flask import Flask

app = Flask(__name__)
@app.route('/')
@app.route('/home')
def home():
    return "sibal"
@app.route('/user/<user_name>/<int:user_id>')
def user(user_name, user_id):
    return f'Hello, {user_name}({user_id})!'
'''
http://127.0.0.1:5000/ 뒤에 “/home”이라고 붙여도 동일하게 헬로 월드가 출력되는 페이지가 뜬다. 
“/”이나 “/home”이나 둘 다 같은 페이지를 출력하도록 연결했기 때문에. 
그리고 만약 “/user”로 접속하면 헬로 유저가 뜰 거다. 
Flask에서는 이렇게 쉽게 웹 페이지를 라우팅 할 수 있다
'''

if __name__ == '__main__':
    # app.run(debug=True) # debug=True : 해당 파일의 코드를 수정할 때마다 Flask가 변경된 것을 인식하고 다시 시작한다
    app.run()
''' 
실행을 하면 Running on http://127.0.0.1:5000/라는 메시지가 뜨는데 
로컬 환경에서 5000번 포트를 통해 해당 웹 페이지를 확인할 수 있다
'''