from google.cloud import bigquery
from google.oauth2.service_account import Credentials
import json

class BigQueryWriter:
    def __init__(self, key_file):
        with open(key_file, "r") as f:
            credentials_data = json.load(f)

        self.client = bigquery.Client(
            project=credentials_data["project_id"],
            credentials=Credentials.from_service_account_info(credentials_data)
            )

    def _get_schema(self, data):
        """Generate a BigQuery schema from a data dictionary."""
        schema = []
        for key, value in data[0].items():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                # This is an array of records
                record_schema = bigquery.SchemaField(
                    name=key,
                    field_type="RECORD",
                    mode="REPEATED",
                    fields=[bigquery.SchemaField(subkey, "STRING") for subkey in value[0].keys()]
                )
                schema.append(record_schema)
            else:
                schema.append(bigquery.SchemaField(key, "STRING"))
        return schema

    def replace_null_with_none(self, data):
        """
        Recursive function to replace all null values with None in the data.
        """
        if isinstance(data, list):
            return [self.replace_null_with_none(item) for item in data]
        elif isinstance(data, dict):
            return {key: self.replace_null_with_none(value) for key, value in data.items()}
        elif data is None:  # 'is' keyword is used to check for None identity
            return None
        else:
            return data

    def write_data(self, dataset_id, table_id, data):
        dataset_ref = self.client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)

        dataset = bigquery.Dataset(dataset_ref)
        table = bigquery.Table(table_ref)

        # Check if dataset exists, if not, create it
        try:
            self.client.get_dataset(dataset)
        except Exception:
            self.client.create_dataset(dataset)

        # Check if table exists, if not, create it
        try:
            table = self.client.get_table(table)
        except Exception:
            schema = self._get_schema(data)
            table.schema = schema
            table = self.client.create_table(table)

        # Replace null with None in data
        data = self.replace_null_with_none(data)

        # Insert data into the table
        errors = self.client.insert_rows(table, data)
        if errors:
            print(f"Encountered errors while inserting rows: {errors}")
        else:
            print(f"Inserted {len(data)} rows into {dataset_id}.{table_id}")
