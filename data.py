import json
"""Routines associated with the application data.
"""

courses = {}

def load_data():
    """Load the data from the json file.
    """
    courses = json.load(open('json/course.json'))
    return sorted(courses, key=lambda x: x["id"])


