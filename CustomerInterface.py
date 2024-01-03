from tkinter import *

from PIL import Image, ImageTk

import MenuInterface
import ViewCustomerModuleInterface, AddCustomer


class CustomerInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Customer")
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        background_image_path = "assets/customer.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface, font=("Arial", 12),
                                          bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)  # Adjust the position

        self.modules_button = []

        self.customer_frame = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.customer_frame.place(x=self.window.winfo_screenwidth() / 4 + 55,
                                  y=self.window.winfo_screenheight() / 2 + 35, anchor="center")
        self.customer_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.upper_button = Frame(self.customer_frame, bg="#968802", highlightbackground="#968802",
                                  highlightthickness=0)
        self.upper_button.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Create a list of button labels
        button_labels = ["View Customer"]

        # Create and pack buttons with adjusted width and height
        for label in button_labels:
            button = Button(self.upper_button, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=25, height=3)
            button.pack(side=LEFT, padx=10)
            self.modules_button.append(button)

        self.upper_button.pack()

        self.middle_button = Frame(self.customer_frame, bg="#968802", highlightbackground="#968802",
                                   highlightthickness=0)
        self.middle_button.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Create a list of button labels
        button_labels = ["Add Customer"]

        # Create and pack buttons with adjusted width and height
        for label in button_labels:
            button = Button(self.middle_button, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=25, height=3)
            button.pack(side=LEFT, padx=10)
            self.modules_button.append(button)

        self.middle_button.pack()

        self.lower_button = Frame(self.customer_frame, bg="#968802", highlightbackground="#968802",
                                  highlightthickness=0)
        self.lower_button.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Create a list of button labels
        button_labels = ["Recent Customer"]

        # Create and pack buttons with adjusted width and height
        for label in button_labels:
            button = Button(self.lower_button, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=25, height=3)
            button.pack(side=LEFT, padx=10)
            self.modules_button.append(button)
        self.lower_button.pack()

        self.end_button = Frame(self.customer_frame, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.end_button.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)
        button_labels = ["Remove Customer"]
        for label in button_labels:
            button = Button(self.end_button, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white", width=25,
                            height=3)
            button.pack(side=LEFT, padx=10)
            self.modules_button.append(button)
        self.end_button.pack()

        self.modules_button[0].config(command=self.view_customer)
        self.modules_button[1].config(command=self.add_customer)
        self.modules_button[2].config(command=self.recent_customer)
        self.modules_button[3].config(command=self.remove_customer)

    def view_customer(self):
        ViewCustomerModuleInterface.ViewCustomerModulesInterface(self.window, 0)

    def add_customer(self):
        AddCustomer.AddCustomer(self.window, 1)

    def recent_customer(self):
        ViewCustomerModuleInterface.ViewCustomerModulesInterface(self.window, 2)

    def remove_customer(self):
        ViewCustomerModuleInterface.ViewCustomerModulesInterface(self.window, 3)

    def menu_interface(self):
        MenuInterface.MenuInterface(self.window)


if __name__ == "__main__":
    root = Tk()
    login_interface = MenuInterface.MenuInterface(root)
    root.mainloop()
