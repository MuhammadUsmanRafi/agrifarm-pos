import tkinter as tk


def on_horizontal_scroll(*args):
    canvas.xview(*args)


root = tk.Tk()
root.title("Horizontal Scrollbar in Frame")

# Create a frame
frame = tk.Frame(root, width=300, height=200)
frame.pack()

# Create a canvas within the frame
canvas = tk.Canvas(frame, bg="white", width=300, height=200, scrollregion=(0, 0, 800, 200))

# Add a horizontal scrollbar to the frame
horizontal_scrollbar = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
horizontal_scrollbar.pack(side="bottom", fill="x")

# Configure the canvas to update the scrollbar
canvas.config(xscrollcommand=horizontal_scrollbar.set)

# Add widgets or content to the canvas
for i in range(20):
    label = tk.Label(canvas, text=f"Label {i}")
    canvas.create_window((i * 40, 100), window=label, anchor="nw")

# Bind the canvas to the scrollbar
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Pack the canvas
canvas.pack(side="left", fill="both", expand=True)

root.mainloop()
