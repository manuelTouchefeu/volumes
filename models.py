"""
Copyright (c) 2018, Manuel Touchefeu.

This file is part of Volumes.

Volumes is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Volumes is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <https://www.gnu.org/licenses/>.


"""

import time
import re
import hashlib
import sqlite3
from bottle import request


data_base = "volumes.sqlite3"


class Connection:
    def __init__(self):
        global data_base
        self.db = sqlite3.connect(data_base)
        self.conn = self.db.cursor()


class Author:
    def __init__(self, id, last_name, first_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
    def __str__(self):
        if self.first_name is None:
            return "%s" % self.last_name
        return "%s %s" % (self.first_name, self.last_name)


class Category:
    def __init__(self, index, description):
        self.index = index
        self.description = description # contrainte unique!


class Publisher:
    def __init__(self, id, name):
        self.id = id
        self.name = name # contrainte unique!
        

class Series:
    def __init__(self, id, title, finished, books=[]):
        self.id = id
        self.title = title
        self.finished = finished
        self.books = books



class Book:
    def __init__(self, id, isbn, authors, title, series, category, publisher, date, description, annotation):
        self.id_book = id
        self.isbn = isbn
        self.category = category
        self.authors = authors
        self.title = title
        self.series = series
        self.publisher = publisher
        self.date = date
        self.description = description
        self.annotation = annotation

    def __str__(self):
        return self.title


def check_form(form):
    """ Param: un objet bottle.request.form """
    checked_form = {}
    checked_form["isbn"] = None if len(form.isbn) == 0 else form.isbn.strip()
    if checked_form["isbn"] is not None and len(checked_form["isbn"]) != 13 and len(checked_form["isbn"]) != 10:
        return False
    checked_form["category"] = form.category
    if checked_form["category"] == "-":
        return False
    checked_form["title"] = format_string(form.title)
    if len(checked_form["title"]) == 0:
        return False
    checked_form["series"] = None if len(form.series) == 0 else format_string(form.series)
    checked_form["authors"] = form.author
    if len(checked_form["authors"]) == 0:
        return False
    checked_form["publisher"] = format_string(form.publisher)
    if len(checked_form["publisher"]) == 0:
        return False
    date = form.date
    try:
        checked_form["date"] = int(date)
        assert checked_form["date"] <= time.localtime().tm_year
    except ValueError:
        return False
    except AssertionError:
        return False
    checked_form["description"] = None if len(form.description) == 0 else format_string(form.description)
    checked_form["annotation"] = None if len(form.annotation) == 0 else format_string(form.annotation)
    return checked_form


class BookManager(Connection):

    def __init__(self):
        Connection.__init__(self)

    def get_categories(self):
        result = []
        self.conn.execute("SELECT ref, description FROM categories ORDER BY ref")
        for b in self.conn.fetchall():
            result.append(Category(b[0], b[1]))
        return result

    #def get_books(self, isbn=None, category=None, title=None, series=None, author=None, publisher=None, date=None):
    def get_books(self, strict=False, **kwargs):
        sql = "SELECT authors.id, authors.last_name, authors.first_name, \
                      books.id, books.title, books.isbn, books.date, books.annotation, books.description, \
                      series.id, series.title, series.finished,\
                      publishers.id, publishers.name, \
                      categories.ref, categories.description \
               FROM books_authors \
               LEFT JOIN authors \
               ON books_authors.author_id = authors.id \
               LEFT JOIN books \
               ON books_authors.book_id = books.id \
               LEFT JOIN series \
               ON books.series = series.id \
               LEFT JOIN publishers \
               ON books.publisher = publishers.id \
               LEFT JOIN categories \
               ON books.category = categories.ref"

        where_clauses = []
        search_results = []
        for key, value in kwargs.items():
            if key != "date" and key != "book":
                value = format_string(value)
            if key == "date":
                where_clauses.append("books.date = %d" % int(value))
            if key == "isbn":
                where_clauses.append("books.isbn = '%s'" % value)
            if key == "publisher":
                where_clauses.append("publishers.name LIKE '%{}%'".format(value))
            if key == "author":
                where_clauses.append("(authors.first_name LIKE '%{}%' \
                                       OR authors.last_name LIKE '%{}%')".format(value, value))
            if key == "title":
                where_clauses.append("(books.title LIKE '%{}%' OR series.title LIKE '%{}%')".format(value, value))
            if key == "series":
                if strict is False:
                    where_clauses.append("series.title LIKE '%{}%'".format(value))
                else:
                    where_clauses.append("series.title='{}'".format(value))
            if key == "comment":
                where_clauses.append("books.annotation LIKE '%{}%'".format(value))
            if key == "book":
                where_clauses.append("books.id = %d" % value)
            if key == "dewey":
                self.conn.execute("SELECT ref FROM categories WHERE description LIKE '%{}%'".format(value))
                refs = [a[0] for a in self.conn.fetchall()]
                refs_cop = list(refs)
                for ref in refs:
                    if re.match(r'^\d00$', ref):
                        refs_cop = [elt for elt in refs_cop if elt == ref or not re.match(r"%c[1-9]\d" % ref[0], elt)]
                    if re.match(r'^\d\d0$', ref):
                        refs_cop = [elt for elt in refs_cop if elt == ref or not re.match(r"%c%c\d" % (ref[0], ref[1]), elt)]
                for index, ref in enumerate(refs_cop):
                    length = len(ref) - 1
                    ref = list(ref)
                    while length >= 0:
                        if ref[length] == '0':
                            ref[length] = '_'
                            length -= 1
                        else:
                            break
                    refs_cop[index] = "".join(ref)
                if refs_cop:
                    clauses = " OR ".join(["categories.ref LIKE '{}'".format(item) for item in refs_cop])
                    where_clauses.append("({})".format(clauses))
                else:
                    return search_results
        if where_clauses:
            sql += " WHERE "
            sql += " AND ".join(where_clauses)


        #sql += " GROUP BY books.series"

        if "order" in kwargs.keys():
            sql += " ORDER BY %s" % kwargs['order']
        else:
            sql += " ORDER BY books.date"
            #sql += " GROUP BY books.series"

        self.conn.execute(sql)

        for b in self.conn.fetchall():
            author = Author(b[0], b[1], b[2])
            series = None if b[9] is None else Series(b[9], b[10], b[11])
            publisher = Publisher(b[12], b[13])
            category = Category(b[14], b[15])
            if search_results and b[3] == search_results[search_results.__len__()-1].id_book:
                search_results[search_results.__len__()-1].authors.append(author)    
            else:
                search_results.append(Book(b[3], b[5], [author], b[4], series, category, publisher, b[6], b[8], b[7]))
        
        # En cas de recherche d'auteur (un seul auteur pour chaque livre trouvé):
        if "author" in kwargs.keys():
             for book in search_results:
                 sql = "SELECT authors.id, authors.last_name, authors.first_name \
                        FROM books_authors \
                        LEFT JOIN authors \
                        ON books_authors.author_id = authors.id \
                        WHERE books_authors.book_id = %d" % book.id_book
                 self.conn.execute(sql)
                 for author in self.conn.fetchall():
                    if author[0] != book.authors[0].id:
                        book.authors.append(Author(author[0], author[1], author[2]))
            
        return search_results

    def get_author(self, last_name, first_name):
        if first_name is not None:
            sql = "SELECT id, last_name, first_name \
                          FROM authors \
                          WHERE last_name = '%s' \
                          AND first_name = '%s'" % (format_string(last_name), format_string(first_name))
        else:
            sql = "SELECT id, last_name, first_name \
                          FROM authors \
                          WHERE last_name = '%s' \
                          AND first_name is NULL" % format_string(last_name)
        self.conn.execute(sql)
        q = self.conn.fetchone()

        return None if q is None else Author(q[0], q[1], q[2])

    def add_author(self, last_name, first_name):
        self.conn.execute("INSERT INTO authors (last_name, first_name) \
                           VALUES (?, ?)", (last_name, first_name))
        self.db.commit()

    def get_series(self, s_id):
        # recherche par id ou titre
        try:
            self.conn.execute("SELECT id, title, finished FROM series \
                               WHERE id = %d" % s_id)
        except TypeError:
            self.conn.execute("SELECT id, title, finished FROM series \
                                           WHERE title = '%s'" % s_id)
        q = self.conn.fetchone()
        s = None if q is None else Series(q[0], q[1], q[2])
        if s is not None:
            s.books = self.get_books(strict=True, series=s.title)
        return None if q is None else s

    def get_all_series(self, w):
        sql = "SELECT id, title, finished FROM series"
        if w == '1' or w == '0' or w == '2':
            sql += " WHERE finished=%s" % w
        sql += " ORDER BY title"
        print(sql)
        self.conn.execute(sql)
        q = self.conn.fetchall()
        return None if q is None else [Series(s[0], s[1], s[2]) for s in q]

    def toggle_series_finished(self, s_id, status):
        s = self.get_series(s_id)
        print(s.title)
        print(status)
        sql = "UPDATE series SET finished=%d WHERE id=%d" % (status, s.id)
        print(sql)
        self.conn.execute(sql)
        self.db.commit()
        return 0

    def update_series(self, s_id, title):
        self.conn.execute("UPDATE series SET title='%s' WHERE id=%d" % (format_string(title), s_id))
        self.db.commit()

    def add_series(self, title):
        self.conn.execute("INSERT INTO series (title) \
                           VALUES ('%s')" % format_string(title))
        self.db.commit()

    def get_publisher(self, name):
        self.conn.execute("SELECT id, name FROM publishers \
                           WHERE name = '%s'" % format_string(name))
        q = self.conn.fetchone()
        return None if q is None else Publisher(q[0], q[1])

    def add_publisher(self, name):
        self.conn.execute("INSERT INTO publishers (name) \
                           VALUES ('%s')" % format_string(name))
        self.db.commit()
        
    def add_book(self, form):
        if form["series"] is not None and self.get_series(form["series"]) is None:
            self.add_series(form["series"])
        form["series"] = None if form["series"] is None else self.get_series(form["series"]).id

        if self.get_publisher(form["publisher"]) is None:
            self.add_publisher(form["publisher"])
        form["publisher"] = self.get_publisher(form["publisher"]).id
       
        self.conn.execute("INSERT INTO books (isbn, title, series, category, publisher, date, description, annotation) \
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (form["isbn"], form["title"], form["series"], form["category"], form["publisher"], form["date"], form["description"], form["annotation"]))
        self.db.commit()
        self.conn.execute("SELECT MAX(id) FROM books")
        book_id = self.conn.fetchone()[0]
        for author in form["authors"].split(';'):
            author_names = author.split(',')
            last_name = author_names[0].strip()
            first_name = None if len(author_names) == 1 else author_names[1].strip();
            if self.get_author(last_name, first_name) is None:
                self.add_author(last_name, first_name)
            author = self.get_author(last_name, first_name)
            self.conn.execute("INSERT INTO books_authors (author_id, book_id) \
                               VALUES (?, ?)", (author.id, book_id))
            self.db.commit()

        return self.get_books(book=book_id)[0]

    def update_book(self, modif, id_book):
        sql = "UPDATE books SET"
        temp = []
        print(modif)
        for key, value in modif.items():
            if value is None:
                continue

            elif key == "authors":
                # Récupérer les auteurs du livre.
                self.conn.execute("SELECT authors.id \
                                   FROM books_authors \
                                   LEFT JOIN authors \
                                   ON books_authors.author_id = authors.id \
                                   WHERE books_authors.book_id = %d" % id_book)
                book_authors = [a[0] for a in self.conn.fetchall()]
                # Récupérer les auteurs de la requête
                req_authors = []
                for author in value.split(';'):
                    author_names = author.split(',')
                    last_name = author_names[0].strip()
                    first_name = None if len(author_names) == 1 else author_names[1].strip();                   
                    if self.get_author(last_name, first_name) is None:
                        self.add_author(last_name, first_name)
                    req_authors.append(self.get_author(last_name, first_name).id)
                # Tester et enregistrer
                for a in book_authors:  
                    if a not in req_authors:
                        print('supp', a)
                        self.conn.execute("DELETE FROM books_authors \
                                           WHERE author_id=%s AND book_id=%d" % (a, id_book))
                        self.db.commit()
                for a in req_authors:
                    if a not in book_authors:
                        print('add', a)
                        self.conn.execute("INSERT INTO books_authors (author_id, book_id) \
                                           VALUES (?, ?)", (a, id_book))
                        self.db.commit()
                continue

            elif key == "series":
                if self.get_series(value) is None:                   
                    self.add_series(value)
                value = self.get_series(value).id
            elif key == "publisher":
                if self.get_publisher(value) is None:
                    self.add_publisher(value)
                value = self.get_publisher(value).id

            if key == "date" or key == "publisher" or key == "series":
                temp.append(" %s = %d" % (key, value))
            else:
                temp.append(" %s = '%s'" % (key, format_string(value)))

        sql += ", ".join(temp)
        sql += " WHERE id = %d" % id_book
        self.conn.execute(sql)
        self.db.commit()

    def del_book(self, book_id):
        self.conn.execute("DELETE FROM books \
                           WHERE id = %d" % book_id)
        self.conn.execute("DELETE FROM books_authors \
                           WHERE book_id = %d" % book_id)
        self.db.commit()

    # suggestions
    def get_publishers_list(self, extract):
        self.conn.execute("SELECT id, name FROM publishers \
                           WHERE name LIKE '%{}%'".format(format_string(extract)))
        return [Publisher(p[0], p[1]) for p in self.conn.fetchall()]

    def get_series_list(self, extract):
        self.conn.execute("SELECT id, title, finished FROM series \
                           WHERE title LIKE '%{}%'".format(format_string(extract)))
        return [Series(p[0], p[1], p[2]) for p in self.conn.fetchall()]

    def get_authors_list(self, extract):
        sql = "SELECT id, last_name, first_name \
                           FROM authors\
                           WHERE last_name LIKE '%{}%'".format(format_string(extract))
        self.conn.execute(sql)
        return [Author(p[0], p[1], p[2]) for p in self.conn.fetchall()]


def format_string(string):
    string = string.strip()
    return string.replace("'", "’")


class User:
    def __init__(self, user_id, last_name, first_name, login):
        self.id = user_id
        self.last_name = last_name
        self.first_name = first_name
        self.login = login

    def __repr__(self):
        return "{} {}".format(self.first_name, self.last_name)


class UserManager(Connection):
    def __init__(self):
        Connection.__init__(self)

    def add_user(self, last_name, first_name, login, password):
        password = hashlib.sha256(password.encode()).hexdigest()
        self.conn.execute("INSERT INTO users (last_name, first_name, login, password) \
                           VALUES (?, ?, ?, ?)", (last_name, first_name, login, password))
        self.db.commit()

    def supp_user(self, user_id):
        self.conn.execute('DELETE FROM users \
                           WHERE id=%d' % user_id)
        self.db.commit()

    def authentication(self, login, password):
        password = hashlib.sha256(password.encode()).hexdigest()
        self.conn.execute("SELECT id, last_name, first_name, login \
                           FROM users \
                           WHERE login=? AND password=?", (login, password))
        res = self.conn.fetchone()
        if res is None:
            return None
        return User(res[0], res[1], res[2], res[3])

    def get_user(self, user_id):
        self.conn.execute("SELECT id, last_name, first_name, login \
                           FROM users \
                           WHERE id=%d" % user_id)
        res = self.conn.fetchone()
        if res:
            return User(res[0], res[1], res[2], res[3])
        return None

    def get_users(self):
        self.conn.execute("SELECT id, last_name, first_name, login \
                           FROM users")
        return [User(user[0], user[1], user[2], user[3]) for user in self.conn.fetchall()]

