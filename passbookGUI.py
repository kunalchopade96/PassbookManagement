import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import mysql.connector as m

db=m.connect(host='localhost',user="root",password="Kunal1996@",database="bank")
cursor=db.cursor()
cursor.execute("create table if not exists Account(Ac_No int primary key auto_increment, name varchar(100), Ac_balance float, password varchar(100)) auto_increment=1000001")

def enter_password(event):
    password_entry = event.widget
    password_entry.config(show='*')

def create_account():
    window = tk.Toplevel()
    window.title('Create Account')
    window.geometry('800x500')

    tk.Label(window, text='Enter Name', font=20).pack(pady=10)
    name_entry = ttk.Entry(window)
    name_entry.pack(pady=10)
    tk.Label(window, text='Enter Account Balance', font=20).pack(pady=10)
    balance_entry = ttk.Entry(window)
    balance_entry.pack(pady=10)
    tk.Label(window, text='Enter Password', font=20).pack(pady=10)
    password_entry = ttk.Entry(window, show='')
    password_entry.bind('<FocusIn>', enter_password)
    password_entry.pack(pady=10)

    def submit():
        name = name_entry.get()
        balance = balance_entry.get()
        password = password_entry.get()
        if not name or not balance or not password:
            msg.showerror(title='Error', message='Please enter all the fields')
        else:
            try:
                balance = float(balance)
            except ValueError:
                msg.showerror(title='Error', message='Please enter a valid balance')
                return
            cursor = db.cursor()
            query = 'INSERT INTO Account (name, Ac_balance, password) VALUES (%s, %s, %s)'
            cursor.execute(query, [name, balance, password])
            db.commit()
            ac_no=cursor.lastrowid
            msg.showinfo(title='Success', message=f'Welcome {name}\nAccount created successfully!\n Account number : {ac_no}')
            window.destroy()

    ttk.Button(window, text='Enter', command=submit).pack(pady=10)
    ttk.Button(window, text='Back', command=window.destroy).pack(pady=10)

def check_balance():
    window = tk.Toplevel()
    window.title('Check Balance')
    window.geometry('800x500')

    tk.Label(window, text='Enter Account Number', font=20).pack(pady=10)
    account_entry = ttk.Entry(window)
    account_entry.pack(pady=10)
    tk.Label(window, text='Enter Password', font=20).pack(pady=10)
    password_entry = ttk.Entry(window, show='')
    password_entry.bind('<FocusIn>', enter_password)
    password_entry.pack(pady=10)

    def submit():
        account_number = account_entry.get()
        password = password_entry.get()
        if not account_number or not password:
            msg.showerror(title='Error', message='Please enter all the fields')
        else:
            cursor = db.cursor()
            query = 'SELECT Ac_balance FROM Account WHERE Ac_no = %s AND password = %s'
            cursor.execute(query, [account_number, password])
            result = cursor.fetchone()
            db.commit()
            if result:
                balance = result[0]
                msg.showinfo(title='Success', message=f'Account Balance is: {balance}')
            else:
                msg.showerror(title='Error', message='Invalid account number or password')
        window.destroy()

    ttk.Button(window, text='Enter', command=submit).pack(pady=10)
    ttk.Button(window, text='Back', command=window.destroy).pack(pady=10)

def deposit_amount():
    window = tk.Toplevel()
    window.title('Deposit Amount')
    window.geometry('800x500')

    tk.Label(window, text='Enter Account Number', font=20).pack(pady=10)
    account_entry = ttk.Entry(window)
    account_entry.pack(pady=10)
    tk.Label(window, text='Enter Password', font=20).pack(pady=10)
    password_entry = ttk.Entry(window, show='')
    password_entry.bind('<FocusIn>', enter_password)
    password_entry.pack(pady=10)
    tk.Label(window, text='Enter Amount to be Deposited', font=20).pack(pady=10)
    amount_entry = ttk.Entry(window)
    amount_entry.pack(pady=10)

    def submit():
        account_number = account_entry.get()
        password = password_entry.get()
        amount = amount_entry.get()
        if not account_number or not password or not amount:
            msg.showerror(title='Error', message='Please enter all the fields')
        else:
            try:
                amount = float(amount)
            except ValueError:
                msg.showerror(title='Error', message='Please enter a valid amount')
                return
            if amount < 0:
                msg.showerror(title='Error', message='Amount cannot be negative')
                return
            cursor = db.cursor()
            query = 'SELECT Ac_balance FROM Account WHERE Ac_no = %s AND password = %s'
            cursor.execute(query, [account_number, password])
            result = cursor.fetchone()
            if result:
                balance = result[0]
                new_balance = balance + amount
                query = 'UPDATE Account SET Ac_balance = %s WHERE Ac_no = %s'
                cursor.execute(query, [new_balance, account_number])
                db.commit()
                msg.showinfo(title='Success', message=f'Amount {amount} deposited successfully')
                window.destroy()
            else:
                msg.showerror(title='Error', message='Invalid account number or password')

    ttk.Button(window, text='Enter', command=submit).pack(pady=10)
    ttk.Button(window, text='Back', command=window.destroy).pack(pady=10)


def withdraw_amount():
    window = tk.Toplevel()
    window.title('Withdraw Amount')
    window.geometry('800x500')

    tk.Label(window, text='Enter Account Number', font=20).pack(pady=10)
    account_entry = ttk.Entry(window)
    account_entry.pack(pady=10)
    tk.Label(window, text='Enter Password', font=20).pack(pady=10)
    password_entry = ttk.Entry(window, show='')
    password_entry.bind('<FocusIn>', enter_password)
    password_entry.pack(pady=10)
    tk.Label(window, text='Enter Amount to Withdraw', font=20).pack(pady=10)
    amount_entry = ttk.Entry(window)
    amount_entry.pack(pady=10)

    def submit():
        account_number = account_entry.get()
        password = password_entry.get()
        amount = amount_entry.get()
        if not account_number or not password or not amount:
            msg.showerror(title='Error', message='Please enter all the fields')
        else:
            try:
                amount = float(amount)
            except ValueError:
                msg.showerror(title='Error', message='Please enter a valid amount')
                return
            if amount < 0:
                msg.showerror(title='Error', message='Amount cannot be negative')
                return
            cursor = db.cursor()
            query = 'SELECT Ac_balance FROM Account WHERE Ac_no = %s AND password = %s'
            cursor.execute(query, [account_number, password])
            result = cursor.fetchone()
            if not result:
                msg.showerror(title='Error', message='Invalid account number or password')
                return
            balance = result[0]
            if amount > balance:
                msg.showerror(title='Error', message='Insufficient balance')
                return
            new_balance = balance - amount
            query = 'UPDATE Account SET Ac_balance = %s WHERE Ac_no = %s'
            cursor.execute(query, (new_balance, account_number))
            db.commit()
            msg.showinfo(title='Success', message='Amount withdrawn successfully')
            window.destroy()

    ttk.Button(window, text='Enter', command=submit).pack(pady=10)
    ttk.Button(window, text='Back', command=window.destroy).pack(pady=10)

def main_menu():
    window = tk.Tk()
    window.title('Main Menu')
    window.geometry('800x500')

    ttk.Button(window, text='Create Account', command=create_account).pack(pady=10)
    ttk.Button(window, text='Check Balance', command=check_balance).pack(pady=10)
    ttk.Button(window, text='Deposit Amount', command=deposit_amount).pack(pady=10)
    ttk.Button(window, text='Withdraw Amount', command=withdraw_amount).pack(pady=10)
    ttk.Button(window, text='Exit', command=exit).pack(pady=10)

    window.mainloop()

main_menu()
   
