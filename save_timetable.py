"""
Program to save the timetable to a file. Change the classes and their timings in the provided format only.
"""

import json

periods = {
    "Monday": {"Chemistry": "08:00", "Computer Science": "09:40", "Physics": "10:30"},
    "Tuesday": {"Maths": "08:00", "Physics": "08:50", "Computer Science": "10:30"},
    "Wednesday": {"Maths": "08:50", "English": "09:40", "Chemistry": "10:30"},
    "Thursday": {"English": "08:00", "Chemistry": "08:50", "Physics": "09:40", "Computer Science": "10:30"},
    "Friday": {"Maths": "08:50", "Physics": "09:40", "Chemistry": "10:30"}
}

json.dump(periods, open("timetable.json", "w"), indent=4)
