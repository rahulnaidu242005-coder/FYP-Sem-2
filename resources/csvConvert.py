import csv
import json

input_file = "metakeys.csv"
output_file = input_file.split('.')[0]+".json"

with open(input_file, mode='r', newline='', encoding='utf-8') as csvfile:
    data = list(csv.DictReader(csvfile))

with open(output_file, mode='w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, indent=4)