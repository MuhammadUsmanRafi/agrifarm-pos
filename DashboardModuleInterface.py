from tkinter import *

from PIL import Image, ImageTk

import DashboardInterface
import MenuInterface


class DashboardModuleInterface:
    def __init__(self, window, num):
        self.window = window
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        background_image_path = "assets/dashboard_module_1.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.dashboard_menu_interface,
                                          font=("Arial", 12), bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)  # Adjust the position

        self.dashboard_frame = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.dashboard_frame.place(x=10, y=self.window.winfo_screenheight() / 6)
        self.dashboard_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.upper_button = Frame(self.dashboard_frame, bg="#968802", highlightbackground="#968802",
                                  highlightthickness=0)
        self.upper_button.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.button_labels = ["View Companies", "Add ", "Delete Company", "Place Order"]
        self.module_label = Label(self.window, text=self.button_labels[num], font=("Arial", 30, "bold"),
                                  background="#968802", foreground="white")
        self.module_label.place(x=self.window.winfo_screenwidth() / 4 * 2.3, y=20)
        self.window.title(self.button_labels[num])

        self.modules_button = []
        for label in self.button_labels:
            button = Button(self.upper_button, text=label, font=("Arial", 12, "bold"), bg="#487307", fg="white",
                            width=25, height=3)
            button.pack(padx=10, pady=10)
            self.modules_button.append(button)

        self.upper_button.pack()

        self.modules_button[num].config(bg="#193700")

        for i, button in enumerate(self.modules_button):
            self.modules_button[i].config(command=lambda: self.modules_action(i))
            button.bind("<Button-1>", self.toggle_button_color)

        self.modules_button[0].config(command=lambda: self.modules_action(0))
        self.modules_button[1].config(command=lambda: self.modules_action(1))
        self.modules_button[2].config(command=lambda: self.modules_action(2))
        self.modules_button[3].config(command=lambda: self.modules_action(3))

    def toggle_button_color(self, event):
        for button in self.modules_button:
            button.config(bg="#487307")
        button = event.widget
        button.config(bg="#193700")

    def modules_action(self, num):
        self.module_label.config(text=self.button_labels[num])
        self.window.title(self.button_labels[num])

    def dashboard_menu_interface(self):
        DashboardInterface.DashboardInterface(self.window)


if __name__ == "__main__":
    root = Tk()
    login_interface = MenuInterface.MenuInterface(root)
    root.mainloop()
