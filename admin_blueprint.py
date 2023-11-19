import traceback
from flask import Blueprint, Response, jsonify, request
from dataclasses import asdict
from .database.eventhosting import get_engine, get_admin, authenticate_admin
from typing import Tuple

admin_routes = Blueprint('admin_routes', __name__)


@admin_routes.route("/admin_details/<username>", methods=["GET"])
def get_admin_details(username: str) -> Tuple[Response, int]:
    try:
        engine = get_engine()
        admin = get_admin(engine, username)
        admin = asdict(admin)
        del admin["PASSWORD"]
        response = jsonify(admin)
        response.headers[
            "Access-Control-Allow-Origin"] = "*"  # This is unsafe, but good enough
        return response, 200

    except Exception as e:
        return jsonify(error=traceback.format_exc()), 500


@admin_routes.route("authenticate", methods=["POST"])
def authenticate() -> Tuple[Response, int]:
    try:
        engine = get_engine()
        auth_args = request.json
        authenticated = authenticate_admin(engine, auth_args["username"],
                                           auth_args["password"])
        response = jsonify(is_authenticated=authenticated)
        response.headers[
            "Access-Control-Allow-Origin"] = "*"  # This is unsafe, but good enough
        return response, (200 if authenticated else 401)

    except Exception as e:
        return jsonify(error=traceback.format_exc()), 500
