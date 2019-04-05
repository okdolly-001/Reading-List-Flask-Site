from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import (render_template, request, redirect,
                   url_for, flash, Blueprint, session as login_session)
from flask_login import login_required, current_user
from database_setup import Base, BookCategory, Book

# Create a bluerpin
readinglist = Blueprint('readinglist', 'readinglist',
                        template_folder='templates')

# Connect to Database and create database session
engine = create_engine('sqlite:///readinglist.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@readinglist.route('/about')
@readinglist.route('/bookcategory/about')
def showAboutPage():
    return render_template('about.html')


@readinglist.route('/')
@readinglist.route('/bookcategory/')
def showBookCategories():
    """Show all book categories created by current user. If not logged in, 
    show book categories from pre-populated database.
    """
    if 'user_id' not in login_session:
        flash("Login to add, edit and delete items", category='warning')
        bookCategories = session.query(
            BookCategory).filter_by(user_id=1).all()
        return render_template('bookCategories.html',
                               bookCategories=bookCategories)
    else:
        bookCategories = session.query(BookCategory).filter_by(
            user_id=current_user.id).all()
        return render_template('bookCategories.html',
                               bookCategories=bookCategories)


@readinglist.route('/bookcategory/<int:book_category_id>/')
@readinglist.route('/bookcategory/<int:book_category_id>/book/')
def showBooks(book_category_id):
    """Show all books with book_category_id

    Fetch the books created by current user with book_category_id.
    If user is not logged in, show the books in default database with
    book_category_id. 
    If book_category is not found, display message.

    Args:
        book_category_id ([int])

    Returns:
        Direct to the books page
    """
    if 'user_id' not in login_session:
        bookcategory = session.query(BookCategory).filter_by(
            id=book_category_id, user_id=1).first()
    else:
        bookcategory = session.query(BookCategory).filter_by(
            id=book_category_id, user_id=current_user.id).first()
    if not bookcategory:
        return "No book has been created in this category."
    # Already check user is authorized to see the book category
    books = session.query(Book).filter_by(
        book_category_id=book_category_id).all()
    return render_template('books.html', books=books,
                           bookcategory=bookcategory)


# Show a bookcategory book
@readinglist.route('/bookcategory/<int:book_category_id>/book/<int:book_id>')
def showBook(book_category_id, book_id):
    """Show book detail

    Fetch the book created by current user with book_id.
    If user is not logged in, show a book in default database with book_id. 
    Otherwise, display message.

    Args:
        book_id ([int])

    Returns:
        Direct to the book detail page
    """
    if 'user_id' not in login_session:
        book = session.query(Book).filter_by(user_id=1, id=book_id).first()
    else:
        book = session.query(Book).filter_by(
            user_id=current_user.id, id=book_id).first()
    if not book:
        return "Book is not found "
    return render_template('book.html', book=book)


@readinglist.route('/bookcategory/new/', methods=['GET', 'POST'])
@login_required
def newBookCategory():
    """Create new book when user is logged in, 
    otherwise, redirect to login page (@login_required).
    """
    if request.method == 'POST':
        newBookCategory = BookCategory(
            description=request.form['category'],
            user_id=current_user.id)
        session.add(newBookCategory)
        session.commit()
        return redirect(url_for('readinglist.showBookCategories'))
    return render_template('newBookCategory.html')


@readinglist.route('/bookcategory/<int:book_category_id>/book/new/',
                   methods=['GET', 'POST'])
@login_required
def newBook(book_category_id):
    """Create a new book with book_category_id

    Can only be done if user is logged in and has created 
    book_category_id

    Args:
        book_category_id ([int])

    Returns:
        Direct to books page of book_category_id
    """
    bookcategory = session.query(BookCategory).filter_by(
        id=book_category_id, user_id=current_user.id).first()
    if request.method == 'POST':
        newItem = Book(
            title=request.form['title'],
            description=request.form['description'],
            book_category_id=book_category_id,
            user_id=current_user.id)
        session.add(newItem)
        session.commit()
        return redirect(
            url_for(
                'readinglist.showBooks',
                book_category_id=book_category_id))
    return render_template('newbook.html', book_category=bookcategory)


@readinglist.route(
    '/bookcategory/<int:book_category_id>/edit',
    methods=['GET', 'POST'])
@login_required
def editBookCategory(book_category_id):
    """Edit a book category created by the current user with 
    book_category_id
    """
    edited_bookcategory = session.query(BookCategory).filter_by(
        id=book_category_id, user_id=current_user.id).first()

    if request.method == 'POST':
        if request.form['description']:
            edited_bookcategory.description = request.form['description']
        session.add(edited_bookcategory)
        session.commit()
        return redirect(
            url_for(
                'readinglist.showBooks',
                book_category_id=book_category_id))
    else:
        return render_template(
            'editbookcategory.html', bookcategory=edited_bookcategory)


@readinglist.route(
    '/bookcategory/<int:book_category_id>/book/<int:book_id>/edit',
    methods=['GET', 'POST'])
@login_required
def editBook(book_category_id, book_id):
    """Edit a book created by the current user    

    User is logged in because @login_required will redirect to login
    page if not logged in.

    Returns:
        Redirect to the book detail page.
    """

    editedBook = session.query(Book).filter_by(
        id=book_id, user_id=current_user.id).first()
    # Need to pass all the book categories so
    # a user can change by scrolling
    bookCategories = session.query(BookCategory).filter_by(
        user_id=current_user.id).all()
    if not editedBook:
        return "Sorry, you didn't create this book."
    if request.method == 'POST':
        if request.form['title']:
            editedBook.title = request.form['title']
        if request.form['description']:
            editedBook.description = request.form['description']
        if request.form['book_category_id']:
            editedBook.book_category_id = request.form['book_category_id']
        session.add(editedBook)
        session.commit()
        return redirect(
            url_for(
                'readinglist.showBook',
                book_category_id=book_category_id, book_id=book_id))
    else:
        return render_template(
            'editbook.html', book=editedBook, bookcategories=bookCategories)


@readinglist.route(
    '/bookcategory/delete',
    methods=['GET'])
@login_required
def deleteBookCategories():
    """Display book category page with delete icon on each book category"""
    bookCategories = session.query(BookCategory).filter_by(
        user_id=current_user.id).all()
    return render_template(
        'deletebookcategories.html', bookCategories=bookCategories)


@readinglist.route(
    '/bookcategory/<int:book_category_id>/delete',
    methods=['GET', 'POST'])
@login_required
def deleteBookCategory(book_category_id):
    """Delete a book category created by the current user with 
    book_category_id.
    User is logged in because @login_required will redirect to login
    page if not logged in.
    """
    itemToDelete = session.query(BookCategory).filter_by(
        id=book_category_id, user_id=current_user.id).first()
    if not itemToDelete:
        return "Sorry, you didn't create this category."
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Book Cateogry Successfully Deleted')
        return redirect(
            url_for(
                'readinglist.showBookCategories'))
    return render_template(
        'deletebookcategory.html', item=itemToDelete)


@readinglist.route(
    '/bookcategory/<int:book_category_id>/book/<int:book_id>/delete',
    methods=['GET', 'POST'])
@login_required
def deleteBook(book_category_id, book_id):
    """ Delete a book created by the current user with
    book_category_id and book_id

    User is logged in because @login_required will redirect to login
    page if not logged in.

    Returns:
        Redirect to books page with book_category_id 
    """

    itemToDelete = session.query(Book).filter_by(
        id=book_id, user_id=current_user.id).first()
    if not itemToDelete:
        return "Sorry, you didn't create this book."
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Book Successfully Deleted')
        return redirect(
            url_for(
                'readinglist.showBooks',
                book_category_id=book_category_id))
    else:
        return render_template(
            'deletebook.html', item=itemToDelete,
            book_category_id=book_category_id)
