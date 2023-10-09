from tkinter import *

from PIL import Image, ImageTk

import MenuInterface


class SettingInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Help & Support")
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        background_image_path = "assets/setting.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface, font=("Arial", 12),
                                          bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        self.frame = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.frame.place(x=self.window.winfo_screenwidth() / 4 * 3, y=self.window.winfo_screenheight() / 3 * 1.9, anchor="center")

        self.frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        self.setting_frame = Frame(self.frame, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.setting_frame.pack()
        self.setting_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        title_label = Label(self.setting_frame, text='Change Password', font=("Arial", 20, "bold"), bg="#968802",
                            fg="white")
        title_label.pack(pady=10)

        self.user_frame = Frame(self.setting_frame, bg="#968802")
        self.user_frame.pack(pady=10, fill="x")

        self.user_label = Label(self.user_frame, text="  Old Password:", font=("Arial", 12), bg="#968802", fg="white")
        self.user_label.pack(side=LEFT, padx=(0, 10))

        self.old_pass = Entry(self.user_frame, font=("Arial", 12), bg="white")
        self.old_pass.focus_set()
        self.old_pass.pack(fill="x", expand=True)

        pass_frame = Frame(self.setting_frame, bg="#968802")
        pass_frame.pack(pady=10, fill="x")

        pass_label = Label(pass_frame, text="New Password:", font=("Arial", 12), bg="#968802", fg="white")
        pass_label.pack(side=LEFT, padx=(0, 10))

        password_var = StringVar()
        self.new_pass = Entry(pass_frame, font=("Arial", 12), show="*", bg="white", textvariable=password_var)
        self.new_pass.pack(fill="x", expand=True)
        login_button = Button(self.setting_frame, text='Confirm', command=self.change_password, font=("Arial", 12),
                              bg="#487307", fg="white", width=20)
        login_button.pack(pady=10)

    def change_password(self):
        pass

    def menu_interface(self):
        MenuInterface.MenuInterface(self.window)


if __name__ == "__main__":
    root = Tk()
    SettingInterface(root)
    root.mainloop()
