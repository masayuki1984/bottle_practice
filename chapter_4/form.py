from bottle import get, post, request, route, run, template
import random

FRAMEWORKS = [
    ('Angular', 'TypeScript', 'https://angular.io/'),
    ('Bottle', 'Python', 'https://bottlepy.org/'),
    ('Flask', 'Python', 'https://flask.palletsprojects.com/'),
    ('Ruby on Rails', 'Ruby', 'https://rubyonrails.org/'),
    ('Spring Framework', 'Java', 'https://spring.io/'),
    ('Play Framework', 'Scala/Java', 'https://www.playframework.com/')
]

ADDFORM = """
    <div>
    <b>{{a}}</b> + <b>{{b}}</b> = 
    <form action = "/myform/addthem" method="POST">
        <input type = 'text' name = 'answer' size = '6' value = '0'>
        <input type = 'hidden' name = 'a' value = '{{a}}'>
        <input type = 'hidden' name = 'b' value = '{{b}}'>
        <input type = 'submit' value = 'Go'>
    </form>
    </div>
"""

@route('/myform/choose')
def choose_name():
    content = """
    <h1>Webフレームワーク選択</h1>
    <p>下のリストから選択してください</p>
    <form action = "/myform/show" method='POST'>
        <select name = 'framework'>
            %for i in range(len(FRAMEWORKS)):
                <option value= {{i}}>{{FRAMEWORKS[i][0]}}</option>
            %end
        </select>
        <input type = 'submit' value='確定'>
    </form>
    """

    return template(content, FRAMEWORKS=FRAMEWORKS)

@post('/myform/show')
def show_data():
    id = request.forms.get('framework')
    show = FRAMEWORKS[int(id)]
    content = """
    <div>
    <b>フレームワーク名: </b>{{show[0]}}<br>
    <b>言語: </b>:{{show[1]}}<br>
    <b>URL: </b><a href='{{show[2]}}' target='_blank'>
    {{show[2]}}</a>
    </div>
    <p><a href='/myform/choose'>選択画面に戻る</a>
    """

    return template(content, show = show)

@get('/myform/addthem')
def start_add():
    welcome = """
        <h1>4桁足し算練習プログラムにようこそ!</h1>
    """
    return template(welcome+ADDFORM, a = random.randint(1000, 9999), b = random.randint(1000, 9999))

@post('/myform/addthem')
def check_add():
    answer = int(request.forms.get('answer'))
    a = int(request.forms.get('a'))
    b = int(request.forms.get('b'))

    if answer == a+b:
        correct = """
            <h1>その通り!では次の問題</h1>
        """
        return template(correct+ADDFORM, a = random.randint(1000, 9999), b = random.randint(1000, 9999))
    failure = """
        <p>残念でしたもう一回</p>
    """
    return (template(failure+ADDFORM, a = a, b = b))

@route('/myform/cry')
def cry():
    cryform = """
        <h1>やまびこプロジェクト</h1>
        <p>何か叫んでください</p>
        <form action = '/myform/echo' method = 'post'>
            <p><input type = 'text' size = '20' name = 'cry' value = 'おーい'></p>
            <input type = 'submit' value = 'CRY'>
        </form>
    """
    return cryform

@post('/myform/echo')
def echo():
    cry = request.forms.getunicode('cry')
    echo = """
        <b>{{cry}}</b>
        %for i in range(len(cry)):
            <br>{{cry[i:]}}
        %end
        <p><a href='/myform/cry'>また叫ぶ</p>
    """
    return template(echo, cry=cry)

run(host='localhost', port=8782, reloader=True)