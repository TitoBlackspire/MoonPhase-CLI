#! /usr/bin/env python3

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import datetime
from geopy.geocoders import Nominatim


config_path = Path.home() / ".config" / "moonphase" / ".env"

# Fixes the issue of a empty .env location variable to ensure correct set and rise times
def enterENV():
    

    envPath = Path(config_path)

    with open(envPath, 'w') as envFile:
        
        locKey = input("Please enter your city (Example: California) > ")
        
        envFile.write(f"Location='{locKey}'")

# Load .env and pull the Location key into variable.
envset = False
while envset == False:
    load_dotenv(config_path)
    Locationkey = os.getenv("Location")
    if Locationkey == None:
        enterENV()
        envset = False
    else:
        envset = True

# Use the current date for current moon phase data
current_date = datetime.datetime.now()
date = current_date.strftime("%Y-%m-%d")

# Use geocoding to get the coordinates from the provided Location
geolocator = Nominatim(user_agent="MoonPhaseTracker")
location = geolocator.geocode(Locationkey)
lat = location.latitude
lon = location.longitude

# Constant variables
APIurl = f"https://aa.usno.navy.mil/api/rstt/oneday?date={date} &coords={lat}, {lon}"

# Moon phase ascii file path
current_dir = Path(__file__).parent
moon_phase_dir = current_dir / "MoonFiles"


# Fix json from being a string back into json for better data parsing
def fixJSON(json_str: str) -> dict:
    
    dict_json = json.loads(json_str)

    return dict_json


def outputinfo(moon_fracillum: str, moon_phase: str, moon_rise_time: str, moon_set_time: str) -> None:
    
    infoStr = f"""\n
    Date: {date}

    Current Moon Phase: {moon_phase}

    Moon Luminosity: {moon_fracillum}

    Moonrise Time: {moon_rise_time}
    
    Moonset Time: {moon_set_time}
    """
    print(infoStr)


# Select the current ascii moon art to print
def moonselection(moon_phase: str) -> None:

    for phases in moon_phase_dir.iterdir():
        phases = str(phases)# Turn the possix type to string to use the .find() to match moon phase to ascii

        if phases.find(moon_phase) != -1:
            
            #print(phases)
            moon_phase_file = Path(phases)
            with open(moon_phase_file) as PhaseFile:
                print("\n", PhaseFile.read())
            break

        else:
            continue
        return


# Parse the usno api information 
def parse_data(parsable_json_data: dict) -> str:
    
    current_moon_phase = parsable_json_data["properties"]["data"]["curphase"]
    
    current_moon_fracillum = parsable_json_data["properties"]["data"]["fracillum"]
    
    # Extra information 
    moon_info_list = parsable_json_data["properties"]["data"]["moondata"]

    moon_rise_info = moon_info_list[1]
    moon_set_info = moon_info_list[0]

    moon_rise_time = moon_rise_info["time"]
    moon_set_time = moon_set_info["time"]

    return current_moon_phase, current_moon_fracillum, moon_rise_time, moon_set_time
    

# Call the aa.usno.navy.mil api
def getrequest(lat: float, lon: float) -> dict:
    
    ApiRequest = requests.get(APIurl)
    post = ApiRequest.json() 
    inital_json_str = json.dumps(post, indent=1)

    parsable_json_data = fixJSON(inital_json_str)
    
    return parsable_json_data

 
if __name__ == "__main__":
    


    data = getrequest(lat, lon) 
    moon_phase, moon_fracillum, mrt, mst = parse_data(data)

    moonselection(moon_phase.lower().replace(" ", "_")) # Print the Moon phase Ascii first

    outputinfo(moon_fracillum, moon_phase, mrt, mst) # Finish by printing the data on the screen 
