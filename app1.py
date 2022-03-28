
@app.route('/bucket', methods=['POST'])
def delete_reviews():
    name_receive = request.form['title_give']
    db.bucketlist.delete_one({'title': name_receive})
    return jsonify({'msg': '삭제 완료!'})