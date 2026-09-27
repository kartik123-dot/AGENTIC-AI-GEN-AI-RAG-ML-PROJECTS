import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Simple Counter App")
root.geometry("300x200")  # Set the size of the window

# Initialize the counter variable
counter = 0

# Function to update the counter label
def update_label():
    count_label.config(text=f"Count: {counter}")

# Function to increment the counter
def increment():
    global counter
    counter += 1
    update_label()

# Function to decrement the counter
def decrement():
    global counter
    counter -= 1
    update_label()

# Create a label to display the counter
count_label = tk.Label(root, text=f"Count: {counter}", font=("Helvetica", 16))
count_label.pack(pady=20)

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Create the Increment button
increment_button = tk.Button(button_frame, text="Increment", command=increment, width=10)
increment_button.pack(side=tk.LEFT, padx=5)

# Create the Decrement button
decrement_button = tk.Button(button_frame, text="Decrement", command=decrement, width=10)
decrement_button.pack(side=tk.LEFT, padx=5)

# Start the Tkinter event loop
root.mainloop()
