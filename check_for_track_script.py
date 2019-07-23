import json
import requests
'''
The purpose of this script is to perform a simple check if the cruise ID from
user input has a track or not. (1) prompts the user in the terminal "What is your
cruise ID?" (2) once the user inputs a number either returns "Cruise ID: ### has
no cruise track" or "Cruise ID: ### has a cruise track"
'''

END_POINT = "https://cchdo.ucsd.edu/api/v1/cruise"
API_KEY = ""

def get_cruise_json():
    #requests all cruise info from END_POINT and creates dictionary of all cruise ids
    r = requests.get(END_POINT)
    cruise_dict = {cruise["id"]:cruise["expocode"] for cruise in r.json()['cruises']}
    return cruise_dict

def get_user_cruise(cruise_dict):
    user_cruise = input("What is your cruise ID (e.g. '1217')? \n")
    #check to make sure the cruise is a number and an existing cruise
    if (not user_cruise.isdigit()) and (user_cruise not in cruise_dict.values()):
        print("Please enter a valid cruise from https://cchdo.ucsd.edu/api/v1/cruise")
        quit()

    return user_cruise

def find_non_tracked(user_cruise):

    #requests json for cruise from user input and checks if track exists
    t = requests.get(END_POINT + "/" + str(user_cruise))
    cruise_object = t.json()
    cruise_track = cruise_object["geometry"]["track"]

    if len(cruise_track) == 0:
        print("Cruise ID: " + str(user_cruise) + " has no cruise track")

    else:
        print("Cruise ID: " + str(user_cruise) + " has a cruise track")


if __name__ == "__main__":

    r = ''
    cruise_dict = get_cruise_json()
    user_cruise = get_user_cruise(cruise_dict)
    no_tracks_output = find_non_tracked(user_cruise)
