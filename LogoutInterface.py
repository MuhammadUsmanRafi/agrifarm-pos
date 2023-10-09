from tkinter import *

from PIL import Image, ImageTk

import LoginInterface


class LogoutInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Logout")
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        background_image_path = "assets/logout_bg_2.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.login = Button(self.window, text="Login", command=lambda: LoginInterface.LoginInterface(self.window),
                            font=("Arial", 15, "bold"), bg="#968802", fg="white", width=20)
        x_position = (self.window.winfo_screenwidth()) / 5 * 1.5
        y_position = (self.window.winfo_screenheight()) * 0.7
        self.login.place(x=x_position, y=y_position)

        self.exit = Button(self.window, text="Exit", command=self.exit, font=("Arial", 15, "bold"), bg="#968802",
                           fg="white", width=20)
        x_position = (self.window.winfo_screenwidth()) / 5 * 3 - 100
        y_position = (self.window.winfo_screenheight()) * 0.7
        self.exit.place(x=x_position, y=y_position)

    def show_main_interface(self):
        LoginInterface.LoginInterface(self.window)

    def exit(self):
        self.window.destroy()
