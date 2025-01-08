"""
Volumes est un gestionnaire de bibliothèque personnelle.
Il se présente sous la forme d'un application web qui permet
d'enregistrer des livres, de faire des recherches sur plusieurs critères,
et d'accéder au descriptif d'un livre donné.

Les données sont enregistrées dans une BDD sqlite3.
Volumes utilise le micro-framework bottle, distribué sous licence MIT
(Homepage and documentation: http://bottlepy.org/)

Copyright (c) 2018, Manuel Touchefeu.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

github: https://github.com/manuelTouchefeu/volumes

"""


from bottle import route, run, template, static_file, error, default_app, redirect, response
from models import *
import json


def login_required(fn):
    def check(*args, **kwargs):
        cookie = request.get_cookie("user", secret='secret-key')
        if cookie and UserManager().get_user(int(cookie)):
            return fn(*args, **kwargs)            
        else:
            redirect('/login')
    return check


@route('/login')
def login():
    return template('login.tpl')


@route('/login_form', method='POST')
def login_form():
    log = request.forms.login
    password = request.forms.password
    user = UserManager().authentication(log, password)
    if user:
        response.set_cookie('user', str(user.id), secret='secret-key', max_age=700000)  # max_age=600
        redirect('/')
    redirect('/login')


@route('/logout')
def logout():
    response.delete_cookie('user')
    redirect('/login')


@route('/', method=['GET', 'POST'])
@login_required
def home():
    offset = 10
    if request.method == 'POST':
        books = []
        offset = int(request.json['offset'])
        for b in BookManager().get_books(order="books.id")[-offset:-(offset-10)]:
            tmp = {'id': b.id_book, 'title': b.title, 'publisher': b.publisher.name, 'date': b.date,
                   'author': ", ".join([a.__str__() for a in b.authors])}
            if b.series is not None:
                tmp['book_series'] =  b.series.title
            books.append(tmp)
        books.reverse()
        return json.dumps({'books': books})

    books = BookManager().get_books(order="books.id")[-offset::]
    books.reverse()
    return template('home.tpl', books=books)



@route('/book/<book_id>')
@login_required
def book(book_id):
    try:
        book = BookManager().get_books(book=int(book_id))
    except ValueError:
        return "Vous êtes priés de ne pas rentrer n'importe quoi dans l'URL! (%s)" % request.url
    if not book:
        return template('404.tpl')
    return template('book.tpl', book=book[0], categories=BookManager().get_categories())


@route('/update/<book_id>', method='POST')
@login_required
def update(book_id):
    form = check_form(request.forms)
    if form is False:
        redirect('/book/%s' % book_id)
    BookManager().update_book(form, int(book_id))   
    redirect('/book/%s' % book_id)


@route('/del', method='POST')
@login_required
def delete():
    book_id = int(request.json['id'].split('_')[1])
    BookManager().del_book(book_id)
    return 'ok'


@route('/search', method=['GET', 'POST'])
@login_required
def search():
    kwargs = {}
    if request.method == "POST":
        for key in request.forms.keys():
            value = request.forms.getunicode(key)
            if len(value) > 0 and key != "bouton":
                kwargs[key] = value
        books = BookManager().get_books(**kwargs)
        return template('search.tpl', books=books, form=request.forms)
    form = {"isbn": "", "title": "", "author": "", "publisher": "", "date": "", "dewey": "", "comment": ""} 
    return template('search.tpl', form=form, books=False)


@route('/add', method=['GET', 'POST'])
@login_required
def add():
    categories = BookManager().get_categories()
    if request.method == "POST":
        #if BookManager().get_books(isbn=request.forms.ibsn):
        #    form = {"isbn": "Déjà enregistré!", "title": "", "author": "nom, prenom", "publisher": "", "series": "", "date": "année", "description": "sur le livre", "annotation": "sur l'édition"}
        #    return template('add.tpl', form=form, categories=categories, book=None)
        form = check_form(request.forms)
        if form is None:
            return template('add.tpl', form=request.forms, categories=categories, book=None)
        book = BookManager().add_book(form)
        return template('add.tpl', form=request.forms, categories=categories, book=book)

    form = {"isbn": "", "title": "", "author": "nom, prenom", "publisher": "", "series": "", "date": "année", "description": "sur le livre", "annotation": "sur l'édition"}
    return template('add.tpl', form=form, categories=categories, book=None)


@route('/add_ajax', method='POST')
def add_ajax(): 
    """ Renvoie des suggestions au client """
    content = request.POST.content
    table = request.POST.table
    if content is not None:
        if table == 'publisher':
            content = BookManager().get_publishers_list(content)
        elif table == 'author':
            content = BookManager().get_authors_list(content)
        elif table == 'series':
            content = BookManager().get_series_list(content)
        content = [s.__dict__ for s in content]
        return json.dumps(content)
    return ""


@route('/export', method='POST')
def export(): 
    """ Export au format CSV d'un résultat de recherche """
    books = BookManager().get_books(**request.json)
    cible = open("static/export.csv", "w")
    for book in books:
        authors = ", ".join([b.__str__() for b in book.authors])
        series = None if book.series is None else book.series.title
        line = "{}|{}|{}|{}|{}|{}|{}|{}\n".format(book.isbn, series, book.title, authors,
                                                  book.publisher.name,
                                                  book.date, book.category.index, book.annotation)
        cible.write(line)
    cible.close() 
    return "ok"


@route('/categories')
@login_required
def categories():
    return template('categories.tpl', categories=BookManager().get_categories())


@route('/series/<id_series>')
@login_required
def series_one(id_series):
    return template('series_one.tpl', s=BookManager().get_series(int(id_series)))


@route('/series_all/<what>')
@login_required
def series(what):
    s = BookManager().get_all_series(what)
    return template('series.tpl', series=s)


@route('/update_series', method='POST')
@login_required
def update_series():
    print(request.json)
    action = request.json['action']
    if action == 'finished':
        value = int(request.json['status'])
        BookManager().toggle_series_finished(int(request.json['s_id']), value)
    elif action == 'title':
        BookManager().update_series(int(request.json['s_id']), request.json['title'])
    return request.json


# ADMIN _______________________________________________________________________________________________________________
@route('/admin')
@login_required
def users():
    return template('users.tpl', users=UserManager().get_users())


@route('/add_user', method='POST')
def add_user():
    last_name = request.forms.last_name
    first_name = request.forms.first_name
    log = request.forms.login
    password = request.forms.password
    UserManager().add_user(last_name, first_name, log, password)
    redirect('/admin')

# DIVERS ______________________________________________________________________________________________________________
# static files
@route('/static/<filename:path>')
def send_static_file(filename):
    return static_file(filename, root='./static')


# 404
@error(404)
def error404(error):
    return template('404.tpl')


# favicon
@route('/favicon.ico', method='GET')
def get_favicon():
    return static_file('favicon.png', root='./static/icones')


application = default_app()
if __name__ == '__main__':
	#import pdb; pdb.set_trace()
	run(reloader=True, debug=True, host='0.0.0.0', port=8080)
#run(reloader=True, debug=True, host='0.0.0.0', port=8080)