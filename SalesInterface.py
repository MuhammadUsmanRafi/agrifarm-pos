from tkinter import *

from PIL import Image, ImageTk

import MenuInterface


class SalesInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Sales")
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        # Set background image for the login window
        background_image_path = "assets/sales.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface,
                                          font=("Arial", 12), bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)  # Adjust the position

        self.sales_frame = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.sales_frame.place(x=(self.window.winfo_screenwidth() / 2) + ((self.window.winfo_screenwidth() / 2) / 2),
                               y=self.window.winfo_screenheight() / 2 + 35, anchor="center")  # Adjust the vertical position by subtracting 30 pixels
        self.sales_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.upper_button = Frame(self.sales_frame, bg="#968802", highlightbackground="#968802",
                                  highlightthickness=0)
        self.upper_button.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Create a list of button labels
        button_labels = ["New Sales"]

        # Create and pack buttons with adjusted width and height
        for label in button_labels:
            button = Button(self.upper_button, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=25,
                            height=3)
            button.pack(side=LEFT, padx=10)  # Adjust width, height, and padding

        self.upper_button.pack()

        self.middle_button = Frame(self.sales_frame, bg="#968802", highlightbackground="#968802",
                                   highlightthickness=0)
        self.middle_button.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Create a list of button labels
        button_labels = ["View Day Transactions"]

        # Create and pack buttons with adjusted width and height
        for label in button_labels:
            button = Button(self.middle_button, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=25,
                            height=3)
            button.pack(side=LEFT, padx=10)  # Adjust width, height, and padding

        self.middle_button.pack()

        self.lower_button = Frame(self.sales_frame, bg="#968802", highlightbackground="#968802",
                                  highlightthickness=0)
        self.lower_button.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Create a list of button labels
        button_labels = ["Manage Invoice"]

        # Create and pack buttons with adjusted width and height
        for label in button_labels:
            button = Button(self.lower_button, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=25, height=3)
            button.pack(side=LEFT, padx=10)  # Adjust width, height, and padding

        # Place the upper_button Frame inside the menu_frame
        self.lower_button.pack()

    def menu_interface(self):
        MenuInterface.MenuInterface(self.window)


if __name__ == "__main__":
    root = Tk()
    login_interface = MenuInterface.MenuInterface(root)
    root.mainloop()
