from flask import Flask  # 从flask包中导入Flask类
app = Flask(__name__)    # 实例化这个类,创建一个程序对象app


@app.route('/')  # 装饰器来为这个函数绑定对应的 URL 装饰器
def hello():             # 定义hello函数
    return '<h1>Hello Totoro!</h1><img src="http:helloflask.com/totoro.gif">'  # 返回字符串
