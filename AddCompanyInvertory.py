import base64
from tkinter import *
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

import DashboardInterface
import ViewCompaniesInterface
from Database import company


class AddCompanyInventory:
    def __init__(self, window, num):
        self.labels = ["View Companies", "Add Company", "Delete Company", "Place Order"]
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

        self.add_product_frame = Frame(self.add_outer_frame, bg="#968802", highlightbackground="black",
                                       highlightthickness=2)  # Added black border
        self.add_product_frame.pack()

        self.add_product_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.title_label = Label(self.add_product_frame, text="Add Company", font=("Arial", 16, "bold"), bg="#968802",
                                 fg="white")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(5, 10))

        self.product_name_label = Label(self.add_product_frame, text="Company Name:", font=("Arial", 12), bg="#968802",
                                        fg="white")
        self.product_name_label.grid(row=1, column=0, sticky="e", pady=(5, 5))

        self.product_name_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_name_entry.grid(row=1, column=1, pady=(5, 5))
        self.product_name_entry.focus_set()

        self.product_company_name_label = Label(self.add_product_frame, text="Company Email:", font=("Arial", 12),
                                                bg="#968802", fg="white")
        self.product_company_name_label.grid(row=2, column=0, sticky="e", pady=(5, 5))

        self.product_company_name_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_company_name_entry.grid(row=2, column=1, pady=(5, 5))

        self.product_brand_name_label = Label(self.add_product_frame, text="Company Phone:", font=("Arial", 12),
                                              bg="#968802", fg="white")
        self.product_brand_name_label.grid(row=3, column=0, sticky="e", pady=(5, 5))

        self.product_brand_name_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_brand_name_entry.grid(row=3, column=1, pady=(5, 5))

        self.product_category_name_label = Label(self.add_product_frame, text="Address of Company:", font=("Arial", 12),
                                                 bg="#968802", fg="white")
        self.product_category_name_label.grid(row=4, column=0, sticky="e", pady=(5, 5))

        self.product_category_name_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_category_name_entry.grid(row=4, column=1, pady=(5, 5))

        self.product_rate_label = Label(self.add_product_frame, text="Company Category:", font=("Arial", 12),
                                        bg="#968802", fg="white")
        self.product_rate_label.grid(row=5, column=0, sticky="e", pady=(5, 5))

        self.product_rate_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_rate_entry.grid(row=5, column=1, pady=(5, 5))

        self.upload_image_button = Button(self.add_product_frame, text="Upload Image", font=("Arial", 12), bg="#487307",
                                          fg="white", width=15, command=self.upload_image)
        self.upload_image_button.grid(row=6, column=0, columnspan=2, pady=(0, 10))

        self.image_path_label = Label(self.add_product_frame, text="", font=("Arial", 10), bg="#968802", fg="white")
        self.image_path_label.grid(row=7, column=0, columnspan=2, pady=(0, 10))

        self.add_button = Button(self.add_product_frame, text="Add Company", font=("Arial", 12, "bold"), bg="#487307",
                                 fg="white", width=25, height=2, command=self.add_product)
        self.add_button.grid(row=8, column=0, columnspan=2, pady=(0, 20))

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image",
                                               filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        self.image_path_label.config(text=file_path)

    def add_product(self):
        CName = self.product_name_entry.get()
        cEmail = self.product_company_name_entry.get()
        cPhone = self.product_brand_name_entry.get()
        cAddress = self.product_category_name_entry.get()
        cCategory = self.product_rate_entry.get()
        cImage = self.image_path_label.cget("text")

        self.window.attributes('-topmost', False)
        # self.window.state('iconic')

        with open(cImage, "rb") as image_file:
            binary_data = image_file.read()
            binary_data = base64.b64encode(binary_data).decode('utf-8')

        product_data = {"CName": CName, "cEmail": cEmail, "cPhone": cPhone, "cAddress": cAddress,
                        "cCategory": cCategory, "cImage": binary_data}

        # Create a top-level window for confirmation
        confirmation_window = Toplevel(self.window)
        confirmation_window.title("Confirmation")
        x = (confirmation_window.winfo_screenwidth() - 500) // 2
        y = (confirmation_window.winfo_screenheight() - 500) // 2

        confirmation_window.geometry(f"{500}x{500}+{x}+{y}")

        # Display the data in the confirmation window
        data_label = Label(confirmation_window, text=f"Company Name: {CName}\n"
                                                     f"Company Email:{cEmail}\n"
                                                     f"Company Phone: {cPhone}\n"
                                                     f"Company Address: {cAddress}\n"
                                                     f"Company Category:{cCategory}\n", font=("Arial", 12),
                           bg="#968802", fg="white")
        data_label.pack()

        image = Image.open(cImage)
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
        result = company.insert_one(product_data)

        if result.inserted_id:
            messagebox.showinfo("Success", "Data saved into the database.")

            self.product_name_entry.delete(0, END)
            self.product_company_name_entry.delete(0, END)
            self.image_path_label.config(text="")

        # Close the confirmation window
        confirmation_window.destroy()
        ViewCompaniesInterface.ViewCompaniesInterface(self.window, 0)

    def menu_interface(self):
        DashboardInterface.DashboardInterface(self.window)


if __name__ == "__main__":
    root = Tk()
    add_product_interface = AddCompanyInventory(root, 1)
    root.mainloop()
