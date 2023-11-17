import traceback
from flask import Blueprint, Response, jsonify, request
from dataclasses import asdict
from database.eventhosting import get_engine, get_student, authenticate_student, insert_student, get_students

student_routes = Blueprint('student_routes', __name__)

@student_routes.route("/student_details/<username>", methods = ["GET"])
def get_student_details(username: str) -> Response:
    try:
        engine = get_engine()
        student = get_student(engine, username)
        student = asdict(student)
        del student["PASSWORD"]
        return student
    except Exception as e:
        return jsonify(error=traceback.format_exc()),500

@student_routes.route("/students_details", methods = ["GET"])
def get_students_details() -> Response:
    try:
        engine = get_engine()
        get_args: dict = request.json
        result = get_students(engine,
                     get_args.get("majors", ["%"]),
                     get_args.get("citizenships", ["%"]),
                     get_args.get("races", ["%"]),
                     get_args.get("genders", ["%"]))
        students = []
        for student in result:
            students.append(asdict(student))
            del students[-1]["PASSWORD"]
    except Exception as e:
        return jsonify(error=traceback.format_exc()),400
    return jsonify(students)
    
        
    
@student_routes.route("authenticate", methods=["GET"])
def authenitcate() -> Response:
    try:
        engine = get_engine()
        auth_args = request.json
        authenitcated = authenticate_student(engine, auth_args["username"], auth_args["password"])
        return jsonify(is_authenticated=authenitcated), (200 if authenitcated \
        else 401)
    except Exception as e:
        return jsonify(error=traceback.format_exc()),500

@student_routes.route("create", methods=["POST"])
def create_student() -> Response:
    try:
        create_args: dict = request.json
        engine = get_engine()
        insert_student(engine,
                       create_args["name"],
                       create_args["username"],
                       create_args["password"],
                       create_args["email"],
                       create_args.get("race"),
                       create_args.get("department"),
                       create_args.get("major"),
                       create_args["citizenship"],
                       create_args.get("year"),
                       create_args["gender"])
    except Exception as e:
        return jsonify(error=traceback.format_exc()),400
    return "Success", 200
    
