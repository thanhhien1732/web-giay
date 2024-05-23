from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
import pymysql

# Tạo một đối tượng Flask để khởi động ứng dụng
app = Flask(__name__)

# Thiết lập khóa bí mật để bảo mật ứng dụng
app.secret_key = '&^RY%Rghjgu756tu654'

# Thiết lập địa chỉ của cơ sở dữ liệu MySQL và một số cấu hình khác
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost/shoestore?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Thiết lập kích thước trang và kích thước bình luận cho ứng dụng
app.config['PAGE_SIZE'] = 12
app.config['COMMENT_SIZE'] = 5

# Thiết lập pymysql làm thay đổi để tương thích với MySQL
pymysql.install_as_MySQLdb()

# Khởi tạo đối tượng SQLAlchemy để làm việc với cơ sở dữ liệu
db = SQLAlchemy(app=app)

# Thiết lập cấu hình cho dịch vụ lưu trữ đám mây Cloudinary
cloudinary.config(
    cloud_name='dwgmes935',
    api_key='565359326669478',
    api_secret='EO_yXZ884mTKE1gv_5kydHFu8tw'
)

# Khởi tạo đối tượng LoginManager để quản lý việc đăng nhập trong ứng dụng
login = LoginManager(app=app)