import base64
from io import BytesIO
from tkinter import *
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk
from pymongo import errors

import ViewCustomerModuleInterface
from Database import customer


class UpdateCustomerInterface:
    def __init__(self, window, customer_name, customer_email, customer_address, image):
        self.image = image
        self.image_path = None
        self.window = window
        self.window.title(customer_name)
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

        # Back Button
        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface, font=("Arial", 12),
                                          bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        # Outer Frame
        self.add_outer_frame = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.add_outer_frame.place(x=self.window.winfo_screenwidth() / 2, y=self.window.winfo_screenheight() / 2,
                                   anchor="center")
        self.add_outer_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Customer Frame
        self.add_customer_frame = Frame(self.add_outer_frame, bg="#968802", highlightbackground="#968802",
                                        highlightthickness=0)
        self.add_customer_frame.pack()
        self.add_customer_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Customer Image
        decoded_image_data = base64.b64decode(self.image)
        self.customer_image = Image.open(BytesIO(decoded_image_data))
        self.customer_image = self.customer_image.resize((200, 200))
        self.customer_image = ImageTk.PhotoImage(self.customer_image)

        self.customer_image_label = Label(self.add_customer_frame, image=self.customer_image, bg="white")
        self.customer_image_label.grid(row=0, column=0, rowspan=5, padx=(0, 20))

        # Upload Image Button
        self.upload_image_button = Button(self.add_customer_frame, text="Change Image", font=("Arial", 12),
                                          bg="#487307", fg="white", width=15, command=self.upload_image)
        self.upload_image_button.grid(row=5, column=0, padx=(0, 20))

        # Title Label
        self.title_label = Label(self.add_customer_frame, text=customer_name, font=("Arial", 30, "bold"), bg="#968802",
                                 fg="white")
        self.title_label.grid(row=0, column=1, columnspan=2, pady=(5, 10), sticky="w")

        # Customer Email Entry
        self.customer_email_label = Label(self.add_customer_frame, text="Customer Email:", font=("Arial", 12),
                                          bg="#968802", fg="white")
        self.customer_email_label.grid(row=1, column=1, sticky="e", pady=(5, 5))

        self.customer_email_entry = Entry(self.add_customer_frame, font=("Arial", 12))
        self.customer_email_entry.grid(row=1, column=2, pady=(5, 5))
        self.customer_email_entry.focus_set()
        self.customer_email_entry.insert(0, customer_email)

        # Customer Address Entry
        self.customer_address_label = Label(self.add_customer_frame, text="Customer Address:", font=("Arial", 12),
                                            bg="#968802", fg="white")
        self.customer_address_label.grid(row=2, column=1, sticky="e", pady=(5, 5))

        self.customer_address_entry = Entry(self.add_customer_frame, font=("Arial", 12))
        self.customer_address_entry.grid(row=2, column=2, pady=(5, 5))
        self.customer_address_entry.insert(0, customer_address)

        # Update Customer Button
        self.add_button = Button(self.add_customer_frame, text=f"Update {customer_name}", font=("Arial", 12, "bold"),
                                 bg="#487307", fg="white", width=25, height=2, command=self.update_customer)
        self.add_button.grid(row=3, column=1, columnspan=2, pady=(0, 20))

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image",
                                               filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        self.image_path = file_path

    def menu_interface(self):
        ViewCustomerModuleInterface.ViewCustomerModulesInterface(self.window, 0)

    def update_customer(self):
        customer_name = self.title_label.cget("text")
        customer_email = self.customer_email_entry.get()
        customer_address = self.customer_address_entry.get()
        image_path = self.image_path

        self.window.attributes('-topmost', False)
        # Validate input fields
        if not customer_name or not customer_email or not customer_address:
            messagebox.showerror("Error", "Please fill in all the fields.")
            return

        # Prepare customer data for update
        customer_data = {"CustomerEmail": customer_email, "CustomerAddress": customer_address,
                         "CustomerImage": self.image if not image_path else self.encode_image(image_path)}

        # Create a top-level window for confirmation
        confirmation_window = Toplevel(self.window)
        confirmation_window.title("Confirmation")
        x = (confirmation_window.winfo_screenwidth() - 500) // 2
        y = (confirmation_window.winfo_screenheight() - 500) // 2

        confirmation_window.geometry(f"{500}x{500}+{x}+{y}")

        # Display the data in the confirmation window
        data_label = Label(confirmation_window, text=f"Customer Name: {customer_name}\n"
                                                     f"Customer Email: {customer_email}\n"
                                                     f"Customer Address: {customer_address}\n", font=("Arial", 12),
                           bg="#968802", fg="white")
        data_label.pack()

        if image_path:
            image = Image.open(image_path)
            image = image.resize((300, 300))
            image = ImageTk.PhotoImage(image)

            image_label = Label(confirmation_window, image=image)
            image_label.image = image
            image_label.pack()
        else:
            decoded_image_data = base64.b64decode(self.image)
            image = Image.open(BytesIO(decoded_image_data))
            image = image.resize((200, 200))
            image = ImageTk.PhotoImage(image)
            image_label = Label(confirmation_window, image=image)
            image_label.image = image
            image_label.pack()

        # Add Yes and No buttons
        yes_button = Button(confirmation_window, text="Yes", font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=10,
                            command=lambda: self.save_to_database(customer_name, customer_data, confirmation_window))
        yes_button.pack(side="left", padx=20)

        no_button = Button(confirmation_window, text="No", font=("Arial", 12, "bold"), bg="#487307", fg="white",
                           width=10, command=confirmation_window.destroy)
        no_button.pack(side="right", padx=20)

    def save_to_database(self, customer_name, customer_data, confirmation_window):
        self.window.attributes('-topmost', True)
        self.window.state('zoomed')
        result = None
        try:
            # Update the document based on the customer name
            result = customer.update_one({"CustomerName": customer_name}, {"$set": customer_data})
            print(f"Matched {result.matched_count} document(s) and modified {result.modified_count} document(s)")
        except errors.PyMongoError as e:
            print(f"Error updating document: {e}")

        if result and result.modified_count > 0:
            messagebox.showinfo("Success", "Data updated in the database.")

            # Clear entry fields after successful update
            self.customer_email_entry.delete(0, END)
            self.customer_address_entry.delete(0, END)

        # Close the confirmation window
        confirmation_window.destroy()
        # Assuming ViewCustomerModulesInterface displays the updated customer list
        ViewCustomerModuleInterface.ViewCustomerModulesInterface(self.window, 0)

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            binary_data = image_file.read()
            binary_data = base64.b64encode(binary_data).decode('utf-8')
        return binary_data
