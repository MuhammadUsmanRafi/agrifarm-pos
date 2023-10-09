from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

import InventoryManagementInterface
import UpdateInventoryModuleInterface


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

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface,
                                          font=("Arial", 12), bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        self.title_label = Label(self.window, text=f"{self.labels[num]}", font=("Arial", 40, "bold"),
                                 background="#968802", foreground="white")
        self.title_label.place(x=self.window.winfo_screenwidth() / 2 - 150, y=20)

        self.frames = []

        agricultural_machinery = [
            {"name": "Tractor", "image_path": "assets/products/Tractor.png", "count": 10, "rate": 1000},
            {"name": "Plow", "image_path": "assets/products/Plow.png", "count": 15, "rate": 500},
            {"name": "Tiller", "image_path": "assets/products/Tiller.png", "count": 5, "rate": 1200},
            {"name": "Seeder", "image_path": "assets/products/Seeder.png", "count": 20, "rate": 800},
            {"name": "Harvester", "image_path": "assets/products/Harvester.png", "count": 8, "rate": 2500}
        ]

        for i in range(5):
            frame = Frame(self.window, bg="#487307", highlightbackground="#487307", highlightthickness=0)
            frame.place(x=i * (self.window.winfo_screenwidth() / 5) + 22, y=self.window.winfo_screenheight() / 5 + 40)

            machinery_name = agricultural_machinery[i]["name"]
            image_path = agricultural_machinery[i]["image_path"]
            count = agricultural_machinery[i]["count"]
            rate = agricultural_machinery[i]["rate"]

            label = Label(frame, text=f"{machinery_name}", font=("Arial", 18, "bold"), background="#487307",
                          foreground="white")
            label.pack(side=TOP, pady=10)

            machinery_image = Image.open(image_path)
            machinery_image = self.crop_center(machinery_image, 180, 180)
            machinery_image = ImageTk.PhotoImage(machinery_image)

            image_label = Label(frame, image=machinery_image)
            image_label.image = machinery_image
            image_label.pack()

            description_label = Label(frame,
                                      text=f"Count: {count}\nRate: {rate}K",
                                      font=("Arial", 15), background="#487307", foreground="white")
            description_label.pack()

            # Create a lambda function to pass additional arguments to button_click
            button = Button(frame, text="View", font=("Arial", 12),
                            command=lambda name=machinery_name, path=image_path, c=count, r=rate:
                            self.button_click(name, path, c, r, num),  # Pass num as an argument
                            width=20, background="#968802", foreground="white")
            button.pack(side=TOP, padx=10, pady=5)

            if num == 2:
                button.config(text="Update")
            elif num == 3:
                button.config(text="Remove")

            self.frames.append(frame)

        self.search_frame = Frame(self.window, bg="white", highlightbackground="#968802", highlightthickness=0)
        self.search_frame.place(x=self.window.winfo_screenwidth() / 2 - 100, y=self.window.winfo_screenheight() / 8)

        self.search_label = Label(self.search_frame, text="Search: ", font=("Arial", 12, "bold"), background="white")
        self.search_label.pack(side=LEFT, padx=(0, 10))

        self.user_entry = Entry(self.search_frame, font=("Arial", 12), bg="white")
        self.user_entry.focus_set()
        self.user_entry.pack(fill="x", expand=True)

    def menu_interface(self):
        InventoryManagementInterface.InventoryManagementInterface(self.window)

    def button_click(self, machinery_name, image_path, count, rate, num):
        if num == 2 or num == 0:
            UpdateInventoryModuleInterface.UpdateInventoryModuleInterface(self.window, machinery_name, image_path,
                                                                          count, rate)
        if num == 3:
            messagebox.askyesno("Confirm Remove", f"Do you want to remove {machinery_name}?")

    @staticmethod
    def crop_center(pil_image, width, height):
        img_width, img_height = pil_image.size
        left = (img_width - width) / 2
        top = (img_height - height) / 2
        right = (img_width + width) / 2
        bottom = (img_height + height) / 2
        return pil_image.crop((left, top, right, bottom))


if __name__ == "__main__":
    root = Tk()
    view_inventory_interface = ViewInventoryModulesInterface(root, 0)
    root.mainloop()
