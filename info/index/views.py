from info.models import User,News
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
    # 点击排行数据展示
    new_list = None
    try:
       new_list = News.query.order_by(News.clicks.desc()).limit(10)
    except Exception as e:
        current_app.logger.error(e)
    click_news_list = []
    for news in new_list:
        click_news_list.append(news.to_dict()) if new_list else None




    data = {
        "user_info":user.to_dict() if user else None,
        "click_news_list": click_news_list
    }

    return render_template("news/index.html",data = data)


@index_blue.route('/favicon.ico')
def send_img():
    """ 网站图标(favicon)展示"""
    return current_app.send_static_file('news/favicon.ico')
