# Reading List Flask website

  

Python Flask CRUD web app with sqlalchemy, Google oauth2client , and Flask-login.

  

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://choosealicense.com/)

  

## Table of Contents <!-- omit in toc -->

*  [Instructions](#instructions)

*  [Website Views](#website-views)

*  [JSON](#json-api)

*  [Display for anonymous users](#display-book-categories-from-pre-populated-database-to-an-anonymous-user)

*  [Authentication](#authentication-with-google-by-clicking-login-in-menu-bar)

*  [CRUD](#crud)

-  [Description of Model](#description-of-model)

-  [Repository contents](#repository-contents)
- [Tips](#tips)

-  [Trouble-shooting](#trouble-shooting)

  

## Instructions

  

If vagrant is not installed in your machine, download vagrant first.

Initiate vagrant virtual environment:

  

```shell

vagrant up

vagrant ssh

cd /vagrant

```

If you can't see the files, try the following command:

```shell

vagrant reload

vagrant ssh

cd /vagrant

```

Create the database:

  

```shell

python database_setup.py

```

  

Populate the database:

  

```shell

python lotsofbooks.py

```

  

Run app

  

```shell

python app.py

```

  

Go to: [http://localhost:5000/](http://localhost:5000/)

  

**Note that Google will reject sign-in from [http://0.0.0.0:5000](http://0.0.0.0:8000).**

**Login might take a few seconds.**

  

## Website Views

  

- ### JSON API

>#### Get book categories: (http://localhost:5000/bookcategory/JSON). If a user is not logged in, then the categories will come from the pre-populated database.

  

![Book Categories JSON](static/img/book-category-JSON.png)

  

>  #### Get books under a given category: Just go to the books page for that cateogory and add '/JSON' to the url. For example:

(http://localhost:5000/bookcategory/2/book/JSON)

![Books under a given category ](static/img/book-JSON.png)

  > #### Get a specific book: Go to the page for a specific book and add '/JSON' to the url. For example:
  -/bookcategory/<int:category_id>/book/<int:book_id>/JSON

* ### Display book categories from pre-populated database to an anonymous user

  

![Homepage](static/img/not-logged-in.png)

  

* ### Display books under the Memoir/Biography category from pre-populated database to an anonymous user.

  

![Books under a category](static/img/books.png)

  

* ### Authentication with Google by clicking 'Login' in menu bar

  

![Google Sign-In page](static/img/google-sign.png)

  

- ### CRUD

> A user can create, delete or edit a book category or a book created by the user.

![Add category page](static/img/add-book-category.png)

![Edit category page](static/img/edit-category.png)

![Add book page](static/img/add-book.png)

![Edit book page](static/img/edit-book.png)

  

[(Back to top)](#top)

  

## Description of Model

  

Database schema:

  

#### User:

  

- id

- name

- email

- picture

- book_categories

- books

  

#### BookCategory:

  

- id

- description

- user_id

- user

- books

  

#### Book:

  

- id

- title

- description

- book_category_id

- book_category

- user_id

- user

  

I factored the Flask app into three blueprints: readinglist, auth and api for modularity. Please read below about what each blueprint does. I used flask-login package to manage views, so that when a user types in a url that she or he is not authorized, the user will be directed to the Google log-in page.

  

## Repository contents

  

-  [app.py](app.py): Initiate Flask app

-  [database_setup.py](database_setup.py): Set up the database.

-  [lotsofbooks.py](lotsofbooks.py): Populate the database.

-  [model/](model)

  

-  [readinglist.py](model/readinglist.py): Create app routes for all CRUD functions for both book category and book.

-  [api.py](model/api.py): Python file used to populate the database.

-  [auth.py](model/auth.py): Create a user authentication system using Google library oauth2client, enable log-in, log-out.

  

-  [user.py](model/user.py): Create a user in the database based on user information returned by API call to oauth2client, used by auth.py

  

-  [static/](static)

  

-  [img/](static/img): Images used in the main application.

-  [css/](static/css): CSS files used in the main application.

  

-  [templates/](templates): HTML webpage templates.

  

[(Back to top)](#top)

  
## Tips
* [Flask Blueprint]([https://danidee10.github.io/2016/11/20/flask-by-example-8.html](https://danidee10.github.io/2016/11/20/flask-by-example-8.html)): a blueprint defines a collection of views, templates and static assets.
* [flask-login]([https://stackoverflow.com/questions/20136090/how-do-i-handle-login-in-flask-with-multiple-blueprints](https://stackoverflow.com/questions/20136090/how-do-i-handle-login-in-flask-with-multiple-blueprints)):
>One application has only one login manager no matter how many blueprints you use (of course there can be specific exceptions for example when blueprints are independent, but in this case you probably can't use  `flask-login`). Because:
>1.  You have 1 entry point
>2.  If user is not logged in, he will be redirected to login/registration page
>3.  You have 1 user loader
>How login manager works:
>1.  It registers  `current_user`  in request context
>2.  `before_request`  reads your session, gets user id, loads the user with  `user_loader`  and set it to  `current_user`  or  `AnonymousUser`
>3.  When you visit the private page,  `login_required`  checks  `current_user.is_authenticated()`  else redirects to login page
>4.  On login, it adds user id to the session
>So you must initialize only one login manager instance for flask application and then use  `login_required`  and  `current_user`  in all your blueprints.
* [Bulma](https://bulma.io/): one of the easiest to use CSS framework.
* [Docstrings - one line vs multiple line](https://stackoverflow.com/questions/9392096/docstrings-one-line-vs-multiple-line)

* [SQLAlchemy `filter_by` and  `filter`](https://stackoverflow.com/questions/2128505/whats-the-difference-between-filter-and-filter-by-in-sqlalchemy):`db.users.filter_by(name='Joe')`

`db.users.filter(db.users.name=='Joe')`

* [\__init__ file has to be placed in the directory you want to import from]([https://stackoverflow.com/questions/4142151/how-to-import-the-class-within-the-same-directory-or-sub-directory](https://stackoverflow.com/questions/4142151/how-to-import-the-class-within-the-same-directory-or-sub-directory))
* autopep8  run recursively on a directory structure: `autopep8 --in-place --recursive .`
## Trouble-shooting
- Google sign in returns 404
>Solution: Add www.localhost:5000 to the redirect_uris.

- Change in style.css not reflected in the page
>Solution: Clear cache, cmd + shift + delete for Chrome in Mac

  

[(Back to top)](#top)
