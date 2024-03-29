from iss_tracker import *
import unittest
from flask import Flask
from unittest.mock import MagicMock, patch

# Mock data for static functions
data = [{
        'EPOCH': '2024-049T12:00:00.000Z', 
        'X': {'@units': 'km', '#text': '-4796.4389037341698'}, 
        'Y': {'@units': 'km', '#text': '-4363.3713205600798'}, 
        'Z': {'@units': 'km', '#text': '2028.7075926579801'}, 
        'X_DOT': {'@units': 'km/s', '#text': '4.0'}, 
        'Y_DOT': {'@units': 'km/s', '#text': '-2.5'}, 
        'Z_DOT': {'@units': 'km/s', '#text': '5.5'}
        }, 
        {
        'EPOCH': '2024-054T00:20:00.000Z', 
        'X': {'@units': 'km', '#text': '-4896.5098728732'}, 
        'Y': {'@units': 'km', '#text': '-4000.6043300798'}, 
        'Z': {'@units': 'km', '#text': '2300.7075926579801'}, 
        'X_DOT': {'@units': 'km/s', '#text': '4.0'}, 
        'Y_DOT': {'@units': 'km/s', '#text': '-2.0'}, 
        'Z_DOT': {'@units': 'km/s', '#text': '7.0'}
        }, 
        {
        'EPOCH': '2024-62T12:00:00.000Z', 
        'X': {'@units': 'km', '#text': '-5006.209374282'}, 
        'Y': {'@units': 'km', '#text': '-4232.223231345'}, 
        'Z': {'@units': 'km', '#text': '2124.7075926579801'}, 
        'X_DOT': {'@units': 'km/s', '#text': '5'}, 
        'Y_DOT': {'@units': 'km/s', '#text': '-2.0'}, 
        'Z_DOT': {'@units': 'km/s', '#text': '6.0'}
        },

        {
        'EPOCH': '2024-62T12:00:00.000Z', 
        'X': {'@units': 'km', '#text': '-5006.209374282'}, 
        'Y': {'@units': 'km', '#text': '-4232.223231345'}, 
        'Z': {'@units': 'km', '#text': '2124.7075926579801'}, 
        'X_DOT': {'@units': 'km/s', '#text': '5'}, 
        'Y_DOT': {'@units': 'km/s', '#text': '-2.0'}, 
        'Z_DOT': {'@units': 'km/s', '#text': '6.0'}
        }
    ]

class TestGetStateVectorData(unittest.TestCase):
    @patch('requests.get')
    @patch('xmltodict.parse')
    def test_get_state_vector_data(self, mock_xmltodict_parse, mock_requests_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<ndm><oem><body><segment><data><stateVector><EPOCH>2024-059T13:04:00.000Z</EPOCH><X units="km">-1678.6226199341099</X><Y units="km">5429.50109555156</Y><Z units="km">-3727.33126342164</Z><X_DOT units="km/s">-6.25282193719364</X_DOT><Y_DOT units="km/s">1.0191494035819</Y_DOT><Z_DOT units="km/s">4.3033190811508302</Z_DOT></stateVector></data></segment></body></oem></ndm>'
        mock_requests_get.return_value = mock_response
       
        mock_xml_data = {
            'ndm': {
                'oem': {
                    'body': {
                        'segment': {
                            'data': {
                                'stateVector': [{
                                    "EPOCH": "2024-059T13:04:00.000Z",
                                    "X": {
                                        "@units": "km",
                                        "#text": "-1678.6226199341099"
                                    },
                                    "X_DOT": {
                                        "@units": "km/s",
                                        "#text": "-6.25282193719364"
                                    },
                                    "Y": {
                                        "@units": "km",
                                        "#text": "5429.50109555156"
                                    },
                                    "Y_DOT": {
                                        "@units": "km/s",
                                        "#text": "1.0191494035819"
                                    },
                                    "Z": {
                                        "@units": "km",
                                        "#text": "-3727.33126342164"
                                    },
                                    "Z_DOT": {
                                        "@units": "km/s",
                                        "#text": "4.3033190811508302"
                                    }
                                }]
                            }
                        }
                    }
                }
            }
        }

        mock_xmltodict_parse.return_value = mock_xml_data

        # Call the function with limit and offset
        result = getStateVectorData(limit=1, offset=0)

        # Assert that the function returns a list containing the state vector dictionary
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        expected_state_vector = {
            "EPOCH": "2024-059T13:04:00.000Z",
            "X": {
                "#text": "-1678.6226199341099",
                "@units": "km"
            },
            "X_DOT": {
                "#text": "-6.25282193719364",
                "@units": "km/s"
            },
            "Y": {
                "#text": "5429.50109555156",
                "@units": "km"
            },
            "Y_DOT": {
                "#text": "1.0191494035819",
                "@units": "km/s"
            },
            "Z": {
                "#text": "-3727.33126342164",
                "@units": "km"
            },
            "Z_DOT": {
                "#text": "4.3033190811508302",
                "@units": "km/s"
            }
        }
        
        self.assertDictEqual(result[0], expected_state_vector)

def test_getNowEpoch():
    """Function ensures it's extracting the epoch closest to current time"""
    latest_epoch = getNowEpoch(data)
    assert(latest_epoch == data[-1])

def test_calculateSpeed_1():
    """Function calculates speed from Cartesian Vectors when all of the speeds equal 0 km/s"""
    speed = calculateSpeed(0, 0, 0)
    assert(speed == 0)

def test_calculateSpeed_2():
    """Function calculates speed from Cartesian Vectors when the speeds are non 0 km/s"""
    speed = calculateSpeed(float(data[2]['X_DOT']['#text']), float(data[2]['Y_DOT']['#text']), float(data[2]['Z_DOT']['#text']))
    assert(speed == (math.sqrt(65)))

def test_calculateLocation_latitude():
    """Function tests latitude eqution"""
    location = calculateLocation(float(data[-1]['X']['#text']), float(data[-1]['Y']['#text']), float(data[-1]['Z']['#text']), data[-1]['EPOCH'])
    lat = location['Latitude [degrees]']
    expected_latitude = math.degrees(math.atan2(float(data[-1]['Z']['#text']), math.sqrt(float(data[-1]['X']['#text'])*float(data[-1]['X']['#text']) + float(data[-1]['Y']['#text'])*float(data[-1]['Y']['#text'])))) 
    assert(lat == round(expected_latitude,3))

def test_calculateLocation_longitude():
    """Function tests longitude equation"""
    dt_object = datetime.strptime(data[-1]['EPOCH'], '%Y-%jT%H:%M:%S.%fZ')

    hours = dt_object.hour
    minutes = dt_object.minute

    location = calculateLocation(float(data[-1]['X']['#text']), float(data[-1]['Y']['#text']), float(data[-1]['Z']['#text']), data[-1]['EPOCH'])
    longitude = location['Longitude [degrees]']
    
    expected_longitude = math.degrees(math.atan2(float(data[-1]['Y']['#text']), float(data[-1]['X']['#text']))) - ((hours - 12) + (minutes/60))*(360/24) + 19
    if expected_longitude > 180: 
        expected_longitude = -180 + (expected_longitude- 180)
    if expected_longitude < -180: 
        expected_longitude = 180 + (expected_longitude + 180)

    assert(longitude == round(expected_longitude,3))

def test_calculateLocation_altitude():
    """Function tests altitude equation"""
    location = calculateLocation(float(data[-1]['X']['#text']), float(data[-1]['Y']['#text']), float(data[-1]['Z']['#text']), data[-1]['EPOCH'])
    altitude = location['Altitude [km]']
    expected_altitude = math.sqrt(float(data[-1]['X']['#text'])*float(data[-1]['X']['#text']) + float(data[-1]['Y']['#text'])*float(data[-1]['Y']['#text']) + float(data[-1]['Z']['#text'])*float(data[-1]['Z']['#text'])) - 6371.0 
    assert(altitude == round(expected_altitude ,3)) 

class TestEpochRoute(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def get_epoch1(self) -> dict:
        """Function returns the first epoch in the data set for testing
        Returns:
            dict: Dictionry of first index in list of data returned
        """
        response = self.app.get('/epochs')
        data = response.get_json()
        first_epoch = data[0]
        return first_epoch
    
    def get_epoch2(self) -> dict:
        """Function returns the last epoch in the data set for testing
        Returns:
            dict: Dictionary of last index in the data returned
        """
        response = self.app.get('/epochs')
        data = response.get_json()
        last_epoch = data[-1]
        return last_epoch

    def get_epoch3(self) -> dict: 
        """Function returns the middle epoch in the data set for testing
        Returns:
            dict: Dictionary of middle index in the data returned
        """
        response = self.app.get('/epochs')
        data = response.get_json()
        index = (len(data) // 2)
        middle_epoch = data[index]
        return middle_epoch

    def test_epoch_available1(self):
        first_epoch = self.get_epoch1()
        # Send a GET request to the endpoint with a valid epoch
        utc_time = first_epoch['EPOCH']
        response = self.app.get(f'/epochs/{utc_time}')
        data = response.get_json()

        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the returned data matches the expected data
        expected_data = first_epoch
        
        self.assertEqual(data, expected_data)

    def test_epoch_available2(self):
        last_epoch = self.get_epoch2()
        # Send a GET request to the endpoint with a valid epoch
        utc_time = last_epoch['EPOCH']
        response = self.app.get(f'/epochs/{utc_time}')
        data = response.get_json()

        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the returned data matches the expected data
        expected_data = last_epoch
        
        self.assertEqual(data, expected_data)

    def test_epoch_available3(self):
        middle_epoch = self.get_epoch3()
        # Send a GET request to the endpoint with a valid epoch
        utc_time = middle_epoch['EPOCH']
        response = self.app.get(f'/epochs/{utc_time}')
        data = response.get_json()

        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the returned data matches the expected data
        expected_data = middle_epoch

        self.assertEqual(data, expected_data)

    def test_epoch_not_available(self):
        # Send a GET request to the endpoint with an invalid epoch
        response = self.app.get('/epochs/invalid_epoch')
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the response indicates the epoch is not available
        expected_response = "Epoch not available \n"
        self.assertEqual(response.data.decode('utf-8'), expected_response)

    # limit = int, offset = None
    def test_epoch_query1(self):
        # Send a GET request to the endpoint with an invalid epoch
        response = self.app.get('/epochs?limit=2')
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)

        expected_response_length = 2
        data = response.get_json()
        self.assertEqual(len(data), expected_response_length)

    # limit = 0, offset = None
    def test_epoch_query2(self):
        # Send a GET request to the endpoint with an invalid epoch
        response = self.app.get('/epochs?limit=0')
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)

        expected_response_length = 0
        data = response.get_json()
        self.assertEqual(len(data), expected_response_length)

    # limit = None, offset = 0
    def test_epoch_query3(self):
        response = self.app.get('/epochs')
        data = response.get_json()
        expected_response_length = len(data)

        # Send a GET request to the endpoint with an invalid epoch
        response = self.app.get('/epochs?offset=0')
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(len(data), expected_response_length)
   
    # limit = None, offset = Positive Integer
    def test_epoch_query4(self):
        response = self.app.get('/epochs')
        data = response.get_json()
        expected_response_length = len(data)

        # Send a GET request to the endpoint with an invalid epoch
        response = self.app.get('/epochs?offset=10')
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(len(data), expected_response_length - 10)

    # limit = None, offset = Large Negative Number (outputs entire data set)
    def test_epoch_query5(self):
        response = self.app.get('/epochs')
        data = response.get_json()
        expected_response_length = len(data)

        offset = expected_response_length + 100

        # Send a GET request to the endpoint with an invalid epoch
        response = self.app.get(f'/epochs?offset=-{offset}')
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(len(data), expected_response_length)

    # limit = Large Positive Number, offset = None
    def test_epoch_query6(self):
        response = self.app.get('/epochs')
        data = response.get_json()
        expected_response_length = len(data)
        large_limit = expected_response_length + 100

        # Send a GET request to the endpoint with an invalid epoch
        response = self.app.get(f'/epochs?limit={large_limit}')
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(len(data), expected_response_length)

    # limit != None, offset = None
    def test_epoch_query7(self):
        response = self.app.get('/epochs')
        data = response.get_json()

        # Send a GET request to the endpoint with an invalid epoch
        response = self.app.get(f'/epochs?limit=bx')
        expected_response = "Error: Limit must be an integer \n"
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)
        
        data = response.get_data(as_text=True)
        self.assertEqual(data, expected_response)

    # limit != Numeric, offset = Number
    def test_epoch_query8(self):
        response = self.app.get('/epochs')
        data = response.get_json()

        # Send a GET request to the endpoint with an invalid epoch
        response = self.app.get(f'/epochs?limit=bx&offset=1')
        expected_response = "Error: Limit must be an integer \n"
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)
        
        data = response.get_data(as_text=True)
        self.assertEqual(data, expected_response)

    # limit = Numeric, offset = Non Numeric
    def test_epoch_query9(self):
        response = self.app.get('/epochs')
        data = response.get_json()

        # Send a GET request to the endpoint with an invalid epoch
        response = self.app.get(f'/epochs?limit=5&offset=bx')
        expected_response = "Error: Offset must be an integer \n"
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)
        
        data = response.get_data(as_text=True)
        self.assertEqual(data, expected_response)

    def test_speed1(self):
        first_epoch = self.get_epoch1()
        # Send a GET request to the endpoint with a valid epoch
        utc_time = first_epoch['EPOCH']
        instantaneous_speed = round(calculateSpeed(float(first_epoch['X_DOT']['#text']), float(first_epoch['Y_DOT']['#text']), float(first_epoch['Z_DOT']['#text'])),3)
        expected_data = {"INSTANTANEOUS SPEED": {"#text": instantaneous_speed, "@units": "km/s"}}
        response = self.app.get(f'/epochs/{utc_time}/speed')
        data = response.get_json()
        self.assertEqual(data, expected_data)

    def test_speed2(self):
        response = self.app.get('/epochs/2022-067T09:46:00.000Z/speed')
        data = response.get_data(as_text=True)
        self.assertEqual(data, "Epoch not available \n")

    def test_header(self):
        response = self.app.get('/header')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)

    def test_metadata(self):
        response = self.app.get('/metadata')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)

    def test_comment(self):
        response = self.app.get("/comment")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, List)

    def test_now(self):
        response = self.app.get("/now")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        assert('Geoposition' in data)

    def test_location_1(self):
        response = self.app.get("/epochs/2022-067T09:46:00.000Z/location")
        self.assertEqual(response.status_code, 200)
        assert(response.get_data(as_text=True) == "Epoch not available \n")

if __name__ == '__main__':
    unittest.main()