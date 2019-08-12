# -*- coding: utf-8 -*-
import os
import sys

import click
from flask import Flask, render_template  # 从flask包中导入Flask类
from flask_sqlalchemy import SQLAlchemy

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)    # 实例化这个类,创建一个程序对象app
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    #全局的两个变量移到这个函数里
    name = 'QingYang Zhu'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.context_processor
def inject_user(): # 函数名称可以任意修改
    user = User.query.first()
    return dict(user=user) # 需要返回字典

@app.errorhandler(404)
def page_not_found(e):
	    return render_template('404.html'), 404


class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20)) # 名字
# P19 生成虚拟数据


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(60)) # 电影标题
    year = db.Column(db.String(4)) # 电影年份

@app.route('/')  # 装饰器来为这个函数绑定对应的 URL 装饰器
def index():             # 定义视图函数
    # user = User.query.first()  #读取用户记录
    movies = Movie.query.all() # 读取所有电影记录
    return render_template('index.html', movies=movies)  # 返回字符串
