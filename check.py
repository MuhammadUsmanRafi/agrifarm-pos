import time
from tkinter import *
from tkinter import ttk

import qrcode
from PIL import Image, ImageTk

import SalesInterface
from Database import product


class NewSalesModuleInterface:
    def __init__(self, window):

        self.product_collection = product
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

        search_button = Button(self.customer_entries_frame, text="Search", command=self.search_bill,
                               font=("Arial", 12, "bold"), bg="#487307", fg="white")
        search_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        name_label = Label(self.customer_entries_frame, text="Customer Name:", font=("Arial", 12, "bold"), bg="#968802",
                           foreground="white")
        name_label.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        self.customer_name_entry = Entry(self.customer_entries_frame, font=("Arial", 12, "bold"))
        self.customer_name_entry.grid(row=0, column=4, padx=10, pady=5, sticky="w")

        phone_label = Label(self.customer_entries_frame, text="Customer Phone:", font=("Arial", 12, "bold"),
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

        bill_label = Label(self.bill_area, bg="white", foreground="#968802", text="Bill Area",
                           font=("Arial", 20, "bold"), anchor="center")
        bill_label.config(padx=180, pady=200)
        bill_label.pack()

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

    def total(self):
        pass

    def generate_bill(self):
        pass

    def clear_field(self):
        pass

    def generate_qr_code(self, data):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=2, )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        return ImageTk.PhotoImage(image=img)

    def show_qr_code(self):
        data = "This is the data of the QR code"
        qr_code_image = self.generate_qr_code(data)
        self.qr_img_label.config(image=qr_code_image)
        self.qr_img_label.image = qr_code_image

    def discount(self, percentage):
        pass

    def menu_interface(self):
        SalesInterface.SalesInterface(self.window)

    def update_time(self):
        current_time = time.strftime("%I:%M %p")
        self.system_time_label.config(text=current_time)
        self.window.after(1000, self.update_time)

    def search_bill(self):
        pass

    def add_to_cart(self):
        pass

    def clear(self):
        self.product_name_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.product_name_entry.focus_set()


if __name__ == "__main__":
    root = Tk()
    login_interface = NewSalesModuleInterface(root)
    root.mainloop()
