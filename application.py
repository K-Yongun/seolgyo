import requests, json
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup as bs
from datetime import datetime

식단표 = {}
pre_date =""

def do_crawling():    
    global 식단표
    p = requests.get('http://portal.snue.ac.kr/enview/2015/food.jsp')
    soup = bs(p.text, "html.parser")
    t = soup.select('tr>td')
    
    for i in range(0, len(t), 5):
        요일 = t[i].text[0]
        날짜 = t[i].text[1:]
        아침 = t[i + 1].text.split()
        점심 = t[i + 2].text.split()
        저녁 = t[i + 3].text.split()
        교직원 = t[i + 4].text.split()
        식단표[날짜] = {}
        식단표[날짜]['아침'] = 아침
        식단표[날짜]['점심'] = 점심
        식단표[날짜]['저녁'] = 저녁
        식단표[날짜]['교직원'] = 교직원
        식단표[날짜]['요일'] = 요일


def 메뉴보기(날짜, 구분):
    출력 =  "\n★{0}({1})의 {2} 식단표★\n".format(날짜, 식단표[날짜]["요일"], 구분)
    출력 += "\n".join(식단표[날짜][구분])
    return 출력


application = Flask(__name__)

@application.route('/')
def index():
    return "Hello world!"


@application.route('/message', methods=['POST'])
def message():
    global pre_date
    mon = str(datetime.today().month)
    day = str(datetime.today().day)
    if len(mon) == 1:
        mon = "0" + mon
    if len(day) == 1:
        day = "0" + day
    date = mon + "/" + day
    req = request.get_json()
    menu = req["userRequest"]["utterance"]
    if date!=pre_date:
        do_crawling()
    pre_date=date    
    t = 메뉴보기(date, menu)
    res = {
        "timezone": "Asia/Seoul",
        "lang": "kr",
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": t
                    }
                }
            ]
        }
    }
    return jsonify(res)


if __name__ == '__main__':
    application.run(host='127.0.0.1', port=5000)