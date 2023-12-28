from tkinter import *

from PIL import Image, ImageTk

import CustomerInterface
import DashboardInterface
import HelpSupportInterface
import InventoryManagementInterface
import LogoutInterface
import ReportingAnalyticsInterface
import SalesInterface
import SettingInterface
from main import MainInterface


class MenuInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Menu")
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        # Set background image for the login window
        background_image_path = "assets/Menu_bg_img.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back to Home", command=self.show_main_interface,
                                          font=("Arial", 12), bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)  # Adjust the position

        self.menu_frame = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.menu_frame.place(x=self.window.winfo_screenwidth() / 2, y=self.window.winfo_screenheight() / 2 - 100,
                              anchor="center")  # Adjust the vertical position by subtracting 30 pixels
        self.menu_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.upper_button = Frame(self.menu_frame, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.upper_button.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)
        self.buttons = []
        # Create a list of button labels
        button_labels = ["Companies", "Inventory Management", "Customer Management", "Sales"]

        # Create and pack buttons with adjusted width and height
        for label in button_labels:
            button = Button(self.upper_button, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=25, height=3)
            self.buttons.append(button)
            button.pack(side=LEFT, padx=10)  # Adjust width, height, and padding

        self.upper_button.pack()

        self.lower_button = Frame(self.menu_frame, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.lower_button.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Create a list of button labels
        button_labels = ["Reporting & Analysis", "Help & Support", "Setting", "Logout"]

        # Create and pack buttons with adjusted width and height
        for label in button_labels:
            button = Button(self.lower_button, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=25, height=3)
            self.buttons.append(button)
            button.pack(side=LEFT, padx=10)  # Adjust width, height, and padding

        # Place the upper_button Frame inside the menu_frame
        self.lower_button.pack()

        self.buttons[0].config(command=lambda: self.companies())
        self.buttons[1].config(command=lambda: self.inventory())
        self.buttons[2].config(command=lambda: self.customer())
        self.buttons[3].config(command=lambda: self.sales())
        self.buttons[4].config(command=lambda: self.analytics())
        self.buttons[5].config(command=lambda: self.support())
        self.buttons[6].config(command=lambda: self.setting())
        self.buttons[7].config(command=lambda: self.logout())

    def companies(self):
        DashboardInterface.DashboardInterface(self.window)

    def inventory(self):
        InventoryManagementInterface.InventoryManagementInterface(self.window)

    def customer(self):
        CustomerInterface.CustomerInterface(self.window)

    def sales(self):
        SalesInterface.SalesInterface(self.window)

    def analytics(self):
        ReportingAnalyticsInterface.ReportingAnalyticsInterface(self.window)

    def support(self):
        HelpSupportInterface.HelpSupportInterface(self.window)

    def setting(self):
        SettingInterface.SettingInterface(self.window)

    def logout(self):
        LogoutInterface.LogoutInterface(self.window)

    def show_main_interface(self):
        MainInterface(self.window)


if __name__ == "__main__":
    root = Tk()
    login_interface = MenuInterface(root)
    root.mainloop()
