import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

import ViewCustomerModuleInterface
from Database import customer, productsales


class ViewCustomerOrder:
    def __init__(self, window, name, email):
        self.window = window
        self.window.title("View Customer Order")
        self.window.geometry(f"{int(window.winfo_screenwidth() / 1.5)}x{int(window.winfo_screenheight() / 1.5)}")
        self.window.iconbitmap("icon.ico")

        # Background Image
        self.background_image_path = "assets/login_bg2.png"
        self.background_image = Image.open(self.background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface, font=("Arial", 12),
                                          bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        self.add_outer_frame = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.add_outer_frame.place(x=self.window.winfo_screenwidth() / 2, y=self.window.winfo_screenheight() / 2 + 10,
                                   anchor="center")
        self.add_outer_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.title_label = Label(self.add_outer_frame, text="Customer Orders", font=("Arial", 30, "bold"), bg="#968802",
                                 fg="white")
        self.title_label.pack()

        self.tree = ttk.Treeview(self.add_outer_frame, columns=(
            "OrderNumber", "CustomerName", "CustomerEmail", "TotalAmount", "DiscountedAmount", "OrderDate"),
                                 show="headings")

        self.tree.heading("OrderNumber", text="Order Number")
        self.tree.heading("CustomerName", text="Customer Name")
        self.tree.heading("CustomerEmail", text="Customer Email")
        self.tree.heading("TotalAmount", text="Total Amount")
        self.tree.heading("DiscountedAmount", text="Discounted Amount")
        self.tree.heading("OrderDate", text="Order Date")

        # Set column widths
        self.tree.column("OrderNumber", width=100)
        self.tree.column("CustomerName", width=200)
        self.tree.column("CustomerEmail", width=200)
        self.tree.column("TotalAmount", width=200)
        self.tree.column("DiscountedAmount", width=200)
        self.tree.column("OrderDate", width=200)

        self.tree.pack(pady=20)

        self.add_button = Button(self.add_outer_frame, text=f"View Products", font=("Arial", 12, "bold"), bg="#487307",
                                 fg="white", width=25, height=2, command=self.view_products)
        self.add_button.pack()

        # Initialize an empty list to store products
        self.products = []

        self.display_orders(name, email)

    def view_products(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_row = self.tree.item(selected_item, "values")
            bill_number = selected_row[0]

            # Fetch product data from the database for the selected bill number
            product_data = self.get_products_by_bill_number(bill_number)

            # Create a table with product details in a new window
            self.create_product_details_window(product_data)

    def get_products_by_bill_number(self, bill_number):
        product_data = []
        for product in self.products:
            if product["BillNo"] == int(bill_number):
                product_data = product["Products"]
        return product_data

    def create_product_details_window(self, product_data):
        # Create a new window for displaying product details
        details_window = Toplevel(self.window)
        self.window.attributes('-topmost', False)
        details_window.title("Product Details")

        # Treeview for displaying product details
        details_tree = ttk.Treeview(details_window, show="headings", height=16)
        details_tree["columns"] = ("Product", "UnitPrice", "Quantity", "TotalPrice")

        details_tree.heading("#1", text="Product")
        details_tree.heading("#2", text="Unit Price")
        details_tree.heading("#3", text="Quantity")
        details_tree.heading("#4", text="Total Price")

        # Set column widths
        column_widths = {"Product": 200, "UnitPrice": 100, "Quantity": 100, "TotalPrice": 100}

        for column, width in column_widths.items():
            details_tree.column(column, width=width, anchor="center")

        details_tree.pack()

        # Insert product details into the Treeview
        for item in product_data:
            details_tree.insert("", "end",
                                values=(item["Product Name"], item["Unit Price"], item["Quantity"], item["t_Price"]))

        # OK button to close the details window
        ok_button = Button(details_window, text="OK", command=lambda: self.destory(details_window), font=("Arial", 12),
                           bg="#487307",
                           fg="white", width=15)
        ok_button.pack(side=BOTTOM, pady=10, padx=10)

    def destory(self, details_window):
        details_window.destroy()
        self.window.attributes('-topmost', True)

    def display_orders(self, name, email):
        customer_data = customer.find_one({"CustomerName": name, "CustomerEmail": email})

        if customer_data:
            orders = customer_data.get("Orders", [])

            for item in self.tree.get_children():
                self.tree.delete(item)

            for order_number in orders:
                result = productsales.find_one({"BillNo": order_number})
                product_data = self.fetch_product_data(order_number)

                self.tree.insert("", "end", values=(
                    order_number, name, email, result["TotalPrice"], result["DiscountedPrice"], result["DateTime"]))

                # Store product data in the self.products list for later retrieval
                self.products.append({"BillNo": order_number, "Products": product_data})

    def fetch_product_data(self, bill_number):
        # Fetch product data from the productsales collection for the given bill number
        product_data = productsales.find_one({"BillNo": int(bill_number)})
        if product_data:
            return product_data.get("Products", [])
        return []

    def menu_interface(self):
        ViewCustomerModuleInterface.ViewCustomerModulesInterface(self.window, 0)

