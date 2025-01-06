CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "publishers" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS "series" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(150) NOT NULL UNIQUE, finished integer not null default 0);
CREATE TABLE IF NOT EXISTS "books_authors" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "author_id" integer NOT NULL REFERENCES "authors" ("id"), "book_id" integer NOT NULL REFERENCES "books" ("id"), UNIQUE ("book_id", "author_id"));
CREATE TABLE IF NOT EXISTS "authors" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "last_name" varchar(150) NOT NULL, "first_name" varchar(150) NULL, UNIQUE(last_name, first_name));
CREATE TABLE users (id INTEGER PRIMARY KEY NOT NULL, last_name TEXT NOT NULL,
                first_name TEXT NOT NULL,
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                UNIQUE (last_name, first_name),
                UNIQUE (login));
CREATE TABLE IF NOT EXISTS "books" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "isbn" varchar(13) NULL, "title" varchar(200) NOT NULL, "date" integer NOT NULL, "annotation" varchar(250) NULL, "series" integer NULL REFERENCES "series" ("id"), "category" varchar(20) NOT NULL REFERENCES "categories" ("ref"), "publisher" integer NOT NULL REFERENCES "publishers" ("id"), "description" varchar(10000) NULL);
CREATE TABLE IF NOT EXISTS "categories" ("ref" varchar(20) NOT NULL PRIMARY KEY, "description" varchar(200) NOT NULL);
