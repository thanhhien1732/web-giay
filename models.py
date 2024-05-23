from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from __init__ import app, db
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum

# Lớp cơ sở cho tất cả các model, chứa trường ID chung
class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

# Enum định nghĩa vai trò của người dùng
class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

# Model đại diện cho người dùng
class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name

# Model đại diện cho danh mục sản phẩm
class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(20), nullable=False)
    products = relationship('Product', back_populates='category', lazy=True)

    def __str__(self):
        return self.name

# Model đại diện cho sản phẩm
class Product(BaseModel):
    __tablename__ = 'product'

    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    receipt_details = relationship('ReceiptDetail', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)

    category = relationship('Category', back_populates='products', lazy=True)

    def __str__(self):
        return self.name

# Model đại diện cho bình luận
class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    create_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.content

# Model đại diện cho hóa đơn
class Receipt(BaseModel):
    create_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)

# Liên kết giữa sản phẩm và hóa đơn, lưu chi tiết hóa đơn
class ReceiptDetail(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)

# Tạo bảng và cơ sở dữ liệu nếu chạy script này
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
