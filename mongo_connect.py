import pymongo
import constants

def connectMongo():
	url = "mongodb://" + constants.host + "/" + constants.db
	client = pymongo.MongoClient(url)
	db = client[constants.db]
	collection = db[constants.collection]
	return collection

