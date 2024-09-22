from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId


class MongoDB:
    def __init__(self):
        self.uri = "mongodb://localhost:27017"
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client['DB_CREWINSIGHTS']

    def updateFilter(self, filter):
        if "_id" in filter:
            filter.update({"_id": ObjectId(filter.get("_id"))})
        if "id_user" in filter:
            filter.update({"id_user": ObjectId(filter.get("id_user"))})
        if "id_chat" in filter:
            filter.update({"id_chat": ObjectId(filter.get("id_chat"))})
        return filter

    def getDocuments(self, collection, filter={}):
        new_filter = self.updateFilter(filter)
        result = self.db[collection].find(new_filter)
        return list(result)
    
    def getOneDocument(self, collection, filter):
        new_filter = self.updateFilter(filter)
        return self.db[collection].find_one(new_filter)

    def insertOne(self, collection, document):
        new_document = self.updateFilter(document)
        result = self.db[collection].insert_one(new_document)
        return result.inserted_id
    
    def updateOne(self, collection, filter, new_data, array_filters=None):
        new_filter = self.updateFilter(filter)
        if array_filters:
            result = self.db[collection].update_one(
                new_filter, 
                new_data, 
                array_filters=array_filters
            )
        else:
            result = self.db[collection].update_one(new_filter, new_data)
        return {
            "matched_count": result.matched_count,
            "modified_count": result.modified_count
        }
    
    def deleteOne(self, collection, filter):
        new_filter = self.updateFilter(filter)
        return self.db[collection].delete_one(new_filter)

    