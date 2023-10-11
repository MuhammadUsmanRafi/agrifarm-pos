from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

import CustomerInterface
import EditCustomerModuleInterface


class ViewCustomerModulesInterface:
    def __init__(self, window, num):
        self.labels = ["Recent Customer", "Favourite Customer", "Edit Customer", "Delete Customer"]
        self.window = window
        self.window.title(self.labels[num])
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        background_image_path = "assets/inventory_modules.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface, font=("Arial", 12),
                                          bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        self.title_label = Label(self.window, text=f"{self.labels[num]}", font=("Arial", 40, "bold"),
                                 background="#968802", foreground="white")
        self.title_label.place(x=self.window.winfo_screenwidth() / 2 - 170, y=20)

        self.frames = []

        agricultural_machinery = [{"name": "Usman", "image_path": "assets/customer/Usman.png", "Order": 10},
                                  {"name": "Usman", "image_path": "assets/customer/Usman.png", "Order": 15},
                                  {"name": "Muneeb", "image_path": "assets/customer/Usman.png", "Order": 5},
                                  {"name": "Muneeb", "image_path": "assets/customer/Usman.png", "Order": 20},
                                  {"name": "Farhan", "image_path": "assets/customer/Usman.png", "Order": 8}]

        for i in range(5):
            frame = Frame(self.window, bg="#487307", highlightbackground="#487307", highlightthickness=0)
            frame.place(x=i * (self.window.winfo_screenwidth() / 5) + 22, y=self.window.winfo_screenheight() / 5 + 40)

            machinery_name = agricultural_machinery[i]["name"]
            image_path = agricultural_machinery[i]["image_path"]
            count = agricultural_machinery[i]["Order"]

            label = Label(frame, text=f"{machinery_name}", font=("Arial", 18, "bold"), background="#487307",
                          foreground="white")
            label.pack(side=TOP, pady=10)

            machinery_image = Image.open(image_path)
            machinery_image = machinery_image.resize((180, 180))
            machinery_image = ImageTk.PhotoImage(machinery_image)

            image_label = Label(frame, image=machinery_image)
            image_label.image = machinery_image
            image_label.pack()

            description_label = Label(frame, text=f"Order: {count}", font=("Arial", 15), background="#487307",
                                      foreground="white")
            description_label.pack()

            # Create a lambda function to pass additional arguments to button_click
            button = Button(frame, text="View", font=("Arial", 12),
                            command=lambda name=machinery_name, path=image_path, c=count: self.button_click(name, path,
                                                                                                            c, num),
                            # Pass num as an argument
                            width=20, background="#968802", foreground="white")
            button.pack(side=TOP, padx=10, pady=5)

            if num == 2:
                button.config(text="Edit")
            elif num == 3:
                button.config(text="Delete")

            self.frames.append(frame)

        self.search_frame = Frame(self.window, bg="white", highlightbackground="#968802", highlightthickness=0)
        self.search_frame.place(x=self.window.winfo_screenwidth() / 2 - 100, y=self.window.winfo_screenheight() / 8)

        self.search_label = Label(self.search_frame, text="Search: ", font=("Arial", 12, "bold"), background="white")
        self.search_label.pack(side=LEFT, padx=(0, 10))

        self.user_entry = Entry(self.search_frame, font=("Arial", 12), bg="white")
        self.user_entry.focus_set()
        self.user_entry.pack(fill="x", expand=True)

    def menu_interface(self):
        CustomerInterface.CustomerInterface(self.window)

    def button_click(self, machinery_name, image_path, count, num):
        if num == 0 or num == 1 or num == 2:
            (EditCustomerModuleInterface.EditCustomerModuleInterface(self.window, machinery_name, image_path, count))
        if num == 3:
            messagebox.askyesno("Confirm Remove", f"Do you want to remove {machinery_name}?")

