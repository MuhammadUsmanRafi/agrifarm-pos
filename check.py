from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

import SalesInterface
from Database import productsales


class DayTransactionModuleInterface:
    def __init__(self, window):
        self.products = []
        self.window = window
        self.db = productsales
        self.window.title("Transaction")
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        # Set background image for the login window
        background_image_path = "assets/transaction.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface, font=("Arial", 12),
                                          bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        # Frame to contain the Treeview
        frame = Frame(self.window, background="white")
        frame.place(x=self.window.winfo_screenwidth() / 8.2, y=self.window.winfo_screenheight() / 3)

        # Treeview for displaying data
        self.tree = ttk.Treeview(frame, show="headings", height=16)
        self.tree["columns"] = ("BillNo", "CustomerName", "CustomerPhone", "TotalPrice", "DiscountedPrice", "DateTime")

        self.tree.heading("#1", text="BillNo")
        self.tree.heading("#2", text="CustomerName")
        self.tree.heading("#3", text="CustomerPhone")
        self.tree.heading("#4", text="TotalPrice")
        self.tree.heading("#5", text="DiscountedPrice")
        self.tree.heading("#6", text="DateTime")

        # Set column widths
        column_widths = {"BillNo": 170, "CustomerName": 170, "CustomerPhone": 170, "TotalPrice": 170,
                         "DiscountedPrice": 170, "DateTime": 170}

        for column, width in column_widths.items():
            self.tree.column(column, width=width, anchor="center")

        self.tree.pack()

        button = Button(frame, text="Show Products", font=("Arial", 12, "bold"), bg="#487307", fg="white", width=25,
                        height=3, command=self.show_products)
        button.pack(side=BOTTOM, pady=10, padx=10)

        # Frame for displaying chart
        self.chart_frame = Frame(self.window, background="white")
        self.chart_frame.place(x=self.window.winfo_screenwidth() / 2, y=self.window.winfo_screenheight() / 2)

        # Populate treeview with data
        self.populate_treeview()
    def menu_interface(self):
        SalesInterface.SalesInterface(self.window)

    def show_products(self):
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
        print(product_data)
        return product_data

    def create_product_details_window(self, product_data):
        # Create a new window for displaying product details
        details_window = Toplevel(self.window)
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
        ok_button = Button(details_window, text="OK", command=details_window.destroy, font=("Arial", 12), bg="#487307",
                           fg="white", width=15)
        ok_button.pack(side=BOTTOM, pady=10, padx=10)

    def populate_treeview(self):
        current_date = datetime.now()
        start_of_today = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_tomorrow = start_of_today + timedelta(days=1)

        # Fetch data from the database for the entire current day
        data = self.db.find()

        for index, row in enumerate(data, start=1):
            # Convert the string representation of the date to a datetime object
            row_date = datetime.strptime(row["DateTime"], "%Y-%m-%d %H:%M:%S")

            if row_date.date() == current_date.date():
                self.products.append({"BillNo": row["BillNo"], "Products": row["Products"]})
                self.tree.insert("", "end", values=(
                    row["BillNo"], row["CustomerName"], row["CustomerPhone"], row["TotalPrice"], row["DiscountedPrice"],
                    row["DateTime"]))

