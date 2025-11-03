import customtkinter as ctk
from tkinter import messagebox, ttk
import mysql.connector

# ---------------- DATABASE CONNECTION ----------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Angelin@2006",
        database="library_db"
    )

# ---------------- GUI SETUP ----------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Library Management System")
app.geometry("1100x700")

# ---------------- HELPER FUNCTIONS ----------------
def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def back_to_home():
    clear_frame()
    create_dashboard()

def create_card(parent, title, desc, button_text, command):
    frame = ctk.CTkFrame(parent, corner_radius=15, fg_color="white")
    frame.pack_propagate(False)
    frame.configure(width=280, height=180)

    title_label = ctk.CTkLabel(frame, text=title, font=("Helvetica", 17, "bold"), text_color="#005f73")
    title_label.pack(pady=(15, 5))

    desc_label = ctk.CTkLabel(frame, text=desc, font=("Helvetica", 13), text_color="black", wraplength=220)
    desc_label.pack(pady=(0, 10))

    btn = ctk.CTkButton(frame, text=button_text, width=100, height=30, fg_color="#0a9396",
                        hover_color="#007f7b", command=command)
    btn.pack(pady=(5, 10))
    return frame

def display_table(parent, headers, rows):
    frame = ctk.CTkScrollableFrame(parent, fg_color="white")
    frame.pack(pady=10, padx=20, fill="both", expand=True)
    for i, header in enumerate(headers):
        lbl = ctk.CTkLabel(frame, text=header, font=("Helvetica", 15, "bold"), text_color="#005f73")
        lbl.grid(row=0, column=i, padx=15, pady=10)
    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            lbl = ctk.CTkLabel(frame, text=val, font=("Helvetica", 13))
            lbl.grid(row=r, column=c, padx=15, pady=6)

# ---------------- FEATURE PAGES ----------------

def view_all_books_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="📚 All Books", font=("Helvetica", 22, "bold")).pack(pady=15)
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description]
        conn.close()
        display_table(main_frame, headers, rows)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396",
                  hover_color="#007f7b", command=back_to_home).pack(pady=20)

def available_books_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="📗 Available Books", font=("Helvetica", 22, "bold")).pack(pady=15)
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT book_id, title, author, genre, year
            FROM books
            WHERE book_id NOT IN (SELECT book_id FROM issued_books WHERE return_date IS NULL)
        """)
        rows = cur.fetchall()
        conn.close()
        headers = ["Book ID", "Title", "Author", "Genre", "Year"]
        display_table(main_frame, headers, rows)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396",
                  hover_color="#007f7b", command=back_to_home).pack(pady=20)

def issued_books_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="📕 Issued Books", font=("Helvetica", 22, "bold")).pack(pady=15)
    try:
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
        headers = ["Issue ID", "Book Title", "Member Name", "Issue Date", "Due Date"]
        display_table(main_frame, headers, rows)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396",
                  hover_color="#007f7b", command=back_to_home).pack(pady=20)

def issue_book_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="📘 Issue a Book", font=("Helvetica", 22, "bold")).pack(pady=15)
    frame = ctk.CTkFrame(main_frame)
    frame.pack(pady=20)
    book_id = ctk.CTkEntry(frame, width=200, placeholder_text="Book ID")
    member_id = ctk.CTkEntry(frame, width=200, placeholder_text="Member ID")
    book_id.grid(row=0, column=0, padx=10, pady=5)
    member_id.grid(row=0, column=1, padx=10, pady=5)
    def issue():
        if not book_id.get() or not member_id.get():
            messagebox.showerror("Error", "Enter both fields")
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM issued_books WHERE book_id=%s AND return_date IS NULL", (book_id.get(),))
            if cur.fetchone():
                messagebox.showwarning("Unavailable", "Book already issued.")
                conn.close()
                return
            cur.execute("""
                INSERT INTO issued_books (book_id, member_id, issue_date, due_date)
                VALUES (%s,%s,CURDATE(),DATE_ADD(CURDATE(), INTERVAL 14 DAY))
            """, (book_id.get(), member_id.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Book issued successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
    ctk.CTkButton(frame, text="Issue", fg_color="#0a9396", hover_color="#007f7b", command=issue).grid(row=1, column=0, columnspan=2, pady=10)
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396",
                  hover_color="#007f7b", command=back_to_home).pack(side="bottom", pady=20)

def return_book_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="🔁 Return a Book", font=("Helvetica", 22, "bold")).pack(pady=15)
    frame = ctk.CTkFrame(main_frame)
    frame.pack(pady=20)
    issue_id = ctk.CTkEntry(frame, width=300, placeholder_text="Enter Issue ID")
    issue_id.grid(row=0, column=0, padx=10)
    def return_book():
        if not issue_id.get():
            messagebox.showerror("Error", "Enter Issue ID")
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("UPDATE issued_books SET return_date=CURDATE() WHERE issue_id=%s AND return_date IS NULL", (issue_id.get(),))
            conn.commit()
            if cur.rowcount == 0:
                messagebox.showwarning("Not Found", "Invalid or already returned.")
            else:
                messagebox.showinfo("Success", "Book returned successfully.")
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
    ctk.CTkButton(frame, text="Return", fg_color="#0a9396", hover_color="#007f7b", command=return_book).grid(row=0, column=1, padx=10)
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396",
                  hover_color="#007f7b", command=back_to_home).pack(side="bottom", pady=20)

def search_books_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="🔍 Search Books", font=("Helvetica", 22, "bold")).pack(pady=15)
    search_frame = ctk.CTkFrame(main_frame)
    search_frame.pack(pady=10)
    entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Enter title or author...")
    entry.grid(row=0, column=0, padx=10)
    result_frame = ctk.CTkFrame(main_frame)
    result_frame.pack(fill="both", expand=True)
    def search():
        for w in result_frame.winfo_children():
            w.destroy()
        term = entry.get().strip()
        if not term:
            messagebox.showwarning("Empty", "Enter a search term")
            return
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT book_id, title, author, genre, year FROM books WHERE title LIKE %s OR author LIKE %s", (f"%{term}%", f"%{term}%"))
        rows = cur.fetchall()
        conn.close()
        headers = ["Book ID", "Title", "Author", "Genre", "Year"]
        display_table(result_frame, headers, rows)
    ctk.CTkButton(search_frame, text="Search", fg_color="#0a9396", hover_color="#007f7b", command=search).grid(row=0, column=1, padx=10)
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396",
                  hover_color="#007f7b", command=back_to_home).pack(side="bottom", pady=20)

def view_members_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="👥 View Members", font=("Helvetica", 22, "bold")).pack(pady=15)
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT member_id, name, email, phone FROM members")
        rows = cur.fetchall()
        conn.close()
        headers = ["ID", "Name", "Email", "Phone"]
        display_table(main_frame, headers, rows)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396",
                  hover_color="#007f7b", command=back_to_home).pack(pady=20)

def add_member_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="➕ Add Member", font=("Helvetica", 22, "bold")).pack(pady=15)
    frame = ctk.CTkFrame(main_frame)
    frame.pack(pady=20)
    name = ctk.CTkEntry(frame, width=200, placeholder_text="Name")
    email = ctk.CTkEntry(frame, width=200, placeholder_text="Email")
    phone = ctk.CTkEntry(frame, width=200, placeholder_text="Phone")
    name.grid(row=0, column=0, padx=10, pady=5)
    email.grid(row=0, column=1, padx=10, pady=5)
    phone.grid(row=0, column=2, padx=10, pady=5)
    def add_member():
        if not name.get() or not email.get():
            messagebox.showerror("Error", "Fill all fields")
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO members (name, email, phone) VALUES (%s,%s,%s)", (name.get(), email.get(), phone.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Member added successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
    ctk.CTkButton(frame, text="Add Member", fg_color="#0a9396", hover_color="#007f7b", command=add_member).grid(row=1, column=0, columnspan=3, pady=10)
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396",
                  hover_color="#007f7b", command=back_to_home).pack(side="bottom", pady=20)

def overdue_books_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="⚠️ Overdue Books", font=("Helvetica", 22, "bold")).pack(pady=15)
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT i.issue_id, b.title, m.name, i.due_date
            FROM issued_books i
            JOIN books b ON i.book_id = b.book_id
            JOIN members m ON i.member_id = m.member_id
            WHERE i.return_date IS NULL AND i.due_date < CURDATE()
        """)
        rows = cur.fetchall()
        conn.close()
        headers = ["Issue ID", "Book", "Member", "Due Date"]
        display_table(main_frame, headers, rows)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396",
                  hover_color="#007f7b", command=back_to_home).pack(pady=20)

# ---------------- DASHBOARD ----------------
def create_dashboard():
    ctk.CTkLabel(main_frame, text="📚 LIBRARY MANAGEMENT SYSTEM", font=("Helvetica", 26, "bold")).pack(pady=25)
    grid = ctk.CTkFrame(main_frame, fg_color="#edf6f9", corner_radius=15)
    grid.pack(pady=20)
    grid.grid_columnconfigure((0,1,2), weight=1)
    grid.grid_rowconfigure((0,1,2), weight=1)
    cards = [
        ("Available Books", "See all available books.", "Open", available_books_page),
        ("Issued Books", "View currently issued books.", "Open", issued_books_page),
        ("Issue Book", "Issue a book to a member.", "Issue", issue_book_page),
        ("Return Book", "Return borrowed books.", "Return", return_book_page),
        ("Search Books", "Search books by title or author.", "Search", search_books_page),
        ("View All Books", "Browse all books.", "View", view_all_books_page),
        ("Overdue Books", "View overdue books.", "Check", overdue_books_page),
        ("View Members", "View registered members.", "View", view_members_page),
        ("Add Member", "Register a new member.", "Add", add_member_page),
    ]
    r=c=0
    for title, desc, btn, cmd in cards:
        card=create_card(grid,title,desc,btn,cmd)
        card.grid(row=r,column=c,padx=25,pady=25)
        c+=1
        if c==3:
            c=0; r+=1

# ---------------- MAIN FRAME ----------------
main_frame = ctk.CTkFrame(app, fg_color="white")
main_frame.pack(fill="both", expand=True)
create_dashboard()
app.mainloop()
