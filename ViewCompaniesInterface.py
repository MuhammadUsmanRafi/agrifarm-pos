import base64
from io import BytesIO
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

import DashboardInterface
import UpdateCompanyInterface
from Database import company


class ViewCompaniesInterface:
    def __init__(self, window, num):
        self.labels = ["View Companies", "Add Company", "Delete Company", "Place Order"]
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

        # Search frame
        self.search_frame = Frame(self.window, bg="white", highlightbackground="#968802", highlightthickness=0)
        self.search_frame.place(x=self.window.winfo_screenwidth() / 2 - 100, y=self.window.winfo_screenheight() / 8)

        # Search label
        self.search_label = Label(self.search_frame, text="Search: ", font=("Arial", 12, "bold"), background="white")
        self.search_label.pack(side=LEFT, padx=(0, 10))

        # User entry for search
        self.user_entry = Entry(self.search_frame, font=("Arial", 12), bg="white", validate="key")
        self.user_entry.focus_set()
        self.user_entry.pack(fill="x", expand=True)

        # Bind the perform_search method to the KeyRelease event
        self.user_entry.bind("<KeyRelease>", lambda event: self.perform_search(num))

        # Display all companies initially
        self.display_companies(num)

    def on_frame_configure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def menu_interface(self):
        DashboardInterface.DashboardInterface(self.window)

    def button_click(self, cName, cEmail, cPhone, cAddress, cCategory, cImage, num):
        if num == 0:
            UpdateCompanyInterface.UpdateCompanyInterface(self.window, cName, cEmail, cPhone, cAddress, cCategory,
                                                          cImage)
        if num == 2:
            user_response = messagebox.askyesno("Confirm Remove", f"Do you want to remove {cName}?")
            if user_response:
                company.delete_one({"CName": cName, "cEmail": cEmail, "cCategory": cCategory})
                self.display_companies(num)

    def perform_search(self, num):
        search_term = self.user_entry.get().lower()
        if search_term:
            # Filter companies based on the search term
            filtered_companies = [company_data for company_data in company.find() if
                                  search_term in company_data["CName"].lower()]
        else:
            # If search term is empty, display all companies
            filtered_companies = company.find()

        # Update the displayed companies
        self.update_display(filtered_companies, num)

    def update_display(self, companies_data, num):
        # Clear existing frames
        for widget in self.outer_frame.winfo_children():
            widget.destroy()

        # Display the filtered companies
        for i, company_data in enumerate(companies_data):
            frame = Frame(self.outer_frame, bg="#487307", highlightbackground="#487307", highlightthickness=0)
            frame.grid(row=0, column=i, padx=5, pady=5)

            cName = company_data["CName"]
            cEmail = company_data["cEmail"]
            cPhone = company_data["cPhone"]
            cAddress = company_data["cAddress"]
            cCategory = company_data["cCategory"]
            cImage = company_data["cImage"]

            label = Label(frame, text=f"{cName}", font=("Arial", 18, "bold"), background="#487307", foreground="white")
            label.pack(side=TOP, pady=10)

            # Use BytesIO to open the image from bytes
            image = Image.open(BytesIO(base64.b64decode(cImage)))
            image = image.resize((180, 180))
            image = ImageTk.PhotoImage(image)
            image_label = Label(frame, image=image)
            image_label.image = image
            image_label.pack()

            description_label = Label(frame, text=f"Email: {cEmail}\nPhone: {cPhone}\nCategory: {cCategory}",
                                      font=("Arial", 12), background="#487307", foreground="white", anchor='w')
            description_label.pack()

            button_text = "View" if num != 2 else "Update" if num == 2 else "Remove"
            button = Button(frame, text=button_text, font=("Arial", 12),
                            command=lambda name=cName, email=cEmail, phone=cPhone, address=cAddress, category=cCategory,
                                           image=cImage, n=num: self.button_click(name, email, phone, address, category,
                                                                                  image, n), width=20,
                            background="#968802", foreground="white")
            button.pack(side=TOP, padx=10, pady=5)

            if num == 2:
                button.config(text="Remove")

    def display_companies(self, num):
        # Display all companies initially
        companies_data = company.find()
        self.update_display(companies_data, num)


if __name__ == "__main__":
    root = Tk()
    view_companies_interface = ViewCompaniesInterface(root, 0)
    root.mainloop()
