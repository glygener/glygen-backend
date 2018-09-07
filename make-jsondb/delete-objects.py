import os,sys
import string
import commands
from optparse import OptionParser
import glob
import json
import pymongo
from pymongo import MongoClient


__version__="1.0"
__status__ = "Dev"



###############################
def main():

	usage = "\n%prog  [options]"
        parser = OptionParser(usage,version="%prog version___")
        parser.add_option("-c","--coll",action="store",dest="coll",help="Collection name")
        
        (options,args) = parser.parse_args()
        for key in ([options.coll]):
            if not (key):
                parser.print_help()
                sys.exit(0)


        config_obj = json.loads(open("conf/config.json", "r").read())
        path_obj  =  config_obj[config_obj["server"]]["pathinfo"]
        root_obj =  config_obj[config_obj["server"]]["rootinfo"]
        db_obj = config_obj[config_obj["server"]]["dbinfo"]
        

	client = MongoClient('mongodb://localhost:27017')
	db = client[db_obj["dbname"]]

        coll = options.coll
        result = db[coll].delete_many({})



if __name__ == '__main__':
	main()

