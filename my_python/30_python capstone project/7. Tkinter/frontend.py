import tkinter as tk
from tkinter import messagebox

# Create the main application window
root = tk.Tk()
root.title("Greeting App")
root.geometry("300x200")  # Set the size of the window
# Function to display the greeting
def greet():
    name = name_entry.get()
    if name:
        messagebox.showinfo("Greeting", f"Hello, {name}!")
    else:
        messagebox.showwarning("Input Error", "Please enter your name.")

# Create a label
name_label = tk.Label(root, text="Enter your name:")
name_label.pack(pady=10)  # Padding around the widget

# Create an entry box for user input
name_entry = tk.Entry(root)
name_entry.pack(pady=10)

# Create a button that triggers the greet function
greet_button = tk.Button(root, text="Greet", command=greet)
greet_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
