import json
from flask_bcrypt import Bcrypt
from __init__ import app, db
from models import Category, Product, User, Receipt, ReceiptDetail, UserRole, Comment
from flask_login import current_user
from sqlalchemy import func

# Hàm đọc nội dung từ file JSON
def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

# Hàm load danh sách các danh mục sản phẩm từ cơ sở dữ liệu
def load_categories():
    return Category.query.all()

# Hàm load danh sách sản phẩm từ cơ sở dữ liệu với các điều kiện tùy chọn
def load_products(cate_id=None, kw=None, from_price=None, to_price=None, page=1):
    products = Product.query.filter(Product.active.is_(True))

    if cate_id:
        products = products.filter(Product.category_id == cate_id)

    if kw:
        products = products.filter(Product.name.contains(kw))

    if from_price:
        products = products.filter(Product.price >= from_price)

    if to_price:
        products = products.filter(Product.price <= to_price)

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return products.slice(start, end).all()

# Hàm lấy thông tin chi tiết của một sản phẩm theo ID
def get_product_by_id(product_id):
    return Product.query.get(product_id)

# Hàm đếm số lượng sản phẩm
def count_products():
    return Product.query.filter(Product.active.is_(True)).count()

# Đối tượng Bcrypt để mã hóa mật khẩu
bcrypt = Bcrypt(app)

# Hàm thêm mới một người dùng vào cơ sở dữ liệu
def add_user(name, username, password, **kwargs):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(name=name.strip(), username=username.strip(), password=hashed_password, email=kwargs.get('email'), avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()

# Hàm kiểm tra đăng nhập của người dùng
def check_login(username, password, role=UserRole.USER):
    if username and password:
        user = User.query.filter_by(username=username.strip(), user_role=role).first()
        if user and bcrypt.check_password_hash(user.password, password.strip()):
            return user

# Hàm lấy thông tin người dùng theo ID
def get_user_by_id(user_id):
    return User.query.get(user_id)

# Hàm đếm số lượng sản phẩm trong giỏ hàng
def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += int(c['quantity']) * float(c['price'])

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }

# Hàm thêm mới một hóa đơn từ giỏ hàng
def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for c in cart.values():
            d = ReceiptDetail(receipt=receipt, product_id=c['id'], quantity=c['quantity'], unit_price=c['price'])

            db.session.add(d)

        db.session.commit()

# Hàm thống kê số lượng sản phẩm theo danh mục
def category_stats():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
        .join(Product, Category.id == Product.category_id, isouter=True)\
        .group_by(Category.id, Category.name).all()

# Hàm thêm mới một bình luận
def add_comment(content, product_id):
    c = Comment(content=content, product_id=product_id, user=current_user)

    db.session.add(c)
    db.session.commit()

    return c

# Hàm lấy danh sách bình luận của một sản phẩm
def get_comments(product_id, page=1):
    page_size = app.config['COMMENT_SIZE']
    start = (page - 1) * page_size

    return Comment.query.filter(Comment.product_id == product_id)\
        .order_by(-Comment.id).slice(start, start + page_size).all()

# Hàm đếm số lượng bình luận của một sản phẩm
def count_comment(product_id):
    return Comment.query.filter(Comment.product_id == product_id).count()
