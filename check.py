import base64
from io import BytesIO
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

import CustomerInterface
import UpdateCustomerModuleInterface
from Database import customer

DEFAULT_ADDRESS = 'abc_address'
DEFAULT_IMAGE = '''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'''  # Replace this with the actual base64 string for the default image


class ViewCustomerModulesInterface:
    def __init__(self, window, num):
        self.labels = ["View Customer", "Add Customer", "Recent Customer", "Remove Customer"]
        self.window = window
        self.window.title(self.labels[num])
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        background_image_path = "assets/inventory_modules.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface, font=("Arial", 12),
                                          bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        self.title_label = Label(self.window, text=f"{self.labels[num]}", font=("Arial", 40, "bold"),
                                 background="#968802", foreground="white")
        self.title_label.place(x=self.window.winfo_screenwidth() / 2 - 150, y=20)

        self.canvas = Canvas(self.window, bg="white", highlightbackground="#968802", highlightthickness=0)
        self.canvas.place(x=0, y=self.window.winfo_screenheight() / 5, relwidth=1, relheight=0.5)

        self.outer_frame = Frame(self.canvas, bg="white", highlightbackground="#968802", highlightthickness=0)
        self.outer_frame.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = Scrollbar(self.window, orient=HORIZONTAL, command=self.canvas.xview)
        self.scrollbar.place(x=0, y=self.window.winfo_screenheight() * 0.65, relwidth=1, height=20)

        self.canvas.config(xscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.outer_frame, anchor='nw')

        self.outer_frame.bind("<Configure>", lambda event, canvas=self.canvas: self.on_frame_configure(canvas))

        # Search frame
        self.search_frame = Frame(self.window, bg="white", highlightbackground="#968802", highlightthickness=0)
        self.search_frame.place(x=self.window.winfo_screenwidth() / 2 - 100, y=self.window.winfo_screenheight() / 8)

        # Search label
        self.search_label = Label(self.search_frame, text="Search: ", font=("Arial", 12, "bold"), background="white")
        self.search_label.pack(side=LEFT, padx=(0, 10))

        # User entry for search
        self.user_entry = Entry(self.search_frame, font=("Arial", 12), bg="white", validate="key")
        self.user_entry.focus_set()
        self.user_entry.pack(fill="x", expand=True)

        # Bind the perform_search method to the KeyRelease event
        self.user_entry.bind("<KeyRelease>", lambda event: self.perform_search(num))

        # Display all customers initially
        self.display_customers(num)

    def on_frame_configure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def menu_interface(self):
        CustomerInterface.CustomerInterface(self.window)

    def button_click(self, customer_name, customer_email, customer_address, image, num):
        if num == 2 or num == 0:
            UpdateCustomerModuleInterface.UpdateCustomerInterface(self.window, customer_name, customer_email,
                                                                  customer_address, image)
        if num == 3:
            user_response = messagebox.askyesno("Confirm Remove", f"Do you want to remove {customer_name}?")
            if user_response:
                customer.delete_one({"CustomerName": customer_name, "CustomerEmail": customer_email})
                self.display_customers(num)

    def perform_search(self, num):
        search_term = self.user_entry.get().lower()
        if search_term:
            # Filter customers based on the search term
            filtered_customers = [customer_data for customer_data in customer.find() if
                                  search_term in customer_data["CustomerName"].lower()]
        else:
            # If search term is empty, display all customers
            filtered_customers = customer.find()

        # Update the displayed customers
        self.update_display(filtered_customers, num)

    def update_display(self, customers_data, num):
        # Clear existing frames
        for widget in self.outer_frame.winfo_children():
            widget.destroy()

        # Display the filtered customers
        for i, customer_data in enumerate(customers_data):
            frame = Frame(self.outer_frame, bg="#487307", highlightbackground="#487307", highlightthickness=0)
            frame.grid(row=0, column=i, padx=5, pady=5)

            customer_name = customer_data["CustomerName"]
            customer_email = customer_data["CustomerEmail"]
            customer_address = customer_data.get("CustomerAddress", DEFAULT_ADDRESS)  # Use default if not found
            image_data = customer_data.get("CustomerImage", DEFAULT_IMAGE)  # Use default if not found
            decoded_image_data = base64.b64decode(image_data)

            label = Label(frame, text=f"{customer_name}", font=("Arial", 18, "bold"), background="#487307",
                          foreground="white")
            label.pack(side=TOP, pady=10)

            # Use BytesIO to open the image from bytes
            image = Image.open(BytesIO(decoded_image_data))
            image = image.resize((180, 180))
            image = ImageTk.PhotoImage(image)
            image_label = Label(frame, image=image)
            image_label.image = image
            image_label.pack()

            description_label = Label(frame, text=f"Email: {customer_email}\nAddress: {customer_address}",
                                      font=("Arial", 12), background="#487307", foreground="white", anchor='w')
            description_label.pack()

            button_text = "View" if num != 2 else "Update" if num == 2 else "Remove"
            button = Button(frame, text=button_text, font=("Arial", 12),
                            command=lambda name=customer_name, email=customer_email, address=customer_address,
                                           path=image_data, n=num: self.button_click(name, email, address, path, n),
                            width=20, background="#968802", foreground="white")
            button.pack(side=TOP, padx=10, pady=5)

            if num == 2:
                button.config(text="Update")
            elif num == 3:
                button.config(text="Remove")

    def display_customers(self, num):
        # Display all customers initially
        customers_data = customer.find()
        self.update_display(customers_data, num)


# If you have other parts of your code, make sure to include them here.

# For testing purposes, you can create a Tkinter window and run the interface:
if __name__ == "__main__":
    root = Tk()
    app = ViewCustomerModulesInterface(root, 0)  # Change the second argument based on the module you want to test
    root.mainloop()
