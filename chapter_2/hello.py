from bottle import route, run

PAGES = """
<h2>サンプルページリスト</h2>
<ul>
    <li><a href='/hello/you/Shimizu'>Shimizuさん</a></li>
    <li><a href='/hello/you/Numazu'>Numazuさん</a></li>
    <li><a href='/hello/show/1'>商品1</a></li>
    <li><a href='/hello/show/3'>商品3</a></li>
</ul>
"""

@route('/hello')
def index():
    return('<h1>こんにちはボトルさん</h1>'+PAGES)

@route('/hello/you/<name>')
def yourname(name):
    return('Your name is :<b>%s</b>'%name)

def get_product(id):
    products =['デスクトップ', 'ノート', 'タブレット', 'スマートフォン']
    return products[id]

@route('/hello/show/<id>')
def show_product(id):
    true_id = int(id)
    return ('<b>%s</b>をお探しですか'%get_product(true_id))

run(host='localhost', port=8782)