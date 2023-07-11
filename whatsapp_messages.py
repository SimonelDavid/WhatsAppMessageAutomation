import csv
import pywhatkit

# Path to CSV file containing phone numbers
csv_file_path = 'phone_numbers.csv'

# Message to send
message = "Salutare! Ai aplicat pentru a face parte din ROSPIN Community Local TaskForce. Ti-am trimis zilele trecute doua e-mailuri cu mai multe detalii. As vrea sa imi spui daca l-ai primit sau nu. 🤗🚀"

# Read phone numbers from CSV file and send messages
with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        for number in row:
            # Send message using pywhatkit
            pywhatkit.sendwhatmsg_instantly(number, message)

            print(f"Message sent to {number}")
