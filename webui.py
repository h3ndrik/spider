import json
from bottle import Bottle, run, template, static_file, TEMPLATE_PATH
from bottle import route, request, response, abort
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext import serializer
import logging
from spider.models import *

app = Bottle()

engine = create_engine('sqlite:///spider.db')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

@app.route('/')
def index():
    return template('index', title='Spider Search')

@app.route('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root='./webui/img')

#@app.route('/search/')
#@app.route('/suche/<query>')
#def suche():
#    q = request.query.q or ''
#    start = request.query.start or 1
#    num = request.query.num or 10
#    result = session.query(Files).filter(Files.filename.like('%'+q+'%')).all()
#    return template('make_table', rows=result)

#@app.route('/show/<id:int>')
#def show(id=None):
#    assert isinstance(id, int)
#    return "Not implemented!"

@app.route('/api/search/')
def api_search():
    q = request.query.q
    #q_test = request.GET.get('q', '').strip()
    start = int(request.query.start or 0)
    num = int(request.query.num or 20)
    result = session.query(Files).filter(Files.filename.like('%'+q+'%'))
    if result:
        print('Query \"' + q + '\" Returned ' + str(result.count()) + ' results')
        return {'num_results': str(result.count()), 'results': [file._asdict() for file in result[start:start+num]]}
    else:
        abort(400, 'Query \"' + q + '\" Returned no results')

@app.route('/api/new/')
def api_new():
    start = int(request.query.start or 0)
    num = int(request.query.num or 20)
    result = session.query(Files).order_by(Files.mtime)
    if result:
        return {'num_results': str(result.count()), 'results': [file._asdict() for file in result[start:start+num]]}
    else:
        abort(400, 'Nothing found')

@app.route('/js/<filename>')
def js_static(filename):
    return static_file(filename, root='./webui/js')

@app.route('/img/<filename>')
def img_static(filename):
    return static_file(filename, root='./webui/img')

@app.route('/css/<filename>')
def img_static(filename):
    return static_file(filename, root='./webui/css')

TEMPLATE_PATH.insert(0,'webui/views/')
run(app, host='localhost', port=8080, debug=True, reloader=True)
