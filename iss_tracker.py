#!/usr/bin/env python3
from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
from datetime import datetime, timezone
from typing import List
import json
import logging
import math
import numpy as np
import requests
import xmltodict

DATA_SOURCE = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
EARTH_RADIUS = 6371.0  # km

# Initialize Nominatim API 
geolocator = Nominatim(user_agent="ISS_TRACKER")

app = Flask(__name__)

def getStateVectorData(limit=None, offset=None) -> List[dict]:
    """Function GETS ISS data from NASA Website and returns a list of epochs with the specified limit and offset. 
    Args:
        limit (int): The number of epochs the API should return no more than. 
        offset (int): The number of data points offset from the beginning. 
    Returns:
        List[dict]: List of state vector dictionaries that are filtered based on the provied limit and offset
    """
    r = requests.get(DATA_SOURCE)
    if (r.status_code == 200):
        logging.info("HTTP Request Successful")

        # Store XML data into a list of dictionaries
        xml_data = xmltodict.parse(r.text)
        state_vectors:list = xml_data['ndm']['oem']['body']['segment']['data']['stateVector']
        data = []

        # Each state vector lists the time in UTC; position X, Y, and Z in km; and velocity X, Y, and Z in km/s.
        for state_vector in state_vectors:           
            state_dict = {
                'EPOCH': state_vector['EPOCH'],
                'X': state_vector['X'],
                'Y': state_vector['Y'],
                'Z': state_vector['Z'],
                'X_DOT': state_vector['X_DOT'],
                'Y_DOT': state_vector['Y_DOT'],
                'Z_DOT': state_vector['Z_DOT'],
            }
            data.append(state_dict)

        # If limit is provided, the function takes a slice of state_vectors from offset to offset+limit. 
        # If only offset is provided, it takes a slice starting from offset to the end of the list. 
        # If neither limit nor offset is provided, it processes all state_vectors as before.

        if (limit is not None) and (str(limit).isnumeric()) and (int(limit) > len(data)):
            limit = None 

        if limit is None and offset is None: 
            # return entire data set
            return data
        
        if limit is None and offset is not None: 
            # return offset to end of data
            # last data point is inclusive
            return data[offset:]
        
        if limit > 0 and offset is None: 
            return data[0:limit]

        if limit > 0 and offset is not None: 
            return data[offset:offset + limit]

        if limit < 0:
            # return empty data set if limit is negative 
            return [{}]
    else:       
        logging.error(f"Bad HHTP Request {r.status_code}")
        return None

def getNowEpoch(data:List[dict]) -> dict:
    """Function finds the most up to date epoch compared to execution of program and prints data.
    Args:
        data (List[dict]): List of state vectore dictionaries
    Returns:
        dict: Dictionary containing epoch information closest to the time of the program's execution
    """
    now_utc = datetime.now(timezone.utc)
    formatted_now = now_utc.strftime("%Y-%jT%H:%M:%S.%fZ")
    min_diff = float('inf')
    stored_epoch = {}
    # Parse through data and find the epoch containing the data closest to current time
    for epoch in data: 
        epochTime = epoch['EPOCH']
        timestamp1 = datetime.strptime(formatted_now, "%Y-%jT%H:%M:%S.%fZ")
        timestamp2 = datetime.strptime(epochTime, "%Y-%jT%H:%M:%S.%fZ")
        time_diff = (timestamp1 - timestamp2).total_seconds()
        if (time_diff <= 0):
            break
        else:
            if(time_diff < min_diff):
                min_diff = time_diff
                stored_epoch = epoch
    return stored_epoch

def calculateSpeed(x_dot:float, y_dot: float, z_dot: float) -> float:
    """Function computes speed from cartesian velocity vectors
    Args:
        x_dot (float): Cartesian velocity vector in the x direction
        y_dot (float): Cartesian velocity vector in the y direction
        z_dot (float): Cartesian velocity vector in the z direction
    Returns:
        float: Vector speed
    """
    speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)
    return speed

def calculateLocation(x:float, y:float, z:float) -> dict:
    """Function calculates the geolocation of the ISS from 
        the x/y/z coordinates recorded with respect to the center of the earth. 
    Args:
        x (float): X coordinate of the ISS measured with respect to the center of the earth
        y (float): Y coordinate of the ISS measured with respect to the center of the earth
        z (float): Z coordinate of the ISS measured with respect to the center of the earth
    Returns:
        dict: Dcictionary containing geolocation details of the ISS
    """
    # Initialize geolocation attributes to None
    address = None
    city = None
    state = None
    country = None
    code = None

    # TODO FIX
    altitude = math.sqrt(x**2 + y**2 + z**2) - EARTH_RADIUS # km
    longitude = np.degrees(np.arctan2(y, x))                # degrees
    #latitude = np.degrees(np.arcsin(z/(EARTH_RADIUS + altitude)))
    latitude = np.degrees(np.arcsin(z/EARTH_RADIUS))        # degrees
    #latitude = np.degrees(np.arccos(z/math.sqrt(x**2 + y**2 + z**2)))        # degrees
    location_tuple_string = f"{latitude}, {longitude}"
    geoposition = geolocator.reverse(location_tuple_string)

    if geoposition is not None: 
        address = geoposition.raw['address']
        city = address.get('city', '')
        state = address.get('state', '')
        country = address.get('country', '')
        code = address.get('country_code')

    iss_location = {
        "Altitude [km]": round(altitude,3), 
        "Longitude [degrees]": round(longitude,3), 
        "Latitude [degrees]": round(latitude,3), 
        "Geoposition": {"City": city, "State": state, "Country": country, "Country Code": code}
        }
    
    return iss_location

# curl http://127.0.0.1:5000/epochs
# curl -X GET http://127.0.0.1:5000/epochs
# curl 'http://127.0.0.1:5000/epochs?limit=int&offset=int' (Must surround with quotes becuase & behaves strange on Linux CL)
@app.route("/epochs", methods=['GET'])
def epochs() -> List[dict]:
    """Function calls the StateVector() method to return the data given the limit and offset query parameters. 
    Returns:
        List[dict]: List of state vector dictionaries that are filtered based on the provied limit and offset
    """
    # Limit and Offset return None if nothing is passed 
    limit = request.args.get('limit', )
    offset = request.args.get('offset', )
    
    # limit = None, offset = None
    if limit is None and offset is None:
        return (getStateVectorData(limit, offset))
    
    # limit != None, offset = None
    if offset is None and limit is not None: 
        try:
            limit = int(limit)
            if limit == 0:
                return ([])
            return getStateVectorData(limit, offset)
        except ValueError: 
            return "Error: Limit must be an integer \n"
        
    if limit is None and offset is not None: 
        try:
            offset = int(offset)
            return getStateVectorData(limit, offset)
        except ValueError: 
            return "Error: Offset must be an integer \n"
    try:
        limit = int(limit)
        if limit == 0:
            return ([])
    except ValueError: 
        return "Error: Limit must be an integer \n"
    try:
        offset = int(offset)
    except ValueError: 
        return "Error: Offset must be an integer \n"
 
    return (getStateVectorData(limit, offset))

# curl http://127.0.0.1:5000/epochs/<epoch>
@app.route("/epochs/<epoch>", methods=['GET'])
def epoch(epoch:str) -> dict:
    """Function parses through entire data set and extracts the epoch of intreset
    Args:
        epoch (str): Datetime string for specific state vectors
    Returns:
        dict: State vector data of specific epoch
    """
    data = getStateVectorData()
    for entry in data:
        if (entry["EPOCH"] == epoch):
            return entry
    return "Epoch not available \n"

# curl http://127.0.0.1:5000/epochs/<epoch>/speed
@app.route("/epochs/<epoch>/speed", methods=['GET'])
def speed(epoch:str) -> dict:
    """Function returns instantaneous speed of a specific epoch in the data set
    Args:
        epoch (str): Datetime string for specific state vectors
    Returns:
        dict: Dictionary containing instantaneous speed information
    """
    data = getStateVectorData()
    for entry in data:
        if (entry["EPOCH"] == epoch):
            instantaneous_speed = round(calculateSpeed(float(entry['X_DOT']['#text']), float(entry['Y_DOT']['#text']), float(entry['Z_DOT']['#text'])),3)
            return({"INSTANTANEOUS SPEED": {"#text": instantaneous_speed, "@units": "km/s"}})       
    return "Epoch not available \n"

# curl http://127.0.0.1:5000/comment
@app.route("/comment", methods=['GET'])
def comment() -> list:
    """Function extracts the comment list object from the ISS data. 
    Returns:
        list: Formatted list of comment data from ISS
    """
    r = requests.get(DATA_SOURCE)
    if (r.status_code == 200):
        logging.info("HTTP Request Successful")
        xml_data = xmltodict.parse(r.text)
        comments:list = xml_data['ndm']['oem']['body']['segment']['data']['COMMENT']
        return(jsonify(comments))
    else:       
        logging.error(f"Bad HHTP Request {r.status_code}")
        return None

# curl http://127.0.0.1:5000/header
@app.route("/header", methods=['GET'])
def header() -> dict:
    """Function extracts the header from the ISS data. 
    Returns:
        dict: Dictionary of header information including information about creation date and originator. 
    """
    r = requests.get(DATA_SOURCE)
    if (r.status_code == 200):
        logging.info("HTTP Request Successful")
        xml_data = xmltodict.parse(r.text)
        header:dict = xml_data['ndm']['oem']['header']
        return header
    else:       
        logging.error(f"Bad HHTP Request {r.status_code}")
        return None

# curl http://127.0.0.1:5000/metadata
@app.route("/metadata", methods=['GET'])
def metadata() -> dict:
    """Function extracts the metadata about the ISS Data. 
    Returns:
        dict: Dictionary of metadata containing object name and id, center name, 
            reference frame, time system, etc.  
    """
    r = requests.get(DATA_SOURCE)
    if (r.status_code == 200):
        logging.info("HTTP Request Successful")
        xml_data = xmltodict.parse(r.text)
        metadata:dict = xml_data['ndm']['oem']['body']['segment']['metadata']
        return metadata
    else:       
        logging.error(f"Bad HHTP Request {r.status_code}")
        return None

# curl http://127.0.0.1:5000/epochs/<epoch>/location
@app.route("/epochs/<epoch>/location")  
def location(epoch:str) -> dict:
    """Function parses through entire data set and extracts the epoch of intreset 
            to return its altitude, longitude, altitude, and geoposition. 
        Args:
            epoch (str): Datetime string for specific state vectors
        Returns:
            dict:
    """
    data = getStateVectorData()
    for entry in data:
        if (entry["EPOCH"] == epoch):
            iss_location = calculateLocation(float(entry['X']['#text']), float(entry['Y']['#text']), float(entry['Z']['#text']))
            return iss_location
        
    return "Epoch not available \n"

# curl http://127.0.0.1:5000/now
@app.route("/now", methods=['GET'])
def now() -> dict:
    """Function resturns instantaneous speed, latitude, longitude, altitude, and 
    geoposition for the Epoch that is nearest in time
    Returns:
        dict: Dictionary containing data of ISS geoposition, speed, etc. 
    """
    data = getStateVectorData()
    now_epoch = getNowEpoch(data)
    instantaneous_speed = round(calculateSpeed(float(now_epoch['X_DOT']['#text']), float(now_epoch['Y_DOT']['#text']), float(now_epoch['Z_DOT']['#text'])), 3)
    iss_location = calculateLocation(float(now_epoch['X']['#text']), float(now_epoch['Y']['#text']), float(now_epoch['Z']['#text']))
    iss_data = iss_location
    iss_data["Instantaneous Speed [km/s]"] = instantaneous_speed
    return iss_data

# curl http://127.0.0.1:5000/now/time
@app.route("/now/time", methods=['GET'])
def nowTime() -> dict:
    """Function returns dictionary of current time and latest epoch time. 
        The time difference between the time stamps should never be greater than 4 minutes. 
    Returns:
        dict: Dictionary of current time and latest epoch time. 
    """
    now_utc = datetime.now(timezone.utc)
    formatted_now = now_utc.strftime("%Y-%jT%H:%M:%S.%fZ")
    
    data = getStateVectorData()
    now_epoch = getNowEpoch(data)

    times_dict = {
        "Current Time": formatted_now, 
        "Latest Epoch Time": now_epoch["EPOCH"]
    }
    return times_dict

if __name__ == "__main__":
    app.run(debug=True,  host='0.0.0.0')
