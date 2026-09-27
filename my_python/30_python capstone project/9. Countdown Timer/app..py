from plyer import notification
from tkinter import messagebox
from tkinter import *
import time

# Assign class and set dimensions of the interface
window = Tk()
window.geometry("300x200")
window.title("Countdown Timer and Notification")

# Set background color of the window
window.config(bg='lightblue')

# Remove the placeholders for every entry field based on click
def h_click(event):
    hour_entry.delete(0, 'end')

def m_click(event):
    min_entry.delete(0, 'end')

def s_click(event):
    sec_entry.delete(0, 'end')

# Function to activate Python countdown timer and show notifications once timer is up
def timer():
    try:
        hours_value = int(hour_entry.get())
        mins_value = int(min_entry.get())
        secs_value = int(sec_entry.get())
        
        # Validate input
        if hours_value < 0 or mins_value < 0 or secs_value < 0:
            raise ValueError("Time values cannot be negative")

        timer_time = hours_value * 3600 + mins_value * 60 + secs_value

        if timer_time > 0:
            while timer_time >= 0:
                hour, remainder = divmod(timer_time, 3600)
                min, sec = divmod(remainder, 60)
                hours.set(hour)
                mins.set(min)
                secs.set(sec)
                time.sleep(1)
                window.update()
                timer_time -= 1

            notification.notify(
                title="TIMER ALERT",
                message="Hey kodi!\nDid you do what you wanted to achieve? \nIf not, try again with a new timer",
                timeout=30,
            )
            messagebox.showinfo(message="Timer Complete!")
        else:
            messagebox.showerror(message="Timer value must be greater than 0")
    except ValueError as e:
        messagebox.showerror(message=f"Enter Valid Time: {e}")

# Label for displaying the title of the app
title_label_1 = Label(window, text="Timer with Notification", font=("Gayathri", 12), bg='lightblue')
title_label_1.pack()
title_label_2 = Label(window, text="Put 0 in fields not of use", font=("Gayathri", 10), bg='lightblue')
title_label_2.pack()

# Variables using which the timer is updated in the function
hours = IntVar()
mins = IntVar()
secs = IntVar()

# To read user input for hours, minutes, and seconds
hour_entry = Entry(window, width=3, textvariable=hours, font=("Ubuntu Mono", 18), bg='white')
min_entry = Entry(window, width=3, textvariable=mins, font=("Ubuntu Mono", 18), bg='white')
sec_entry = Entry(window, width=3, textvariable=secs, font=("Ubuntu Mono", 18), bg='white')

# Placeholder for the entry widgets
hour_entry.insert(0, '00')
min_entry.insert(0, '00')
sec_entry.insert(0, '00')

# Positioning the entry widgets
hour_entry.place(x=80, y=40)
min_entry.place(x=130, y=40)
sec_entry.place(x=180, y=40)

# To link the defined placeholder removal functions on mouse click
hour_entry.bind("<Button-1>", h_click)
min_entry.bind("<Button-1>", m_click)
sec_entry.bind("<Button-1>", s_click)

# Button to activate the timer function
button = Button(window, text='Start Timer', bg='cyan', command=timer)
button.pack(pady=40)

# Close the window and exit the app
window.mainloop()
