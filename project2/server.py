"""
Server entrypoint.

!!! DO NOT MODIFY THIS FILE !!!

"""

import argparse
import json
import random
import sys
from typing import Dict, List, Union

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy

from stroll import Server


def main(args: List[str]) -> None:
    """Parse the arguments given to the server, and call the appropriate method."""

    parser = argparse.ArgumentParser(description="Server for CS-523 project 2.")
    subparsers = parser.add_subparsers(help="Command")

    parser_setup = subparsers.add_parser(
        "setup", help="Generate a pair of secret and public keys."
    )
    parser_setup.add_argument(
        "-p",
        "--pub",
        help="Name of the file in which to write the public key.",
        default="key.pub",
        type=argparse.FileType("wb")
    )
    parser_setup.add_argument(
        "-s",
        "--sec",
        help="Name of the file in which to write the secret key.",
        default="key.sec",
        type=argparse.FileType("wb")
    )
    parser_setup.add_argument(
        "-S",
        "--subscriptions",
        help="Subscriptions recognized by the server.",
        type=str,
        required=True,
        default=list(),
        action="append"
    )

    parser_setup.set_defaults(callback=server_setup)

    parser_run = subparsers.add_parser("run", help="Run the server.")
    parser_run.add_argument(
        "-p",
        "--pub",
        help="Name of the file containing the public key.",
        default="key.pub",
        type=argparse.FileType("rb")
    )
    parser_run.add_argument(
        "-s",
        "--sec",
        help="Name of the file containing the secret key.",
        default="key.sec",
        type=argparse.FileType("rb")
    )

    parser_run.set_defaults(callback=server_run)

    namespace = parser.parse_args(args)

    if "callback" in namespace:
        namespace.callback(namespace)

    else:
        parser.print_help()


def server_setup(args: argparse.Namespace) -> None:
    """Handle `setup` subcommand."""

    public_key_fd = args.pub
    secret_key_fd = args.sec
    subscriptions = args.subscriptions
    subscriptions.append("username")

    try:
        secret_key, public_key = Server.generate_ca(subscriptions)

        public_key_fd.write(public_key)
        secret_key_fd.write(secret_key)

        public_key_fd.flush()
        secret_key_fd.flush()

    finally:
        args.pub.close()
        args.sec.close()


def server_run(args: argparse.Namespace) -> None:
    """Handle `run` subcommand."""

    # pylint: disable=global-statement
    global PUBLIC_KEY
    global SECRET_KEY
    global SERVER

    try:
        PUBLIC_KEY = args.pub.read()
        SECRET_KEY = args.sec.read()

    finally:
        args.pub.close()
        args.sec.close()

    SERVER = Server()

    host = "0.0.0.0"
    port = 8080

    APP.run(host=host, port=port, debug=True, threaded=False, processes=1)


APP = Flask(__name__)


DB = SQLAlchemy()


class PoI(DB.Model):
    """A PoI object consists of the following:

    poi_id -- ID of the PoI
    poi_name -- Name of the PoI
    poi_address -- Address of the PoI
    grid_id -- Grid in which the PoI is present
    poi_ratings -- List of ratings for the PoI.
    """

    # pylint: disable=no-member

    poi_id = DB.Column(DB.Integer, primary_key=True)
    poi_name = DB.Column(DB.String)
    poi_address = DB.Column(DB.String)
    grid_id = DB.Column(DB.Integer)
    poi_ratings = DB.Column(DB.String)

    def to_dict(self) -> Dict[str, Union[int, str]]:
        """
        Return a dictionary representation of the object.
        """
        return dict(
            poi_id=self.poi_id,
            poi_name=self.poi_name,
            poi_address=self.poi_address,
            grid_id=self.grid_id,
            poi_ratings=self.poi_ratings,
        )


APP.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fingerprint.db"
APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
DB.app = APP
DB.init_app(APP)


PUBLIC_KEY = None
SECRET_KEY = None
SERVER = None


@APP.route("/public-key", methods=["GET"])
def get_public_key():
    """Handle requests for public key."""
    return PUBLIC_KEY, 200


@APP.route("/register", methods=["POST"])
def register():
    """Handle registrations."""
    username = request.files.get("username").read().decode("utf-8")
    subscriptions_raw = request.files.get("subscriptions").read().decode("utf-8")
    issuance_req = request.files.get("issuance_req").read()
    subscriptions = json.loads(subscriptions_raw)
    registration_res = SERVER.process_registration(
        SECRET_KEY,
        PUBLIC_KEY,
        issuance_req,
        username,
        subscriptions
    )

    server_res = make_response(registration_res)
    return server_res


def convert_loc_to_gridval(loc):
    """Placeholder function. Final function would convert the location to a grid value."""
    return int(loc)


@APP.route("/poi-loc", methods=["POST"])
def get_poi_loc():
    """Takes in a latitude and longitude as input, returns a list of associated POIs."""

    lat = float(request.files.get("lat").read().decode("utf-8"))
    lon = float(request.files.get("lon").read().decode("utf-8"))
    types = json.loads(request.files.get("types").read().decode("utf-8"))
    signature = request.files.get("signature").read()
    message = (f"{lat},{lon}").encode("utf-8")

    valid = SERVER.check_request_signature(
        PUBLIC_KEY, message, types, signature
    )

    if not valid:
        return "Invalid signature", 401

    # PoIs are within coordinates (46.5, 6.55) and (46.57, 6.65)
    # mapped to a 10 x 10 grid
    if 46.5 <= lat <= 46.57 and 6.55 <= lon <= 6.65:
        cell_x = ((lat - 46.5) / 0.07) * 10
        cell_y = ((lon - 6.55) / 0.1) * 10
        cell_id = int(cell_x + (cell_y * 10))
        records = PoI.query.filter_by(grid_id=cell_id).all()

        if records:
            poi_list = [record.to_dict()["poi_id"] for record in records]
            poi_list_res = {"poi_list": poi_list}
        else:
            poi_list_res = {"poi_list": []}
    else:
        poi_list_res = {"poi_list": []}

    return jsonify(poi_list_res)


@APP.route("/poi-grid", methods=["POST"])
def get_poi_list():
    """Takes in a cell ID as input, returns a list of associated POIs."""

    cell_id = int(request.files.get("cell_id").read().decode("utf-8"))
    types = json.loads(request.files.get("types").read().decode("utf-8"))
    signature = request.files.get("signature").read()
    message = (f"{cell_id}").encode("utf-8")

    valid = SERVER.check_request_signature(
        PUBLIC_KEY, message, types, signature
    )

    if not valid:
        return "Invalid signature", 401

    records = PoI.query.filter_by(grid_id=cell_id).all()

    if records:
        poi_list = [record.to_dict()["poi_id"] for record in records]
        poi_list_res = {"poi_list": poi_list}

    else:
        return "Not found", 404

    return jsonify(poi_list_res)


@APP.route("/poi", methods=["GET"])
def get_poi_info():
    """Takes in a PoI ID as input, returns information about that PoI.
    We have a paramter 'noise_factor' for tuning.
    This is used to slightly alter the size of responses sent by the server.
    Server adds padding records based on the noise factor. Do not change
    the noise code, this is used to simulate slight variations in traces
    from the server."""

    poi_id = request.args.get('poi_id')
    noise_factor = 10

    records = PoI.query.filter_by(poi_id=int(poi_id)).all()
    if records:
        poi_info = records[0].to_dict()
        poi_info["poi_ratings"] = json.loads(poi_info["poi_ratings"])

        random_length = random.randint(0, noise_factor)
        padding = [-1 for x in range(0, random_length)]
        poi_info["padding"] = padding

    else:
        return "Not found", 404

    return jsonify(poi_info)


if __name__ == "__main__":
    main(sys.argv[1:])
