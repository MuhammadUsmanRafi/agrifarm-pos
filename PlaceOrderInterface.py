import smtplib
import tkinter as tk
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import *
from tkinter import ttk, messagebox

from PIL import Image, ImageTk

import CompanyOrders
from Database import company, companyorders


class PlaceOrderInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Place Order")

        # Get the screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Set the window size to fill the entire screen
        self.window.geometry(f"{screen_width}x{screen_height}")

        # Set background image for the login window
        background_image_path = "assets/login_bg2.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = tk.Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface, font=("Arial", 12),
                                          bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        self.company_collection = company
        self.orders_collection = companyorders

        self.outer = tk.Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.outer.place(x=(self.window.winfo_screenwidth() / 2), y=self.window.winfo_screenheight() / 2 + 20,
                         anchor="center")
        self.outer.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)
        # Frame to hold the content
        content_frame = tk.Frame(self.outer, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        content_frame.pack()
        content_frame.config(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Dropdown menu for selecting a company
        self.company_label = tk.Label(content_frame, text="Select Company:", font=("Arial", 12), bg="#968802",
                                      fg="white")
        self.company_label.pack(pady=10)

        # Fetch company names from the database
        company_names = [companies["CName"] for companies in self.company_collection.find()]

        self.selected_company = tk.StringVar()
        self.company_dropdown = ttk.Combobox(content_frame, textvariable=self.selected_company, values=company_names,
                                             font=("Arial", 12))
        self.company_dropdown.pack()
        self.company_dropdown.set("Select Company")

        # Entries for entering product details
        self.product_name_label = tk.Label(content_frame, text="Enter Product Name:", font=("Arial", 12), bg="#968802",
                                           fg="white")
        self.product_name_label.pack()

        self.product_name_entry = tk.Entry(content_frame, font=("Arial", 12))
        self.product_name_entry.pack()

        self.quantity_label = tk.Label(content_frame, text="Enter Quantity:", font=("Arial", 12), bg="#968802",
                                       fg="white")
        self.quantity_label.pack()

        self.quantity_entry = tk.Entry(content_frame, font=("Arial", 12))
        self.quantity_entry.pack()

        # Button to add product details
        self.add_product_button = tk.Button(content_frame, text="Add More Product", command=self.add_product,
                                            font=("Arial", 12), bg="#487307", fg="white", width=20, height=1)
        self.add_product_button.pack(pady=5)

        # Button to place the order
        self.place_order_button = tk.Button(content_frame, text="Place Order", command=self.place_order,
                                            font=("Arial", 12), bg="#487307", fg="white", width=20, height=1)
        self.place_order_button.pack(pady=5)

        # Lists to store product details
        self.product_list = []

    def add_product(self):
        product_name = self.product_name_entry.get().strip()
        quantity = self.quantity_entry.get().strip()

        if not product_name or not quantity:
            messagebox.showerror("Error", "Please enter product details.")
            return

        product_details = {"product_name": product_name, "quantity": quantity}
        self.product_list.append(product_details)

        # Clear the entry fields
        self.product_name_entry.delete(0, tk.END)
        self.product_name_entry.focus_set()
        self.quantity_entry.delete(0, tk.END)

    def place_order(self):
        selected_company = self.selected_company.get()

        if selected_company == "Select Company" or not self.product_list:
            messagebox.showerror("Error", "Please select a company and add products.")
            return

        # Convert date to datetime object for compatibility with MongoDB
        order_date_pakistan = datetime.now()

        order_data = {"company_name": selected_company, "products": self.product_list,
                      "order_date": order_date_pakistan}

        self.orders_collection.insert_one(order_data)

        # Send an email to the company
        company_info = self.company_collection.find_one({"CName": selected_company})
        if company_info and "cEmail" in company_info:
            company_email = company_info["cEmail"]
            sender_email = "musmanrajputt490@gmail.com"
            sender_password = "iuox lzmd wzlr awrb"  # Replace with your email password

            subject = "New Order Placement"
            body = (
                f"Dear Manager of {selected_company},\n\nA new order has been placed on {order_date_pakistan} from Agrifarm."
                f"\n\nDetails:\n\n")

            # Format product details in a table
            body += "<table border='1'><tr><th>Product Name</th><th>Quantity</th></tr>"
            for product in self.product_list:
                body += f"<tr><td>{product['product_name']}</td><td>{product['quantity']}</td></tr>"
            body += "</table>"

            body += (f'\n\nBest Regards,\n\n'
                     f'Muhammad Usman\n\n'
                     f'Manager of Agrifarm\n\n'
                     f'Contact: +92 123 456789\n\n'
                     f'Email: agrifarm@gmail.com')

            # Set up the email message
            message = MIMEMultipart()
            message.attach(MIMEText(body, "html"))
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = company_email

            # Connect to the SMTP server and send the email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, company_email, message.as_string())

            messagebox.showinfo("Success", "Order placed successfully! Email sent to the company.")
        else:
            messagebox.showwarning("Warning", "Company email not found. Order placed successfully, but email not sent.")

        # Clear the product list
        self.product_list = []

        result = messagebox.showinfo("Success", "Order placed successfully!")
        if result:
            CompanyOrders.CompanyOrders(self.window)

    def menu_interface(self):
        CompanyOrders.CompanyOrders(self.window)
