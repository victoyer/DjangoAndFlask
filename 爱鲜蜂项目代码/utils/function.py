import random


def get_ticket():
    s = 'qwertyuiopasdfghjkl1234567890zxcvbnmSGHKNJLKMXCVBN'
    ticket = ''
    for i in range(30):
        ticket += random.choice(s)
    ticket = 'TK_' + ticket
    return ticket


def get_order_random_id():
    s = 'qwertyuiopasdfghjkl1234567890zxcvbnmSGHKNJLKMXCVBN'
    order_num = ''
    for i in range(30):
        order_num += random.choice(s)

    return order_num
