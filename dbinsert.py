import json

def insert_data(data, db):

    # Your code here. Insert the data into a collection 'arachnid'
    db.mumbai.insert(data)
    pass


if __name__ == "__main__":
    
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.maps

    with open('mumbai_india.json') as f:
        
        try :
            data = json.loads(f.read())
        except Exception :
            print 
            raise
        insert_data(data, db)
        print db.mumbai.find_one()