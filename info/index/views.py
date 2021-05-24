from . import index_blue
from flask import render_template, current_app
import logging

@index_blue.route('/')
def index():
    """首页"""
    return render_template('news/index.html')


@index_blue.route('/favicon.ico')
def send_img():
    """ 网站图标(favicon)展示"""
    return current_app.send_static_file('news/favicon.ico')
