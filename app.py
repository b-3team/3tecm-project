from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML 화면 보여주기
@app.route('/')
def login_form():
    return render_template('index.html')

##HTML 화면 보여주기2
@app.route('/join')
def join():
    return render_template('join.html')

##HTML 화면 보여주기3
@app.route('/login')
def login():
    return render_template('index.html')

#회원가입
@app.route('/api/join', methods=['POST'])
def api_join():
        userid_receive = request.form['userid_give']
        password_receive = request.form['password_give']
        password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
        username_receive = request.form['username_give']
        useremail_receive = request.form['useremail_give']

        doc = {
            'userid': userid_receive, #아이디
            'password': password_hash, #비밀번호
            'username': username_receive, #이름
            'useremail': useremail_receive, #이메일
        }
        db.users.insert_one(doc)

        return jsonify({'result': 'success','msg': '가입 완료!'})

#로그인 기능
@app.route('/api/login', methods=['POST'])
def api_login():
    userid_receive =request.form['userid_give']
    password_receive = request.form['password_give']

    # hash 기능으로 pw를 암호화한다.
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    # id, 암호화된 pw 가지고 있는 유저 찾기.
    result = db.users.find_one({'userid': userid_receive, 'password': pw_hash})
    # 찾으면 JWT 토큰 발급.
    if result is not None:
        payload = {
            'userid': userid_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=100)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        # 만든 토큰을 준다.
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'msg': '아이디 / 비밀번호가 일치하지 않습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)