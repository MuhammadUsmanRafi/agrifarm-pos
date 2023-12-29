import tkinter as tk
from tkinter import ttk, SOLID

from PIL import Image, ImageTk

import CompanyOrders
from Database import companyorders


class CompanyOrdersInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Company Orders")

        # Set the window size to fill the entire screen
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}")

        # Set background image for the login window
        background_image_path = "assets/login_bg2.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = tk.Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = tk.Button(self.window, text="Back", command=self.menu_interface, font=("Arial", 12),
                                             bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        # Frame to hold the content
        self.content_frame = tk.Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.content_frame.place(x=(self.window.winfo_screenwidth() / 2), y=self.window.winfo_screenheight() / 2 + 20,
                                 anchor="center", relwidth=0.75, relheight=0.5)
        self.content_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.company_label = tk.Label(self.content_frame, text="Orders", font=("Arial", 16, "bold"), bg="#968802",
                                      fg="white")
        self.company_label.pack()

        # Treeview to display orders with vertical scrollbar
        self.tree = ttk.Treeview(self.content_frame, columns=("Company", "Products", "Order Date", "Order Time"),
                                 show="headings")
        self.tree.heading("Company", text="Company")
        self.tree.heading("Products", text="Products")
        self.tree.heading("Order Date", text="Order Date")
        self.tree.heading("Order Time", text="Order Time")

        # Vertical scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(expand=True, fill="both")  # Expand and fill the available space

        # Fetch and display orders
        self.display_orders()

    def display_orders(self):
        # Fetch orders from the database
        orders_cursor = companyorders.find()
        orders = list(orders_cursor)

        # Clear existing items in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert orders into the treeview
        for order in orders:
            company_name = order["company_name"]
            order_date = order["order_date"].strftime("%Y-%m-%d")
            order_time = order["order_date"].strftime("%H:%M:%S")

            # Insert each product as a separate row
            for product in order["products"]:
                product_name = product["product_name"]
                quantity = product["quantity"]

                values = (company_name, product_name, quantity, order_date, order_time)

                # Insert values for each order
                self.tree.insert("", "end", values=values)

        # Configure the "merged" tag to span multiple columns
        self.tree.tag_configure("merged", font=("Arial", 12, "bold"), background="#f0f0f0")

    def menu_interface(self):
        CompanyOrders.CompanyOrders(self.window)
