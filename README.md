# Library Manager

## Video Demo: https://youtu.be/3PqT3RnIIZ8

## Description

This is a basic library management system, the idea adapted from [Frappe's Dev Hiring Test](https://frappe.io/dev-hiring-test). You can add and update books and members, and add transactions - that is, borrows and returns for every member. Each member starts off with 500 INR in his or her account, an amount that changes as they borrow and return books.

### `app.py`

This file is the crux of the web application: it contains all the code for the logic and the database interactions along with some other stuff (collectively known as the backside). This app connects to a DB titled `library.db`, which you'll have to create previously (see `db.sql` section).

After the setup and activation of the virtual environment, you can run `flask run --port 8000` to run the web application. You can now access it at http://localhost:8000/.

### `db.sql`

This file contains the SQL code necessary for the project's DB. This is how you set up your DB:

- Open Terminal, and run `sqlite3` to open the SQLite Shell.
- Run `.read db.sql` to create a DB with the necessary schema.
- Run `.save library.db` to save the DB to the file system.

### `Pipfile`, `Pipfile.lock` and `.gitignore`

`Pipfile` and `Pipfile.lock` are files for Pipenv, which is what I used in this project. Run `pipenv install` inside your directory to create a new virtual environment with the required packages.

`.gitignore` lists all the files (all DB files, in this case) that Git should ignore.

### Templates

There are four templates for four pages - the home page (index), books, members, and transactions. I used Bootstrap to design these pages.

## About Me

Hi, I'm Safwan, a freshman living in Madurai, India. Thanks for checking out Library Manager!
