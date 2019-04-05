from flask import jsonify, Blueprint, session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Book, BookCategory


api = Blueprint('api', 'api')
engine = create_engine('sqlite:///readinglist.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@api.route('/JSON')
@api.route('/bookcategory/JSON')
def allBookCategoriesJSON():
    """Display JSON for all book categories created by the current user"""
    if 'user_id' not in login_session:
        bookcategories = session.query(BookCategory).filter_by(
            user_id=1).all()
    else:
        bookcategories = session.query(BookCategory).filter_by(
            user_id=login_session['user_id']).all()
    if bookcategories is None:
        return "Sorry, the category does not exist in our database"
    return jsonify(BookCategory=[i.serialize for i in bookcategories])


@api.route('/bookcategory/<int:category_id>/book/JSON')
def booksJSON(category_id):
    """Display JSON for all books created by the current user \
    with category_id """
    if 'user_id' not in login_session:
        books = session.query(Book).filter_by(
            book_category_id=category_id, user_id=1).all()
    else:
        books = session.query(Book).filter_by(
            book_category_id=category_id,
            user_id=login_session['user_id']).all()

    return jsonify(Book=[r.serialize for r in books])


@api.route('/bookcategory/<int:category_id>/book/<int:book_id>/JSON')
def bookJSON(category_id, book_id):
    """Display JSON for a specific book created by the current user \
    with category_id and book_id"""
    if 'user_id' not in login_session:
        book = session.query(Book).filter_by(
            book_category_id=category_id, id=book_id, user_id=1).first()
    else:
        book = session.query(Book).filter_by(
            book_category_id=category_id, id=book_id,
            user_id=login_session['user_id']).first()
    if not book:
        return "Sorry,there is no book that satisfy your" \
            "criteria in the database."
    return jsonify(Book=book.serialize)
