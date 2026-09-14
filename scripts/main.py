#! /usr/bin/env python3

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import toml
import datetime
from geopy.geocoders import Nominatim


envPath = Path.home() / ".config" / "moonphase" / ".env"
envload = load_dotenv(envPath)
configPath = Path.home() / ".config" / "moonphase" / "config.toml"
tomlFile = toml.load(configPath)

# Fixes the issue of a empty .env location variable to ensure correct set and rise times
def enterConfigLocation():
    
    with open(configPath, 'a') as configFile:
        
        locKey = input("Please enter your city (Example: California) > ")
        
        configFile.write(f"location = '{locKey}'\n")



# Load .env and pull the Location key into variable.
def get_location():
    try:
        Locationkey = tomlFile['location']
        return Locationkey
    except:
        enterConfigLocation()
            

# Use the current date for current moon phase data
current_date = datetime.datetime.now()
date = current_date.strftime("%Y-%m-%d")

# Use geocoding to get the coordinates from the provided Location
geolocator = Nominatim(user_agent="MoonPhaseTracker")
Locationkey = get_location()

location = geolocator.geocode(Locationkey)
lat = location.latitude
lon = location.longitude

# Constant variables
APIurl = f"https://aa.usno.navy.mil/api/rstt/oneday?date={date} &coords={lat}, {lon}"

# Moon phase ascii file path
current_dir = Path(__file__).parent
moon_phase_dir = current_dir / "MoonFiles"


def check_last_run():
        
        lastrun = os.getenv("LastRun")
        
        if lastrun == date:
            return True
        else:
            return False


def log_last_run(moon_phase, moon_fracillum, rise_time, set_time):
    with open(envPath, 'w') as envFile:
        
        envFile.write(f"LastRun='{date}'\n")
        envFile.write(f"LastPhase='{moon_phase}'\n")
        envFile.write(f"LastFracillum='{moon_fracillum}'\n")
        envFile.write(f"LastRise='{rise_time}'\n")
        envFile.write(f"LastSet='{set_time}'\n")

def get_last_moon():

    lastphase = os.getenv("LastPhase")
    lastfracillum = os.getenv("LastFracillum")
    lastrise = os.getenv("LastRise")
    lastset = os.getenv("LastSet")
    
    return lastphase, lastfracillum, lastrise, lastset
    

# Fix json from being a string back into json for better data parsing
def fixJSON(json_str: str) -> dict:
    
    dict_json = json.loads(json_str)

    return dict_json




def outputinfo(moon_fracillum: str, moon_phase: str, moon_rise_time: str, moon_set_time: str) -> None:
    
    infoStr = f"""\n
    ┌Description─────────────────────────────┐
    │   Date: {date}                     │
    │   Current Moon Phase: {moon_phase}  │
    │   Moon Luminosity: {moon_fracillum}                 │
    │   Moonrise Time: {moon_rise_time}                 │
    │   Moonset Time: {moon_set_time}                  │
    └────────────────────────────────────────┘
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
    
    ran_today = check_last_run()
    if ran_today == True:
        moon_phase, moon_fracillum, mrt, mst = get_last_moon()
        moonselection(moon_phase.lower().replace(" ", "_"))
        outputinfo(moon_fracillum, moon_phase, mrt, mst)
    else:

        data = getrequest(lat, lon) 
        moon_phase, moon_fracillum, mrt, mst = parse_data(data)

        moonselection(moon_phase.lower().replace(" ", "_")) # Print the Moon phase Ascii first

        outputinfo(moon_fracillum, moon_phase, mrt, mst) # Finish by printing the data on the screen 
        
        log_last_run(moon_phase, moon_fracillum, mrt, mst)


