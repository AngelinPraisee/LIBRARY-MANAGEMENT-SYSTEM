# frontend.py
import customtkinter as ctk
from tkinter import messagebox
from backend import (
    get_available_books, get_issued_books, search_books,
    issue_book, return_book, get_members
)

# ---------------- HELPER FUNCTIONS ----------------
def clear_frame(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

def display_table(parent, headers, rows):
    table_frame = ctk.CTkScrollableFrame(parent, fg_color="white")
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    for i, header in enumerate(headers):
        label = ctk.CTkLabel(table_frame, text=header, font=("Helvetica", 15, "bold"), text_color="#005f73")
        label.grid(row=0, column=i, padx=15, pady=10)

    for r_index, row in enumerate(rows, start=1):
        for c_index, value in enumerate(row):
            label = ctk.CTkLabel(table_frame, text=value, font=("Helvetica", 13))
            label.grid(row=r_index, column=c_index, padx=15, pady=6)

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

# ---------------- FEATURE PAGES ----------------
def available_books_page(main_frame, back_to_home):
    clear_frame(main_frame)
    ctk.CTkLabel(main_frame, text="📗 Available Books", font=("Helvetica", 22, "bold")).pack(pady=15)
    rows = get_available_books()
    display_table(main_frame, ["Book ID", "Title", "Author", "Genre", "Year"], rows)
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396", command=back_to_home).pack(pady=20)

def issued_books_page(main_frame, back_to_home):
    clear_frame(main_frame)
    ctk.CTkLabel(main_frame, text="📕 Issued Books", font=("Helvetica", 22, "bold")).pack(pady=15)
    rows = get_issued_books()
    display_table(main_frame, ["Issue ID", "Book Title", "Member Name", "Issue Date", "Due Date"], rows)
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396", command=back_to_home).pack(pady=20)

def search_books_page(main_frame, back_to_home):
    clear_frame(main_frame)
    ctk.CTkLabel(main_frame, text="🔍 Search Books", font=("Helvetica", 22, "bold")).pack(pady=10)

    search_frame = ctk.CTkFrame(main_frame)
    search_frame.pack(pady=10)

    search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Enter title or author...")
    search_entry.grid(row=0, column=0, padx=10)

    result_frame = ctk.CTkFrame(main_frame)
    result_frame.pack(fill="both", expand=True, pady=10)

    def search_action():
        for widget in result_frame.winfo_children():
            widget.destroy()
        term = search_entry.get().strip()
        if not term:
            messagebox.showwarning("Empty", "Please enter a search term.")
            return
        rows = search_books(term)
        display_table(result_frame, ["Book ID", "Title", "Author", "Genre", "Year"], rows)

    ctk.CTkButton(search_frame, text="Search", fg_color="#0a9396", command=search_action).grid(row=0, column=1, padx=10)
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396", command=back_to_home).pack(side="bottom", pady=20)

def issue_book_page(main_frame, back_to_home):
    clear_frame(main_frame)
    ctk.CTkLabel(main_frame, text="📘 Issue Book", font=("Helvetica", 22, "bold")).pack(pady=15)

    frame = ctk.CTkFrame(main_frame)
    frame.pack(pady=20)

    book_entry = ctk.CTkEntry(frame, width=200, placeholder_text="Book ID")
    book_entry.grid(row=0, column=0, padx=10)
    member_entry = ctk.CTkEntry(frame, width=200, placeholder_text="Member ID")
    member_entry.grid(row=0, column=1, padx=10)

    def issue_action():
        success, msg = issue_book(book_entry.get(), member_entry.get())
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showwarning("Error", msg)

    ctk.CTkButton(frame, text="Issue", fg_color="#0a9396", command=issue_action).grid(row=1, column=0, columnspan=2, pady=10)
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396", command=back_to_home).pack(side="bottom", pady=20)

def return_book_page(main_frame, back_to_home):
    clear_frame(main_frame)
    ctk.CTkLabel(main_frame, text="🔁 Return Book", font=("Helvetica", 22, "bold")).pack(pady=15)
    frame = ctk.CTkFrame(main_frame)
    frame.pack(pady=20)
    entry = ctk.CTkEntry(frame, width=300, placeholder_text="Enter Issue ID")
    entry.grid(row=0, column=0, padx=10)

    def return_action():
        success, msg = return_book(entry.get())
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showwarning("Error", msg)

    ctk.CTkButton(frame, text="Return", fg_color="#0a9396", command=return_action).grid(row=0, column=1, padx=10)
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396", command=back_to_home).pack(side="bottom", pady=20)

def view_members_page(main_frame, back_to_home):
    clear_frame(main_frame)
    ctk.CTkLabel(main_frame, text="👥 View Members", font=("Helvetica", 22, "bold")).pack(pady=20)
    rows = get_members()
    if rows:
        display_table(main_frame, ["Member ID", "Name", "Email", "Phone"], rows)
    else:
        ctk.CTkLabel(main_frame, text="No members found.", font=("Helvetica", 14)).pack(pady=20)
    ctk.CTkButton(main_frame, text="⬅ Back to Home", fg_color="#0a9396", command=back_to_home).pack(side="bottom", pady=20)
