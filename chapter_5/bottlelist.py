import sqlite3
from bottle import post, get, request, route, run, template

### データベースの作成と確認(最初のみ)
@route('/blist/init')
def init():
    drop_tb = 'DROP TABLE IF EXISTS bottles'
    create_tb = 'CREATE TABLE bottles(' + \
        'id INTEGER PRIMARY KEY AUTOINCREMENT, ' + \
        'name TEXT NOT NULL, ' + \
        'material TEXT NOT NULL, ' + \
        'color TEXT NOT NULL, ' + \
        'ml INTEGER NOT NULL, ' + \
        'price INTEGER NOT NULL)'
    
    con = sqlite3.connect('bottles.db')
    cur = con.cursor()
    cur.execute(drop_tb)
    cur.execute(create_tb)
    insert(cur, 'アイスピッチャー', 'ガラス', '透明', 2000, 1200)
    con.commit()

    blist = select_all(cur)
    con.close()

    if len(blist) > 0:
        tplt = """
            <p>テーブルbottlesを作成しました</p>
            <p>
            %for cell in blist[-1]:
            {{cell}},
            %end
            </p>
        """
        return template(tplt, blist=blist)
    return ('初期化失敗')

@get('/blist/new')
def new():
    tplt = """
        <h1>データの新規作成</h1>
        <form action='/blist/new' method='POST'>
        %s
        </form>
    """ % form_template()

    return template(tplt, clms=CLMS)

@post('/blist/new')
def added_new():
    name = request.forms.getunicode('name')
    material = request.forms.getunicode('material')
    color = request.forms.getunicode('color')
    ml = request.forms.get('ml')
    price = request.forms.get('price')

    con = sqlite3.connect('bottles.db')
    cur = con.cursor()

    insert(cur, name, material, color, ml, price)
    con.commit()

    blist= select_all(cur)
    con.close() 

    tplt = """
        <h1>データを保存しました</h1>
        <p>
        %for cell in blist[-1]:
        {{cell}},
        %end
        </p>
    """
    return template(tplt, blist=blist)

### テンプレート関係
CLMS = [('name', '商品名'), ('material', '材質'), ('color', '色'), ('ml', '容量(ml)'), ('price', '価格(円)')]

def form_template():
    tplt = """
        %for i in range(len(clms)):
            <p><label for='{{clms[i][0]}}'>{{clms[i][1]}}:</label>
            <input type='text' id='{{clms[i][0]}}' name='{{clms[i][0]}}' size='20'>
            </p>
        %end
        <input type='submit' value='GO'>
    """
    return tplt

### データベース操作
# 新規作成
def insert(cur: sqlite3.Cursor, name: str, material: str, color: str, ml: int, price: int):
    insert_str = 'INSERT INTO bottles(name, material, color, ml, price) VALUES (?, ?, ?, ?, ?)'
    cur.execute(insert_str, (name, material, color, ml, price))

# 全選択
def select_all(cur: sqlite3.Cursor) -> list:
    select_str = 'SELECT * FROM bottles'
    cur.execute(select_str)
    return cur.fetchall()

# Webサーバの起動
run(host='localhost', port=8782, reloader=True)