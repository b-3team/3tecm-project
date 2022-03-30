from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

# 버킷리스트 저장하기
@app.route('/save', methods=['POST'])
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

    return jsonify({'msg': '버킷리스트가 저장되었습니다!'})

#버킷리스트 보여주기
@app.route('/bucket', methods=['GET'])
def read_reviews():
    buckets = list(db.bucketlist.find({}, {'_id': False}))
    return jsonify({'all_buckets': buckets})

#버킷리스트 삭제하기
@app.route('/bucket', methods=['DELETE'])
@login_required
def delete_reviews():
    name_receive = request.form['title_give']
    db.bucketlist.delete_one({'title': name_receive})
    return jsonify({'msg': '버킷리스트가 삭제되었습니다!'})


#내용(content) 변경
@app.route('/bucket', methods=['PUT'])
@login_required
def change_content():
    content_receive = request.args.get('content')
    db.bucketlist.update_one({'user_id': request.user_id}, {'$set': {'content': content_receive}})
    return jsonify({'result': 'success', 'msg': '내용 변경완료 했습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)