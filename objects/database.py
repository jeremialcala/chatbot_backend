import pymongo
from constants import *


class Database:
    def __init__(self, schema=SCHEMA, conn=MONGO):
        super().__init__()
        self.schema = schema
        self.client = pymongo.MongoClient(conn)
        self.db = self.client[schema]

    def get_client(self):
        return self.client

    def close_connection(self):
        self.client.close()

    def get_schema(self):
        return self.db
