import os

# 获取项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 获取templates的路径
templates_dir = os.path.join(BASE_DIR, 'templates')

# 获取static的路径
static_dir = os.path.join(BASE_DIR, 'static')

# 获取img路径
UPLOAD_DIR = os.path.join(static_dir, 'img')
