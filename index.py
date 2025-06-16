from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import sqlite3

root = Tk()
root.title("Contact List")
root.geometry("800x500")
root.resizable(False, False)

# Variables
FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()
contact_id = None  # Global variable to track selected contact id

# SQLite Database Functions
def Database():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS member (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            firstname TEXT,
            lastname TEXT,
            gender TEXT,
            age TEXT,
            address TEXT,
            contact TEXT
        )
    """)
    conn.commit()
    cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
    fetch = cursor.fetchall()
    tree.delete(*tree.get_children())
    for data in fetch:
        tree.insert('', 'end', values=data)
    conn.close()

def SubmitData():
    if FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or AGE.get() == "" or ADDRESS.get() == "" or CONTACT.get() == "":
        messagebox.showwarning("Warning", "Please fill in all fields")
        return
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO member (firstname, lastname, gender, age, address, contact) VALUES (?, ?, ?, ?, ?, ?)",
                   (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), ADDRESS.get(), CONTACT.get()))
    conn.commit()
    conn.close()
    ClearFields()
    AddNewWindow.destroy()
    Database()

def UpdateData():
    global contact_id
    if not contact_id:
        return
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE member SET firstname=?, lastname=?, gender=?, age=?, address=?, contact=?
        WHERE id=?
    """, (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), ADDRESS.get(), CONTACT.get(), contact_id))
    conn.commit()
    conn.close()
    ClearFields()
    AddNewWindow.destroy()
    contact_id = None
    Database()

def DeleteData():
    global contact_id
    if not tree.selection():
        messagebox.showwarning("Warning", "Please select a record to delete")
        return
    result = messagebox.askquestion('Confirm', 'Are you sure you want to delete this record?', icon="warning")
    if result == 'yes':
        selected_item = tree.selection()[0]
        item = tree.item(selected_item)
        contact_id = item['values'][0]
        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM member WHERE id=?", (contact_id,))
        conn.commit()
        conn.close()
        tree.delete(selected_item)
        contact_id = None

# GUI Functions
def ClearFields():
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")

def AddNew():
    global AddNewWindow
    ClearFields()
    AddNewWindow = Toplevel()
    AddNewWindow.title("Add New Contact")
    AddNewWindow.geometry("400x300")
    AddNewWindow.resizable(False, False)

    ContactForm = Frame(AddNewWindow)
    ContactForm.pack(side=TOP, pady=10)

    Label(ContactForm, text="First Name", font=('arial', 12)).grid(row=0, column=0, padx=5, pady=5, sticky=W)
    Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 12)).grid(row=0, column=1)

    Label(ContactForm, text="Last Name", font=('arial', 12)).grid(row=1, column=0, padx=5, pady=5, sticky=W)
    Entry(ContactForm, textvariable=LASTNAME, font=('arial', 12)).grid(row=1, column=1)

    Label(ContactForm, text="Gender", font=('arial', 12)).grid(row=2, column=0, padx=5, pady=5, sticky=W)
    Radiobutton(ContactForm, text="Male", variable=GENDER, value="Male").grid(row=2, column=1, sticky=W)
    Radiobutton(ContactForm, text="Female", variable=GENDER, value="Female").grid(row=2, column=1, sticky=E)

    Label(ContactForm, text="Age", font=('arial', 12)).grid(row=3, column=0, padx=5, pady=5, sticky=W)
    Entry(ContactForm, textvariable=AGE, font=('arial', 12)).grid(row=3, column=1)

    Label(ContactForm, text="Address", font=('arial', 12)).grid(row=4, column=0, padx=5, pady=5, sticky=W)
    Entry(ContactForm, textvariable=ADDRESS, font=('arial', 12)).grid(row=4, column=1)

    Label(ContactForm, text="Contact No.", font=('arial', 12)).grid(row=5, column=0, padx=5, pady=5, sticky=W)
    Entry(ContactForm, textvariable=CONTACT, font=('arial', 12)).grid(row=5, column=1)

    Button(ContactForm, text="Save", width=15, command=SubmitData).grid(row=6, column=1, pady=10)

def OnSelected(event):
    global contact_id, AddNewWindow
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, 'values')
    contact_id = values[0]
    FIRSTNAME.set(values[1])
    LASTNAME.set(values[2])
    GENDER.set(values[3])
    AGE.set(values[4])
    ADDRESS.set(values[5])
    CONTACT.set(values[6])

    AddNewWindow = Toplevel()
    AddNewWindow.title("Update Contact")
    AddNewWindow.geometry("400x300")
    AddNewWindow.resizable(False, False)

    ContactForm = Frame(AddNewWindow)
    ContactForm.pack(side=TOP, pady=10)

    Label(ContactForm, text="First Name", font=('arial', 12)).grid(row=0, column=0, sticky=W)
    Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 12)).grid(row=0, column=1)

    Label(ContactForm, text="Last Name", font=('arial', 12)).grid(row=1, column=0, sticky=W)
    Entry(ContactForm, textvariable=LASTNAME, font=('arial', 12)).grid(row=1, column=1)

    Label(ContactForm, text="Gender", font=('arial', 12)).grid(row=2, column=0, sticky=W)
    Radiobutton(ContactForm, text="Male", variable=GENDER, value="Male").grid(row=2, column=1, sticky=W)
    Radiobutton(ContactForm, text="Female", variable=GENDER, value="Female").grid(row=2, column=1, sticky=E)

    Label(ContactForm, text="Age", font=('arial', 12)).grid(row=3, column=0, sticky=W)
    Entry(ContactForm, textvariable=AGE, font=('arial', 12)).grid(row=3, column=1)

    Label(ContactForm, text="Address", font=('arial', 12)).grid(row=4, column=0, sticky=W)
    Entry(ContactForm, textvariable=ADDRESS, font=('arial', 12)).grid(row=4, column=1)

    Label(ContactForm, text="Contact", font=('arial', 12)).grid(row=5, column=0, sticky=W)
    Entry(ContactForm, textvariable=CONTACT, font=('arial', 12)).grid(row=5, column=1)

    Button(ContactForm, text="Update", width=15, command=UpdateData).grid(row=6, column=1, pady=10)

# Treeview for Contact Table
scrollbary = Scrollbar(root, orient=VERTICAL)
scrollbarx = Scrollbar(root, orient=HORIZONTAL)

tree = ttk.Treeview(root, columns=("ID", "First Name", "Last Name", "Gender", "Age", "Address", "Contact"), 
                    yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

scrollbary.config(command=tree.yview)
scrollbarx.config(command=tree.xview)

scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.pack(side=BOTTOM, fill=X)

tree.heading("ID", text="ID")
tree.heading("First Name", text="First Name")
tree.heading("Last Name", text="Last Name")
tree.heading("Gender", text="Gender")
tree.heading("Age", text="Age")
tree.heading("Address", text="Address")
tree.heading("Contact", text="Contact")

tree['show'] = 'headings'

for col in tree["columns"]:
    tree.column(col, anchor=W, width=100)

tree.pack(fill=BOTH, expand=1)
tree.bind('<Double-1>', OnSelected)

# Buttons
frame = Frame(root)
frame.pack(pady=10)

Button(frame, text="Add New", width=10, command=AddNew).grid(row=0, column=0, padx=10)
Button(frame, text="Delete", width=10, command=DeleteData).grid(row=0, column=1, padx=10)
Button(frame, text="Exit", width=10, command=root.quit).grid(row=0, column=2, padx=10)

# Load data on start
Database()
root.mainloop()

