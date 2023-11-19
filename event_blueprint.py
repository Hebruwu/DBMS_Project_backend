import traceback
from dataclasses import asdict

import dateutil.parser
import dateutil.tz
from flask import Blueprint, Response, jsonify, request

from .database.eventhosting import get_engine, get_feedback, insert_event, get_events, \
    insert_invite, update_invite, insert_feedback, get_invites

from typing import Tuple

event_routes = Blueprint('event_routes', __name__)


@event_routes.route("create", methods=["POST"])
def create_event() -> Tuple[Response, int]:
    try:
        engine = get_engine()
        create_args: dict = request.json
        create_args["date_from"] = dateutil.parser.parse(create_args["date_from"],
                                                         ignoretz=False)
        create_args["date_to"] = dateutil.parser.parse(create_args["date_to"],
                                                       ignoretz=False)
        insert_event(engine, create_args["name"],
                     create_args["date_from"],
                     create_args["date_to"],
                     create_args["type"],
                     create_args["modality"],
                     create_args["location"],
                     create_args["aid"],
                     create_args.get("description"))
    except Exception as e:
        return jsonify(error=traceback.format_exc()), 400

    response = jsonify("Success")
    # Don't know if we need to specify CORS header here. Left as is for now.
    return response, 200


@event_routes.route("events_details", methods=["GET"])
def get_events_details() -> Tuple[Response, int]:
    try:
        engine = get_engine()
        events = get_events(engine)
        events = [asdict(event) for event in events]

    except Exception as e:
        return jsonify(error=traceback.format_exc()), 400

    response = jsonify(events)
    response.headers[
        "Access-Control-Allow-Origin"] = "*"  # This is unsafe, but good enough
    return response, 200


@event_routes.route("create/invite", methods=["POST"])
def create_event_invite() -> Tuple[Response, int]:
    try:
        engine = get_engine()
        create_args = request.json
        insert_invite(engine,
                      None,
                      create_args["eid"],
                      create_args["sid"])
    except Exception as e:
        return jsonify(error=traceback.format_exc()), 400

    response = jsonify("Success")
    # Don't know if we need to specify CORS header here. Left as is for now.
    return response, 200


@event_routes.route("create/feedback", methods=["POST"])
def create_event_feedback() -> Tuple[Response, int]:
    try:
        engine = get_engine()
        create_args = request.json
        insert_feedback(engine,
                        create_args["username"],
                        create_args["eid"],
                        create_args["feedback"])
    except Exception as e:
        return jsonify(error=traceback.format_exc()), 400

    response = jsonify("Success")
    # Don't know if we need to specify CORS header here. Left as is for now.
    return response, 200


@event_routes.route("modify/invite", methods=["PUT"])
def modify_event_invite() -> Tuple[Response, int]:
    try:
        engine = get_engine()
        put_args = request.json
        update_invite(engine,
                      put_args["username"],
                      put_args["eid"],
                      put_args["attending"])
    except Exception as e:
        return jsonify(error=traceback.format_exc()), 400

    response = jsonify("Success")
    # Don't know if we need to specify CORS header here. Left as is for now.
    return response, 200


@event_routes.route("invites/<username>", methods=["GET"])
def get_events_and_invites(username: str) -> Tuple[Response, int]:
    try:
        engine = get_engine()
        result = get_invites(engine, username)
        events_and_invites = []
        for i in range(0, len(result), 2):
            events_and_invites.append({
                "invite": asdict(result[i]),
                "event": asdict(result[i + 1])
            })
    except Exception as e:
        return jsonify(error=traceback.format_exc()), 400
    response = jsonify(events_and_invites)
    response.headers[
        "Access-Control-Allow-Origin"] = "*"  # This is unsafe, but good enough
    return response, 200


@event_routes.route("feedback/<eid>", methods=["GET"])
def get_students_and_feedback(eid: int) -> Tuple[Response, int]:
    try:
        engine = get_engine()
        result = get_feedback(engine, eid)
        students_and_feedback = []
        for i in range(0, len(result), 2):
            student = asdict(result[i + 1])
            del student["PASSWORD"]
            students_and_feedback.append({
                "feedback": asdict(result[i]),
                "student": student
            })
    except Exception as e:
        return jsonify(error=traceback.format_exc()), 400

    response = jsonify(students_and_feedback)
    response.headers[
        "Access-Control-Allow-Origin"] = "*"  # This is unsafe, but good enough

    return response, 200
