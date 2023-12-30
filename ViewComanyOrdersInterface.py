import tkinter as tk
from datetime import datetime
from tkinter import ttk, SOLID

from PIL import Image, ImageTk

import CompanyOrders
# Replace these imports with your actual module imports
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
        self.tree = ttk.Treeview(self.content_frame, columns=("Company", "Warehouse", "Order Date and Time"),
                                 show="headings")
        self.tree.heading("Company", text="Company")
        self.tree.heading("Warehouse", text="Warehouse")
        self.tree.heading("Order Date and Time", text="Order Date and Time")

        self.tree.pack(expand=True, fill="both")

        self.show_products_button = tk.Button(self.content_frame, text="Show Products", command=self.show_products,
                                              font=("Arial", 12, "bold"), bg="#487307", fg="white", width=20, height=3)
        self.show_products_button.pack(pady=10)

        # Fetch and display orders
        self.display_orders()

    def display_orders(self):
        orders_cursor = companyorders.find()
        orders = list(orders_cursor)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for order in orders:
            company_name = order["company_name"]
            order_date = order["order_date"]
            warehouse = order["warehouse_name"]

            values = (company_name, warehouse, order_date)

            self.tree.insert("", "end", values=values, tags=("order_tag",))

    def show_products(self):
        self.window.attributes('-topmost', False)
        # Get the selected item in the treeview
        selected_item = self.tree.focus()
        if selected_item:
            order_details = self.tree.item(selected_item, "values")
            company_name, warehouse_name, order_date_str = order_details

            # Convert order_date_str to a datetime object
            order_date = datetime.strptime(order_date_str, "%Y-%m-%d %H:%M:%S.%f")

            selected_order = companyorders.find_one(
                {"company_name": company_name, "order_date": order_date, "warehouse_name": warehouse_name})

            # Open a new window to display product details
            product_details_window = tk.Toplevel(self.window)
            product_details_window.title("Product Details")

            # Create and configure a treeview for product details
            product_tree = ttk.Treeview(product_details_window, columns=("Product Name", "Quantity"), show="headings", )
            product_tree.heading("Product Name", text="Product Name")
            product_tree.heading("Quantity", text="Quantity")

            # Insert product details into the treeview
            for product in selected_order["products"]:
                product_name = product["product_name"]
                quantity = product["quantity"]
                product_tree.insert("", "end", values=(product_name, quantity))

            # Pack the treeview and configure for visibility
            product_tree.pack(expand=True, fill="both")
            product_tree.tag_configure("merged", font=("Arial", 12, "bold"), background="#f0f0f0")

            # Add "OK" button to close the product details window
            ok_button = tk.Button(product_details_window, text="OK",
                                  command=lambda: self.destory(product_details_window), font=("Arial", 12, "bold"),
                                  bg="#487307", fg="white", width=10, )
            ok_button.pack(pady=10)

    def destory(self, product_details_window):
        self.window.attributes('-topmost', True)
        product_details_window.destroy()

    def menu_interface(self):
        CompanyOrders.CompanyOrders(self.window)
