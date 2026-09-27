import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Simple Tkinter App")
root.geometry("200x100")  # Set window size

# Function to print "Hello, World!" in the console
def say_hello():
    print("Hello, World!")
    print('good bye')

# Create a button that triggers the say_hello function
hello_button = tk.Button(root, text="Click Me", command=say_hello)
hello_button.pack(pady=20)  # Pack the button into the window

# Start the Tkinter event loop
root.mainloop()
