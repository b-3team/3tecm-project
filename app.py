from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('putinfo_page.html')

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