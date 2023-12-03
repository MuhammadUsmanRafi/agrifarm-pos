from io import BytesIO
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

import InventoryManagementInterface
import UpdateInventoryModuleInterface
from Database import product


class ViewInventoryModulesInterface:
    def __init__(self, window, num):
        self.labels = ["View Inventory", "Add Product", "Update Product", "Remove Product"]
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

        products_data = product.find()

        for i, product_data in enumerate(products_data):
            frame = Frame(self.outer_frame, bg="#487307", highlightbackground="#487307", highlightthickness=0)
            frame.grid(row=0, column=i, padx=5, pady=5)

            product_name = product_data["product_name"]
            company = product_data["product_company"]
            image_data = product_data["product_image"]
            count = product_data["product_count"]
            rate = product_data["product_rate"]

            label = Label(frame, text=f"{product_name}", font=("Arial", 18, "bold"), background="#487307",
                          foreground="white")
            label.pack(side=TOP, pady=10)

            image = Image.open(BytesIO(image_data))
            image = image.resize((180, 180))
            image = ImageTk.PhotoImage(image)
            image_label = Label(frame, image=image)
            image_label.image = image
            image_label.pack()

            description_label = Label(frame, text=f"Company: {company}\nCount: {count}\nRate: {rate}K",
                                      font=("Arial", 12), background="#487307", foreground="white", anchor='w')
            description_label.pack()

            button_text = "View" if num != 2 else "Update" if num == 2 else "Remove"
            button = Button(frame, text=button_text, font=("Arial", 12),
                            command=lambda name=product_name, path=image, c=count, r=rate: self.button_click(name,
                                                                                                             company,
                                                                                                             path, c, r,
                                                                                                             num),
                            width=20, background="#968802", foreground="white")
            button.pack(side=TOP, padx=10, pady=5)

            if num == 2:
                button.config(text="Update")
            elif num == 3:
                button.config(text="Remove")

            # Search frame
            self.search_frame = Frame(self.window, bg="white", highlightbackground="#968802", highlightthickness=0)
            self.search_frame.place(x=self.window.winfo_screenwidth() / 2 - 100, y=self.window.winfo_screenheight() / 8)

            # Search label
            self.search_label = Label(self.search_frame, text="Search: ", font=("Arial", 12, "bold"),
                                      background="white")
            self.search_label.pack(side=LEFT, padx=(0, 10))

            # User entry for search
            self.user_entry = Entry(self.search_frame, font=("Arial", 12), bg="white")
            self.user_entry.focus_set()
            self.user_entry.pack(fill="x", expand=True)

    def on_frame_configure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def menu_interface(self):
        InventoryManagementInterface.InventoryManagementInterface(self.window)

    def button_click(self, product_name, company, image, count, rate, num):
        if num == 2 or num == 0:
            UpdateInventoryModuleInterface.UpdateInventoryModuleInterface(self.window, product_name, company, image,
                                                                          count, rate)
        if num == 3:
            user_response = messagebox.askyesno("Confirm Remove", f"Do you want to remove {product_name}?")
            if user_response:
                product.delete_one({"product_name": product_name, "product_company": company})
                ViewInventoryModulesInterface(self.window, 0)


if __name__ == "__main__":
    root = Tk()
    view_inventory_interface = ViewInventoryModulesInterface(root, 0)
    root.mainloop()
