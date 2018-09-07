import os,sys
import json
import csv
import glob

from optparse import OptionParser
from SPARQLWrapper import SPARQLWrapper, JSON 

import pymongo
from pymongo import MongoClient


__version__="1.0"
__status__ = "Dev"


######################
def load_dataframe(data_frame, sheet_name, in_file, separator):

    field_list = []
    data_frame[sheet_name] = {}
    with open(in_file, 'r') as FR:
        csv_grid = csv.reader(FR, delimiter=separator, quotechar='"')
        row_count = 0
        for row in csv_grid:
            row_count += 1
            if row_count == 1:
                field_list = row
            else:
                row_obj = {}
                for j in xrange(1,len(field_list)):
                    field_name  = field_list[j]
                    row_obj[field_name] = [] if row[j].strip() == "" else row[j].replace("\"","").split("|")
                main_id = row[0].strip()
                if main_id not in data_frame[sheet_name]:
                    data_frame[sheet_name][main_id] = []
                data_frame[sheet_name][main_id].append(row_obj)
    return field_list





###############################
def main():

    usage = "\n%prog  [options]"
    parser = OptionParser(usage,version="%prog " + __version__)
    parser.add_option("-s","--species",action="store",dest="species",help="human/mouse")

    (options,args) = parser.parse_args()
    for file in ([options.species]):
        if not (file):
            parser.print_help()
            sys.exit(0)
        
    species = options.species
    tax_id = "9606" if species == "human" else "10090"



    data_frame = {}

    file_list = glob.glob("reviewed/%s_*_*.csv" % (species))

    for in_file in file_list:
        file_name = os.path.basename(in_file)
        prefix = "_".join(file_name.split(".")[0].split("_")[2:])
        field_list = load_dataframe(data_frame, prefix, in_file, ",")
        value_list = {}
        main_id = field_list[0]
        for canon in data_frame[prefix]:
            for row_obj in data_frame[prefix][canon]:
                if main_id not in value_list:
                    value_list[main_id] = []
                value_list[main_id].append(canon)
                for field in field_list[1:]:
                    for v in row_obj[field]:
                        if field not in value_list:
                            value_list[field] = []
                        value_list[field].append(v)
        stat_buffer = "\tStatistics:\n"
        for field in field_list:
            stat_buffer += "\t%10s : %s\n" % (len(sorted(set(value_list[field]))), field)
        readme_file_one = "reviewed/%s" % (file_name[:-3]) + "readme.manual.txt"
        readme_file_two = "reviewed/%s" % (file_name[:-3]) + "readme.txt"

        if os.path.exists(readme_file_one) == False:
            continue

        readme_buffer = open(readme_file_one, "r").read()
        readme_buffer += stat_buffer
        with open(readme_file_two, "w") as FW:
            FW.write("%s\n" % (readme_buffer))
        print file_name






if __name__ == '__main__':
	main()
