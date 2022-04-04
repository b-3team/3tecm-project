from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')

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

#내용 수정하기
@app.route('/bucket', methods=['POST'])
def like_star():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg': 'like 연결되었습니다!'})

#삭제하기
@app.route('/show', methods=['POST'])
def delete_star():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg': 'delete 연결되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)