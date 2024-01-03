import base64
from tkinter import *
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

import CustomerInterface
import ViewCustomerModuleInterface
from Database import customer


class AddCustomer:
    def __init__(self, window, num):
        self.labels = ["View Customer", "Add Customer", "Recent Customer", "Remove Customer"]
        self.window = window
        self.window.title(self.labels[num])
        self.window.geometry(f"{int(window.winfo_screenwidth() / 1.5)}x{int(window.winfo_screenheight() / 1.5)}")
        self.window.iconbitmap("icon.ico")

        background_image_path = "assets/login_bg2.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface, font=("Arial", 12),
                                          bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        self.add_outer_frame = Frame(self.window, bg="#968802", highlightbackground="black", highlightthickness=2)
        self.add_outer_frame.place(x=self.window.winfo_screenwidth() / 2, y=self.window.winfo_screenheight() / 2 + 11,
                                   anchor="center")
        self.add_outer_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.add_customer_frame = Frame(self.add_outer_frame, bg="#968802", highlightbackground="black",
                                        highlightthickness=2)  # Added black border
        self.add_customer_frame.pack()

        self.add_customer_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.title_label = Label(self.add_customer_frame, text="Add Customer", font=("Arial", 16, "bold"), bg="#968802",
                                 fg="white")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(5, 10))

        self.customer_name_label = Label(self.add_customer_frame, text="Customer Name:", font=("Arial", 12),
                                         bg="#968802", fg="white")
        self.customer_name_label.grid(row=1, column=0, sticky="e", pady=(5, 5))

        self.customer_name_entry = Entry(self.add_customer_frame, font=("Arial", 12))
        self.customer_name_entry.grid(row=1, column=1, pady=(5, 5))
        self.customer_name_entry.focus_set()

        self.customer_email_label = Label(self.add_customer_frame, text="Customer Email:", font=("Arial", 12),
                                          bg="#968802", fg="white")
        self.customer_email_label.grid(row=2, column=0, sticky="e", pady=(5, 5))

        self.customer_email_entry = Entry(self.add_customer_frame, font=("Arial", 12))
        self.customer_email_entry.grid(row=2, column=1, pady=(5, 5))

        self.customer_address_label = Label(self.add_customer_frame, text="Customer Address:", font=("Arial", 12),
                                            bg="#968802", fg="white")
        self.customer_address_label.grid(row=3, column=0, sticky="e", pady=(5, 5))

        self.customer_address_entry = Entry(self.add_customer_frame, font=("Arial", 12))
        self.customer_address_entry.grid(row=3, column=1, pady=(5, 5))

        self.upload_image_button = Button(self.add_customer_frame, text="Upload Image", font=("Arial", 12),
                                          bg="#487307", fg="white", width=15, command=self.upload_image)
        self.upload_image_button.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        self.image_path_label = Label(self.add_customer_frame, text="", font=("Arial", 10), bg="#968802", fg="white")
        self.image_path_label.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        self.add_button = Button(self.add_customer_frame, text="Add Customer", font=("Arial", 12, "bold"), bg="#487307",
                                 fg="white", width=25, height=2, command=self.add_customer)
        self.add_button.grid(row=6, column=0, columnspan=2, pady=(0, 20))

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image",
                                               filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        self.image_path_label.config(text=file_path)

    def add_customer(self):
        customer_name = self.customer_name_entry.get()
        customer_email = self.customer_email_entry.get()
        customer_address = self.customer_address_entry.get()
        image_path = self.image_path_label.cget("text")

        self.window.attributes('-topmost', False)

        with open(image_path, "rb") as image_file:
            binary_data = image_file.read()
            binary_data = base64.b64encode(binary_data).decode('utf-8')

        customer_data = {"CustomerName": customer_name, "CustomerEmail": customer_email,
                         "CustomerAddress": customer_address, "CustomerImage": binary_data, "Orders": []}

        # Display customer data in a confirmation window
        self.display_confirmation(customer_data, image_path)

    def display_confirmation(self, customer_data, image_path):
        # Create a top-level window for confirmation
        confirmation_window = Toplevel(self.window)
        confirmation_window.title("Confirmation")
        x = (confirmation_window.winfo_screenwidth() - 500) // 2
        y = (confirmation_window.winfo_screenheight() - 500) // 2

        confirmation_window.geometry(f"{500}x{500}+{x}+{y}")

        # Display the data in the confirmation window
        data_label = Label(confirmation_window, text=f"Customer Name: {customer_data['CustomerName']}\n"
                                                     f"Customer Email: {customer_data['CustomerEmail']}\n"
                                                     f"Customer Address: {customer_data['CustomerAddress']}\n",
                           font=("Arial", 12), bg="#968802", fg="white")
        data_label.pack()

        image = Image.open(image_path)
        image = image.resize((300, 300))
        image = ImageTk.PhotoImage(image)

        image_label = Label(confirmation_window, image=image)
        image_label.image = image
        image_label.pack()

        # Add Yes and No buttons
        yes_button = Button(confirmation_window, text="Yes", font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=10, command=lambda: self.save_to_database(customer_data, confirmation_window))
        yes_button.pack(side="left", padx=20)

        no_button = Button(confirmation_window, text="No", font=("Arial", 12, "bold"), bg="#487307", fg="white",
                           width=10, command=confirmation_window.destroy)
        no_button.pack(side="right", padx=20)

    def save_to_database(self, customer_data, confirmation_window):
        # Check if the customer with the same name and email exists
        existing_customer = customer.find_one(
            {"CustomerName": customer_data['CustomerName'], "CustomerEmail": customer_data['CustomerEmail']})

        if existing_customer:
            # Update existing customer
            result = customer.update_one(
                {"CustomerName": customer_data['CustomerName'], "CustomerEmail": customer_data['CustomerEmail']},
                {"$set": customer_data}, upsert=True)
            messagebox.showinfo("Success", "Data updated in the database.")
        else:
            result = customer.insert_one(customer_data)
            messagebox.showinfo("Success", "Data saved into the database.")

        if result.upserted_id or result.modified_count > 0:
            # Clear entry widgets and labels
            self.customer_name_entry.delete(0, END)
            self.customer_email_entry.delete(0, END)
            self.customer_address_entry.delete(0, END)
            self.image_path_label.config(text="")

            # Close the confirmation window
            confirmation_window.destroy()
            self.window.attributes('-topmost', True)
            ViewCustomerModuleInterface.ViewCustomerModulesInterface(self.window, 3)
        else:
            messagebox.showerror("Error", "Failed to save/update data in the database.")

    def menu_interface(self):
        CustomerInterface.CustomerInterface(self.window)


if __name__ == "__main__":
    root = Tk()
    add_customer_interface = AddCustomer(root, 1)
    root.mainloop()
