import os
import csv
from pathlib import Path

data_dir = Path(os.path.dirname(__file__))
local_authority_csv = 'local-authority-eng.csv'
cvs_file_path = os.path.join(data_dir, local_authority_csv)


class LocalAuthorityMapping:

    def __init__(self):
        self.local_authority_mapping = {}
        with open(cvs_file_path, 'r') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                key = f"local-authority-eng:{row['local-authority-eng']}"
                self.local_authority_mapping[key] = row['official-name']

    def get_local_authority_name(self, local_authority_id):
        return self.local_authority_mapping.get(local_authority_id)
