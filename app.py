from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import jwt

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## 로그인 페이지
@app.route('/')
def login_form():
    return render_template('login.html')

#로그인 페이지
@app.route('/login')
def login():
    return render_template('main.html')

#회원가입 페이지
@app.route('/join')
def join():
    return render_template('join.html')

#회원가입
@app.route('/api/join', methods=['POST'])
def api_join():
    #회원정보 생성
        userid_receive = request.form['userid_give']
        password_receive = request.form['pw_give']
        username_receive = request.form['username_give']
        useremail_receive = request.form['useremail_give']


        doc = {
            'userid': userid_receive,
            'pw': password_receive,
            'username': username_receive,
            'useremail': useremail_receive,
        }

        db.bucketinfo.insert_one(doc)

        return jsonify({'msg': '가입완료!'})


# 아이디 중복확인 API
@app.route('/join/check_dup', methods=['POST'])
def check_dup():
    userid_receive = request.form['userid_give']
    exists = bool(db.user.find_one({"userid": userid_receive}))
    return jsonify({'result': 'success', 'exists': exists})

#로그인 기능
@app.route('/api/login', methods=['POST'])
def api_login():
    userid_receive =request.form['userid_give']
    password_receive = request.form['password_give']


    # id, 암호화된 pw 가지고 있는 유저 찾기.
    result = db.users.find_one({'userid': userid_receive, 'password': password_receive})
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

@app.route('/writebucket')
def write():
    return render_template('putinfo.html')


## API 역할을 하는 부분
@app.route('/review', methods=['POST'])
def write_review():
    title_receive = request.form['title_give']
    dateY_receive = request.form['dateY_give']
    dateM_receive = request.form['dateM_give']
    photo1_receive = request.form['photo1_give']
    photo2_receive = request.form['photo2_give']
    photo3_receive = request.form['photo3_give']
    text_receive = request.form['text_give']

    doc = {
        'title': title_receive,
        'dateY': dateY_receive,
        'dateM': dateM_receive,
        'photo1': photo1_receive,
        'photo2': photo2_receive,
        'photo3': photo3_receive,
        'text': text_receive
    }

    db.bucket.insert_one(doc)

    return jsonify({'msg': '게시 완료!'})


@app.route('/review', methods=['GET'])
def read_reviews():
    reviews =list(db.bucket.find({},{'_id':False}))
    return jsonify({'all_reviews': reviews})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)