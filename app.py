import streamlit as st
import sqlite3

# --- DATABASE CONNECTION ---
conn = sqlite3.connect('data/library.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    available INTEGER
)
''')
conn.commit()

# --- STREAMLIT UI ---
st.title("📚 Library Management System")

menu = ["Available Books", "Issue Book", "Return Book", "Add Book"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Available Books":
    st.subheader("Available Books")
    books = cursor.execute("SELECT * FROM books WHERE available=1").fetchall()
    if books:
        st.table(books)
    else:
        st.info("No books available.")

elif choice == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    if st.button("Add Book"):
        cursor.execute("INSERT INTO books (title, author, available) VALUES (?, ?, 1)", (title, author))
        conn.commit()
        st.success("✅ Book added successfully!")
