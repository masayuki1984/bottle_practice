from bottle import route, run, template
from datetime import date

@route('/tplt/today')
def showtoday():
    return template('今日の日付:<b>{{today}}</b>', today = date.today())

@route('/tplt/calc/<a>')
def calc(a):
    a = int(a)
    calctp = """
        <p>{{a}}の2乗は{{sq_a}}</p>
        <p>2の{{a}}乗は{{pw_a}}</p>
    """
    return template(calctp, a = a, sq_a = a*a, pw_a = 2**a)

run(host='localhost', port=8782, reloader=True)