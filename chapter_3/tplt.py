from bottle import route, run, template
from datetime import date
import random

PAGES = [
    ('today', '今日の日付'),
    ('calc/3', '3の2乗と2の3乗'),
    ('calc/5', '5の2乗と2の5乗'),
    ('colors', 'for文で色のリスト'),
    ('morecolors', 'コード埋め込みで乱数'),
    ('show1/2', 'if文、id2'),
    ('show1/4', 'if文、id4'),
    ('show2/0', 'if文埋め込み、id3'),
    ('show2/5', 'if文埋め込み、id4')
]

PAGES_TEMPLATE = """
<h1>第3章 テンプレート</h1>
<h2>サンプルページリスト</h2>
<ul>
%for page in PAGES:
    <li><a href='/tplt/{{page[0]}}'>{{page[1]}}</a></li>
%end
</ul>
"""

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

@route('/tplt/colors')
def showcolors():
    colors = ['赤', '黄', '青', '緑', '白', '黒', '茶']
    content = """
        <p>カラーリスト</p>
        <ul>
            %for color in colors :
                <li>{{color}}</li>
            %end
        </ul>
        おすすめの色は{{thiscolor}}
    """
    return template(content, colors = colors, thiscolor = random.choice(colors))

@route('/tplt/morecolors')
def showmore():
    content = """
        %import random
        %more = ['橙', '灰', '紫', '金', '銀']
        おすすめの色は{{random.choice(more)}}
    """
    return template(content)

@route('/tplt/show1/<id>')
def show_product1(id):
    products = ['Tシャツ', 'ズボン', 'ワンピース', 'スーツ']
    id = int(id)
    content = 'お探しの商品は<br>'
    if(id < len(products)):
        return template(content + '<b>{{product}}</b>ですね', product = products[id])
    return content + '<b>ありません</b>'

@route('/tplt/show2/<id>')
def show_product2(id):
    products = ['フライパン', 'まな板', '包丁', 'やかん']
    id = int(id)
    content = """
        お探しの商品は<br>
        %if id < len(products):
            <b>{{products[id]}}</b>ですね
        %else:
            <b>ありません</b>
        %end
    """
    return template(content, id = id, products = products)

@route('/tplt')
def index():
    return template(PAGES_TEMPLATE, PAGES=PAGES)

run(host='localhost', port=8782, reloader=True)