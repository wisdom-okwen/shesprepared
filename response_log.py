import csv
from datetime import datetime

log_file = "new_response_logs.csv"
headers = ["Timestamp", "Model", "User_Message", "Response", "Response_Time", "Language_Level"]

def initialize_csv():
    """Initialize the CSV file and write the headers if it doesn't exist."""
    try:
        with open(log_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
    except FileExistsError:
        print('File does not exist')
    finally:
        file.close()



def log_to_csv(model, user_message, response, response_time, language_level):
    """Log data to CSV."""
    with open(log_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), model, user_message, response, response_time, language_level])
    file.close()
    

if __name__ == '__main__':
    initialize_csv()

