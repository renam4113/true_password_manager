import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from string import ascii_lowercase, ascii_uppercase, digits, printable
import random
from cryptography.fernet import Fernet
import json


def generate_key_and_save_to_file(key_file_path):
    key = Fernet.generate_key()
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)
        
# Генерируем и сохраняем ключ в файл cls.key
#generate_key_and_save_to_file('cls.key')


class PasswordManager:
    data = []
    file_name = 'passwords.json'
    key = None



    @classmethod
    def all(cls):
        with open(cls.file_name, 'r') as f:
            cls.data = json.load(f)
        return cls.data
        pass

    @classmethod
    def add(cls, website, username, password):
        key = cls.load_key('cls.key')
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode())
        entry = {'website': website, 'username': username, 'password': encrypted_password.decode()}
        cls.data.append(entry)
        cls.commit()

    @classmethod
    def load_key(cls, key_file_path):
        with open(key_file_path, 'rb') as key_file:
            return key_file.read()

    @classmethod
    def find(cls, website):

        for item in cls.all():
            if website.lower() == item['website'].lower():
                return item
        return None

    @classmethod
    def delete(cls, website):
        item = cls.find(website)
        if item:
            cls.all().remove(item)
            cls.commit()
        else:
            print('Not found')
        pass

    @classmethod
    def commit(cls):
        with open(cls.file_name, 'w') as f:
            json.dump(cls.data, f)




class Application(tk.Tk):
    

    
    image_source = Image.open('logo.png').resize((200, 200))

    def __init__(self):
        super().__init__()
        self.title('Password Manager')
        self.container = ttk.Frame(self)
        self.resizable(False, False)

        # TODO : Add logo
        self.image_file = ImageTk.PhotoImage(self.image_source)
        self.canvas = tk.Canvas(self.container, bg='#F0F0F0', width= 300, height= 300, highlightthickness=0)
        self.canvas.create_text(150, 0, text='My Pass'.title(), fill='black', anchor='n', font=('IMPACT', 30, 'bold'))
        self.canvas.create_image(150, 50, image=self.image_file, anchor='n')
        self.canvas.grid(row=0, column=0, padx=50, pady=50)
        self.main_form = MainForm(self.container, self)
        self.login_form = LoginForm(self.container, self)
        self.login_form.grid(row=1, column=0)
        #self.main_form.grid(row=1, column=0, sticky='EW')
        self.container.grid()

    pass


class LoginForm(ttk.Frame):
    FONT = ('Monaco', 16, 'normal')

    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)
        self.controller = controller
        self.configure(padding=(50, 25))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # TODO : Variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        # TODO : Input Fields
        self.username_label = ttk.Label(self, text='Username', font=self.FONT)
        self.username_entry = ttk.Entry(self, font=self.FONT, textvariable=self.username_var)
        self.password_label = ttk.Label(self, text='Password', font=self.FONT)
        self.password_entry = ttk.Entry(self, font=self.FONT, textvariable=self.password_var)

        self.username_label.grid(row=0, column=0, sticky='w')
        self.username_entry.grid(row=0, column=1, sticky='e')
        self.username_entry.focus()
        self.username_var.set('')
        self.password_label.grid(row=1, column=0, sticky='w')
        self.password_entry.grid(row=1, column=1, sticky='e')
        self.password_var.set('')

        # todo: buttons
        self.login_btn = ttk.Button(self, text='Login', command=self.login)
        self.login_btn.grid(row=2, column=1, sticky='we')

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if username == 'EKS' and password == 'lapchatka':
            self.grid_forget()
            self.controller.main_form.grid(row=1, column=0)
        else:
            messagebox.showwarning('info', 'please check your login information')
        pass

    pass


class MainForm(ttk.Frame):
    # TODO : Config

    FONT = ('Monaco', 16, 'normal')


    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)
        self.configure(padding=(50, 25))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.controller = controller
        # TODO : Define Variables
        self.length_var = tk.IntVar()
        self.length_var.set(16)
        self.website_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        # TODO : Input Fields
        self.website_label = ttk.Label(self, text='Website', font=self.FONT)
        self.website_entry = ttk.Entry(self, font=self.FONT, textvariable=self.website_var)
        self.email_label = ttk.Label(self, text='Email/Username', font=self.FONT)
        self.email_entry = ttk.Entry(self, font=self.FONT, textvariable=self.email_var)
        self.length_label = ttk.Label(self, text='Length', font=self.FONT)
        self.length_entry = ttk.Entry(self, font=self.FONT, textvariable=self.length_var)
        self.password_label = ttk.Label(self, text='Password', font=self.FONT)
        self.password_entry = ttk.Entry(self, width=35, font=self.FONT, textvariable=self.password_var)

        # grid all entries
        self.website_label.grid(row=1, column=0, padx=10, sticky='w')
        self.website_entry.grid(row=1, column=1, padx=10, sticky='we')
        self.website_entry.focus()

        self.email_label.grid(row=2, column=0, padx=10, sticky='w')
        self.email_entry.grid(row=2, column=1, padx=10, sticky='we')
        self.email_entry.insert(0, 'tut mogla bit vasha reklama')
        self.length_label.grid(row=3, column=0, padx=10, sticky='w')
        self.length_entry.grid(row=3, column=1, padx=10, sticky='we')
        self.password_label.grid(row=4, column=0, padx=10, sticky='w')
        self.password_entry.grid(row=4, column=1, padx=10, sticky='we')

        # TODO : Buttons and controls
        self.generate_btn = ttk.Button(self, text='Generate password', command=self.generate_password)
        self.save_btn = ttk.Button(self, text='save', command=self.save_to_file)
        self.find_btn = ttk.Button(self, text='find', command=self.find_from_file)
        self.delete_btn = ttk.Button(self, text='delete', command=self.delete_from_file)
        # grid buttons
        self.save_btn.grid(row=1, column=2, padx=10, sticky='wens')
        self.delete_btn.grid(row=2, column=2, padx=10, sticky='wens')
        self.find_btn.grid(row=3, column=2, padx=10, sticky='wens')
        self.generate_btn.grid(row=4, column=2, padx=10, sticky='wens')

    # TODO : GENERATE PASSWORD FUNCTION
    def generate_password(self):
        length = self.length_var.get()
        alpha_bit = ascii_lowercase + ascii_uppercase + digits + printable
        letters = [l for l in alpha_bit]
        password = random.sample(letters, length)
        self.password_var.set("".join(password))

        pass


    # TODO : Save to data file
    def save_to_file(self):
        website = self.website_entry.get()
        username = self.email_entry.get()
        password = self.password_entry.get()
        PasswordManager.add(website, username, password)
        messagebox.showinfo('New entry', 'new entry has added')
        self.website_var.set('')
        self.password_var.set('')

    # TODO : find entry from file
    def find_from_file(self):
        website = self.website_entry.get()
        entry = PasswordManager.find(website)
        if entry is not None:
            password = entry['password']
            key = PasswordManager.load_key('cls.key')
            fernet = Fernet(key)
            true_password = fernet.decrypt(password.encode()).decode()

            self.website_var.set(entry['website'])
            self.email_var.set(entry['username'])
            self.password_var.set(true_password)

            
    # TODO : delete entry from file
    def delete_from_file(self):
        website = self.website_entry.get()
        user_answer = messagebox.askokcancel(title=f'Delete {website}',
                                             message=f'do you want to delete {website} from your list')
        if user_answer is True:
            if website != '':
                PasswordManager.delete(website)
                self.website_var.set('')
                self.password_var.set('')
                messagebox.showinfo(f"delete alert", f'{website} has deleted from your list')

    pass

#from gui import Application

app = Application()
photo = tk.PhotoImage(file='logo.png')
app.iconphoto(False, photo)
app.configure(bg = 'red')



if __name__ == '__main__':
    app.mainloop()