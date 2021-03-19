"""Routes for the course resource.
"""

from run import app
import json
from flask import request,jsonify
from http import HTTPStatus
import data
from validate import CreateCourseSchema

cd=json.load(open('json/course.json'))
length=len(cd)-1

def search(id):
    begin = 0
    last = length
    while begin <= last:
        mid = (begin + last)//2
        if cd[mid]["id"] == int(id):
            return mid
        if cd[mid]["id"] > int(id):
            last = mid - 1
        else:
            begin = mid + 1

@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE
    index = search(id)
    if index:
        return jsonify({"data": cd[index]}), 200
    return jsonify({"message": "Course "+str(id)+" does not exist"}), 404


@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE
    title_words = []
    metadata = {}
    number = int(request.args.get('page-number', 1))
    size = int(request.args.get('page-size', 10))
    begin_index = size*(number-1)
    last_index = begin_index+size
    if request.args.get('title-words') is not None:
        title_words = request.args.get('title-words').split(',')
    filtered_courses = []
    sliced_courses = []
    if title_words:
        for course in cd:
            title = course["title"]
            for word in title_words:
                if word.lower() in title.lower():
                    filtered_courses.append(course)
    if not filtered_courses and title_words:
        return jsonify(({"message": "No courses available"})), 404
    elif not title_words:
        sliced_courses = cd[begin_index:last_index]
    else:
        sliced_courses = filtered_courses[begin_index:last_index]
    metadata["page_size"] = size
    metadata["page_number"] = number
    if sliced_courses:
        return jsonify({"data": sliced_courses, "metadata": metadata}), 200
    elif filtered_courses:
        return jsonify({"data": filtered_courses, "metadata": metadata}), 200
    return jsonify(({"message": "No courses available"})), 404


@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE
    create_course_schema = CreateCourseSchema()
    errors = create_course_schema.validate(request.form)
    if errors:
        error_message = ''
        for key in errors:
            error_message += errors[key][0] + " "
        return jsonify(({"message": error_message})), 400
    data = request.form.to_dict()
    data['id'] = cd[-1]['id'] + 1
    data['date-created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    data['date-updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    cd.append(data)

    return jsonify({"data": data}), 201


@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    # YOUR CODE HERE
    create_course_schema = CreateCourseSchema()
    errors = create_course_schema.validate(request.form)
    if errors:
        error_message = ''
        for key in errors:
            error_message += errors[key][0] + " "
        return jsonify(({"message": error_message})), 400
    index = search(id)
    if not index:
        return jsonify({
            "message": "The id does not match the payload"
        }), 400
    data = request.form.to_dict()
    data["id"] = int(data["id"])
    updated_course = {**cd[index],
                      **data,
                      'date-updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}
    print("updated course", update_course)
    cd[index] = updated_course
    return jsonify({"data": updated_course}), 200



@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE
    index = search(id)
    if index:
        del cd[index]
        return jsonify({
            "message": "The specified course was deleted"
        }), 200
    else:
        return jsonify({
            "message": f"Course {id} does not exist"
        }), 404
