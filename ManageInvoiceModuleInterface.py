from tkinter import *

from PIL import Image, ImageTk

import SalesInterface


class ManageInvoiceModuleInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Invoice")
        self.window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
        self.window.iconbitmap("icon.ico")

        background_image_path = "assets/ManageInvoice.png"
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.label = Label(self.window, image=self.background_image)
        self.label.place(x=0, y=0)

        self.back_to_home_button = Button(self.window, text="Back", command=self.menu_interface, font=("Arial", 12),
                                          bg="#487307", fg="white", width=15)
        self.back_to_home_button.place(x=10, y=10)

        self.outer_frame = Frame(self.window, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.outer_frame.place(x=self.window.winfo_screenwidth() / 3 , y=self.window.winfo_screenheight() / 3 * .5)
        self.outer_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        # Create a frame for Invoice Integration options
        self.frame = Frame(self.outer_frame, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.frame.pack()
        self.frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)

        Invoice_Label = Label(self.frame, text="Manage Invoice", font=("Arial", 20, "bold"), bg="#968802",
                              foreground="white")
        Invoice_Label.config(padx=10, pady=10)
        Invoice_Label.pack()

        self.Invoice_Integration_frame = Frame(self.frame, bg="#968802", highlightbackground="#968802",
                                               highlightthickness=0)
        self.Invoice_Integration_frame.configure(padx=20, pady=20, borderwidth=2, relief=SOLID)
        self.Invoice_Integration_frame.pack()

        integration_label = Label(self.Invoice_Integration_frame, text="Invoice Integration Options",
                                  font=("Arial", 14, "bold"), bg="#968802", foreground="white")
        integration_label.config(padx=10, pady=10)
        integration_label.grid(row=0, column=0)

        self.integration_option_var = IntVar()
        self.integration_option_var.set(1)

        options = [("WhatsApp", 1), ("Email", 2), ("Printed Form", 3)]

        for text, value in options:
            integration_option = Radiobutton(self.Invoice_Integration_frame, text=text,
                                             variable=self.integration_option_var, value=value,
                                             font=("Arial", 12, "bold"), bg="#968802", foreground="white")
            integration_option.grid(column=0, padx=10, pady=5, sticky="w")

        self.discount_frame = Frame(self.frame, bg="#968802", highlightbackground="#968802", highlightthickness=0)
        self.discount_frame.configure(padx=42, pady=20, borderwidth=2, relief=SOLID)
        self.discount_frame.pack()

        discount_label = Label(self.discount_frame, text="Set Discount", font=("Arial", 20, "bold"), bg="#968802",
                               foreground="white")
        discount_label.config(padx=10, pady=10)
        discount_label.grid(row=0, column=0)

        self.discount_var = DoubleVar()
        self.discount_var.set(0.0)

        discount_entry = Entry(self.discount_frame, textvariable=self.discount_var, font=("Arial", 12, "bold"),
                               width=25)
        discount_entry.grid(column=0, pady=5, sticky="w")

        submit = Button(self.discount_frame, text="Submit", command=lambda: self.submitted(),
                        font=("Arial", 12, "bold"), bg="#487307", fg="white", width=20)

        submit.grid(row=2, column=0)

    def submitted(self):
        SalesInterface.SalesInterface(self.window)

    def menu_interface(self):
        SalesInterface.SalesInterface(self.window)


if __name__ == "__main__":
    root = Tk()
    manage_invoice_interface = ManageInvoiceModuleInterface(root)
    root.mainloop()
