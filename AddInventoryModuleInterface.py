from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk

import InventoryManagementInterface


class AddInventoryModulesInterface:
    def __init__(self, window, num):
        self.labels = ["View Inventory", "Add Product", "Update Product", "Remove Product"]
        self.window = window
        self.window.title(self.labels[num])
        self.window.geometry(
            f"{int(window.winfo_screenwidth() / 1.5)}x{int(window.winfo_screenheight() / 1.5)}")
        self.window.iconbitmap("icon.ico")

        background_image_path = "assets/login_bg2.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface,
                                          font=("Arial", 12), bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        self.add_outer_frame = Frame(self.window, bg="#968802", highlightbackground="black",
                                     highlightthickness=2)
        self.add_outer_frame.place(x=self.window.winfo_screenwidth() / 2, y=self.window.winfo_screenheight() / 2,
                                   anchor="center")
        self.add_outer_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.add_product_frame = Frame(self.add_outer_frame, bg="#968802", highlightbackground="black",
                                       highlightthickness=2)  # Added black border
        self.add_product_frame.pack()

        self.add_product_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.title_label = Label(self.add_product_frame, text="Add Product", font=("Arial", 16, "bold"),
                                 bg="#968802", fg="white")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(5, 10))

        self.product_name_label = Label(self.add_product_frame, text="Product Name:", font=("Arial", 12),
                                        bg="#968802", fg="white")
        self.product_name_label.grid(row=1, column=0, sticky="e", pady=(5, 5))

        self.product_name_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_name_entry.grid(row=1, column=1, pady=(5, 5))
        self.product_name_entry.focus_set()

        self.product_count_label = Label(self.add_product_frame, text="Product Count:", font=("Arial", 12),
                                         bg="#968802", fg="white")
        self.product_count_label.grid(row=2, column=0, sticky="e", pady=(5, 5))

        self.product_count_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_count_entry.grid(row=2, column=1, pady=(5, 5))

        self.product_rate_label = Label(self.add_product_frame, text="Product Rate (K):", font=("Arial", 12),
                                        bg="#968802", fg="white")
        self.product_rate_label.grid(row=3, column=0, sticky="e", pady=(5, 5))

        self.product_rate_entry = Entry(self.add_product_frame, font=("Arial", 12))
        self.product_rate_entry.grid(row=3, column=1, pady=(5, 5))

        self.upload_image_button = Button(self.add_product_frame, text="Upload Image", font=("Arial", 12),
                                          bg="#487307", fg="white", width=15, command=self.upload_image)
        self.upload_image_button.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        self.image_path_label = Label(self.add_product_frame, text="", font=("Arial", 10), bg="#968802", fg="white")
        self.image_path_label.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        self.add_button = Button(self.add_product_frame, text="Add Product", font=("Arial", 12, "bold"), bg="#487307",
                                 fg="white", width=25, height=2, command=self.add_product)
        self.add_button.grid(row=6, column=0, columnspan=2, pady=(0, 20))

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image",
                                               filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        self.image_path_label.config(text=file_path)

    def add_product(self):
        product_name = self.product_name_entry.get()
        product_count = self.product_count_entry.get()
        product_rate = self.product_rate_entry.get()
        image_path = self.image_path_label.cget("text")

    def menu_interface(self):
        InventoryManagementInterface.InventoryManagementInterface(self.window)


if __name__ == "__main__":
    root = Tk()
    add_product_interface = AddInventoryModulesInterface(root, 1)
    root.mainloop()
