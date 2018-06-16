from random import choice


def randomCode():
    # 自动生成ticket
    s = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for ch in range(30):
        code += choice(s)

    # 自生成cookie加上前置
    code = 'TK_' + code

    # 返回生成的cookie
    return code
