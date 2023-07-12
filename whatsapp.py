import os
import stat
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import csv
import pywhatkit
from pathlib import Path

# Global variable to store the file path
file_path = ""

# Function to send messages
def send_messages():
    global file_path
    message = message_entry.get("1.0", tk.END)

    # Check if CSV file has been uploaded
    if not file_path:
        messagebox.showerror("Error", "Please upload a CSV file first.")
        return

    # Check if message is empty
    if not message.strip():
        messagebox.showerror("Error", "Please enter a message.")
        return

    # Get the desired file path
    file_path = 'PyWhatKit_DB.txt'

    # Get current working directory
    current_directory = os.getcwd()

    # Set the file path in the current directory
    db_file_path = os.path.join(current_directory, "PyWhatKit_DB.txt")

    # Change file permissions to read, write, and execute for everyone
    os.chmod(db_file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    try:
        # Read phone numbers from CSV file
        phone_numbers = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            if 'phone_number' not in header:
                raise ValueError("CSV file must have a column named 'phone_number'")
            for row in reader:
                phone_number = row[header.index('phone_number')]
                if not phone_number.startswith("+"):
                    raise ValueError("Phone numbers must start with '+' in the CSV file")
                phone_numbers.append(phone_number)

        # Send messages using pywhatkit
        sent_numbers = []
        for number in phone_numbers:
            pywhatkit.sendwhatmsg_instantly(number, message)
            sent_numbers.append(number)

        # Display success message
        messagebox.showinfo("Success", "Messages sent successfully to:\n\n" + "\n".join(sent_numbers))

    except Exception as e:
        # Display error message
        messagebox.showerror("Error", str(e))

# Function to be executed when the "Upload CSV" button is clicked
def upload_csv():
    global file_path

    # Open file dialog to select a CSV file
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        thick_box.config(relief=tk.SUNKEN)  # Check the checkbox
        thick_box.config(background="green")  # Set background color to green
        messagebox.showinfo("Success", "CSV file uploaded successfully!")

# Create the main window
window = tk.Tk()
window.title("WhatsApp Message Sender")

# Create a label
label = tk.Label(window, text="Click 'Upload CSV' to select a CSV file.")
label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.W)

# Create a button to upload CSV file
upload_button = tk.Button(window, text="Upload CSV", command=upload_csv, relief=tk.FLAT)
upload_button.grid(row=0, column=1, pady=5, padx=(0, 0), sticky=tk.W)

# Create a thick box
thick_box = tk.Label(window, width=2, relief=tk.SOLID)
thick_box.grid(row=0, column=1, pady=0, padx=15)

# Create a message entry field using scrolled text widget
message_label = tk.Label(window, text="Enter the message:")
message_label.grid(row=1, column=0, pady=0, padx=10, sticky=tk.NW)
message_entry = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=10)
message_entry.grid(row=1, column=1, columnspan=2, pady=5, padx=(0, 10))

# Create a button to send the message
send_button = tk.Button(window, text="Send Message", command=send_messages)
send_button.grid(row=2, column=0, columnspan=3, pady=5, padx=10)

# Run the main event loop
window.mainloop()
