import os
import bottle
import pymongo

def mongoconn():
	#if in production environment, get URL from environment variable
	MONGO_URL = "mongodb://gabeochoa:password1@kahana.mongohq.com:10009/cqs_data"
	connection = pymongo.Connection(MONGO_URL)
	db = connection['cqs_data']
	return db
	'''
	try:
		MONGO_URL = "mongodb://gabeochoa:password1@kahana.mongohq.com:10009/cqs_data"
		#MONGO_URL = os.environ.get('MONGOHQ_URL')
		connection = pymongo.Connection(MONGO_URL)
		db = connection['cqs_data']
	# if in development environment, use hardcoded URL
	except:
		MONGO_URL = "mongodb://gabeochoa:password1@kahana.mongohq.com:10009/cqs_data"
		connection = pymongo.Connection(MONGO_URL)
		db = connection['cqs_data']
	return db
	'''