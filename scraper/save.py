import os
import json
import csv

def save_to_json(data, output_file):
    """
    Saves the data to a JSON file.

    :param data: The data to save (typically a list of dictionaries).
    :param output_file: The path to the output JSON file.
    :raises: IOError if the file cannot be written.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

def save_to_csv(data, output_file):
    """
    Saves the data to a CSV file.

    :param data: The data to save (typically a list of dictionaries).
    :param output_file: The path to the output CSV file.
    :raises: IOError if the file cannot be written.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    if not data:
        raise ValueError("No data to write to CSV.")

    # Determine the CSV headers from the keys of the first dictionary
    headers = list(data[0].keys())

    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for entry in data:
            # Convert lists to semicolon-separated strings for CSV
            entry_copy = entry.copy()
            for key, value in entry_copy.items():
                if isinstance(value, list):
                    entry_copy[key] = '; '.join(value)
            writer.writerow(entry_copy)
