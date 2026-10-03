from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password, host, port, database, collection): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = username 
        PASS = password
        HOST = host
        PORT = port 
        DB = database 
        COL = collection
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        if data is not None: 
            insert_result = self.database.animals.insert_one(data)  # data should be dictionary             
            # Return True if successful insert, else False
            if insert_result.inserted_id:
                return True
            else:
                return False
        else: 
            raise Exception("Nothing to save, because data parameter is empty") 

    # Create method to implement the R in CRUD.
    def read(self, query):
        if query is not None:
            # Use find() to return a cursor, then convert to a list
            cursor = self.database.animals.find(query)
            return list(cursor)
        else:
            # Return empty list if no query is provided
            return []
        
     # Create method to implement the U in CRUD.
    def update(self, query, update_data):
        if query is not None and update_data is not None:
            result = self.database.animals.update_many(query, {"$set": update_data})
            
            # Return the number of objects modified
            return result.modified_count
        else:
            raise Exception("Query or update data parameters are empty")

    # Create method to implement the D in CRUD.
    def delete(self, query):
        if query is not None:
            result = self.database.animals.delete_many(query)
            
            # Return the number of objects removed
            return result.deleted_count
        else:
            raise Exception("Query parameter is empty")
