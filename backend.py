# backend.py
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Angelin@2006",  # change if needed
        database="library_db"
    )

def get_available_books():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT book_id, title, author, genre, year 
        FROM books 
        WHERE book_id NOT IN (SELECT book_id FROM issued_books WHERE return_date IS NULL)
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_issued_books():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT i.issue_id, b.title, m.name, i.issue_date, i.due_date 
        FROM issued_books i
        JOIN books b ON i.book_id = b.book_id
        JOIN members m ON i.member_id = m.member_id
        WHERE i.return_date IS NULL
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def search_books(term):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT book_id, title, author, genre, year 
        FROM books 
        WHERE title LIKE %s OR author LIKE %s
    """, (f"%{term}%", f"%{term}%"))
    rows = cur.fetchall()
    conn.close()
    return rows

def issue_book(book_id, member_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM issued_books WHERE book_id=%s AND return_date IS NULL", (book_id,))
    if cur.fetchone():
        conn.close()
        return False, "Book already issued."

    cur.execute("""
        INSERT INTO issued_books (book_id, member_id, issue_date, due_date)
        VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY))
    """, (book_id, member_id))
    conn.commit()
    conn.close()
    return True, "Book issued successfully."

def return_book(issue_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE issued_books SET return_date = CURDATE() WHERE issue_id = %s AND return_date IS NULL", (issue_id,))
    conn.commit()
    updated = cur.rowcount
    conn.close()
    if updated == 0:
        return False, "Invalid or already returned Issue ID."
    return True, "Book returned successfully."

def get_members():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT member_id, name, email, phone FROM members")
    rows = cur.fetchall()
    conn.close()
    return rows
