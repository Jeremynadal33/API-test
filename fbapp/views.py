from flask import Flask, render_template, url_for, request

app = Flask(__name__)

app.config.from_object('config')

def _nothing(x):
    return x
from .utils import *

@app.route('/')
@app.route('/index/')
def index():
    if 'qtitle' in request.args :
        qtitle = request.args.get('qtitle')
    else :
        qtitle = ""

    if 'qcontent' in request.args :
        qcontent = request.args.get('qcontent')
    else :
        qcontent = ""

    if qcontent != "":
        results = "Results : "+str(predict_tags(body = qcontent, title = qtitle))
        hide_result = ""
    elif qtitle != "" or (qcontent == "" and 'qcontent' in request.args):
        results = "Please enter a question content "
        hide_result = ""
    else :
        results = ""
        hide_result = "hidden"
    random_url = url_for('index',random="random", _external = True)

    if 'random' in request.args:
        qtitle, qcontent, results = find_content()

        results = "Results : " + str(results)
        hide_result = ""
    return render_template('index.html',
                           qtitle = qtitle,
                           qcontent = qcontent,
                           results = results,
                           hide_result = hide_result,
                           random_url = random_url)
