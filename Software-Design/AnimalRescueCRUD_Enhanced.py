import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# Configure basic logging to track database transactions
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class AnimalShelter:
    """
    CRUD operations for the Animal collection in MongoDB.
    Handles connections, schema validation, and data aggregation.
    """

    def __init__(self, username, password, host, port, database, collection):
        """
        Initializes the MongoClient and connects to the database.
        """
        try:
            # Use f-strings for a cleaner URI string
            uri = f"mongodb://{username}:{password}@{host}:{port}"
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            
            # Verify the connection is active
            self.client.admin.command('ping')
            
            self.database = self.client[database]
            self.collection = self.database[collection]
            logging.info("Successfully connected to the MongoDB database.")
            
            # Enforce schema rules upon connection
            self.setup_schema_validation()
            
        except ConnectionFailure as e:
            logging.error(f"Could not connect to MongoDB: {e}")
            raise

    def setup_schema_validation(self):
        """
        Applies JSON schema validation to the collection to prevent malformed data injection.
        """
        validation_schema = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["animal_type", "breed", "age_upon_outcome_in_weeks"],
                "properties": {
                    "animal_type": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "breed": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "age_upon_outcome_in_weeks": {
                        "bsonType": ["double", "int"],
                        "minimum": 0,
                        "description": "must be a positive number and is required"
                    }
                }
            }
        }
        
        try:
            self.database.command("collMod", self.collection.name, validator=validation_schema, validationLevel="strict")
            logging.info("Schema validation successfully applied to the collection.")
        except OperationFailure as e:
            # Handle cases where the user lacks admin privileges to modify collections
            logging.warning(f"Schema validation could not be applied due to permission boundaries: {e}")

    def create(self, data: dict) -> bool:
        """
        Inserts a new document into the collection.
        """
        if not data or not isinstance(data, dict):
            logging.warning("Create operation failed. Data parameter is empty or not a dict.")
            return False

        try:
            insert_result = self.collection.insert_one(data)
            if insert_result.inserted_id:
                logging.info(f"Document successfully inserted with ID: {insert_result.inserted_id}")
                return True
            return False
        except OperationFailure as e:
            # Catch errors if the data violates our schema validation rules
            logging.error(f"Failed to insert document. Data may violate schema rules: {e}")
            return False

    def read(self, query: dict) -> list:
        """
        Queries the database and returns a list of matching documents.
        """
        if query is None:
            query = {}

        try:
            cursor = self.collection.find(query)
            results = list(cursor)
            logging.info(f"Read operation successful. Found {len(results)} documents.")
            return results
        except OperationFailure as e:
            logging.error(f"Failed to read from database: {e}")
            return []

    def get_rescue_candidates(self, rescue_type: str) -> list:
        """
        Uses an aggregation pipeline to filter and sort data directly on the server.
        """
        pipeline = []
        
        # Stage 1: Match criteria based on the rescue type
        if rescue_type == 'water':
            pipeline.append({"$match": {
                "animal_type": "Dog",
                "breed": {"$in": ["Labrador Retriever Mix", "Golden Retriever Mix", "Newfoundland Mix"]},
                "sex_upon_outcome": "Intact Female",
                "age_upon_outcome_in_weeks": {"$gte": 26.0, "$lte": 156.0}
            }})
        elif rescue_type == 'mountain':
            pipeline.append({"$match": {
                "animal_type": "Dog",
                "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
                "sex_upon_outcome": "Intact Male",
                "age_upon_outcome_in_weeks": {"$gte": 26.0, "$lte": 156.0}
            }})
        elif rescue_type == 'tracking':
            pipeline.append({"$match": {
                "animal_type": "Dog",
                "breed": {"$in": ["Doberman Pinsch", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
                "sex_upon_outcome": "Intact Male",
                "age_upon_outcome_in_weeks": {"$gte": 20.0, "$lte": 300.0}
            }})
        else:
            return self.read({})
            
        # Stage 2: Sort the results by age on the server side
        pipeline.append({"$sort": {"age_upon_outcome_in_weeks": 1}})
        
        try:
            cursor = self.collection.aggregate(pipeline)
            results = list(cursor)
            logging.info(f"Aggregation successful. Filtered and sorted {len(results)} {rescue_type} candidates.")
            return results
        except OperationFailure as e:
            logging.error(f"Failed to execute aggregation pipeline: {e}")
            return []

    def update(self, query: dict, update_data: dict) -> int:
        """
        Updates documents matching the query.
        """
        if not query or not update_data:
            logging.warning("Update operation failed. Query or update data is missing.")
            return 0

        try:
            result = self.collection.update_many(query, {"$set": update_data})
            logging.info(f"Update operation successful. Modified {result.modified_count} documents.")
            return result.modified_count
        except OperationFailure as e:
            logging.error(f"Failed to update documents: {e}")
            return 0

    def delete(self, query: dict) -> int:
        """
        Deletes documents matching the query.
        """
        if not query:
            logging.warning("Delete operation failed. Query parameter is empty.")
            return 0

        try:
            result = self.collection.delete_many(query)
            logging.info(f"Delete operation successful. Removed {result.deleted_count} documents.")
            return result.deleted_count
        except OperationFailure as e:
            logging.error(f"Failed to delete documents: {e}")
            return 0
