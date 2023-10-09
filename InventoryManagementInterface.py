from tkinter import *

from PIL import Image, ImageTk

import AddInventoryModuleInterface
import ViewInventoryModulesInterface
import MenuInterface


class InventoryManagementInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Inventory")
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        # Set background image for the login window
        background_image_path = "assets/inventory.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface,
                                          font=("Arial", 12), bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        self.inventory_frame = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.inventory_frame.place(x=self.window.winfo_screenwidth() / 2, y=self.window.winfo_screenheight() / 2 + 125,
                                   anchor="center")  # Adjust the vertical position by subtracting 30 pixels
        self.inventory_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.upper_button = Frame(self.inventory_frame, bg="#968802", highlightbackground="#968802",
                                  highlightthickness=0)
        self.upper_button.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.modules = []
        # Create a list of button labels
        button_labels = ["View Inventory", "Add Product"]

        # Create and pack buttons with adjusted width and height
        for label in button_labels:
            button = Button(self.upper_button, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=25,
                            height=3)
            button.pack(side=LEFT, padx=10)
            self.modules.append(button)

        self.upper_button.pack()

        self.lower_button = Frame(self.inventory_frame, bg="#968802", highlightbackground="#968802",
                                  highlightthickness=0)
        self.lower_button.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Create a list of button labels
        button_labels = ["Update Product", "Remove Product"]

        # Create and pack buttons with adjusted width and height
        for label in button_labels:
            button = Button(self.lower_button, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=25,
                            height=3)
            button.pack(side=LEFT, padx=10)
            self.modules.append(button)

        self.lower_button.pack()

        self.modules[0].config(command=lambda: self.modules_button(0))
        self.modules[1].config(command=lambda: self.modules_button(1))
        self.modules[2].config(command=lambda: self.modules_button(2))
        self.modules[3].config(command=lambda: self.modules_button(3))

    def modules_button(self, num):
        if num == 1:
            AddInventoryModuleInterface.AddInventoryModulesInterface(self.window, num)
        else:
            ViewInventoryModulesInterface.ViewInventoryModulesInterface(self.window, num)

    def menu_interface(self):
        MenuInterface.MenuInterface(self.window)


if __name__ == "__main__":
    root = Tk()
    login_interface = MenuInterface.MenuInterface(root)
    root.mainloop()
