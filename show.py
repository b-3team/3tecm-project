from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/first')
def go_bucket():
    return render_template('write.html')

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