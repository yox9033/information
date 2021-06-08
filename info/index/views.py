from info.models import User
from . import index_blue
from flask import render_template, current_app,session
import logging

@index_blue.route('/')
def index():
    """首页"""
    # 1.获取当前用户id
    user_id = session.get("user.id")
    user = None
    # 2.通过id获取用户信息
    if user_id:
        user = User.query.get(user_id)
    data = {
        "user_info":user.to_dict() if user else None
    }

    return render_template("news/index.html",data = data)


@index_blue.route('/favicon.ico')
def send_img():
    """ 网站图标(favicon)展示"""
    return current_app.send_static_file('news/favicon.ico')
