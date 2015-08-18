import os
import bottle
import pymongo

def mongoconn():
	MONGO_URL = os.environ.get('MONGOHQ_URL')
	connection = pymongo.Connection(MONGO_URL)
	return connection['cqs_data']
