from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.MovieDB

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_movies():
    # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    movies = list(db.naver_movies.find({}, {'_id': False}))
    result = {'result': 'success', 'msg': movies}
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify(result)

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