from flask import Flask, render_template, jsonify, request,session
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML 화면 보여주기
@app.route('/')
def login_form():
    return render_template('index.html')

# 로그인(POST) API
@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        if(request.form['id'] == 'admin' and request.form['pw'] == 'admin123'):
            session['login'] = True
            session['user'] = request.form['id']
            return 'Hi, ' + request.form['id']
        else:
            return """<script>alert("로그인이 실패되었습니다!");location.href='/';</script>"""
    else:
        return """<script>alert("not allowd!");location.href='/';</script>"""

        app.secret_key = 'sample_secret'

        user = db.id.find_one({'user_id': user_id}, {'user_pwd': user_pw})
        if user is None:
            return jsonify({'login': False})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)