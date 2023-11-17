import traceback
from flask import Blueprint, Response, jsonify, request
from dataclasses import asdict
from database.eventhosting import get_engine, get_admin, authenticate_admin

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route("/admin_details/<username>", methods = ["GET"])
def get_admin_details(username: str) -> Response:
    try:
        engine = get_engine()
        admin = get_admin(engine, username)
        admin = asdict(admin)
        del admin["PASSWORD"]
        return admin
    except Exception as e:
        return jsonify(error=traceback.format_exc()),500

@admin_routes.route("authenticate", methods=["GET"])
def authenitcate() -> Response:
    try:
        engine = get_engine()
        auth_args = request.json
        authenitcated = authenticate_admin(engine, auth_args["username"], auth_args["password"])
        return jsonify(is_authenticated=authenitcated), (200 if authenitcated \
        else 401)
    except Exception as e:
        return jsonify(error=traceback.format_exc()),500