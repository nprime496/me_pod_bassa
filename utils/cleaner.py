import csv
import re

def remove_non_accentuated_chars(input_string):
    # Define a regular expression pattern that matches all non-accentuated characters
    pattern = r"[^a-zA-ZÀ-ÖØ-öø-ÿ\s/\']"
    # Use the sub() method to replace all non-accentuated characters with an empty string
    output_string = re.sub(",", "", input_string)
    # Return the modified string
    return output_string
# Open the file for reading
with open("dump.txt", "r", encoding="utf-8") as f:
    # Initialize an empty dictionary to store translations
    translations = {}
    # Loop through each line in the file
    for line in f:
        # Ignore lines that contain unwanted characters
        if "=>" not in line and ":" not in line:
            continue
        # Remove newline characters
        line = line.strip()
        # Remove strange formatting characters
        line = line.replace("=>", "->",1)
        line = line.replace(":", "->",1)
        line = line.replace("  ", " ",1)
        # Split the line into key-value pairs
        parts = line.lower().split("->")
        # Ignore lines that don't contain both a key and a value
        if len(parts) < 2:
           continue
        # Store the key-value pair in the dictionary
        key = remove_non_accentuated_chars(parts[0]).strip()
        value = remove_non_accentuated_chars(parts[1]).strip()
        translations[key] = value

# Write the translations to a CSV file
with open("translations.csv", "w", encoding="utf-8", newline="") as f:
    # Create a CSV writer object
    writer = csv.writer(f)
    # Write the header row
    writer.writerow(["bassa", "traduction"])
    # Write each key-value pair as a row in the CSV file
    for key, value in translations.items():
        writer.writerow([key, value])
