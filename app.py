from cs50 import SQL
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQL("sqlite:///library.db")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/books', methods=['GET', 'POST', 'DELETE'])
def books():
    modifiable_fields = {"title": "text", "authors": "text", "isbn": "text", "publisher": "text",
                         "num_pages": "number", "fee": "number", "copies_bought": "number"}

    fields = list(modifiable_fields.keys())

    if request.method == 'POST':
        data = {}
        type = request.form.get("type") or request.json["type"]
        for field in fields:
            data[field] = request.form.get(field) or request.json[field]
        data["copies_available"] = data["copies_bought"]
        fields.append("copies_available")
        if type == "create":
            print(
                f"INSERT INTO books ({', '.join(fields)}) VALUES ({', '.join(list('?' * len(fields)))});")
            db.execute(
                f"INSERT INTO books ({', '.join(fields)}) VALUES ({', '.join(list('?' * len(fields)))});", *data.values())
        elif type == "update":
            id = request.form.get('id') or request.json["id"]
            db.execute(
                f"UPDATE books SET {' = ?, '.join(fields)}= ? WHERE id = ?;", *data.values(), id)
        return redirect('/books')
    elif request.method == 'GET':
        books = db.execute("SELECT * FROM books;")
        return render_template('books.html', books=books, modifiable_fields=modifiable_fields)
    elif request.method == 'DELETE':
        id = request.form.get('id') or request.json["id"]
        db.execute(
            "DELETE FROM books WHERE id = ?;", id)
        return redirect('/books')


@app.route('/members', methods=['GET', 'POST', 'DELETE'])
def members():
    if request.method == 'POST':
        type = request.form.get("type") or request.json["type"]
        full_name = request.form.get("full_name") or request.json["full_name"]
        joined = request.form.get("joined") or request.json["joined"]
        if type == "create":
            db.execute(
                "INSERT INTO members (full_name, joined, cash_left) VALUES (?, ?, ?);", full_name, joined, 500)
        elif type == "update":
            id = request.form.get('id') or request.json["id"]
            db.execute(
                "UPDATE members SET full_name = ?, joined = ? WHERE id = ?;", full_name, joined, id)
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
    transactions = db.execute("SELECT * FROM transactions;")
    members = db.execute("SELECT * FROM members;")
    books = db.execute("SELECT * FROM books;")

    if request.method == 'POST':
        member_id = int(request.form.get(
            "member_select") or request.json["member_select"])
        book_id = int(request.form.get(
            "book_select") or request.json["book_select"])
        trans_date = request.form.get(
            "trans_date") or request.json["trans_date"]
        trans_type = request.form.get(
            "trans_type") or request.json["trans_type"]

        book = list(filter(lambda m: m['id'] == book_id, books))[0]
        member = list(filter(lambda m: m['id'] == member_id, members))[0]
        try:
            if trans_type == "borrow":
                assert member["cash_left"] - book["fee"] > 0
                assert book["copies_available"] > 0

                cash_left = member["cash_left"] - book["fee"]
                book_count = book["copies_available"] - 1
            else:
                book_trans = list(filter(
                    lambda t: t["member_id"] == member_id and t["book_id"] == book_id, transactions))
                borrow_trans = list(
                    filter(lambda t: t["trans_type"] == "borrow", book_trans))
                return_trans = list(
                    filter(lambda t: t["trans_type"] == "return", book_trans))
                assert len(borrow_trans) - len(return_trans) > 0

                cash_left = member["cash_left"] + book["fee"]
                book_count = book["copies_available"] + 1

        except AssertionError:
            return redirect("/transactions")

        db.execute("INSERT INTO transactions (book_id, member_id, trans_date, trans_type) VALUES (?, ?, ?, ?);",
                   book_id, member_id, trans_date, trans_type)

        db.execute("UPDATE members SET cash_left = ? WHERE id = ?",
                   cash_left, member_id)
        db.execute("UPDATE books SET copies_available = ? WHERE id = ?",
                   book_count, book_id)
        return redirect('/transactions')
    elif request.method == 'GET':
        return render_template('transactions.html', members=members, books=books, transactions=transactions)
    elif request.method == 'DELETE':
        id = int(request.form.get('id') or request.json["id"])

        transaction = list(filter(lambda t: t["id"] == id, transactions))[0]
        book_id = transaction["book_id"]
        member_id = transaction["member_id"]
        trans_type = transaction["trans_type"]

        book = list(filter(lambda m: m['id'] == book_id, books))[0]
        member = list(filter(lambda m: m['id'] == member_id, members))[0]

        if trans_type == "borrow":
            cash_left = member["cash_left"] + book["fee"]
            book_count = book["copies_available"] + 1
        else:
            cash_left = member["cash_left"] - book["fee"]
            book_count = book["copies_available"] - 1

        db.execute("UPDATE members SET cash_left = ? WHERE id = ?",
                   cash_left, member_id)
        db.execute("UPDATE books SET copies_available = ? WHERE id = ?",
                   book_count, book_id)

        db.execute(
            "DELETE FROM transactions WHERE id = ?;", id)

        return redirect('/transactions')
