from io import BytesIO
from tkinter import *
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk
from bson import Binary

import InventoryManagementInterface
import ViewInventoryModulesInterface
from Database import product


class UpdateInventoryModuleInterface:
    def __init__(self, window, machinery_name, company, image, count, rate):
        self.image_path = None
        self.window = window
        self.window.title(machinery_name)
        self.window.geometry(f"{int(window.winfo_screenwidth() / 1.5)}x{int(window.winfo_screenheight() / 1.5)}")
        self.window.iconbitmap("icon.ico")

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
        self.add_outer_frame.place(x=self.window.winfo_screenwidth() / 2, y=self.window.winfo_screenheight() / 2,
                                   anchor="center")
        self.add_outer_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Add product frame
        self.add_product_frame = Frame(self.add_outer_frame, bg="#968802", highlightbackground="#968802",
                                       highlightthickness=0)
        self.add_product_frame.pack()
        self.add_product_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Product Image
        self.product_image = Image.open(BytesIO(image))
        self.product_image = self.product_image.resize((200, 200))
        self.product_image = ImageTk.PhotoImage(self.product_image)

        self.product_image_label = Label(self.add_product_frame, image=self.product_image, bg="white")
        self.product_image_label.grid(row=0, column=0, rowspan=5, padx=(0, 20))

        self.upload_image_button = Button(self.add_product_frame, text="Change Image", font=("Arial", 12), bg="#487307",
                                          fg="white", width=15, command=self.upload_image)
        self.upload_image_button.grid(row=5, column=0, padx=(0, 20))

        self.title_label = Label(self.add_product_frame, text=machinery_name, font=("Arial", 30, "bold"), bg="#968802",
                                 fg="white")
        self.title_label.grid(row=0, column=1, columnspan=2, pady=(5, 10), sticky="w")

        self.product_name_label = Label(self.add_product_frame, text="Product Name:", font=("Arial", 12), bg="#968802",
                                        fg="white")
        self.product_name_label.grid(row=1, column=1, sticky="e", pady=(5, 5))

        self.product_name_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_name_entry.grid(row=1, column=2, pady=(5, 5))
        self.product_name_entry.focus_set()
        self.product_name_entry.insert(0, machinery_name)

        self.product_company_label = Label(self.add_product_frame, text="Product Company:", font=("Arial", 12),
                                           bg="#968802", fg="white")
        self.product_company_label.grid(row=2, column=1, sticky="e", pady=(5, 5))

        self.product_company_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_company_entry.grid(row=2, column=2, pady=(5, 5))
        self.product_company_entry.insert(0, company)

        self.product_count_label = Label(self.add_product_frame, text="Product Count:", font=("Arial", 12),
                                         bg="#968802", fg="white")
        self.product_count_label.grid(row=3, column=1, sticky="e", pady=(5, 5))

        self.product_count_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_count_entry.grid(row=3, column=2, pady=(5, 5))
        self.product_count_entry.insert(0, count)

        self.product_rate_label = Label(self.add_product_frame, text="Product Rate (K):", font=("Arial", 12),
                                        bg="#968802", fg="white")
        self.product_rate_label.grid(row=4, column=1, sticky="e", pady=(5, 5))

        self.product_rate_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_rate_entry.grid(row=4, column=2, pady=(5, 5))
        self.product_rate_entry.insert(0, rate)

        # Add Product Button
        self.add_button = Button(self.add_product_frame, text=f"Update {machinery_name}", font=("Arial", 12, "bold"),
                                 bg="#487307", fg="white", width=25, height=2, command=self.add_product)
        self.add_button.grid(row=5, column=1, columnspan=2, pady=(0, 20))

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image",
                                               filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        self.image_path = file_path

    def menu_interface(self):
        InventoryManagementInterface.InventoryManagementInterface(self.window)

    def add_product(self):
        product_name = self.product_name_entry.get()
        product_company_name = self.product_company_entry.get()
        product_count = self.product_count_entry.get()
        product_rate = self.product_rate_entry.get()
        image_path = self.image_path
        try:
            product_count = int(product_count)
            product_rate = float(product_rate)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input for {str(e)}. Please enter a valid number.")
            return

        self.window.attributes('-topmost', False)

        if image_path:
            with open(image_path, "rb") as image_file:
                binary_data = Binary(image_file.read())
            product_data = {"product_name": product_name, "product_company": product_company_name,
                            "product_count": product_count, "product_rate": product_rate, "product_image": binary_data}
        else:
            product_data = {"product_name": product_name, "product_company": product_company_name,
                            "product_count": product_count, "product_rate": product_rate}

        # Create a top-level window for confirmation
        confirmation_window = Toplevel(self.window)
        confirmation_window.title("Confirmation")
        x = (confirmation_window.winfo_screenwidth() - 500) // 2
        y = (confirmation_window.winfo_screenheight() - 500) // 2

        confirmation_window.geometry(f"{500}x{500}+{x}+{y}")

        # Display the data in the confirmation window
        data_label = Label(confirmation_window, text=f"Product Name: {product_name}\n"
                                                     f"Product Company :{product_company_name}\n"
                                                     f"Product Count: {product_count}\n"
                                                     f"Product Rate: {product_rate}\n", font=("Arial", 12),
                           bg="#968802", fg="white")
        data_label.pack()

        if image_path:
            image = Image.open(image_path)
            image = image.resize((300, 300))
            image = ImageTk.PhotoImage(image)

            image_label = Label(confirmation_window, image=image)
            image_label.image = image
            image_label.pack()

        # Add Yes and No buttons
        yes_button = Button(confirmation_window, text="Yes", font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=10, command=lambda: self.save_to_database(product_data, confirmation_window))
        yes_button.pack(side="left", padx=20)

        no_button = Button(confirmation_window, text="No", font=("Arial", 12, "bold"), bg="#487307", fg="white",
                           width=10, command=confirmation_window.destroy)
        no_button.pack(side="right", padx=20)

    def save_to_database(self, product_data, confirmation_window):
        self.window.attributes('-topmost', True)
        self.window.state('zoomed')
        result = product.update_one(
            {"product_name": product_data["product_name"], "product_company": product_data["product_company"]},
            {"$set": product_data})

        if result.modified_count > 0:
            messagebox.showinfo("Success", "Data updated in the database.")

            self.product_name_entry.delete(0, END)
            self.product_company_entry.delete(0, END)
            self.product_count_entry.delete(0, END)
            self.product_rate_entry.delete(0, END)

        # Close the confirmation window
        confirmation_window.destroy()
        ViewInventoryModulesInterface.ViewInventoryModulesInterface(self.window, 0)
