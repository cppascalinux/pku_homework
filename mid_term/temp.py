import tkinter as tk
from tkinter import ttk

root = tk.Tk()
container = ttk.Frame(root)
canvas = tk.Canvas(container)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e:canvas.configure(
        scrollregion=(print(canvas.bbox('all')),canvas.bbox("all"))[1]
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
# scrollable_frame.pack(fill='x')
canvas.configure(yscrollcommand=scrollbar.set)

for i in range(50):
    ttk.Label(scrollable_frame, text="Sample scrolling label").pack()
    # canvas.configure(scrollregion=canvas.bbox("all"))
container.pack()
canvas.pack(side="left", fill="both", expand=True)
print(scrollable_frame.bbox('all'))
# canvas.configure(scrollregion=canvas.bbox("all"))
# canvas.configure(scrollregion=canvas.bbox("all"))
# canvas.configure(scrollregion=canvas.bbox("all"))
# canvas.configure(scrollregion=canvas.bbox("all"))
scrollbar.pack(side="right", fill="y")
# canvas.configure(scrollregion=(0,0,0,10000))
root.mainloop()
# canvas.configure(scrollregion=(0,0,0,10000))
