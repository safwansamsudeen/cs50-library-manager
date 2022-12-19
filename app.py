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


@app.route('/members', methods=['GET', 'POST', 'DELETE'])
def members():
    if request.method == 'POST':
        type = request.form.get("type") or request.json["type"]
        name = request.form.get("name") or request.json["name"]
        joined = request.form.get("joined") or request.json["joined"]
        debt = request.form.get("debt") or request.json["debt"]
        if type == "create":
            db.execute(
                "INSERT INTO members (name, joined, debt ) VALUES (?, ?, ?);", name, joined, debt)
        elif type == "update":
            id = request.form.get('id') or request.json["id"]
            db.execute(
                "UPDATE members SET name = ?, joined = ?, debt = ? WHERE id = ?;", name, joined, debt, id)
        return redirect('/members')
    elif request.method == 'GET':
        members = db.execute("SELECT * FROM members;")
        return render_template('members.html', members=members)
    elif request.method == 'DELETE':
        id = request.form.get('id') or request.json["id"]
        db.execute(
            "DELETE FROM members WHERE id = ?;", id)
        return redirect('/members')


@app.route('/transactions', methods=['GET', 'POST', 'DELETE'])
def transactions():
    if request.method == 'POST':
        type = request.form.get("type") or request.json["type"]
        member_id = request.form.get(
            "member_select") or request.json["member_select"]
        book_id = request.form.get(
            "book_select") or request.json["book_select"]
        trans_date = request.form.get(
            "trans_date") or request.json["trans_date"]
        trans_type = request.form.get(
            "trans_type") or request.json["trans_type"]
        if type == "create":
            db.execute("INSERT INTO transactions (book_id, member_id, trans_date, trans_type) VALUES (?, ?, ?, ?);",
                       book_id, member_id, trans_date, trans_type)
        elif type == "update":
            id = request.form.get('id') or request.json["id"]
            db.execute(
                "UPDATE transactions SET book_id = ?, member_id = ?, trans_date = ?, trans_type = ? WHERE id = ?;", book_id, member_id, trans_date, trans_type, id)
        return redirect('/transactions')
    elif request.method == 'GET':
        members = db.execute("SELECT * FROM members;")
        books = db.execute("SELECT * FROM books;")
        transactions = db.execute("SELECT * FROM transactions;")
        return render_template('transactions.html', members=members, books=books, transactions=transactions)
    elif request.method == 'DELETE':
        id = request.form.get('id') or request.json["id"]
        db.execute(
            "DELETE FROM transactions WHERE id = ?;", id)
        return redirect('/transactions')
