import json
import csv
import logging
from google.cloud import storage
import os
import tempfile

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Google Cloud Storage client setup
storage_client = storage.Client()

# Define GCS bucket and file paths
GCS_BUCKET_NAME = 'gcp-terraform-demo-ax-001-data'
GCS_JSON_FILE = 'data.json'
GCS_CSV_FILE = 'processed_data.csv'


# Read JSON from GCS
def read_json_from_gcs(bucket_name, file_name):
    try:
        # Get the bucket
        bucket = storage_client.get_bucket(bucket_name)
        
        # Get the blob (file object)
        blob = bucket.blob(file_name)
        
        # Download the file content
        json_data = blob.download_as_text()
        
        # Parse JSON content
        data = json.loads(json_data)
        
        # Log the data to check if it was read correctly
        logging.info(f"Read data from GCS: {data}")
        
        return data
    except Exception as e:
        logging.exception(f"Error occurred while reading from GCS: {e}")
        return None


# Process data
def process_data(data):
    if data is None:
        return []
    for item in data:
        try:
            if item["age"] < 30:
                item["category"] = "Young"
            elif 30 <= item["age"] < 40:
                item["category"] = "Middle-aged"
            else:
                item["category"] = "Older"
        except KeyError as e:
            logging.warning(f"Missing key in data: {e}")
        except Exception as e:
            logging.exception(f"Error occurred while processing data: {e}")
    
    # Log processed data to check the result
    logging.info(f"Processed data: {data}")
    
    return data


# Save processed data to GCS as CSV
def save_to_gcs(bucket_name, file_name, data):
    if not data:
        logging.warning("No data to save.")
        return
    keys = data[0].keys()
    
    try:
        # Prepare the CSV content
        csv_content = []
        for row in data:
            csv_content.append([row[key] for key in keys])

        # Log CSV content before writing to GCS
        logging.info(f"CSV Content: {csv_content}")
        
        # Use tempfile to create a temporary file in the local system
        with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='') as tmp_file:
            writer = csv.writer(tmp_file)
            writer.writerow(keys)  # Write headers
            writer.writerows(csv_content)

            # Close the file after writing
            tmp_file.close()

            # Upload CSV file to GCS
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(file_name)
            blob.upload_from_filename(tmp_file.name)

        logging.info(f"Processed data saved to {file_name} in GCS!")
    except Exception as e:
        logging.exception(f"Error occurred while saving to GCS: {e}")


def main():
    data = read_json_from_gcs(GCS_BUCKET_NAME, GCS_JSON_FILE)
    if data is not None:
        processed_data = process_data(data)
        save_to_gcs(GCS_BUCKET_NAME, GCS_CSV_FILE, processed_data)


if __name__ == "__main__":
    main()
