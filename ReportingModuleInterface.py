from tkinter import *

from PIL import Image, ImageTk

import MenuInterface
import ReportingAnalyticsInterface

class ReportingModuleInterface:
    def __init__(self, window, num):
        self.window = window
        self.window.title("Reporting & Analytics")
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        background_image_path = "assets/analytics_modules_2.png"
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
        self.analytics_frame.place(x=8, y=50)
        self.analytics_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)
        self.modules_button = []
        # Create a list of button labels
        self.button_labels = ["Sales Reports", "Inventory reports", "Financial Reports"]

        # Create and pack buttons with adjusted width and height
        for label in self.button_labels:
            button = Button(self.analytics_frame, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=25, height=3)
            self.modules_button.append(button)
            button.pack(side=LEFT, padx=8)

        self.modules_button[num].config(bg="#193700")

        for i, button in enumerate(self.modules_button):
            self.modules_button[i].config(command=lambda: self.modules_action(i))
            button.bind("<Button-1>", self.toggle_button_color)

        self.modules_button[0].config(command=lambda: self.modules_action(0))
        self.modules_button[1].config(command=lambda: self.modules_action(1))
        self.modules_button[2].config(command=lambda: self.modules_action(2))

    def toggle_button_color(self, event):
        for button in self.modules_button:
            button.config(bg="#487307")
        button = event.widget
        button.config(bg="#193700")

    def modules_action(self, num):
        self.window.title(self.button_labels[num])

    def menu_interface(self):
        ReportingAnalyticsInterface.ReportingAnalyticsInterface(self.window)


if __name__ == "__main__":
    root = Tk()
    login_interface = MenuInterface.MenuInterface(root)
    root.mainloop()
