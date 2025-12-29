import tkinter as tk

# Simple test to see if tkinter works
root = tk.Tk()
root.title("Test GUI")
root.geometry("300x200")

label = tk.Label(root, text="If you can see this, tkinter works!")
label.pack(pady=50)

button = tk.Button(root, text="Close", command=root.destroy)
button.pack()

root.mainloop()