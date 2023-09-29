from filestack import Client
import dotenv
import os

dotenv.load_dotenv()

class Filesharer:

    def __init__(self, filepath, api_key=os.getenv("FILESTACK_API_KEY")):
        self.filepath = filepath
        self.api_key = api_key

    def share(self):
        client = Client(self.api_key)
        uploaded_filelink = client.upload(filepath=self.filepath)
        return uploaded_filelink.url