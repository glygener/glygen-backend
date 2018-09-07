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


def reset_sequence_value(db, sequence_name):
    seq_doc = db.c_counters.find_and_modify(
        query={'_id': sequence_name},
        update={'$set': {'sequence_value': 0}},
        upsert=True,
        new=True
    )
    return


def get_next_sequence_value(db, sequence_name):

    seq_doc = db.c_counters.find_and_modify(
        query={'_id': sequence_name}, 
        update={'$inc': {'sequence_value': 1}}, 
        upsert=True, 
        new=True
    )
    return int(seq_doc["sequence_value"])




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
        
        coll_info = {
            "c_glycan":{
                "dbfile":path_obj["jsondbpath"] + "glycandb.json"
                ,"primaryid":"glycanid"
                ,"dbtype":1
            }
            ,"c_protein":{
                "dbfile":path_obj["jsondbpath"] + "proteindb.json"
                ,"primaryid":"proteinid"
                ,"dbtype":1
            }
            ,"c_searchinit":{
                "dbfile":path_obj["jsondbpath"] + "searchinitdb.json"
                ,"primaryid":"searchinitid"
                ,"dbtype":2
            }
	}
        
        
        json_db_file = coll_info[coll]["dbfile"]
        primary_id = coll_info[coll]["primaryid"]
       

        objs = json.loads(open(json_db_file, "r").read())
        flag = True
        reset_sequence_value(db, primary_id)
        
        nrecords = 0
        if coll_info[coll]["dbtype"] == 1:
            for key in objs:
                objs[key]["_id"]  = get_next_sequence_value(db, primary_id)
                result = db[coll].insert_one(objs[key])	
	        nrecords += 1
        elif coll_info[coll]["dbtype"] == 2:
            result = db[coll].insert_one(objs)
            nrecords += 1
        elif coll_info[coll]["dbtype"] == 3:
            for obj in objs:
                category_title = obj["title"]
                category_id = obj["categoryid"]
                for o in obj["datasets"]:
                    o["_id"]  = get_next_sequence_value(db, primary_id)
                    o["categorytitle"] = category_title
                    o["categoryid"] = category_id
                    result = db[coll].insert_one(o)
                    nrecords += 1

        print "Done! Loaded %s objects to %s " % (nrecords, coll)


if __name__ == '__main__':
	main()

