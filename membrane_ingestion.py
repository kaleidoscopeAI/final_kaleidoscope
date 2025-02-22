import json
import requests

class Membrane:
    def __init__(self, data_source):
        self.data_source = data_source

    def ingest_data(self):
        """Ingest data from a specified source (file, URL, or API)."""
        if self.data_source.startswith("http"):
            response = requests.get(self.data_source)
            data = response.json()
        else:
            with open(self.data_source, "r") as file:
                data = json.load(file)
        return data
        
