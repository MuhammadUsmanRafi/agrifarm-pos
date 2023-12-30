import base64
import time
from io import BytesIO
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import qrcode
from PIL import Image, ImageTk

import SalesInterface
from Database import product, productsales


class NewSalesModuleInterface:
    def __init__(self, window):
        self.discount_check = False
        self.total_price = 0
        self.discount_bill = 0
        self.original_total = 0
        self.product_collection = product
        self.cart_items = []
        self.window = window
        self.window.title("Sales")
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        # Set background image for the login window
        background_image_path = "assets/new_sales.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface, font=("Arial", 12),
                                          bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        label = Label(self.window, text="New Sales Billing System", font=("Arial", 40, "bold"), foreground="white",
                      bg="#968802")
        label.place(x=self.window.winfo_screenwidth() / 3.7, y=30)

        self.system_time_label = Label(self.window, text="", font=("Arial", 25, "bold"), bg="#968802",
                                       foreground="white")
        self.system_time_label.place(x=self.window.winfo_screenwidth() - 200, y=40)
        self.update_time()

        self.customer = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.customer.place(x=self.window.winfo_screenwidth() / 5 - 272, y=self.window.winfo_screenheight() / 6.5)
        self.customer.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        customer_label = Label(self.customer, text="Customer Details", font=("Arial", 14, "bold"), bg="#968802",
                               foreground="white")
        customer_label.config(padx=10)
        customer_label.grid(row=0, column=0)

        self.customer_entries_frame = Frame(self.customer, bg="#968802", highlightbackground="#968802",
                                            highlightthickness=0)
        self.customer_entries_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)
        self.customer_entries_frame.grid(row=0, column=1)

        bill_label = Label(self.customer_entries_frame, text="Bill No:", font=("Arial", 12, "bold"), bg="#968802",
                           foreground="white")
        bill_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.bill_no_entry = Entry(self.customer_entries_frame, font=("Arial", 12, "bold"))
        self.bill_no_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.bill_no_entry.delete(0, END)
        latest_bill = productsales.find_one(sort=[("BillNo", -1)])
        if latest_bill:
            self.bill_no_entry.insert(0, latest_bill["BillNo"] + 1)
        else:
            self.bill_no_entry.insert(0, "1")

        search_button = Button(self.customer_entries_frame, text="Search", command=self.search_bill,
                               font=("Arial", 12, "bold"), bg="#487307", fg="white")
        search_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        name_label = Label(self.customer_entries_frame, text="Customer Name:", font=("Arial", 12, "bold"), bg="#968802",
                           foreground="white")
        name_label.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        self.customer_name_entry = Entry(self.customer_entries_frame, font=("Arial", 12, "bold"))
        self.customer_name_entry.grid(row=0, column=4, padx=10, pady=5, sticky="w")

        phone_label = Label(self.customer_entries_frame, text="Phone or Email:", font=("Arial", 12, "bold"),
                            bg="#968802", foreground="white")
        phone_label.grid(row=0, column=5, padx=10, pady=5, sticky="w")

        self.customer_phone_entry = Entry(self.customer_entries_frame, font=("Arial", 12, "bold"))
        self.customer_phone_entry.grid(row=0, column=6, padx=10, pady=5, sticky="w")

        # Product Details Frame

        self.product = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.product.place(x=self.window.winfo_screenwidth() / 5 - 272, y=self.window.winfo_screenheight() / 3 - 9)
        self.product.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        product_label = Label(self.product, text="Product Details", font=("Arial", 14, "bold"), bg="#968802",
                              foreground="white")
        product_label.grid(row=0, column=0, pady=10)

        self.product_frame = Frame(self.product, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.product_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)
        self.product_frame.grid(row=1, column=0)

        product_name_label = Label(self.product_frame, text="Product", font=("Arial", 12, "bold"), bg="#968802",
                                   foreground="white")
        product_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.product_name_entry = Entry(self.product_frame, font=("Arial", 12, "bold"))
        self.product_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        select_product_button = Button(self.product_frame, text="Select Product",
                                       command=lambda: self.show_product_list(self.window), font=("Arial", 12, "bold"),
                                       bg="#487307", fg="white", width=15)
        select_product_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        quantity_label = Label(self.product_frame, text="Quantity", font=("Arial", 12, "bold"), bg="#968802",
                               foreground="white")
        quantity_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.quantity_entry = Entry(self.product_frame, font=("Arial", 12, "bold"))
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Add to Cart Button
        add_to_cart_button = Button(self.product_frame, text="Add to Cart", command=self.add_to_cart,
                                    font=("Arial", 12, "bold"), bg="#487307", fg="white", width=15)
        add_to_cart_button.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Clear Button
        clear_button = Button(self.product_frame, text="Clear", command=self.clear, font=("Arial", 12, "bold"),
                              bg="#487307", fg="white", width=15)
        clear_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # QR Code Frame
        self.QR_Discount = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.QR_Discount.place(x=self.window.winfo_screenwidth() / 2 - 212, y=self.window.winfo_screenheight() / 3 - 9)
        self.QR_Discount.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.discount_frame = Frame(self.QR_Discount, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.discount_frame.grid(row=0, column=0)

        discount_label = Label(self.discount_frame, text="Discount", font=("Arial", 14, "bold"), anchor="center",
                               bg="#968802", foreground="white")
        discount_label.grid(row=0, column=0, padx=10, columnspan=3, sticky="nsew")

        discount_5 = Button(self.discount_frame, text="5% off", command=lambda: self.discount(5),
                            font=("Arial", 12, "bold"), bg="#487307", fg="white", width=10)
        discount_5.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        discount_10 = Button(self.discount_frame, text="10% off", command=lambda: self.discount(10),
                             font=("Arial", 12, "bold"), bg="#487307", fg="white", width=10)
        discount_10.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        discount_20 = Button(self.discount_frame, text="20% off", command=lambda: self.discount(20),
                             font=("Arial", 12, "bold"), bg="#487307", fg="white", width=10)
        discount_20.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.qr_img_label = Label(self.QR_Discount, bg="#968802")
        self.qr_img_label.grid(row=1, column=0, columnspan=3, padx=10, pady=13, sticky="nsew")
        self.show_qr_code()

        self.lowest_frame = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.lowest_frame.place(x=self.window.winfo_screenwidth() / 5 - 272,
                                y=self.window.winfo_screenheight() / 2 * 1.39)
        self.lowest_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.Button_frame = Frame(self.lowest_frame, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.Button_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)
        self.Button_frame.pack()

        total_button = Button(self.Button_frame, text="Total", command=lambda: self.total(), font=("Arial", 12, "bold"),
                              bg="#487307", fg="white", width=24, height=3)
        total_button.grid(row=0, column=0, padx=6, pady=5, sticky="w")
        generate_button = Button(self.Button_frame, text="Generate", command=lambda: self.generate_bill(),
                                 font=("Arial", 12, "bold"), bg="#487307", fg="white", width=24, height=3)
        generate_button.grid(row=0, column=1, padx=6, pady=5, sticky="w")
        clear_button = Button(self.Button_frame, text="Clear", command=lambda: self.clear_field(),
                              font=("Arial", 12, "bold"), bg="#487307", fg="white", width=24, height=3)
        clear_button.grid(row=0, column=2, padx=6, pady=5, sticky="w")

        self.bill_area = Frame(self.window, bg="white", highlightbackground="#968802", highlightthickness=0)
        self.bill_area.place(x=self.window.winfo_screenwidth() / 2 * 1.276, y=self.window.winfo_screenheight() / 3 - 9)
        self.bill_area.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.update_bill_area()

    def show_product_list(self, window):
        self.window = window
        self.select_product_window = Toplevel(self.window)
        self.select_product_window.title("Select Product")
        self.select_product_window.geometry("800x400")

        # Add a search field
        self.search_label = Label(self.select_product_window, text="Search Product:", font=("Arial", 12, "bold"))
        self.search_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.search_entry = Entry(self.select_product_window, font=("Arial", 12, "bold"))
        self.search_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.search_entry.focus_set()
        self.search_entry.bind("<KeyRelease>", lambda event: self.filter_products(event))

        # Create Treeview to display product details
        self.tree = ttk.Treeview(self.select_product_window,
                                 columns=("ProductName", "ProductCompany", "ProductBrand", "QuantityInStock"))
        self.tree.heading("#0", text="Select")
        self.tree.heading("ProductName", text="Product Name")
        self.tree.heading("ProductCompany", text="Company")
        self.tree.heading("ProductBrand", text="Brand")
        self.tree.heading("QuantityInStock", text="Quantity In Stock")
        self.tree["show"] = "headings"

        self.tree.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Add a Select button
        select_button = Button(self.select_product_window, text="Select",
                               command=lambda: self.select_product(self.select_product_window),
                               font=("Arial", 12, "bold"), bg="#487307", fg="white", width=15)
        select_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.select_product_window.rowconfigure(1, weight=1)
        self.select_product_window.columnconfigure(1, weight=1)

        self.window.attributes("-topmost", False)

        self.populate_product_treeview()

    def populate_product_treeview(self):
        # Clear existing items in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch products from MongoDB
        products = self.product_collection.find()

        # Insert products into the Treeview
        for pd in products:
            self.tree.insert("", "end", values=(
                pd["ProductName"], pd["ProductCompany"], pd["ProductBrand"], pd["QuantityInStock"]))

    def filter_products(self, event):
        # Implement product filtering based on the search_entry value
        search_text = self.search_entry.get().lower()

        # Clear existing items in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch products from MongoDB
        products = self.product_collection.find()

        # Insert products into the Treeview based on the search text
        for pd in products:
            product_name = pd["ProductName"]
            if not search_text or search_text in str(product_name).lower():
                self.tree.insert("", "end", values=(
                    pd["ProductName"], pd["ProductCompany"], pd["ProductBrand"], pd["QuantityInStock"]))

    def select_product(self, new_window):
        selected_item = self.tree.selection()
        if selected_item:
            productname = self.tree.item(selected_item, "values")[0]

            # Convert the string representation of ObjectId back to ObjectId
            selected_product = self.product_collection.find_one({"ProductName": productname})

            # Extract product details and set them in the main window
            product_name = selected_product["ProductName"]
            product_company = selected_product["ProductCompany"]
            product_brand = selected_product["ProductBrand"]
            quantity_in_stock = selected_product["QuantityInStock"]

            # Set the product details in the main window
            self.product_name_entry.delete(0, END)
            self.product_name_entry.insert(0, product_name)

            # Destroy the product list window
            new_window.destroy()

    def add_to_cart(self):
        # Get values from entry fields
        product_name = self.product_name_entry.get()
        entered_quantity = self.quantity_entry.get()

        # Check if the entered quantity is a valid positive integer
        if not entered_quantity.isdigit() or int(entered_quantity) <= 0:
            messagebox.showinfo("Invalid Quantity", "Please enter a valid positive quantity.")
            return

        # Convert entered quantity to an integer
        quantity = int(entered_quantity)

        # Check if the product exists in the database
        selected_product = self.product_collection.find_one({"ProductName": product_name})

        if selected_product:
            # Extract product details from the database
            quantity_in_stock = selected_product["QuantityInStock"]
            price_in_stock = selected_product["ProductPrice"]

            # Check if the entered quantity is less than or equal to the quantity in stock
            if quantity <= quantity_in_stock:
                # Check if the product is already in the cart
                existing_cart_item = next((item for item in self.cart_items if item["Product Name"] == product_name),
                                          None)

                if existing_cart_item:
                    # Update the quantity of the existing item
                    self.total_price -= existing_cart_item["t_Price"]
                    existing_cart_item["Quantity"] = quantity
                    existing_cart_item["t_Price"] = price_in_stock * existing_cart_item["Quantity"]
                    self.total_price += existing_cart_item["t_Price"]
                else:
                    # Use the actual price from the database instead of dummy data
                    price = price_in_stock
                    t_price = price_in_stock * quantity
                    self.total_price += t_price

                    # Create a dictionary for the cart item
                    cart_item = {"Product Name": product_name, "Quantity": quantity, "Unit Price": price,
                                 "t_Price": t_price}

                    # Add the cart item to the list
                    self.cart_items.append(cart_item)

                # Update the bill area
                self.update_bill_area()

                # Clear the entry fields
                self.clear()
            else:
                messagebox.showinfo("Insufficient Stock",
                                    f"Quantity is higher than the stock available ({quantity_in_stock}).")

    def update_cart(self):
        selected_item = self.cart_tree.selection()
        if selected_item:
            # Get the selected item index
            item_index = int(selected_item[0][1:]) - 1

            # Get the selected cart item
            selected_cart_item = self.cart_items[item_index]

            # Set the product name and quantity in the entry fields
            self.product_name_entry.delete(0, END)
            self.product_name_entry.insert(0, selected_cart_item["Product Name"])
            self.quantity_entry.delete(0, END)
            self.quantity_entry.insert(0, selected_cart_item["Quantity"])

            # Update the bill area
            self.update_bill_area()

    def delete_cart(self):
        selected_item = self.cart_tree.selection()
        if selected_item:
            # Get the selected item index
            item_index = int(selected_item[0][1:]) - 1

            # Subtract the t_Price of the selected item from the total_price
            self.total_price -= self.cart_items[item_index]["t_Price"]

            # Remove the selected item from the cart_items list
            del self.cart_items[item_index]

            # Update the bill area
            self.update_bill_area()

    def update_bill_area(self):
        # Clear existing items in the Treeview and buttons
        for item in self.bill_area.winfo_children():
            item.destroy()

        # Create Treeview to display cart details
        self.cart_tree = ttk.Treeview(self.bill_area, columns=("Product Name", "Quantity", "Unit Price", "t_Price"),
                                      height=14)
        self.cart_tree.heading("Product Name", text="Product Name")
        self.cart_tree.heading("Quantity", text="Quantity")
        self.cart_tree.heading("Unit Price", text="Unit Price")
        self.cart_tree.heading("t_Price", text="t_Price")
        self.cart_tree["show"] = "headings"

        column_widths = {"Product Name": 180, "Quantity": 70, "Unit Price": 70, "t_Price": 120}
        for column, width in column_widths.items():
            self.cart_tree.column(column, width=width, anchor="center")

        self.cart_tree.grid(row=0, column=0, columnspan=2, pady=5, sticky="nsew")

        # Add items to the Treeview
        for i, item in enumerate(self.cart_items):
            self.cart_tree.insert("", "end",
                                  values=(item["Product Name"], item["Quantity"], item["Unit Price"], item["t_Price"]))

        discount_bill_label = Label(self.bill_area, text="Discount Bill", font=("Arial", 12, "bold"), bg="white")
        discount_bill_label.grid(row=1, column=0, padx=6, pady=2, sticky="nsew")

        discount_bill = Label(self.bill_area, text=f"{self.discount_bill}", font=("Arial", 12, "bold"), bg="white")
        discount_bill.grid(row=1, column=1, padx=6, pady=2, sticky="nsew")

        self.total_bill_label = Label(self.bill_area, text="Total Bill", font=("Arial", 12, "bold"), bg="white")
        self.total_bill_label.grid(row=2, column=0, padx=6, pady=2, sticky="nsew")

        total_bill = Label(self.bill_area, text=f"{self.total_price}", font=("Arial", 12, "bold"), bg="white")
        total_bill.grid(row=2, column=1, padx=6, pady=2, sticky="nsew")

        # Buttons for updating or deleting selected row in the cart
        update_button = Button(self.bill_area, text="Update", command=self.update_cart, font=("Arial", 12, "bold"),
                               bg="#487307", fg="white", width=12, height=2)
        update_button.grid(row=3, column=0, padx=6, pady=2, sticky="nsew")
        delete_button = Button(self.bill_area, text="Delete", command=self.delete_cart, font=("Arial", 12, "bold"),
                               bg="#487307", fg="white", width=12, height=2)
        delete_button.grid(row=3, column=1, padx=6, pady=2, sticky="nsew")

        self.show_qr_code()

    def total(self):
        self.total_price = self.total_price - self.discount_bill
        self.update_bill_area()
        self.show_qr_code()

    def generate_bill(self):
        if not self.cart_items:
            messagebox.showinfo("No Product Selected", "Please select at least one product.")
            return

        # Check if all fields are filled
        if not all([self.bill_no_entry.get(), self.customer_name_entry.get(), self.customer_phone_entry.get()]):
            messagebox.showinfo("Incomplete Fields", "Please fill in all the required fields.")
            return

        # Get data from fields
        bill_no = int(self.bill_no_entry.get())
        customer_name = self.customer_name_entry.get()
        customer_phone = self.customer_phone_entry.get()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        # Prepare data for insertion or update in productsales database
        sales_data = {"BillNo": bill_no, "CustomerName": customer_name, "CustomerPhone": customer_phone,
                      "TotalPrice": self.total_price, "DiscountedPrice": self.total_price - self.discount_bill,
                      "DateTime": current_time, "Products": self.cart_items}

        # 1. Insert QR code base64 into the database
        qr_code_base64 = self.generate_qr_code_base64(sales_data)
        sales_data["QRCodeBase64"] = qr_code_base64

        # 2. Update selected product quantity in the database
        for item in self.cart_items:
            product_name = item["Product Name"]
            selected_product = self.product_collection.find_one({"ProductName": product_name})

            if selected_product:
                # Update product quantity in stock
                new_quantity = selected_product["QuantityInStock"] - item["Quantity"]
                self.product_collection.update_one({"ProductName": product_name},
                                                   {"$set": {"QuantityInStock": new_quantity}})

        # Check if the bill_no already exists in the database
        existing_bill = productsales.find_one({"BillNo": bill_no})
        if existing_bill:
            # Update the existing document
            productsales.update_one({"BillNo": bill_no}, {"$set": sales_data})
            messagebox.showinfo("Update Successful", "Bill updated successfully.")
        else:
            # Insert a new document
            productsales.insert_one(sales_data)
            messagebox.showinfo("Insert Successful", "New bill inserted successfully.")

        # Clear fields and reset the UI
        self.clear_field()

    def clear_field(self):
        NewSalesModuleInterface(self.window)

    def generate_qr_code_base64(self, data):
        # Generate QR code
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=1)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((175, 175))

        # Convert image to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return img_base64

    def generate_qr_code(self, data):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=1, )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((175, 175))
        return ImageTk.PhotoImage(image=img)

    def show_qr_code(self):
        # Gather data for the QR code
        bill_no = self.bill_no_entry.get()
        customer_name = self.customer_name_entry.get()
        customer_phone = self.customer_phone_entry.get()

        selected_products = "\n".join(
            f"{item['Product Name']} - {item['Quantity']} units - ${item['t_Price']}" for item in self.cart_items)

        data = f"Bill No: {bill_no}\nCustomer Name: {customer_name}\nCustomer Phone/Email: {customer_phone}\n\nSelected Products:\n{selected_products}"

        # Generate and display the QR code
        qr_code_image = self.generate_qr_code(data)
        self.qr_img_label.config(image=qr_code_image)
        self.qr_img_label.image = qr_code_image

    def discount(self, percentage):
        if self.total_price > 0:
            self.original_total = sum(cart_item["t_Price"] for cart_item in self.cart_items)

            if self.discount_check:
                self.discount_bill = 0

            discounted_total = self.original_total * (percentage / 100)

            self.discount_bill = self.original_total - (self.original_total - discounted_total)

            self.total_price = self.original_total

            self.discount_check = True

            self.update_bill_area()

    def menu_interface(self):
        SalesInterface.SalesInterface(self.window)

    def update_time(self):
        current_time = time.strftime("%I:%M %p")
        self.system_time_label.config(text=current_time)
        self.window.after(1000, self.update_time)

    def search_bill(self):
        # Retrieve the bill number entered by the user
        bill_no = int(self.bill_no_entry.get())

        # Query the database to check if the bill exists
        existing_bill = productsales.find_one({"BillNo": bill_no})

        if existing_bill:
            # Retrieve data from the existing bill
            customer_name = existing_bill["CustomerName"]
            customer_phone = existing_bill["CustomerPhone"]
            selected_products = existing_bill["Products"]

            # Update UI with the retrieved data
            self.customer_name_entry.delete(0, END)
            self.customer_name_entry.insert(0, customer_name)
            self.customer_phone_entry.delete(0, END)
            self.customer_phone_entry.insert(0, customer_phone)

            # Add products from the existing bill to the cart
            self.cart_items = selected_products
            self.total_price = existing_bill["TotalPrice"]

            # Update the bill area
            self.update_bill_area()

            # Show QR code
            self.show_qr_code()

            messagebox.showinfo("Bill Found", f"Bill {bill_no} found and loaded.")
        else:
            messagebox.showinfo("Bill Not Found", f"Bill {bill_no} not found in the database.")

    def clear(self):
        self.product_name_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.product_name_entry.focus_set()
        self.show_qr_code()


if __name__ == "__main__":
    root = Tk()
    login_interface = NewSalesModuleInterface(root)
    root.mainloop()
