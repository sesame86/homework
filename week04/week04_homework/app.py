from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/camp', methods=['POST'])
def add_List():
    # 1. 클라이언트로부터 데이터를 받기
    name = request.form['name']
    phone = request.form['phone']
    date = request.form['date']
    site = request.form['site']
    site_number = request.form['site_number']
    camp_data = {'name':name, 'phone':phone, 'date':date, 'site':site, 'site_number':site_number}

    # 2. mongoDB에 데이터 넣기
    client = MongoClient('localhost', 27017)
    camp = client.week04_homework.campsite

    camp.insert_one(camp_data)

    result = {'result': 'success', 'msg': '예약 완료'}
    return jsonify(result)


@app.route('/camp', methods=['GET'])
def read_List():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    client = MongoClient('localhost', 27017)
    camp = client.week04_homework.campsite

    # 2. camp 키 값으로 camp 정보 보내주기
    camp = list(camp.find({}, {'_id': False}))
    result = {'result': 'success', 'msg': camp}

    return jsonify(result)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
