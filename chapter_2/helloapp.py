from bottle import Bottle, run

app = Bottle()

PAGES = """
<h2>サンプルページリスト</h2>
<ul>
    <li><a href='/helloapp/you/Shimizu'>Shimizuさん</a></li>
    <li><a href='/helloapp/you/Numazu'>Numazuさん</a></li>
    <li><a href='/helloapp/show/1'>商品1</a></li>
    <li><a href='/helloapp/show/3'>商品3</a></li>
</ul>
"""

@app.route('/helloapp')
def index():
    return('<h1>こんにちはボトルさん</h1>'+PAGES)

@app.route('/helloapp/you/<name>')
def yourname(name):
    return('Your name is :<b>%s</b>'%name)

def get_product(id):
    products =['デスクトップ', 'ノート', 'タブレット', 'スマートフォン']
    return products[id]

@app.route('/helloapp/show/<id>')
def show_product(id):
    true_id = int(id)
    return ('<b>%s</b>をお探しですか'%get_product(true_id))

run(app, host='localhost', port=8782, reloader=True)