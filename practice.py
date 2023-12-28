import base64
import os
import threading
import time

import gspread
import pymongo
import requests
from oauth2client.service_account import ServiceAccountCredentials

# Determine the full path to the JSON credentials file
credentials_file = os.path.join(os.getcwd(), "credentials.json")

# Connect to MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["Agrifarm"]
collection = db["Products"]

# Set up Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive", ]
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(creds)

# Connect to the Google Sheet by its title
sheet_title = "Participants data"
spreadsheet = client.open(sheet_title)
worksheet = spreadsheet.get_worksheet(2)  # assuming the data is in the first worksheet

# Get all the data from the Google Sheet
data = worksheet.get_all_records()

# Ensure the "images" directory exists
images_directory = os.path.join(os.getcwd(), "images")
os.makedirs(images_directory, exist_ok=True)


# Function to process each row
def process_row(row):
    try:
        # Check if 'ProductImage' key exists in the row
        if 'ProductImage' in row:
            # Get the image URL from the row
            image_url = row['ProductImage']

            # Check if the image URL is not empty
            if image_url:
                # Download the image from the URL with a custom User-Agent header
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                image_response = requests.get(image_url, headers=headers)

                # Ensure the "images" directory exists
                os.makedirs(images_directory, exist_ok=True)

                # Construct the image file path with the _id as the filename
                image_filename = f"{row['ProductName']}.jpg"
                image_path = os.path.join(images_directory, image_filename)

                # Save the image to the file system
                with open(image_path, "wb") as image_file:
                    image_file.write(image_response.content)

                # Encode the image to base64
                with open(image_path, "rb") as image_file:
                    base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")

                # Store the base64-encoded string in the row
                row['ProductImage'] = base64_encoded

        # Strip leading and trailing spaces from string values
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.strip()

        if row["ProductName"] == "":
            return

        print(row["ProductName"])
        # Insert the row into MongoDB
        # collection.insert_one(row)
        collection.update_one({"ProductName": row["ProductName"]}, {"$set": row}, upsert=True)

    except requests.exceptions.RequestException as e:
        # Print the error and continue to the next row
        print(f"Error processing row: {e}")
    except Exception as e:
        # Print the error and continue to the next row
        print(f"Unhandled error processing row: {e}")


# Use threading for multithreading
threads = []
for row in data:
    if row["ProductName"] == "":
        break
    thread = threading.Thread(target=process_row, args=(row,))
    threads.append(thread)
    time.sleep(0.5)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Close MongoDB connection
mongo_client.close()

print("The Database has been successfully created")
