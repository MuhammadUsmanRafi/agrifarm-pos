from tkinter import *

from PIL import Image, ImageTk

import MenuInterface
import ReportingModuleInterface


class ReportingAnalyticsInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Reporting & Analytics")
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        # Set background image for the login window
        background_image_path = "assets/analytics.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface, font=("Arial", 12),
                                          bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)  # Adjust the position

        self.analytics_frame = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.analytics_frame.place(x=self.window.winfo_screenwidth() / 2, y=self.window.winfo_screenheight() / 2 + 100,
                                   anchor="center")  # Adjust the vertical position by subtracting 30 pixels
        self.analytics_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.upper_button = Frame(self.analytics_frame, bg="#968802", highlightbackground="#968802",
                                  highlightthickness=0)
        self.upper_button.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)
        self.modules = []
        # Create a list of button labels
        button_labels = ["Sales Reports", "Inventory reports", "Financial Reports"]

        # Create and pack buttons with adjusted width and height
        for label in button_labels:
            button = Button(self.upper_button, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=25, height=3)
            self.modules.append(button)
            button.pack(side=LEFT, padx=10)  # Adjust width, height, and padding

        self.upper_button.pack()

        self.modules[0].config(command=lambda: self.modules_button(0))
        self.modules[1].config(command=lambda: self.modules_button(1))
        self.modules[2].config(command=lambda: self.modules_button(2))

    def modules_button(self, num):
        ReportingModuleInterface.ReportingModuleInterface(self.window, num)

    def menu_interface(self):
        MenuInterface.MenuInterface(self.window)


if __name__ == "__main__":
    root = Tk()
    login_interface = MenuInterface.MenuInterface(root)
    root.mainloop()
