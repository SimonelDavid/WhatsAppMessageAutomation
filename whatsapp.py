import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import pywhatkit

# Global variable to store the file path
file_path = ""

# Function to send messages
def send_messages():
    global file_path
    message = message_entry.get()

    # Check if CSV file has been uploaded
    if not file_path:
        messagebox.showerror("Error", "Please upload a CSV file first.")
        return

    # Check if message is empty
    if not message:
        messagebox.showerror("Error", "Please enter a message.")
        return

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
        messagebox.showinfo("Success", "CSV file uploaded successfully!")

# Create the main window
window = tk.Tk()
window.title("WhatsApp Message Sender")

# Create a label
label = tk.Label(window, text="Click 'Upload CSV' to select a CSV file.")
label.pack(pady=10)

# Create a button to upload CSV file
upload_button = tk.Button(window, text="Upload CSV", command=upload_csv)
upload_button.pack(pady=5)

# Create a message entry field
message_label = tk.Label(window, text="Enter the message:")
message_label.pack(pady=5)
message_entry = tk.Entry(window, width=50)
message_entry.pack()

# Create a button to send the message
send_button = tk.Button(window, text="Send Message", command=send_messages)
send_button.pack(pady=5)

# Run the main event loop
window.mainloop()
