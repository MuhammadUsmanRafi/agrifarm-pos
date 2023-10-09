from tkinter import *

from PIL import Image, ImageTk

import LoginInterface


class MainInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("AGRIFARM")
        self.window.attributes('-topmost', True)
        self.window.state('zoomed')  # Maximize the window
        self.window.iconbitmap("icon.ico")

        # Set background image for the main window
        background_image_path = "assets/start_bg2.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        # Calculate the center position for the login button
        button_width = 200
        button_height = 40
        x_position = (self.window.winfo_screenwidth() - button_width) / 2
        y_position = (self.window.winfo_screenheight() - button_height) * 0.8

        login_button = Button(self.window, text="Click here to Login", width=20,
                              command=self.show_login_interface, background="#487307", foreground="white",
                              font="Arial 12 bold")
        login_button.place(x=x_position, y=y_position)

    def show_login_interface(self):
        LoginInterface.LoginInterface(self.window)


if __name__ == "__main__":
    main_window = Tk()
    main_interface = MainInterface(main_window)
    main_window.mainloop()
