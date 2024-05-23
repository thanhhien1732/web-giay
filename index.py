from flask import render_template, request, redirect, session, url_for, jsonify
from __init__ import app, login
from admin import *
from flask_login import login_user, logout_user, login_required
from models import UserRole
import utils
import math
import cloudinary.uploader

@app.route("/")
def home():
    # Lấy thông tin từ URL
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    page = request.args.get('page', 1)

    # Tải danh sách sản phẩm và đếm tổng số sản phẩm
    products = utils.load_products(cate_id=cate_id, kw=kw, page=int(page))
    couter = utils.count_products()

    # Hiển thị trang chủ với danh sách sản phẩm và phân trang
    return render_template('index.html', products=products, pages=math.ceil(couter/app.config['PAGE_SIZE']))

@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method == 'POST':  
        # Lấy thông tin từ form đăng ký
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')    
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            # Kiểm tra mật khẩu và xử lý ảnh đại diện nếu có
            if password.strip() == confirm.strip():
                avatar = request.files.get('avatar')
                if avatar:
                    # Tải ảnh lên Cloudinary và lấy đường dẫn
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                # Thêm người dùng mới vào hệ thống
                utils.add_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
                
                # Chuyển hướng đến trang đăng nhập
                return redirect(url_for('user_signin'))
            else:
                err_msg = 'Mật khẩu không khớp!!!'
        except Exception as ex:
            err_msg = "Hệ thống đang có lỗi: " + str(ex)
            db.session.rollback()  # Rollback giao dịch nếu có lỗi

    # Hiển thị trang đăng ký với thông báo lỗi nếu có
    return render_template('register.html', err_msg=err_msg)

@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method == 'POST':
        # Lấy thông tin đăng nhập từ form
        username = request.form.get('username')
        password = request.form.get('password')

        # Kiểm tra đăng nhập và chuyển hướng đến trang chủ nếu thành công
        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            next = request.args.get('next', 'home')
            return redirect(request.args.get('next', url_for('home')))
        else:
            err_msg = 'Username or password không chính xác!!!'
    
    # Hiển thị trang đăng nhập với thông báo lỗi nếu có
    return render_template('login.html', err_msg=err_msg)

@app.route('/admin-login', methods=['post'])
def admin_signin():
    # Lấy thông tin đăng nhập quản trị từ form
    username = request.form.get('username')
    password = request.form.get('password')

    # Kiểm tra và đăng nhập quản trị
    user = utils.check_login(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    # Chuyển hướng đến trang quản trị
    return redirect('/admin')
    
@app.route('/user-logout')
def user_signout():
    # Đăng xuất người dùng và chuyển hướng đến trang đăng nhập
    logout_user()
    return redirect(url_for('user_signin'))

@app.context_processor
def common_response():
    # Context processor chia sẻ thông tin chung cho tất cả các template
    return {
        'categories': utils.load_categories(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }

@login.user_loader
def user_load(user_id):
    # Hàm được sử dụng bởi LoginManager để tải người dùng từ cơ sở dữ liệu
    return utils.get_user_by_id(user_id=user_id)

@app.route("/products")
def product_list():
    # Lấy thông tin từ URL để hiển thị danh sách sản phẩm
    cate_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    products = utils.load_products(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price)
    
    # Hiển thị trang danh sách sản phẩm
    return render_template('products.html', products=products)

@app.route("/products/<int:product_id>")
def product_detail(product_id):
    # Lấy thông tin sản phẩm và bình luận để hiển thị chi tiết sản phẩm
    product = utils.get_product_by_id(product_id)
    comments = utils.get_comments(product_id=product_id, page=int(request.args.get('page', 1)))

    # Hiển thị trang chi tiết sản phẩm
    return render_template('product_detail.html', product=product, comments=comments, 
                           pages=math.ceil(utils.count_comment(product_id=product_id)/app.config['COMMENT_SIZE']) )

@app.route("/api/add-cart", methods=['post'])
def add_to_cart():
    # Xử lý thêm sản phẩm vào giỏ hàng và trả về số lượng sản phẩm trong giỏ hàng
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')

    cart = session.get('cart')
    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))

@app.route('/api/update-cart', methods=['put'])
def update_cart():
    # Xử lý cập nhật số lượng sản phẩm trong giỏ hàng và trả về số lượng mới
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    cart = session.get('cart')
    if cart and id in cart:
        cart[id]['quantity'] = quantity
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))

@app.route('/api/delete-cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    # Xử lý xóa sản phẩm khỏi giỏ hàng và trả về số lượng sản phẩm mới
    cart = session.get('cart')

    if cart and product_id in cart:
        del cart[product_id]
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))

@app.route('/cart')
def cart():
    # Hiển thị trang giỏ hàng với thông tin số lượng sản phẩm trong giỏ
    return render_template('cart.html', stats=utils.count_cart(session.get('cart')))

@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    # Xử lý thanh toán và chuyển hướng về trang chủ sau khi thanh toán thành công
    try:
        utils.add_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})
    
    return jsonify({'code': 200})

@app.route('/api/comments', methods=['post'])
@login_required
def add_comment():
    # Xử lý thêm bình luận và trả về thông tin bình luận mới
    data = request.json
    content = data.get('content')
    product_id = data.get('product_id')

    try:
        c = utils.add_comment(content=content, product_id=product_id)
    except:
        return {'status': 404, 'err_msg': 'Chương trình đang bị lỗi!!!'}
    return {'status': 201, 'comment': {
        'id': c.id,
        'content': c.content,
        'create_date': c.create_date,
        'user': {
            'username': current_user.username,
            'avatar': current_user.avatar
        }
    }}

if __name__ == '__main__':
    app.run(debug=True)
