from . import login_bule
from flask import render_template


@login_bule.route('/login')
def login():
    """用户登录注册"""
    return render_template('admin/login.html')