from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.MovieDB

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/rating', methods=['POST'])
def give_rate():
    # rate_receive 클라이언트가 준 rate 가져오기
    rate_receive = request.form['rate_give']
    # movieid_receive 클라이언트가 준 movieid 가져오기
    movieid_receive = request.form['movieid_give']

    # DB에 삽입할 rating 만들기
    rate = {
        'rate': rate_receive,
        'movieid': movieid_receive
        #,'userid'
    }
    # reviews에 review 저장하기
    db.User.insert_one(rate)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '별점저장 완료😎'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)