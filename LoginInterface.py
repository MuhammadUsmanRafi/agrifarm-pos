from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

import MenuInterface
from main import MainInterface


class LoginInterface:
    def __init__(self, window):
        self.show_password_var = None
        self.USERNAME = "admin"
        self.PASSWORD = "123456789"
        self.window = window
        self.window.title("Login")
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        # Set background image for the login window
        background_image_path = "assets/login_bg2.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.frame = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.frame.place(x=self.window.winfo_screenwidth() / 2, y=self.window.winfo_screenheight() / 2,
                         anchor="center")

        self.frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.login_frame = Frame(self.frame, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.login_frame.pack()

        self.login_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        title_label = Label(self.login_frame, text='Login Form', font=("Arial", 20, "bold"), bg="#968802", fg="white")
        title_label.pack(pady=10)

        self.user_frame = Frame(self.login_frame, bg="#968802")
        self.user_frame.pack(pady=10, fill="x")

        self.user_label = Label(self.user_frame, text="Username:", font=("Arial", 12), bg="#968802", fg="white")
        self.user_label.pack(side=LEFT, padx=(0, 10))

        self.user_entry = Entry(self.user_frame, font=("Arial", 12), bg="white")
        self.user_entry.insert(0, self.USERNAME)
        self.user_entry.pack(fill="x", expand=True)

        # Password entry with label and white text color
        pass_frame = Frame(self.login_frame, bg="#968802")
        pass_frame.pack(pady=10, fill="x")

        pass_label = Label(pass_frame, text="Password:", font=("Arial", 12), bg="#968802", fg="white")
        pass_label.pack(side=LEFT, padx=(0, 10))

        password_var = StringVar()
        self.pass_entry = Entry(pass_frame, font=("Arial", 12), show="*", bg="white", textvariable=password_var)
        self.pass_entry.pack(fill="x", expand=True)
        self.pass_entry.insert(0, self.PASSWORD)
        self.pass_entry.focus_set()
        self.show_password_var = BooleanVar()
        show_password_checkbox = Checkbutton(self.login_frame, text='Show Password', font=("Arial", 12),
                                             bg="#968802", fg="white", variable=self.show_password_var,
                                             selectcolor="white", command=self.show_password)
        show_password_checkbox.pack(pady=10)

        login_button = Button(self.login_frame, text='Login', command=self.perform_login, font=("Arial", 12),
                              bg="#487307", fg="white", width=20)
        login_button.pack(pady=10)

        self.back_to_home_button = Button(self.window, text="Back to Home", command=self.show_main_interface,
                                          font=("Arial", 12), bg="#487307", fg="white", width=20)
        button_width = 200
        button_height = 40
        x_position = (self.window.winfo_screenwidth() - button_width) / 2 + 6
        y_position = (self.window.winfo_screenheight() - button_height) * 0.8
        self.back_to_home_button.place(x=x_position, y=y_position)

    def show_main_interface(self):
        MainInterface(self.window)

    def show_password(self):
        if self.show_password_var.get():
            self.pass_entry.config(show="")
        else:
            self.pass_entry.config(show="*")

    def perform_login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()

        if username == self.USERNAME and password == self.PASSWORD:
            MenuInterface.MenuInterface(self.window)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


if __name__ == "__main__":
    root = Tk()
    login_interface = LoginInterface(root)
    root.mainloop()
