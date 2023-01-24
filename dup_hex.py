import json
import os

# Read the json file
with open(os.path.join("data", "test2.json"), 'r') as file:
    data = json.load(file)

# Remove duplicates from the data
unique_data = list({v['hex']: v for v in data}.values())

# Write the unique data back to the json file
with open(os.path.join("data", "final_data.json"), 'w') as file:
    json.dump(unique_data, file)
