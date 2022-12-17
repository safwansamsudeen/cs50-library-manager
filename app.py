from cs50 import SQL
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQL("sqlite:///books.db")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/books', methods=['GET', 'POST', 'DELETE'])
def books():
    if request.method == 'POST':
        type = request.form.get("type") or request.json["type"]
        name = request.form.get("name") or request.json["name"]
        author = request.form.get("author") or request.json["author"]
        price = request.form.get("price") or request.json["price"]
        if type == "create":
            db.execute(
                "INSERT INTO books (name, author, price ) VALUES (?, ?, ?);", name, author, price)
        elif type == "update":
            id = request.form.get('id') or request.json["id"]
            db.execute(
                "UPDATE books SET name = ?, author = ?, price = ? WHERE id = ?;", name, author, price, id)
        return redirect('/books')
    elif request.method == 'GET':
        books = db.execute("SELECT * FROM books;")
        return render_template('books.html', books=books)
    elif request.method == 'DELETE':
        id = request.form.get('id') or request.json["id"]
        db.execute(
            "DELETE FROM books WHERE id = ?;", id)
        return redirect('/books')
