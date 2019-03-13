from flask import Flask,render_template,jsonify,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,and_

from datetime import datetime, timedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///E:/Py/Spider/info.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

bootstrap = Bootstrap(app)
db=SQLAlchemy(app)

class Info(db.Model):
    title=db.Column(db.String(255),nullable=False)
    content=db.Column(db.String(255),nullable=True)
    time=db.Column(db.String(255),nullable=False)
    source=db.Column(db.String(100),nullable=False)
    href=db.Column(db.String(255),nullable=False,primary_key=True)

def count():
    NOW = datetime.utcnow()
    last_24h_submits_count = []
    for h in range(1, 25):
        count = Info.query.filter(Info.time.between(NOW - timedelta(seconds=h * 3600 - 1), NOW - timedelta(hours=h - 1))).count()
        last_24h_submits_count.append(count)



@app.route('/')
def search():
    keyword = request.args.get('keyword')

    if keyword:
        data=[]
        keywords = keyword.split(' ')
        for k in keywords:
            page = request.args.get('page', 1, type=int)
            pagination = Info.query.filter(or_(Info.title.contains(k), Info.content.contains(k))).order_by(
                Info.time.desc()).paginate(page,max_per_page=15)
            data=data+pagination.items

        if pagination:
            return render_template('search.html', pagination=pagination,data=data,keyword=keyword)
        else:
            return render_template('notfind.html')
    else:
        return render_template('test1.html')



@app.route('/ipvm/')
def ipvm():
    page = request.args.get('page', 1, type=int)
    pagination = Info.query.filter_by(source='ipvm').order_by(Info.time.desc()).paginate(page,max_per_page=15)
    data = pagination.items
    #3return render_template("anquanke.html", pagination=pagination, data=data)
    return render_template('ipvm2.html', pagination=pagination, data=data)

@app.route('/anquanke/')
def anquanke():
    #return render_template('anquanke.html')
    page = request.args.get('page', 1, type=int)
    pagination = Info.query.filter_by(source='anquanke').order_by(Info.time.desc()).paginate(page,max_per_page=15)
    data = pagination.items
    return render_template("anquanke.html", pagination=pagination, data=data)

@app.route('/youshang/')
def youshang():
    hik=Info.query.filter_by(source='hik')
    yushi=Info.query.filter_by(source='uniview')
    return render_template('youshang.html',hik=hik,yushi=yushi)

@app.route('/360cert/')
def cert():
    page=request.args.get('page',1,type=int)
    pagination=Info.query.filter(Info.source=="360cert").order_by(Info.time.desc()).paginate(page,max_per_page=15)
    data=pagination.items
    return render_template("360cert.html",pagination=pagination,data=data)


# @app.route('/mail/')
# def send_mail():
#     pass


if __name__ == '__main__':
    app.run()
