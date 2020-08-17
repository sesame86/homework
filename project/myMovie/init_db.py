import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.MovieDB


# DB에 저장할 영화인들의 출처 url을 가져옵니다.
def get_urls():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://api.themoviedb.org/3/movie/550?api_key=a338932a06b8f07fb4c5638b91007531', headers=headers)

    soup = BeautifulSoup(data.text, 'json.parser')

    trs = soup.select('#old_content > table > tbody > tr')

    urls = []
    for tr in trs:
        a = tr.select_one('td.title > div.tit5 > a')
        if a is not None:
            base_url = 'https://www.themoviedb.org/'
            url = base_url + a['href']
            urls.append(url)

    return urls


# 출처 url로부터 영화인들의 사진, 이름, 최근작 정보를 가져오고 mystar 콜렉션에 저장합니다.
def insert_movies(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a').text
    img_url = soup.select_one('#content > div.article > div.mv_info_area > div.poster > a > img')['src']

    doc = {
        'title': title,
        'img_url': img_url,
        'url': url,
    }

    db.tmdbmovies.insert_one(doc)
    print('완료!', title)


# 기존 mystar 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    db.tmdbmovies.drop()  # mystar 콜렉션을 모두 지워줍니다.
    urls = get_urls()
    for url in urls:
        insert_movies(url)


### 실행하기
insert_all()