import json
from bq import BigQueryWriter

# Initialize the BigQueryWriter
bq_writer = BigQueryWriter("../bq-service-acc-key.json")

# Define the dataset and table IDs
dataset_id = "indivu"
table_id = "Example"

# Read Rimi_output.json
with open('example.json', 'r') as f:
    data = json.load(f)

# Define the starting index and the batch size
start_index = 0
batch_size = 500

# Insert the data into BigQuery in batches
for i in range(start_index, len(data), batch_size):
    end_index = i + batch_size
    data_batch = data[i:end_index]
    bq_writer.write_data(dataset_id, table_id, data_batch)
