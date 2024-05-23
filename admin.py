from __init__ import app, db
from models import Category, Product, UserRole
from flask import redirect
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
import utils

# Tạo một lớp con của ModelView để xác thực người dùng
class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        # Kiểm tra xem người dùng đã đăng nhập và có quyền ADMIN hay không
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)
    
    action_disallowed_list = ['delete']

# Tạo một lớp con của AuthenticatedModelView để hiển thị thông tin sản phẩm trong giao diện admin
class ProductView(AuthenticatedModelView):
    # Đặt tên cho cột 'category' thành 'Category' để hiển thị trên trang quản trị
    column_labels = {'category': 'Category'}

    # Liệt kê các cột muốn hiển thị trong danh sách sản phẩm
    column_list = [ 'category', 'name', 'description', 'price', 'image', 'created_date', 'active']

    # Cho phép xem chi tiết sản phẩm
    can_view_details = True

    # Cho phép xuất dữ liệu ra file CSV
    can_export = True

    # Tìm kiếm sản phẩm theo tên và mô tả
    column_searchable_list = ['name', 'description']

    # Bộ lọc sản phẩm theo tên và giá
    column_filters = ['name', 'price']

    # Sắp xếp sản phẩm theo tên, giá và ngày tạo
    column_sortable_list = ['name', 'price', 'created_date']

    # Loại bỏ các cột không muốn hiển thị trong form sửa thông tin sản phẩm
    form_excluded_columns = ['receipt_details', 'comments']

    # Không cho phép thực hiện hành động 'delete' từ giao diện admin
    action_disallowed_list = ['delete']

    # Định dạng hiển thị giá sản phẩm
    def price_formatter(view, context, model, name):
        return "{:,.0f}".format(model.price)
    
    # Đặt định dạng hiển thị giá cho cột 'price'
    column_formatters = {
        'price': price_formatter
    }

    # Đặt tên cho các cột hiển thị
    column_labels = {
        'name': 'Tên SP',
        'description': 'Mô tả',
        'price': 'Giá',
        'image': 'Hình ảnh',
        'category': 'Danh mục',
        'created_date': 'Ngày tạo'
    }

# Tạo một lớp con của BaseView để xử lý việc đăng xuất
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        # Thực hiện việc đăng xuất và chuyển hướng về trang admin
        logout_user()
        return redirect('/admin')
    
    def is_accessible(self):
        # Kiểm tra xem người dùng đã đăng nhập hay chưa
        return current_user.is_authenticated

# Tạo một lớp con của AdminIndexView để tùy chỉnh trang chính của trang admin
class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        # Hiển thị trang chính với các thống kê về danh mục sản phẩm
        return self.render('admin/index.html', stats=utils.category_stats())

# Khởi tạo đối tượng Admin với các cấu hình và đối tượng được định nghĩa trước
admin = Admin(app=app, name="Administration", template_mode='bootstrap4', index_view=MyAdminIndex())

# Thêm các view của ModelView vào trang admin
admin.add_view(AuthenticatedModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session)) 
admin.add_view(LogoutView(name='Logout'))