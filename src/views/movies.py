# movies.py Structure
#
# index()
# This is the route which is the main landing page for displaying all the
# information about the movies. It will check the login_session to see if
# the is a user curerntly logged in. If so then will greet that user letting
# them know they are logged in. Else it will greet the Guest.
# add_book()
# It will check if there currently is a user logged in and will redirect
# them to the movies page. This is in place if someone tries to manually
# type the address location. If there is a user logged in, then direct
# them to the add_book.jinja2 page. Using the request method POST, it will
# retrieve the information from the form and add it to the database. Then
# will send them back to the main page.
# edit_book(book_id)
# This will retrieve information from the database based on the book_id
# given. It will render that information into a form which could be edited.
# delete_book(book_id)
# This will remove a book form the database. There are features added in the
# delete page which make sure the user wants to delete the book.
# get_language_page(language_id)
# This will only list the movies for the chosen language_id

from flask import Blueprint, Flask, render_template, request, redirect, \
                  url_for, jsonify

# Database model
from functools import wraps
from sqlalchemy import desc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, movies, User, Language
from flask import session as login_session
from app import get_user_id, get_user_info
import random
import string

# Commment out the line that referes to the database you are using
engine = create_engine('sqlite:///movies.db')
#engine = create_engine('mysql://root:6bJI%!IEsm#41@q9@localhost/movie_db')
#engine = create_engine('postgresql://movie:x2X&D3Nb!Lz8Mw4q@localhost/movies')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

movies_blueprint = Blueprint('movies', __name__)




# Following functions contain querys that are used at multiple instances
# thoughout the blueprint. They are in place so you do not have to changes
# each instance, but make things easier to do.

# Query fucntion that will return the list of movies in alphabetical order
def get_movies():
    return session.query(movies).order_by(movies.book_title).all()


# Query fuction that will return the languages in the Language model
def get_languages():
    return session.query(Language).all()


# Utilized the functions in app to get the user infromation and uses that
# to display that information in the template. Though the username is
# currently used, this could be helpful for future modifation of information
# that is displayed about the user
def get_current_user():
        return get_user_info(get_user_id(login_session['email']))


# Query function that returns information about the book_id given.
def get_book(book_id):
    return session.query(movies).filter_by(id=book_id).one()


# Query function that returns information about the language_id given.
# This helps to display only movies in that language
def get_book_language(language_id):
    return session.query(movies).filter_by(language_id=language_id).all()

# Function returned to the user when they try to modify a book that they did not create
def user_error():
    return "<script>function modifyBook(){ alert('You are only not authoized to "\
           "modify this book. Please create your own book creation.');" \
           "window.location='/movies/add/book'}</script><body onload='modifyBook()'>"

@movies_blueprint.route('/')
def index():
    if 'username' in login_session:
        return render_template('movies.jinja2',
                                movies=get_movies(),
                                languages=get_languages(),
                                user=get_current_user())
    # This creates a random string of information that will be used in the
    # thrid-party authentication.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('movies.jinja2',
                            movies=get_movies(),
                            languages=get_languages(),
                            STATE=state)

@movies_blueprint.route('/add/book', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        movies = session.query(movies).all()
        # Creating a movies object to add to the databse.
        book = movies(book_img=request.form['book_img'],
                     book_title=request.form['book_title'],
                     book_author=request.form['book_author'],
                     book_description=request.form['book_description'],
                     book_url=request.form['book_url'],
                     language_id=request.form['language_id'],
                     user_id=login_session['user_id'])
        session.add(book)
        session.commit()
        return redirect(url_for('movies.index'))
    else:
        return render_template('add_book.jinja2',
                                languages=get_languages(),
                                user=get_current_user())

@movies_blueprint.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    if get_book(book_id) != login_session['user_id']:
        return user_error()
    if request.method == 'POST':
            session.delete(get_book(book_id))
            session.commit()
            return redirect(url_for('movies.index',movies=get_movies()))
    else:
        return render_template('delete_book.jinja2',
                                movies=get_book(book_id),
                                languages=get_languages(),
                                user=get_current_user())

@movies_blueprint.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if 'username' not in login_session:
        return redirect('/movies')
    editedBook = session.query(movies).filter_by(id=book_id).one()
    user = get_current_user()

    if editedBook.user_id != login_session['user_id']:
        return user_error()
    if user.id == editedBook.user_id:
        if request.method == 'POST':
            editedBook.book_img = request.form['book_img']
            editedBook.book_title = request.form['book_title']
            editedBook.book_author = request.form['book_author']
            editedBook.book_description = request.form['book_description']
            editedBook.book_url = request.form['book_url']
            editedBook.language_id = request.form['language_id']

            session.add(editedBook)
            session.commit()
            return redirect(url_for('movies.index'))
        else:
            return render_template('edit_book.jinja2',
                                    book=get_book(book_id),
                                    languages=get_languages(),
                                    user=get_current_user())


@movies_blueprint.route('/language/<int:language_id>')
def get_language_page(language_id):
    if 'username' in login_session:
        return render_template('movies.jinja2',
                        movies=get_book_language(language_id),
                        languages=get_languages(),
                        user=get_current_user())
    return render_template('movies.jinja2',
                    movies=get_book_language(language_id),
                    languages=get_languages(),
                    user=get_current_user())


# JSON API's to display infromation about the movies
@movies_blueprint.route('/JSON')
def movies_json():
    movies = get_movies()
    return jsonify(movies=[book.serialize for book in movies])

@movies_blueprint.route('/<int:book_id>/JSON')
def book_json(book_id):
    book = get_book(book_id)
    return jsonify(movies=book.serialize)
