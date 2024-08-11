import json
import os
import datetime
data_latest_path = "data-latest.json"


def rewrite_apt_data(apartments_dict):
    # Write the dictionary to the JSON file
    os.rename(data_latest_path, "data-" + str(datetime.datetime.now()) + ".json")
    with open(data_latest_path, 'w') as file:
        json.dump(apartments_dict, file, indent=4)


def get_apt_data():
    # Read the JSON file and load it into a dictionary
    with open(data_latest_path, 'r') as file:
        data_dict = json.load(file)

    return data_dict
