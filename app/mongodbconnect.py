import os
import bottle
import pymongo

#get url that is stored in config
MONGO_URL = "mongodb://gabeochoa:password1@kahana.mongohq.com:10009/cqs_data"

def mongoconn():
	connection = pymongo.Connection(MONGO_URL)
	db = connection['cqs_data']
	return str(db.test.find()[0])


	'''

import urllib
from mongodbconnect import mongoconn
@route('/mongo')
def mongo():
	return mongoconn()
	'''