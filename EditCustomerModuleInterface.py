from tkinter import *

from PIL import Image, ImageTk

import ViewCustomerModuleInterface


class EditCustomerModuleInterface:
    def __init__(self, window, machinery_name, image_path, count):
        self.window = window
        self.window.title(machinery_name)
        self.window.geometry(f"{int(window.winfo_screenwidth())}x{int(window.winfo_screenheight())}")
        self.window.iconbitmap("icon.ico")

        self.background_image_path = "assets/login_bg2.png"
        self.background_image = Image.open(self.background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface,
                                          font=("Arial", 12), bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        self.add_outer_frame = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.add_outer_frame.place(x=self.window.winfo_screenwidth() / 2, y=self.window.winfo_screenheight() / 2,
                                   anchor="center")
        self.add_outer_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Add product frame
        self.add_product_frame = Frame(self.add_outer_frame, bg="#968802", highlightbackground="#968802",
                                       highlightthickness=0)
        self.add_product_frame.pack()
        self.add_product_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Product Image
        self.product_image = Image.open(image_path)
        self.product_image = self.product_image.resize((200, 200))
        self.product_image = ImageTk.PhotoImage(self.product_image)

        self.product_image_label = Label(self.add_product_frame, image=self.product_image, bg="white")
        self.product_image_label.grid(row=0, column=0, rowspan=6, padx=(0, 20))

        self.title_label = Label(self.add_product_frame, text=machinery_name, font=("Arial", 30, "bold"), bg="#968802",
                                 fg="white")
        self.title_label.grid(row=0, column=1, columnspan=2, pady=(5, 10), sticky="w")

        self.product_name_label = Label(self.add_product_frame, text="Product Name:", font=("Arial", 12), bg="#968802",
                                        fg="white")
        self.product_name_label.grid(row=1, column=1, sticky="e", pady=(5, 5))

        self.product_name_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_name_entry.grid(row=1, column=2, pady=(5, 5))
        self.product_name_entry.focus_set()
        self.product_name_entry.insert(0, machinery_name)

        self.product_count_label = Label(self.add_product_frame, text="Product Count:", font=("Arial", 12),
                                         bg="#968802", fg="white")
        self.product_count_label.grid(row=2, column=1, sticky="e", pady=(5, 5))

        self.product_count_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_count_entry.grid(row=2, column=2, pady=(5, 5))
        self.product_count_entry.insert(0, count)
        # Add Product Button
        self.add_button = Button(self.add_product_frame, text=f"Add {machinery_name}", font=("Arial", 12, "bold"),
                                 bg="#487307",
                                 fg="white", width=25, height=2, command=self.add_product)
        self.add_button.grid(row=3, column=1, columnspan=2, pady=(0, 20))

    def menu_interface(self):
        ViewCustomerModuleInterface.ViewCustomerModulesInterface(self.window, 0)

    def add_product(self):
        product_name = self.product_name_entry.get()
        product_count = self.product_count_entry.get()
        ViewCustomerModuleInterface.ViewCustomerModulesInterface(self.window, 0)
