from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/bucket', methods=['POST'])
def write_review():
    title_receive = request.form['title_give']
    heart_receive = request.form['heart_give']
    difficulty_receive = request.form['difficulty_give']
    photo_receive = request.form['photo_give']
    period_receive = request.form['period_give']
    content_receive = request.form['content_give']

    doc = {
        'title':title_receive,
        'heart':heart_receive,
        'difficulty':difficulty_receive,
        'photo': photo_receive,
        'period': period_receive,
        'content': content_receive
    }

    db.bucketlist.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


@app.route('/bucket', methods=['GET'])
def read_reviews():
    buckets = list(db.bucketlist.find({}, {'_id': False}))
    return jsonify({'all_buckets': buckets})

@app.route('/bucket', methods=['POST'])
def delete_reviews():
    name_receive = request.form['title_give']
    db.bucketlist.delete_one({'name': name_receive})
    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)