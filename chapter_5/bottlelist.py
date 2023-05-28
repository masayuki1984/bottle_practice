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

@route('/blist')
def get_list():
    con = sqlite3.connect('bottles.db')
    cur = con.cursor()
    blist = select_all(cur)
    con.close()

    tplt = """
        <h1>ボトルリスト</h1>
        <p><a href='/blist/new'>データを追加</a></p>
        <hr>
        <table>
        %for b in blist:
            <tr>
                <td>{{b[0]}}</td>
                <td><a href='/blist/{{b[0]}}'>{{b[1]}}</a></td>
            </tr>
        %end
        </table>
    """
    return template(tplt, blist=blist)

@get('/blist/new')
def new():
    tplt = """
        <h1>データの新規作成</h1>
        <form action='/blist/new' method='POST'>
        %s
        </form>
    """ % form_template()

    return template(tplt, clms=CLMS, btl=None)

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
    """ + detail_template()

    return template(tplt, clms = CLMS, btl=blist[-1])

@route('/blist/<id>')
def show_details(id):
    con = sqlite3.connect('bottles.db')
    cur = con.cursor()
    btl = select_by_id(cur, id)
    con.close()

    tplt = """
        <h1>データの詳細</h1>
    """ + detail_template()

    return template(tplt, clms = CLMS, btl = btl)

@get('/blist/update/<id>')
def update_it(id):
    con = sqlite3.connect('bottles.db')
    cur = con.cursor()
    btl = select_by_id(cur, id)
    con.close()

    tplt = """
        <h1>データid{{btl[0]}}のアップデート</h1>
        <form action = '/blist/updated/{{btl[0]}}' method = 'POST'>
        %s
        </form>
        <hr>
        <p><a href='/blist'>一覧に戻る</a></p>
    """ % form_template()

    return template(tplt, clms=CLMS, btl=btl)

@post('/blist/updated/<id>')
def updated(id):
    name = request.forms.getunicode('name')
    material = request.forms.getunicode('material')
    color = request.forms.getunicode('color')
    ml = request.forms.get('ml')
    price = request.forms.get('price')

    con = sqlite3.connect('bottles.db')
    cur = con.cursor()
    update(cur, id, name, material, color, ml, price)
    con.commit()

    btl = select_by_id(cur, id)
    con.close()

    tplt = """
        <h1>データを更新しました</h1>
    """ + detail_template()

    return template(tplt, clms=CLMS, btl=btl)

@route('/blist/delete/<id>')
def delete_it(id):
    tplt = """
        <h1>データid{{id}}の削除</h1>
        <h2>本当に削除しますか？この操作は取り消せません</h2>
        <p><a href='/blist/deleted/{{id}}'>永遠に削除する</a></p>
        <p><a href='/blist/update/{{id}}'>更新だけする</a></p>
        <p><a href='/blist'>何もせず一覧に戻る</a></p>
    """
    return template(tplt, id=id)

@route('/blist/deleted/<id>')
def deleted(id):
    con = sqlite3.connect('bottles.db')
    cur = con.cursor()
    delete(cur, id)
    con.commit()
    con.close()

    htmlstr = """
        <h1>データを削除しました</h1>
        <p><a href='/blist'>一覧に戻る</a></p>
    """
    return htmlstr

### テンプレート関係
CLMS = [('name', '商品名'), ('material', '材質'), ('color', '色'), ('ml', '容量(ml)'), ('price', '価格(円)')]

def form_template():
    tplt = """
        %for i in range(len(clms)):
            <p><label for='{{clms[i][0]}}'>{{clms[i][1]}}:</label>
            <input type='text' id='{{clms[i][0]}}' name='{{clms[i][0]}}'
            %if btl:
                value='{{btl[i+1]}}'
            %end
            size='20'>
            </p>
        %end
        <input type='submit' value='GO'>
    """
    return tplt

def detail_template():
    tplt = """
        <p><b>id: </b>{{btl[0]}}</p>
        %for i in range(len(clms)):
            <p><b>{{clms[i][1]}}: </b>{{btl[i+1]}}</p>
        %end
        <hr>
        <p><a href='/blist'>一覧に戻る</a></p>
        <p><a href='/blist/update/{{btl[0]}}'>データを更新</a></p>
        <p><a href='/blist/delete/{{btl[0]}}'>データを削除</a></p>
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

# 1件選択
def select_by_id(cur, id):
    select_str = 'SELECT * FROM bottles WHERE id = ?'
    cur.execute(select_str, id)
    return cur.fetchone()

# 更新
def update(cur, id, name, material, color, ml, price):
    upd_str = 'UPDATE bottles SET name=?, material=?, color=?, ml=?, price=? WHERE id = ?'
    cur.execute(upd_str, (name , material, color, ml, price, id))

# 削除
def delete(cur, id):
    delete_str = 'DELETE FROM bottles WHERE id = ?'
    cur.execute(delete_str, id)

# Webサーバの起動
run(host='localhost', port=8782, reloader=True)