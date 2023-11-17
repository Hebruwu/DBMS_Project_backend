# FLASK Application

1) Request for get_admin_details for admin having username test:

GET http://127.0.0.1:5000/eventhosting/admins/admin_details/test

Response:
```
{
  "AID": 1,
  "EMAIL": "test",
  "NAME": "test",
  "USERNAME": "test"
}
```

2) Request for get_student_details for student having username judith77:

GET http://127.0.0.1:5000/eventhosting/students/student_details/judith77

Response: 

```
{
  "CITIZENSHIP": "New Zealand",
  "DEPARTMENT": "",
  "EMAIL": "judith77@vt.edu",
  "GENDER": "O",
  "MAJOR": "Creative Technologies",
  "NAME": "Katherine Burns",
  "RACE": "Black or African American",
  "SID": 1,
  "USERNAME": "judith77",
  "YEAR": "Junior\r"
}
```

3) Authenticate Student

Request:
GET http://127.0.0.1:5000/eventhosting/students/authenticate
headers:
Content-Type: application/json
Body:

```
{
    "username": "test",
    "password": "test"
}
```

Response:
If Authentication Suceeded HTTP Status Code -> 200
If Authentication Failed HTTP Status Code -> 401
If Exception HTTP Status Code -> 500

4) Authenticate Admin

Request:
GET http://127.0.0.1:5000/eventhosting/admins/authenticate
headers:
Content-Type: application/json
Body:

```
{
    "username": "test",
    "password": "test"
}
```

Response:
If Authentication Suceeded HTTP Status Code -> 200
If Authentication Failed HTTP Status Code -> 401
If Exception HTTP Status Code -> 500

5) Create Event

POST http://127.0.0.1:5000/eventhosting/events/create

headers: 
Content-Type: application/json

Body: 

```
{
    "name": "test",
    "type": "test",
    "date_from": "2011-10-10T14:48:00.000-04:00",
    "date_to": "2011-11-10T14:48:00.000-04:00",
    "modality": "test",
    "location": "test",
    "aid": 1,
    "description" : "can be omnitted/nullable"
}
```

Response:
Success
HTTP 200 OK
Failure
HTTP 400 BAD REQUEST

5) Create Student

POST http://127.0.0.1:5000/eventhosting/students/create

headers: 
Content-Type: application/json

Body: 

```
{
    "name": "test",
    "username": "teststudent",
    "password": "test",
    "email": "test",
    "race": "can_be_omnitted",
    "department": "can_be_omnitted",
    "major": "can_be_omnitted",
    "citizenship": "test",
    "year": "can_be_omnitted",
    "gender": "O"
}
```

Response:
Success
HTTP 200 OK
Failure
HTTP 400 BAD REQUEST

6) Get Several Students Details Based On Filters

GET http://127.0.0.1:5000/eventhosting/students/students_details

headers: 
Content-Type: application/json

Example Body: 

```
{
   "citizenships": ["Kuwait", "Switzerland"],
   "genders": ["F"]
}
```

Response:

```
[
    {
        "CITIZENSHIP": "Kuwait",
        "DEPARTMENT": "",
        "EMAIL": "udavis@vt.edu",
        "GENDER": "F",
        "MAJOR": "German",
        "NAME": "Sara Wallace",
        "RACE": "Native Hawaiian or Other Pacific Islander",
        "SID": 2,
        "USERNAME": "udavis",
        "YEAR": "Senior\r"
    },
    {
        "CITIZENSHIP": "Switzerland",
        "DEPARTMENT": "",
        "EMAIL": "smithbrandon@vt.edu",
        "GENDER": "F",
        "MAJOR": "Creative Technologies",
        "NAME": "Kathleen Turner",
        "RACE": "White",
        "SID": 51,
        "USERNAME": "smithbrandon",
        "YEAR": "Freshman\r"
    },
    {
        "CITIZENSHIP": "Switzerland",
        "DEPARTMENT": "",
        "EMAIL": "melissajohnson@vt.edu",
        "GENDER": "F",
        "MAJOR": "Finance",
        "NAME": "Paul Mcneil",
        "RACE": "Hispanic or Latino",
        "SID": 131,
        "USERNAME": "melissajohnson",
        "YEAR": "Senior\r"
    }
]
```
HTTP 200 OK for Success else HTTP 400

7) Get list of events

GET http://127.0.0.1:5000/eventhosting/events/events_details

Response:

```
[
    {
        "DATE_FROM": "Sun, 12 Nov 2023 12:40:38 GMT",
        "DATE_TO": "Sun, 12 Nov 2023 12:40:38 GMT",
        "DESCRIPTION": "test",
        "EID": 4,
        "EVENT_TYPE": "research",
        "E_AID": 1,
        "LOCATION": "now",
        "MODALITY": "online",
        "NAME": "test_event"
    },
    {
        "DATE_FROM": "Sun, 12 Nov 2023 12:41:31 GMT",
        "DATE_TO": "Sun, 12 Nov 2023 12:41:31 GMT",
        "DESCRIPTION": "test",
        "EID": 6,
        "EVENT_TYPE": "research",
        "E_AID": 1,
        "LOCATION": "now",
        "MODALITY": "online",
        "NAME": "testevent"
    },
    {
        "DATE_FROM": "Sun, 12 Nov 2023 12:41:51 GMT",
        "DATE_TO": "Sun, 12 Nov 2023 12:41:51 GMT",
        "DESCRIPTION": "test",
        "EID": 7,
        "EVENT_TYPE": "research",
        "E_AID": 1,
        "LOCATION": "now",
        "MODALITY": "online",
        "NAME": "testevent"
    }
]
```

HTTP 200 if Success else HTTP 400

8) Create An Invite

POST http://127.0.0.1:5000/eventhosting/events/create/invite
headers: 
Content-Type: application/json

Example Body: 

```
{
    "eid": 4,
    "sid": 1
}
```

HTTP 200 if Success else HTTP 400

9) Add Attending Details To An Invite

PUT http://127.0.0.1:5000/eventhosting/events/modify/invite
headers: 
Content-Type: application/json

Example Body: 

```
{
    "eid": 4,
    "username": "judith77",
    "attending": "No"
}
```

HTTP 200 if Success else HTTP 400

10) Add Event Feedback

POST http://127.0.0.1:5000/eventhosting/events/create/feedback
headers: 
Content-Type: application/json

Example Body: 

```
{
    "eid": 4,
    "username": "judith77",
    "feedback": "just a test"
}
```

HTTP 200 if Success else HTTP 400

11) Get Invites And Associated Events for username judith77

GET http://127.0.0.1:5000/eventhosting/events/invites/judith77

Response:

```
[
    {
        "event": {
            "DATE_FROM": "Sun, 12 Nov 2023 12:40:38 GMT",
            "DATE_TO": "Sun, 12 Nov 2023 12:40:38 GMT",
            "DESCRIPTION": "test",
            "EID": 4,
            "EVENT_TYPE": "research",
            "E_AID": 1,
            "LOCATION": "now",
            "MODALITY": "online",
            "NAME": "test_event"
        },
        "invite": {
            "ATTENDING": "No",
            "I_EID": 4,
            "I_SID": 1
        }
    }
]
```

HTTP 200 if Success else HTTP 400

12) Get students and associated feedback for an event having eid 4

GET http://127.0.0.1:5000/eventhosting/events/feedback/4

Response:

```
[
    {
        "feedback": {
            "FEEDBACK": "just a test",
            "P_EID": 4,
            "P_SID": 1
        },
        "student": {
            "CITIZENSHIP": "New Zealand",
            "DEPARTMENT": "",
            "EMAIL": "judith77@vt.edu",
            "GENDER": "O",
            "MAJOR": "Creative Technologies",
            "NAME": "Katherine Burns",
            "RACE": "Black or African American",
            "SID": 1,
            "USERNAME": "judith77",
            "YEAR": "Junior\r"
        }
    }
]
```

HTTP 200 if Success else HTTP 400


To run the Flask app locally install the requirements.txt file and click play on app.py in VSCode
