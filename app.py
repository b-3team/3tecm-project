from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import jwt

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## 로그인 페이지
@app.route('/')
def login_form():
    return render_template('new_login.html')

#메인 페이지
@app.route('/login')
def login():
    return render_template('mybucklist_page.html')

#회원가입 페이지
@app.route('/join')
def join():
    return render_template('join.html')

#회원가입
@app.route('/api/join', methods=['POST'])
def api_join():
    #회원정보 생성
        userid_receive = request.form['userid_give']
        username_receive = request.form['username_give']
        userday_receive = request.form['userday_give']
        usersex_receive = request.form['usersex_give']
        useremail_receive = request.form['useremail_give']


        doc = {
            'userid': userid_receive,
            'username': username_receive,
            'userday': userday_receive,
            'usersex': usersex_receive,
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
    return render_template('putinfo_page.html')

# 저장하기
@app.route('/bucket', methods=['POST'])
def write_bucket():
    title_receive = request.form['title_give']
    heart_receive = request.form['heart_give']
    difficulty_receive = request.form['difficulty_give']
    photo_receive = request.form['photo_give']
    photo1_receive = request.form['photo1_give']
    photo2_receive = request.form['photo2_give']
    period_Y_receive = request.form['period_Y_give']
    period_M_receive = request.form['period_M_give']
    exampleFormControlTextarea1_receive = request.form['exampleFormControlTextarea1_give']

    doc = {
        'title':title_receive,
        'heart':heart_receive,
        'difficulty':difficulty_receive,
        'photo':photo_receive,
        'photo1':photo1_receive,
        'photo2':photo2_receive,
        'period_Y':period_Y_receive,
        'period_M':period_M_receive,
        'exampleFormControlTextarea1':exampleFormControlTextarea1_receive
    }

    db.mybucket.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

# 보여주기
@app.route('/show', methods=['GET'])
def show_bucket():
    bucket_list = list(db.mybucket.find({}, {'_id': False}).sort('difficulty', -1))
    return jsonify({'bucket_lists': bucket_list})

#내용(exampleFormControlTextarea1) 수정하기
@app.route('/show/change', methods=['POST'])
def change_bucket():
    title_receive = request.form['title_give']
    target_bucket = db.mybucket.find_one({'title': title_receive})
    current_content = target_bucket['exampleFormControlTextarea1']

    new_content = current_content.replace("", "",1)

    db.mybucket.update_one({'title': title_receive}, {'$set': {'exampleFormControlTextarea1': new_content}})
    return jsonify({'msg': '내용이 수정되었습니다!'})

#삭제하기
@app.route('/show/delete', methods=['POST'])
def delete_bucket():
    title_receive = request.form['title_give']
    db.mybucket.delete_one({'title': title_receive})
    return jsonify({'msg': '버킷리스트가 삭제되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)