import json
import requests
import pandas as pd
import numpy as np
from zipfile import ZipFile

'''
The purpose of this script is to create nav files in .txt format for all
BOTTLE DATASET cruises that have no track but have files to obtain LATITUDE and
LONGITUDE. This .txt can later patched and curled to cchdo.ucsd.edu to update
the track.
    Steps:
    (1) create dict of all CCHDO cruise IDs, grab the json
    (2) loop thru dict, make a list of cruises with no tracks *that have files*
    (3) loop thru list of non-tracked, for each cruise locate the file with data
        type BOTTLE containing the .csv with nav info
    (4) read .csv file and extract LATITUDE and LONGITUDE columns from .csv and
        write to a .txt navfile titled with the cruise expocode
'''

url = "https://cchdo.ucsd.edu"
END_POINT = "https://cchdo.ucsd.edu/api/v1/"
END_POINT_CRUISE = "https://cchdo.ucsd.edu/api/v1/cruise/"
API_KEY = ""

def get_cruise_ids():
    #(1) requests all cruise info and creates dictionary of all cruise ids
    r = requests.get(END_POINT + "cruise")
    cruise_dict = {cruise["id"]:cruise["expocode"] for cruise in r.json()['cruises']}

    return cruise_dict

def find_non_tracked_with_files(cruise_dict):
    #(2) get json for each cruise and make list of non-tracked w/files
    # ignore cruises with no tracks and no files
    no_tracks_list = []
    for key in cruise_dict:
        s = requests.get(END_POINT_CRUISE + str(key))
        cruise_object = s.json()

        t = requests.get(END_POINT_CRUISE + str(key) + "/files")
        cruise_all_files = t.json()

        cruise_track = cruise_object["geometry"]["track"]
        cruise_files = cruise_all_files["files"]

        if len(cruise_track) == 0 and len(cruise_files) != 0:
            # list of IDs of all cruises with tracks and with files
            no_tracks_list.append((key))

    return no_tracks_list

def get_info_for_non_tracked(no_tracks_list):
    #(3) obtaining json and files for each nontracked cruise
    for track in no_tracks_list:

        x = requests.get(END_POINT_CRUISE + str(track))
        y = requests.get(END_POINT_CRUISE + str(track) + "/files")

        cruise_object = x.json()
        cruise_files = y.json()

        cruise_expocode = cruise_object["expocode"]

        files_list = cruise_files["files"]

        for key in files_list:
            #example: https://cchdo.ucsd.edu/api/v1/file/5287
            #(4) get data type, role, and path for each file

            z = requests.get(END_POINT + "file/" + str(key))
            indiv_file_data = z.json()

            cruise_role = indiv_file_data["role"]
            cruise_data_type = indiv_file_data["data_type"]
            cruise_file_path = indiv_file_data["file_path"]
            cruise_file_type = indiv_file_data["file_type"]

            # for csv
            #cruise_file_name = indiv_file_data["file_name"]

            #(5) get LAT and LONG and write to .txt file with title of expocode
            if (cruise_role == "dataset") and (cruise_data_type == "bottle") and (cruise_file_type == "text/csv"):

                cruise_csv_url = url + cruise_file_path
                fields = ['LONGITUDE', 'LATITUDE']
                lat_long_data = pd.read_csv(cruise_csv_url,
                                            skiprows = 1,
                                            comment = '#',
                                            usecols = fields)
                #replace all blanks with NaN, drop all NaN values
                lat_long_data.replace('', np.nan, inplace = True)
                lat_long_data.dropna(inplace=True)

                lat_long_data.to_csv(cruise_expocode + "_nav.txt",
                                    header=False,
                                    index=False,
                                    sep='\t',
                                    mode='w')

if __name__ == "__main__":

    cruise_dict = get_cruise_ids()
    no_tracks_list = find_non_tracked_with_files(cruise_dict)
    lat_long_data = get_info_for_non_tracked(no_tracks_list)
