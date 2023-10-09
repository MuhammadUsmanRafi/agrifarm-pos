import tkinter as tk

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius):
    canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, start=90, extent=90, style=tk.ARC)
    canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, start=0, extent=90, style=tk.ARC)
    canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, start=180, extent=90, style=tk.ARC)
    canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, start=270, extent=90, style=tk.ARC)
    canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill="white")
    canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill="white")

# Create the tkinter window
root = tk.Tk()
root.geometry("400x300")

# Create a Canvas to draw the rounded rectangle
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# Coordinates and radius for the rounded rectangle
x1, y1, x2, y2 = 50, 50, 350, 250
radius = 20

# Create the rounded rectangle on the canvas
create_rounded_rectangle(canvas, x1, y1, x2, y2, radius)

# Create a frame on top of the canvas
frame = tk.Frame(root, width=350, height=200, bg="white")
frame.place(x=50, y=50)

root.mainloop()
