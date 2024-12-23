import pymongo
from config import loader
# MongoDB connection parameters
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "myapp"
COLLECTION_NAME = "users"

myConf = loader.Configer()

class MongoDBConnection:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(
            host=myConf.get('mongodb','host'),
            port=int(myConf.get('mongodb', 'port')),
            username=myConf.get('mongodb','username'),
            password=myConf.get('mongodb','password')
        )
        self.db = self.client[str(myConf.get('mongodb','database'))]

    def close_connection(self):
        self.client.close()
