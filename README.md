## The ISS Tracker Flask Application
##### https://coe-332-sp24.readthedocs.io/en/latest/homework/midterm.html

##### Due Date 1: Friday, Mar 8, by 11:59 pm Central Time

### Project Description
We have found an abundance of interesting positional and velocity data for the International Space Station (ISS). Our goal is to create a Microservice/Web Application that allows users to query information about the ISS via an HTTP request made in the browser or in the command line using `curl`. The goal is to design the microservice in a RESTful manner that will allow users of our application to intuitively seek the information they desire. 

### Project Objective 
The objective of this project is to transform our simple ISS Tracker into a full Flask Web Application. The primary aim is to create a web app capable of querying and retrieving interesting positional and velocity data from the International Space Station (ISS) dataset.Our microservice will leverage HTTPS API Requests to ingest real-time data and provide users with insightful information about the ISS. The information we are presenting are similar to the following applications: 

- 1. https://www.n2yo.com/?s=90027
- 2. http://api.open-notify.org/iss-now.json

Using Pytest, we will test our code, and finally, we will containerize the tool using Docker so that anyone may pull our application image and run the Flask service to obtain ISS data in a RESTful manner.

This project is important because it facilitates access to real-time ISS data in a user-friendly manner, enabling researchers, enthusiasts, and developers to gain valuable insights into the movement and dynamics of the International Space Station. For our development as students, deploying a web service teaches us how to write routes in a RESTful manner and helps us understand how backend and frontend development work together to create a seamless tool that lives on the internet for users to interact with. 

### Software Diagram: 
The following software diagram captures the primary components and workflow of our system, describing the process in which a client may query for the NASA ISS data via a containerized web application developed through Flask.

![alt text](https://github.com/reemf123/ISS-Tracker/blob/main/softwareDiagram.png)

### Description of Folder Contents
- `Dockerfile`: Contains instructions for building a Docker image of our program
- `iss_tracker.py`: Main Python script that ingests the ISS data using the requests library, and stores it in a list-of-dictionaries. The script then defines a series of Flask routes: 
    - [GET] `/comment`: Returns ‘comment’ list object from ISS data
    - [GET] `header`: Returns ‘header’ dict object from ISS data
    - [GET] `metadata`: Returns ‘metadata’ dict object from ISS data
    - [GET] `/epochs`: Returns the entire data set
    - [GET] `/epochs?limit=int&offset=int`: Returns modified list of Epochs given query parameters
    - [GET] `/epochs/<epoch>`: Returns state vectors for a specific Epoch from the data set
    - [GET] `/epochs/<epoch>/speed`: Returns instantaneous speed for a specific Epoch in the data set 
    - [GET] `/epochs/<epoch>/location`: Returns latitude, longitude, altitude, and geo-position for a specific Epoch in the data set 
    - [GET] `/now`: Returns instantaneous speed, latitude, longitude, altitude, and geo-position for the Epoch that is nearest in time
    - [GET] `/now/time`: Returns current time and latest epoch time of ISS. The time difference between the time stamps should never be greater than 4 minutes. 

- `test/test_iss_tracker.py`: The testing script for the iss_tracker.py. Ensures the robustness of our program. 
- `softwareDiagram.png`: Software diagram capturing the primary components of the project architecture. 
- `docker-compose.yml`: YAML file used to replace running `docker run` commands. 
- `requirements.txt`: Text file that lists all of the python non standard libraries used to develop the code. 

The repository assumes installation of Docker. 

### Data
Our project ingests the ISS Data via an API GET request that can be accessed either in the form of .xml or .text. 

The ISS data is hosted at the following link: https://spotthestation.nasa.gov/trajectory_data.cfm

The ISS Trajectory Data Contains information on: 
- ISS mass in kg, Drag area in m2, Drag coefficient used in generating the ephemeris. The header also contains lines with details for the first and last ascending nodes within the ephemeris span. Following this is a listing of upcoming ISS translation maneuvers, called “reboosts,” and visiting vehicle launches, arrivals, and departures.

- The information our script utilizes are the state vectors which comes after the header. Each state vector is generated at 4 minute intervals for a total of 15 days. 

- State Vectors include the following metrics utilized by our script: 
    - Time in UTC
    - Position X, Y, and Z in km
    - Velocity X, Y, and Z in km/s

### Instructions on How to Build a Container
Once the homework5 repository has been pulled and you have iss_tracker.py, test_iss_tracker.py, and Dockerfile in the same directory, you build an image of the program with the following command: `docker build -t <dockerhubusername>/<code>:<version> .`

- Example Command: `docker build -t reemf123/iss_tracker:1.0 .`

To ensure the build was succesful, run `docker images`

### Instructions for Deploying Flask Application
To create an instance of your image (a “container”), use the following command: `docker run --name "name-of-app" -d -p 5000:5000 <dockerhubusername>/<code>:<version>`

- Example Command: `docker run --name "iss-tracker-app" -d -p 5000:5000 reemf123/iss_tracker:1.0`

The `-d` flag detaches your terminal from the running container - i.e. it runs the container in the background. The `-p` flag maps a port on the VM (5000, in the above case) to a port inside the container (again 5000, in the above case). 

To check to see if everything is up and running as expected, execute: `docker ps -a`. This should return a list with a container you named, an UP status, and the port mapping that you specified.

### Instructions for Deploying Flask Application with Docker Compose File
Docker compose files are an alternative means/method to execute `docker run` commands, especially critical for multi container Docker Applications. So, after building the image, instead of executing the `docker run` commands detailed above, the YAML file is used to configure the service, then with a single command, you can start up the container from the specifications detailed in the YAML file. 

The general commands are as follows: `docker-compose <verb> <parameters>`

To run the Flask application container, execute: `docker-compose up`

To check to see if everything is up and running as expected, execute: `docker ps -a`. This should return a list with a container you named, an UP status, and the port mapping that you specified in the `docker-compose.yml`.

Once you have ensured that the microservice is up and running, you can access your application vial `curl` and by specifying the port. 

#### Example Commands to Execute in Running Container (See Details about Routes Below):
- `curl localhost:5000/comment`
- `curl localhost:5000/epochs`
- `curl 'localhost:5000/epochs?limit=<int>&offset=<int>'`
- `curl localhost:5000/epochs/<epoch>`
- `curl localhost:5000/epochs/<epoch>/speed`
- `curl localhost:5000/epochs/<epoch>/location`
- `curl localhost:5000/header`
- `curl localhost:5000/metadata`
- `curl localhost:5000/now`
- `curl localhost:5000/now/time`

### Instructions to Run the Containerized Unit Tests
To call a container, `docker run` is used. To execute all of the unit tests written inside the application, pytest is called before the file name containing the unit tests: `docker run --rm <username>/<imagename>:<tag> full/path/to/pytest -vv <path_to_unit_test_in_container>.py`

- Example Command: `docker run --rm reemf123/iss_tracker:1.0 /usr/local/bin/pytest -vv /app/test_iss_tracker.py`

### Instructions For Accessing Web App Routes & Route Output Descriptions
- General Curl Command: `curl -X METHOD [URL Example Domain]`

* Note: All of our Flask Routes support only the `GET` Method. The default curl command is the `GET` method, so it is not required we include `-X` in our commands. 
    - `curl [URL Example Domain]` is equivalent to `curl -X GET [URL Example Domain]`

* Note: You may only run these commands after you have started up the Flask App. 

#### Curl Commands to Routes: `curl http://<ipaddress>:port/route`
- `curl http://127.0.0.1:5000/comment`: Returns the comment list object from the ISS data containing data about the ISS mass, drag area and coefficient, trajectory summary, etc.
```
[
  "Units are in kg and m^2",
  "MASS=459325.00",
  "DRAG_AREA=2040.50",
  "DRAG_COEFF=1.90",
  "SOLAR_RAD_AREA=0.00",
  "SOLAR_RAD_COEFF=0.00",
  "Orbits start at the ascending node epoch",
  "ISS first asc. node: EPOCH = 2024-02-28T13:15:27.792 $ ORBIT = 154 $ LAN(DEG) = 141.98244",
  "ISS last asc. node : EPOCH = 2024-03-14T10:46:57.262 $ ORBIT = 385 $ LAN(DEG) = 90.66259",
  "Begin sequence of events",
  "TRAJECTORY EVENT SUMMARY:",
  null,
  "|       EVENT        |       TIG        | ORB |   DV    |   HA    |   HP    |",
  "|                    |       GMT        |     |   M/S   |   KM    |   KM    |",
  "|                    |                  |     |  (F/S)  |  (NM)   |  (NM)   |",
  "=============================================================================",
  "Crew-8 Launch         061:05:04:27.000             0.0     421.9     414.0",
  "(0.0)   (227.8)   (223.5)",
  null,
  "Crew-8 Docking        062:11:40:05.000             0.0     422.0     413.6",
  "(0.0)   (227.9)   (223.3)",
  null,
  "Crew-7 Undock         068:15:00:00.000             0.0     423.4     411.2",
  "(0.0)   (228.6)   (222.0)",
  null,
  "GMT073 Reboost Preli  073:13:59:00.000             1.5     424.2     409.5",
  "(4.9)   (229.0)   (221.1)",
  null,
  "SpX-30 Launch         074:00:00:00.000             0.0     424.2     414.6",
  "(0.0)   (229.1)   (223.9)",
  null,
  "=============================================================================",
  "End sequence of events"
]
```

- `curl http://127.0.0.1:5000/epochs`: Returns a list of epoch dictionaries for the entire data set. 
    ```
    [   .
        .
        {
            "EPOCH": "2024-067T09:38:00.000Z",
            "X": {
                "#text": "4301.1373581658299",
                "@units": "km"
            },
            "X_DOT": {
                "#text": "0.02487856790891",
                "@units": "km/s"
            },
            "Y": {
                "#text": "-1121.11993906776",
                "@units": "km"
            },
            "Y_DOT": {
                "#text": "7.48166882078805",
                "@units": "km/s"
            },
            "Z": {
                "#text": "-5145.6209145734201",
                "@units": "km"
            },
            "Z_DOT": {
                "#text": "-1.60408889911693",
                "@units": "km/s"
        }
    },
    {
            "EPOCH": "2024-067T09:42:00.000Z",
            "X": {
                "#text": "4151.3383117815602",
                "@units": "km"
            },
            "X_DOT": {
                "#text": "-1.26564183653822",
                "@units": "km/s"
            },
            "Y": {
                "#text": "693.34512702751499",
                "@units": "km"
            },
            "Y_DOT": {
                "#text": "7.5469731894896199",
                "@units": "km/s"
            },
            "Z": {
                "#text": "-5339.1341460376898",
                "@units": "km"
            },
            "Z_DOT": {
                "#text": "0.0013396483748499999",
                "@units": "km/s"
        }
    },
    {
            "EPOCH": "2024-067T09:46:00.000Z",
            "X": {
                "#text": "3700.9359029226498",
                "@units": "km"
            },
            "X_DOT": {
                "#text": "-2.4650399567150201",
                "@units": "km/s"
            },
            "Y": {
                "#text": "2457.5911507043502",
                "@units": "km"
            },
            "Y_DOT": {
                "#text": "7.0656199928161696",
                "@units": "km/s"
            },
            "Z": {
                "#text": "-5144.9297659281201",
                "@units": "km"
            },
            "Z_DOT": {
                "#text": "1.60736275415027",
                "@units": "km/s"
        }
    }
    ]
    ```
    
- `curl 'http://127.0.0.1:5000/epochs?limit=int&offset=int'`: Returns a modified list of epochs from the given query parameters. For example, if `limit=2` and `offset=1`, the second and third epoch from the data set (starting from the beginning) will be outputted. For `curl` commands with query parameters, make sure to include the outer quotes surrounding the command, otherwise the output will be unexpected and incorrect.     
```
[
  {
    "EPOCH": "2024-052T12:04:00.000Z",
    "X": {
        "#text": "3255.40408593245",
        "@units": "km"
    },
    "X_DOT": {
        "#text": "-6.6815260318011402",
        "@units": "km/s"
    },
    "Y": {
        "#text": "3477.7470817142398",
        "@units": "km"
    },
    "Y_DOT": {
        "#text": "2.7795716496999399",
        "@units": "km/s"
    },
    "Z": {
        "#text": "-4849.4419619836599",
        "@units": "km"
    },
    "Z_DOT": {
        "#text": "-2.4918182140635001",
        "@units": "km/s"
    }
  },
  {
    "EPOCH": "2024-052T12:08:00.000Z",
    "X": {
        "#text": "1553.2933215427799",
        "@units": "km"
    },
    "X_DOT": {
        "#text": "-7.41636649187486",
        "@units": "km/s"
    },
    "Y": {
        "#text": "4010.7468991515598",
        "@units": "km"
    },
    "Y_DOT": {
        "#text": "1.63519793497544",
        "@units": "km/s"
    },
    "Z": {
        "#text": "-5263.9972699270802",
        "@units": "km"
    },
    "Z_DOT": {
        "#text": "-0.94189768208915003",
        "@units": "km/s"
    }
  }
]
```

- `curl http://127.0.0.1:5000/epochs/<epoch>`: Returns state vectors for a specific epoch from the data set. A valid epoch datetime string must be passed.  
Example Command: `curl http://127.0.0.1:5000/epochs/2024-054T04:44:00.000Z`
```
{
  "EPOCH": "2024-054T04:44:00.000Z",
  "X": {
        "#text": "-6186.9278788157999",
        "@units": "km"
  },
  "X_DOT": {
        "#text": "-2.7433789078264001",
        "@units": "km/s"
  },
  "Y": {
        "#text": "2583.1243682588401",
        "@units": "km"
  },
  "Y_DOT": {
        "#text": "-4.0707045573474598",
        "@units": "km/s"
  },
  "Z": {
        "#text": "-1102.81718021652",
        "@units": "km"
  },
  "Z_DOT": {
        "#text": "5.8834110564506696",
        "@units": "km/s"
  }
}
```

- `curl http://127.0.0.1:5000/epochs/<epoch>/speed`: Returns the instantaneous speed for a specific epoch in the data set in the form of a JSON dictionary. 
Example Command: `curl http://127.0.0.1:5000/epochs/2024-054T04:44:00.000Z/speed` 
```
{
  "INSTANTANEOUS SPEED": {
    "#text": 7.662,
    "@units": "km/s"
  }
}
```

- `curl http://127.0.0.1:5000/epochs/<epoch>/location`: Returns latitude, longitude, altitude, and geoposition for a specific epoch in the data set. 
```
{
  "Altitude [km]": 421.819,
  "Current Time": "2024-065T04:31:04.648Z",
  "Epoch Time": "2024-065T04:24:00.000Z",
  "Geoposition": {
    "City": "",
    "Country": "Switzerland",
    "Country Code": "ch",
    "State": ""
  },
  "Latitude [degrees]": 46.64,
  "Longitude [degrees]": 6.866
}
```

- `curl http://127.0.0.1:5000/header`: Returns header of ISS data containing creation date and originator. 
```
{
  "CREATION_DATE": "2024-060T17:42:17.631Z",
  "ORIGINATOR": "JSC"
}
```

- `curl http://127.0.0.1:5000/metadata`: Returns metadata about the ISS data including start/stop time, object name/id, etc. 

```
{
    "CENTER_NAME": "EARTH",
    "OBJECT_ID": "1998-067-A",
    "OBJECT_NAME": "ISS",
    "REF_FRAME": "EME2000",
    "START_TIME": "2024-059T12:00:00.000Z",
    "STOP_TIME": "2024-074T12:00:00.000Z",
    "TIME_SYSTEM": "UTC"
}
```

- `curl http://127.0.0.1:5000/now`: Returns instantaneous speed, latitude, longitude, altitude, and geoposition for the Epoch that is nearest in time. This gives us live data about the ISS behavior. 
```
{
    "Altitude [km]": 419.517,
    "Current Time": "2024-065T04:09:25.035Z",
    "Epoch Time": "2024-065T04:08:00.000Z",
    "Geoposition": {
        "City": "",
        "Country": "United States",
        "Country Code": "us",
        "State": "Virginia"
    },
    "Instantaneous Speed [km/s]": 7.664,
    "Latitude [degrees]": 37.044,
    "Longitude [degrees]": -75.935
}
```

The current iteration of our Web Application lacks the capability to decode geolocations for bodies of water. As a result, when the International Space Station (ISS) passes over a lake, river, ocean, or sea, the geoposition data appears as follows:

```
{
  "Altitude [km]": 420.415,
  "Current Time": "2024-066T00:09:01.278Z",
  "Epoch Time": "2024-066T00:08:00.000Z",
  "Geoposition": "No Location Data for the ISS at the moment",
  "Instantaneous Speed [km/s]": 7.666,
  "Latitude [degrees]": 17.142,
  "Longitude [degrees]": -42.499
}
```

- `curl http://127.0.0.1:5000/now/time`: Returns the time of the route execution and the latest epoch in the  ISS data set. 
```
{
  "Current Time": "2024-062T23:14:53.745Z",
  "Latest Epoch Time": "2024-062T23:12:05.000Z"
}
```

### Instructions to Stop Microservice 
To stop your running container and remove it execute: 
- `docker stop <containerId>`
- `docker remove <containerId>`

If you used `docker-compose` to start the container, you may execute `docker-compose down` to stop and remove the container. 