
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Book, BookCategory, User
engine = create_engine('sqlite:///readinglist.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Menu for UrbanBurger

user1 = User(name='Dolly', email='dolly@gmail.com')
session.add(user1)
session.commit()

bookcategory1 = BookCategory(description='Essential Books', user=user1)
session.add(bookcategory1)
session.commit()
bookcategory2 = BookCategory(description='Memoir/Biography', user=user1)
session.add(bookcategory2)
session.commit()
bookcategory3 = BookCategory(description='AI/Mind', user=user1)

session.add(bookcategory3)
session.commit()


book1 = Book(
    title='When Breath Becomes Air',
    description='great book',
    book_category=bookcategory2, user=user1)
session.add(book1)
session.commit()
book2 = Book(
    title='For the Love of Money: A Memoir',
    description='(great; a Columbia-English-major-turned-hedge-fund-analyst-turned-full-time-philanthropist examined his struggles with substance abuse, dysfunctional family relationships, sex and wealth addiction unflinchingly; a thrilling, disorienting moral tale about privileges, Wall-Street and self-worth.',
    book_category=bookcategory2, user=user1)

session.add(book2)
session.commit()

book3 = Book(title='The Future of the Mind',
             description='great & dense as a textbook',
             book_category=bookcategory3, user=user1)

session.add(book3)
session.commit()

book4 = Book(
    title='On the Shortness of Life by Seneca',
    description='I think about getting a tattoo "Life is short," but then life is too short to get a tattoo.',
    book_category=bookcategory1, user=user1)


session.add(book4)
session.commit()

book5 = Book(
    title='Feeling Good: The New Mood Therapy',
    description="If you are depressed, it's a life-saver.",
    book_category=bookcategory1, user=user1)

session.add(book5)
session.commit()
