# 验证访问者是否登录
from flask import session, redirect, url_for
from functools import wraps


def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login'))

    return check_login
