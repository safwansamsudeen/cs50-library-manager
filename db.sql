CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT REQUIRED,
    authors TEXT REQUIRED,
    isbn TEXT REQUIRED,
    publisher TEXT REQUIRED,
    num_pages INTEGER REQUIRED,
    fee INTEGER REQUIRED,
    copies_bought INTEGER REQUIRED,
    copies_available INTEGER REQUIRED
);
CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT REQUIRED,
    joined DATE REQUIRED,
    cash_left INTEGER REQUIRED
);
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER REQUIRED,
    member_id INTEGER REQUIRED,
    trans_date DATE REQUIRED,
    trans_type TEXT REQUIRED,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);