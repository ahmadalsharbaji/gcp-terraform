import json
import csv
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read from a JSON file
def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)  # Use load instead of loads
        return data
    except FileNotFoundError:
        logging.error(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON from file '{file_path}'.")
        return None
    except Exception as e:
        logging.exception(f"Unexpected error occurred while reading the file '{file_path}': {e}")
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
    return data


# Save to output file
def save_to_csv(data, output_file):
    if not data:
        logging.warning("No data to save.")
        return
    keys = data[0].keys()
    try:
        with open(output_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        logging.info(f"Processed data saved to {output_file}!")
    except Exception as e:
        logging.exception(f"Error occurred while saving data to CSV: {e}")


def main():
    input_file = "data.json"
    output_file = "processed_data.csv"

    data = read_json(input_file)
    if data is not None:
        processed_data = process_data(data)
        save_to_csv(processed_data, output_file)


if __name__ == "__main__":
    main()
