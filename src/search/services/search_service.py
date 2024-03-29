import pymongo


class SearchService:

    def __init__(self, cosmos_config):
        self._cosmos_config = cosmos_config

    def search_content(self, search_term):
        client = pymongo.MongoClient(self._cosmos_config["connection_string"])
        db = client[self._cosmos_config["db_name"]]

        content_collection = None

        if db[self._cosmos_config["content_collection_name"]] is None:
            content_collection = db.create_collection(
                self._cosmos_config["content_collection_name"])
        else:
            content_collection = db[self._cosmos_config["content_collection_name"]]

        filter = {
            "$and": [
                {
                    "is_active": {
                        "$eq": True
                    }
                },
                {
                    "$or": [
                        {
                            "title": {
                                "$regex": search_term,
                                "$options": "i"
                            }
                        },
                        {
                            "description": {
                                "$regex": search_term,
                                "$options": "i"
                            }
                        }
                    ]
                }
            ]
        }
        
        projection = {"title": 1, "id": 1}

        results = content_collection.find(filter, projection)
        
        return results
