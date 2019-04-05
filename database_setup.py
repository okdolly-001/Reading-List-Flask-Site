from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask import Flask
from flask_login import UserMixin

app = Flask(__name__)
Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    email = Column(String(250))
    picture = Column(String(250))
    book_categories = relationship("BookCategory",  back_populates="user")
    books = relationship("Book", back_populates="user")


class BookCategory(Base):
    __tablename__ = 'book_category'

    id = Column(Integer, primary_key=True)
    description = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), default=0)
    user = relationship("User", back_populates="book_categories")
    books = relationship(
        "Book", back_populates="book_category",  cascade="all, delete-orphan")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'description': self.description,
            'id': self.id,
        }


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(250))
    book_category_id = Column(Integer, ForeignKey('book_category.id'))
    book_category = relationship("BookCategory", back_populates="books")
    user_id = Column(Integer, ForeignKey('user.id'), default=0)
    user = relationship("User", back_populates="books")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            "category": self.book_category.description,
            'title': self.title,
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///readinglist.db')
Base.metadata.create_all(engine)
