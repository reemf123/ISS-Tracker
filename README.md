## The ISS Tracker Flask Application
##### https://coe-332-sp24.readthedocs.io/en/latest/homework/midterm.html

##### Due Date 1: Friday, Mar 8, by 11:59 pm Central Time

### Project Description
We have found an abundance of interesting positional and velocity data for the International Space Station (ISS). Our goal is to create a Microservice/Web Application that allows users to query information about the ISS via an http request made in the browser or in the command line using `curl`. The goal is to design the microservice in a RESTful manner that will allow users of our application to intuitively seek the information they desire. 

### Project Objective 
The objective of this project is to transform our simple ISS Tracker into a full Flask Web Application. The primary aim is to create a web app capable of querying and retrieving interesting positional and velocity data from the International Space Station (ISS) dataset. The microservice will leverage HTTPS API Requests to ingest real-time data and provide users with insightful information about the ISS. Using Pytest, we will test our code, and finally, we will containerize the tool using Docker so that anyone may pull our application image and run the Flask service to obtain ISS data in a RESTful manner.

This project is important because it facilitates access to real-time ISS data in a user-friendly manner, enabling researchers, enthusiasts, and developers to gain valuable insights into the movement and dynamics of the International Space Station. For our development as students, deploying a web service teaches us how to write routes in a RESTful manner and help us understand how backend and frontend development work together to create a seamless tool that lives on the internet for users to interact with. 


### Software Diagram: 
The following software diagram captures the primary components and workflow of our system, describing the process in which a client may query for the NASA ISS data via a containerized web application developed through Flask.

![alt text](https://github.com/reemf123/ISS-Tracker/blob/main/softwareDiagram.png)

### Description of Folder Contents
- `Dockerfile`: Contains instructions for building a Docker image of our program
- `iss_tracker.py`: Main Python script that ingests the ISS data using the requests library, and stores it in a list-of-dictionaries. The script then defines a series of Flask routes: 
    - [GET] `/epochs`: Returns the entire data set
    - [GET] `/epochs?limit=int&offset=int`: Returns modified list of Epochs given query parameters
    - [GET] `/epochs/<epoch>`: Returns state vectors for a specific Epoch from the data set
    - [GET] `/epochs/<epoch>/speed`: Returns instantaneous speed for a specific Epoch in the data set 
    - [GET] `/now`: 
    - [GET]
    - [GET]
    - [GET]

- `test_iss_tracker.py`: The testing script for the iss_tracker.py. Ensures the robustness of our program. 
- `softwareDiagram.png`: Software diagram capturing as many components of the project as possible. 

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

- Example Command: `docker build -t reemf123/homework05:1.0 .`

To ensure the build was succesful, run `docker images`

### Instructions on How to Deploy Containerized Code as a Flask App
To create an instance of your image (a “container”), use the following command: `docker run --name "name-of-app" -d -p 5000:5000 <dockerhubusername>/<code>:<version>`

- Example Command: `docker run --name "iss-tracker-app" -d -p 5000:5000 reemf123/homework05:1.0`

The `-d` flag detaches your terminal from the running container - i.e. it runs the container in the background. The `-p` flag maps a port on the VM (5000, in the above case) to a port inside the container (again 5000, in the above case). 

To check to see if everything is up and running as expected, execute: `docker ps -a`. This should return a list with a container you named, an UP status, and the port mapping that you specified.

Once you have ensured that the microservice is up and running, you can access your application vial `curl` and by specifying the port. 

Example Commands to Execute Routes in Container (See Details about Routes Below):
- `curl localhost:5000/epochs`
- `curl 'localhost:5000/epochs?limit=<int>&offset=<int>'`
- `curl localhost:5000/now`
- `curl localhost:5000/epochs/<epoch>`
- `curl localhost:5000/epochs/<epoch>/speed`

### Instructions to Stop Microservice 
To stop your running container and remove it execute: 
- `docker stop <containerId>`
- `docker remove <containerId>`

### Instructions to Run the Containerized Unit Tests
To call a container, `docker run` is used. To execute all of the unit tests written inside the application, pytest is called before the file name containing the unit tests: `docker run --rm <username>/<imagename>:<tag> full/path/to/pytest -vv <path_to_unit_test_in_container>.py`

- Example Command: `docker run --rm reemf123/homework05:1.0 /usr/local/bin/pytest -vv /app/test_iss_tracker.py`

### Instructions For Accessing Web App Routes & Route Output Descriptions
- General Curl Command: `curl -X METHOD [URL Example Domain]`

* Note: All of our Flask Routes support only the `GET` Method. The default curl command is the `GET` method, so it is not required we include `-X` in our commands. 
    - `curl [URL Example Domain]` is equivalent to `curl -X GET [URL Example Domain]`

* Note: You may only run these commands after you have started up the Flask App. 

#### Curl Commands to Routes: `curl http://<ipaddress>:port/route`
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
- `curl 'http://127.0.0.1:5000/epochs?limit=int&offset=int'`: Returns a modified list of epochs from the given query parameters. For example, if `limit=2` and `offset=1`, the second and third epoch from the data set (starting from the begginning) will be outputted. For `curl` commands with query parameters, make sure to include the outer quotes surrounding the command, otherwise the output will be unexpected and incorrect.     
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
    "#text": 7.662329220562253,
    "@units": "km/s"
  }
}
```

- `curl http://127.0.0.1:5000/now`: Returns dictionary of state vectors including instantaneous speed for the epoch that is nearest in time to the program execution. This gives us live data about the ISS behavior. 

```
{
  "EPOCH": "2024-054T04:52:00.000Z",
  "INSTANTANEOUS SPEED": {
        "#text": "7.664763151239193",
        "@units": "km/s"
  },
  "X": {
        "#text": "-6555.0513218720598",
        "@units": "km"
  },
  "X_DOT": {
        "#text": "1.2477367460557001",
        "@units": "km/s"
  },
  "Y": {
        "#text": "353.72055802057002",
        "@units": "km"
  },
  "Y_DOT": {
        "#text": "-4.9904725825196596",
        "@units": "km/s"
  },
  "Z": {
        "#text": "1743.0219630343299",
        "@units": "km"
  },
  "Z_DOT": {
        "#text": "5.6821589717515",
        "@units": "km/s"
  }
}
```