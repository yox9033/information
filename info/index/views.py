from info import constants
from info.models import User,News,Category
from info.utils.response_code import RET
from . import index_blue
from flask import render_template, current_app,session,request,jsonify
import logging



@index_blue.route("/news_list")
def get_news_list():
    """获取新闻列表数据"""
    # 分类id
    cid = request.args.get("cid")
    # 页数
    page = request.args.get("page",1)
    # 每页显示数据条数
    per_page = request.args.get("per_page",10)
    try:
        cid = int(cid)
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        cid = 1
        page = 1
        per_page = 10

    # 根据发布时间获取新闻分页paginate
    # if cid ==1:
    #     paginate = News.query.order_by(News.create_time.desc()).paginate(page, per_page, False)
    # else:
    #     paginate = News.query.filter(News.category_id ==cid).order_by(News.create_time.desc()).paginate(page, per_page, False)
    filter = []
    if cid != 1:
        filter.append(News.category_id ==cid)
    paginate = News.query.filter(*filter).order_by(News.create_time.desc()).paginate(page, per_page, False)

    # 获取到当前页面需要展示的数据
    items = paginate.items
    # 当前页数
    current_page = paginate.page
    # 总页数
    total_page = paginate.pages
    new_list = []
    for item in items:
        new_list.append(item.to_dict())

    data = {
        "current_page":current_page,
        "total_page":total_page,
        "news_dict_li":new_list
    }


    return jsonify(errno=RET.OK,errmsg="ok",data = data)













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
       new_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)
    click_news_list = []
    for news in new_list:
        click_news_list.append(news.to_dict()) if new_list else None

    # 新闻分类展示
    categorys = Category.query.all()
    categorys_list = [ ]
    for category in categorys:
        categorys_list.append(category.to_dict())
    data = {
        "user_info":user.to_dict() if user else None,
        "click_news_list": click_news_list,
        "categorys":categorys_list
    }

    return render_template("news/index.html",data = data)


@index_blue.route('/favicon.ico')
def send_img():
    """ 网站图标(favicon)展示"""
    return current_app.send_static_file('news/favicon.ico')
