import os
import bottle
import pymongo

def mongoconn():
	MONGO_URL = os.getenv('MONGOHQ_URL')
	connection = pymongo.Connection(MONGO_URL)
	db = connection['cqs_data']
	return db