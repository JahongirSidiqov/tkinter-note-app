from tkinter import *
import re
from sqlite3 import connect
import sqlite3
database_file = "data4.db"
back_ground_color = "blue"
button_color = "#28393a"
email_format = "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"

username_format = "^[a-z0-9_-]{3,15}$"


def darabaza(name, email, password, text="nothing"):
    try:
        with connect(database_file) as db:
            cursor = db.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS data(
                name VARCHAR,
                email VARCHAR,
                password VARCHAR,
                text VARCHAR
                )
                """
            )
            cursor.execute('''INSERT INTO data (name, email, password, text) VALUES (?, ?, ?, ?)''',
                           (name, email, password, text))
    except sqlite3.OperationalError:
        print("database locked")


def register_func():
    def save_func(name, mail, password):
        if re.match(email_format, mail.get()) and re.match(username_format, name.get()):
            darabaza(name.get(), mail.get(), password.get())
            name_label = Label(screen, text="Ro'yxardan o'tingiz", bg="green")
            name_label.grid(row=5, column=1)
            save['text'] = 'Saqlandi!!!'
        else:
            name_label = Label(screen, text="Malumotlarni to'g'ri kiriting", bg="red")
            name_label.grid(row=5, column=1)
    screen = Tk()
    screen.title("Eslatmalar")
    x = screen.winfo_screenwidth() // 2
    y = int(screen.winfo_screenheight() * 0.1)
    screen.geometry('500x300+' + str(x) + '+' + str(y))
    screen.tkraise()
    screen.configure(bg=back_ground_color)
    # name
    name_lable = Label(screen, text="Ismingizni kiriting: ", fg="white", bg=back_ground_color)
    name_lable.grid(row=0, column=0,  padx=10, pady=10)

    name = Entry(screen, width=50, borderwidth=5)
    name.grid(row=0, column=1)
    # Email
    label_mail = Label(screen, text="Emailni kiriting: ", fg="white", bg=back_ground_color)
    label_mail.grid(row=1, column=0,  padx=10, pady=10)

    mail = Entry(screen, width=50, borderwidth=5)
    mail.grid(row=1, column=1)

    # Password
    lable_password = Label(screen, text="Parol kiriting: ", fg="white", bg=back_ground_color)
    lable_password.grid(row=3, column=0, padx=10, pady=10)

    password = Entry(screen, width=50, borderwidth=5)
    password.grid(row=3, column=1)

    # Save
    save = Button(screen, text="Saqlash", padx=50, command=lambda: save_func(name, mail, password), bg=button_color, fg="white")
    save.grid(row=4, column=1, padx=10, pady=50)
    exit_reg = Button(screen, text="Ortga", padx=50, command=main, bg=button_color, fg="white")
    exit_reg.grid(row=4, column=0)

    screen.mainloop()


def notes(email):
    def save1(text):
        try:
            with connect(database_file, timeout=10) as db:
                cursor = db.cursor()
                updater = '''UPDATE data SET text = ? WHERE email = ?;'''
                cursor.execute(updater, (text, email))
        except sqlite3.OperationalError:
            print("database locked")

    def deli():
        text.delete(0, END)

    def last_note(email_):
        deli()
        with connect(database_file, timeout=10) as db:
            cursor = db.cursor()
            data = cursor.execute('''SELECT email,text FROM data''')
            for row in data:
                email1, text1 = row
                if email_ == email1:
                    text.insert(0, text1)
                    break

    screen2 = Tk()
    screen2.title("Eslatmalar")
    x = screen2.winfo_screenwidth() // 2
    y = int(screen2.winfo_screenheight() * 0.1)
    screen2.geometry('500x300+' + str(x) + '+' + str(y))
    screen2.tkraise()
    screen2.configure(bg=back_ground_color)

    label_password = Label(screen2, text="ESLATMA: ", fg="white", bg=back_ground_color)
    label_password.grid(row=0, column=0, padx=5, pady=20)

    text = Entry(screen2, width=60, borderwidth=5)
    text.grid(row=1, column=0, columnspan=4)

    save = Button(screen2, text="Saqlash", padx=30, command=lambda: save1(text.get()), bg=button_color, fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black")
    save.grid(row=2, column=0,  padx=5, pady=50)

    clean = Button(screen2, text="O'chirish", padx=30, command=lambda: deli(), bg=button_color, fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black")
    clean.grid(row=2, column=1, padx=5)

    last = Button(screen2, text="Tarix", padx=30, command=lambda: last_note(email), bg=button_color, fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black")
    last.grid(row=2, column=2, padx=5)

    exit_main = Button(screen2, text="CHiqish", padx=30, command=lambda: main(), bg=button_color, fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black")
    exit_main.grid(row=2, column=3, padx=5)
    screen2.mainloop()


def main():
    def login(email, password_):
        with connect(database_file, timeout=10) as db:
            cursor = db.cursor()
            data = cursor.execute('''SELECT email,password FROM data''')
            for row in data:
                email1, password1 = row
                if email.get() == str(email1) and password_.get() == str(password1):
                    name_label = Label(screen1, text="Muvofaqiyatli Kirib oldingiz", bg="green")
                    name_label.grid(row=4, column=0)
                    notes(email.get())
                    break
                else:
                    name_lable = Label(screen1, text="Malumotlarni to'g'ri kiriting", bg="red")
                    name_lable.grid(row=4, column=0)
    screen1 = Tk()
    screen1.title("Eslatmalar")
    x = screen1.winfo_screenwidth() // 2
    y = int(screen1.winfo_screenheight() * 0.1)
    screen1.geometry('500x300+' + str(x) + '+' + str(y))
    screen1.configure(bg=back_ground_color)
    screen1.tkraise()
    # Email
    label_mail = Label(screen1, text="Emailni kiriting: ", fg="white", bg=back_ground_color)
    label_mail.grid(row=0, column=0,  padx=10, pady=15)

    mail = Entry(screen1, width=50, borderwidth=5)
    mail.grid(row=0, column=1)
    # Password
    label_password = Label(screen1, text="Parol kiriting: ", fg="white", bg=back_ground_color)
    label_password.grid(row=1, column=0, padx=10, pady=15)

    password = Entry(screen1, width=50, borderwidth=5, show="*")
    password.grid(row=1, column=1)
    # Kirish
    kirish = Button(screen1, text="Kirish", padx=50, command=lambda: login(mail, password), bg=button_color, fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black")
    kirish.grid(row=3, column=0,  padx= 10, pady= 50)
    # Ro'yxatdan o'tish
    register = Button(screen1, text="Ro'yxatdan o'tish", padx=50, command=register_func, bg=button_color, fg="white")
    register.grid(row=3, column=1)

    screen1.mainloop()


if __name__ == '__main__':
    main()