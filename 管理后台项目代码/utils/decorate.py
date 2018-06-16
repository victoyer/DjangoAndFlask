from flask import session, redirect, url_for
from functools import wraps


# 验证访问者是否登录

def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id:
            return func(*args, **kwargs)

        else:
            return redirect(url_for('admin.login'))

    return check_login
