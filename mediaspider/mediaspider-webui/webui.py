import os
import json
from bottle import Bottle, run, template, static_file, TEMPLATE_PATH
from bottle import route, request, response, abort
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext import serializer
from sqlalchemy import or_
import logging
from mediaspider.models import *
from mediaspider.helper import size2human, timestamp2human
import re
from time import sleep
from configparser import SafeConfigParser

app = Bottle()

database = 'sqlite:///spider.db'
title = 'Spider Search'
host = '0.0.0.0'  # 'localhost'
port = 8080
debug = False
datapath_sub = dict()
search_path = ['/etc', '']
for path in search_path:
    candidate = os.path.join(path, 'spider.conf')
    if os.path.isfile(candidate):
        try:
            config = SafeConfigParser()
            config.read([candidate])
            database = config.get('Spider', 'database')
            title = config.get('WebUI', 'title')
            host = config.get('WebUI', 'host')
            port = config.getint('WebUI', 'port')
            debug = config.getboolean('WebUI', 'debug')
            #datapathsub = list(filter(None, [x.strip() for x in datapath_regexps.splitlines()]))
        except:
            pass
        datapath_sub = dict()
        try:
            datapath_sub = config.items('datapath_substitutions')
        except:
            pass

engine = create_engine(database)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

@app.route('/')
def index():
    return template('index', title=title)

@app.route('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root='./webui/img')

@app.route('/search/')
@app.route('/suche/')
@app.route('/search')
@app.route('/suche')
def suche():
    q = request.query.q
    start = int(request.query.start or 0)
    num = int(request.query.num or 20)
    return template('index', title=title, results=api_search(start=start, num=num, q=q), q=q)

@app.route('/new/')
@app.route('/neues/')
@app.route('/new')
@app.route('/neues')
def neues():
    start = int(request.query.start or 0)
    num = int(request.query.num or 20)
    return template('index', title=title, results=api_new(start=start, num=num))

@app.route('/detail/<id:int>')
def detail(id=None):
    return template('index', title=title, filedetail=api_detail(id))

@app.route('/api/detail/<id:int>')
def api_detail(id=None):
    assert isinstance(id, int)
    filedetail = session.query(Files).filter(Files.id == id).one()._asdict()
    if filedetail['mime'] == 'directory':
        filechildrenorm = session.query(Files).filter(Files.filename.like(filedetail['filename']+'/%')).filter(~Files.filename.like(filedetail['filename']+'/%/%')).all()
        # TODO: limit!
        filechildren = [child._asdict() for child in filechildrenorm]
    else:
        filechildren = None
    filemeta = [meta._asdict() for meta in session.query(Metadata).filter(Metadata.id == id)]
    filedetail['link'] = filedetail['filename']
    for path, subst in datapath_sub:
        filedetail['link'] = re.sub(r'^'+path, subst, filedetail['link'])
    for meta in filemeta:
        meta['coverlink'] = meta['cover']
        for path, subst in datapath_sub:
            if meta['coverlink']:
                meta['coverlink'] = re.sub(r'^'+path, subst, meta['coverlink'])
    return {'detail': filedetail, 'meta': filemeta, 'children': filechildren}

@app.route('/api/search/')
def api_search(q=None, start=None, num=None):
    if not q:
        q = request.query.q
        #q_test = request.GET.get('q', '').strip()
    if not start:
        start = int(request.query.start or 0)
    if not num:
        num = int(request.query.num or 20)
    if q == '':
        return {'num_results':0, 'start':start, 'num':num, 'results': []}
    else:
        q = re.sub(r' ', '%', q)
        result = session.query(Files).filter(Files.filename.like('%'+q+'%'))
    if result:
        print('Query \"' + q + '\" Returned ' + str(result.count()) + ' results')
        filedetail = [file._asdict() for file in result[start:start+num]]
        for file in filedetail:
            file['link'] = file['filename']
            for path, subst in datapath_sub:
                file['link'] = re.sub(r'^'+path, subst, file['link'])
        return {'num_results': result.count(), 'start':start, 'num':num, 'results': filedetail}
    else: # TODO isn't reached?!
        abort(400, {'num_results': '0'})

@app.route('/api/new/')
def api_new(start=None, num=None):
    if not start:
        start = int(request.query.start or 0)
    if not num:
        num = int(request.query.num or 20)
    result = session.query(Files).order_by(Files.mtime.desc())
    if result:
        filedetail = [file._asdict() for file in result[start:start+num]]
        for file in filedetail:
            file['link'] = file['filename']
            for path, subst in datapath_sub:
                file['link'] = re.sub(r'^'+path, subst, file['link'])
        return {'num_results': result.count(), 'start':start, 'num':num, 'results': filedetail}
    else:
        abort(400, 'Nothing found')

#@app.route('/file/<filename:path>')
#def file_static(filename):
#    return static_file(filename, root='/')

@app.route('/js/<filename:path>')
def js_static(filename):
    return static_file(filename, root='./js')

@app.route('/img/<filename:path>')
def img_static(filename):
    return static_file(filename, root='./img')

@app.route('/css/<filename:path>')
def img_static(filename):
    return static_file(filename, root='./css')

TEMPLATE_PATH.insert(0,'views/')
run(app, host=host, port=port, debug=debug, reloader=debug)
