"""
Client entrypoint.

!!! DO NOT MODIFY THIS FILE !!!

"""

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import requests

from stroll import Client

#
# Network communications
#


SERVER_HOSTNAME = "cs523-server"
TOR_PROXY = "socks5h://localhost:9050"
TOR_HOSTNAME_FILENAME = Path("/client/tor/hidden_service/hostname")


class ClientHTTPError(Exception):
    """An unexpected HTTP status was received."""


#
# Parser
#


def main(args: List[str]) -> None:
    """Parse the arguments given to the client, and call the appropriate method."""

    parser = argparse.ArgumentParser(description="Client for CS-523 project 2.")
    subparsers = parser.add_subparsers(help="Command")

    # Get public key parser.
    parser_get_pk = subparsers.add_parser(
        "get-pk", help="Retrieve the public key from the server."
    )
    parser_get_pk.add_argument(
        "-o",
        "--out",
        help="Name of the file in which to write the public key.",
        type=argparse.FileType("wb"),
        default="key-client.pub",
    )
    parser_get_pk.add_argument(
        "-t",
        "--tor",
        help="Use Tor to connect to the server.",
        action="store_true"
    )
    parser_get_pk.set_defaults(callback=client_get_pk)

    # Register parser.
    parser_register = subparsers.add_parser(
        "register", help="Register the client to the server."
    )
    parser_register.add_argument(
        "-p",
        "--pub",
        help="Name of the file from which to read the public key.",
        type=argparse.FileType("rb"),
        default="key-client.pub"
    )
    parser_register.add_argument(
        "-u",
        "--user",
        help="User name.",
        type=str,
        required=True
    )
    parser_register.add_argument(
        "-o",
        "--out",
        help="Name of the file in which to write the attribute-based credential.",
        type=argparse.FileType("wb"),
        default="anon.cred"
    )
    parser_register.add_argument(
        "-S",
        "--subscriptions",
        help="Subscriptions to register.",
        type=str,
        required=True,
        action="append"
    )
    parser_register.add_argument(
        "-t",
        "--tor",
        help="Use Tor to connect to the server.",
        action="store_true"
    )

    parser_register.set_defaults(callback=client_register)

    # Parser for part 1 of the project 2
    parser_loc = subparsers.add_parser("loc", help="Part 1 of the project 2.")
    parser_loc.add_argument(
        "lat",
        help="Latitude.",
        type=float
    )
    parser_loc.add_argument(
        "lon",
        help="Longitude.",
        type=float
    )
    parser_loc.add_argument(
        "-p",
        "--pub",
        help="Name of the file from which to read the public key.",
        type=argparse.FileType("rb"),
        default="key-client.pub"
    )
    parser_loc.add_argument(
        "-c",
        "--credential",
        help="Name of the file from which to read the attribute-based credential.",
        type=argparse.FileType("rb"),
        default="anon.cred"
    )
    parser_loc.add_argument(
        "-T",
        "--types",
        help="Types of services to request.",
        type=str,
        required=True,
        action="append"
    )
    parser_loc.add_argument(
        "-t",
        "--tor",
        help="Use Tor to connect to the server.",
        action="store_true"
    )

    parser_loc.set_defaults(callback=client_loc)

    # Parser for part 3 of the project 2
    parser_grid = subparsers.add_parser("grid", help="Part 3 of the project 2.")
    parser_grid.add_argument(
        "cell_id",
        help="Cell identifier.",
        type=int
    )
    parser_grid.add_argument(
        "-p",
        "--pub",
        help="Name of the file from which to read the public key.",
        type=argparse.FileType("rb"),
        default="key-client.pub"
    )
    parser_grid.add_argument(
        "-c",
        "--credential",
        help="Name of the file from which to read the attribute-based credential.",
        type=argparse.FileType("rb"),
        default="anon.cred"
    )
    parser_grid.add_argument(
        "-T",
        "--types",
        help="Types of services to request.",
        type=str,
        default=list(),
        action="append"
    )
    parser_grid.add_argument(
        "-t",
        "--tor",
        help="Use Tor to connect to the server.",
        action="store_true"
    )
    parser_grid.set_defaults(callback=client_grid)

    namespace = parser.parse_args(args)

    if "callback" in namespace:
        namespace.callback(namespace)

    else:
        parser.print_help()


def read_hostname(hostname_path: Path) -> str:
    """Retrieve an hostname from a file."""

    with hostname_path.open("r") as hostname_fd:
        hostname = hostname_fd.read().strip()

    return hostname


def get_conn_params(use_tor: bool) -> Tuple[str, Optional[str]]:
    """Compute connections parameters."""
    if use_tor:
        host = read_hostname(TOR_HOSTNAME_FILENAME)
        proxy = TOR_PROXY
    else:
        host = f"{SERVER_HOSTNAME}:8080"
        proxy = None

    return host, proxy


def create_session(proxy: str) -> requests.Session:
    """Create a Requests session."""

    session = requests.session()

    if proxy:
        session.proxies = {"http": proxy, "https": proxy}

    return session


def client_get_pk(args: argparse.Namespace) -> None:
    """Handle `get-pk` subcommand."""

    public_key_fd = args.out

    try:
        host, proxy = get_conn_params(args.tor)

        url = f"http://{host}/public-key"

        # Done in a proper way, we would use HTTPS instead of HTTP.
        session = create_session(proxy)
        res = session.get(url=url)

        if res.status_code != 200:
            raise ClientHTTPError(
                "The client failed to retrieve the public key from the server!"
            )

        public_key = res.content

        public_key_fd.write(public_key)
        public_key_fd.flush()

    finally:
        args.out.close()


def client_register(args: argparse.Namespace) -> None:
    """Handle `register` subcommand."""

    try:
        public_key = args.pub.read()

    finally:
        args.pub.close()

    try:
        credential_fd = args.out

        username = args.user
        subscriptions = args.subscriptions

        # Copy to prepare registration
        subscriptions_client = copy.deepcopy(subscriptions)

        client = Client()
        issuance_req, state = client.prepare_registration(
            public_key, username, subscriptions_client
        )

        host, proxy = get_conn_params(args.tor)

        # Done in a proper way, we would use HTTPS instead of HTTP.
        url = f"http://{host}/register"
        files = {
            "username": username,
            "subscriptions": json.dumps(subscriptions),
            "issuance_req": issuance_req,
        }

        session = create_session(proxy)
        res = session.post(url=url, files=files)

        if res.status_code != 200:
            raise ClientHTTPError("The client failed to register to the server!")

        issuance_res = res.content

        credential = client.process_registration_response(
            public_key, issuance_res, state
        )

        credential_fd.write(credential)
        credential_fd.flush()

    finally:
        args.out.close()


def client_loc(args: argparse.Namespace) -> None:
    """Handle `loc` subcommand."""

    try:
        lat = args.lat
        lon = args.lon
        types = args.types
        public_key = args.pub.read()
        credential = args.credential.read()

    finally:
        args.pub.close()
        args.credential.close()

    client = Client()
    message = (f"{lat},{lon}").encode("utf-8")
    signature = client.sign_request(public_key, credential, message, types)

    host, proxy = get_conn_params(args.tor)

    url = f"http://{host}/poi-loc"
    files = {
        "lat": str(lat),
        "lon": str(lon),
        "types": json.dumps(types),
        "signature": signature,
    }

    # Done in a proper way, we would use HTTPS instead of HTTP.
    session = create_session(proxy)
    res = session.post(url=url, files=files)

    if res.status_code != 200:
        raise ClientHTTPError(f"Invalid return code {res.status_code}!")

    res_json = res.json()

    poi_ids = res_json["poi_list"]

    if not poi_ids:
        print("Sigh... nothing interesting nearby.")

    # No signature, etc... for retrieving the info about the PoIs themselves.
    for poi_id in poi_ids:
        url = f"http://{host}/poi"
        params = {"poi_id": poi_id}
        res = session.get(url=url, params=params)
        if res.status_code != 200:
            raise ClientHTTPError(f"Invalid return code {res.status_code}!")

        poi = res.json()
        print(f'You are near "{poi["poi_name"]}".')


def client_grid(args: argparse.Namespace) -> None:
    """Handle `grid` subcommand."""

    try:
        cell_id = args.cell_id
        types = args.types
        public_key = args.pub.read()
        credential = args.credential.read()

    finally:
        args.pub.close()
        args.credential.close()

    client = Client()
    message = (f"{cell_id}").encode("utf-8")
    signature = client.sign_request(public_key, credential, message, types)

    host, proxy = get_conn_params(args.tor)

    url = f"http://{host}/poi-grid"
    files = {
        "cell_id": str(cell_id),
        "types": json.dumps(types),
        "signature": signature,
    }

    # Done in a proper way, we would use HTTPS instead of HTTP.
    session = create_session(proxy)
    res = session.post(url=url, files=files)

    if res.status_code != 200:
        raise ClientHTTPError(f"Invalid return code {res.status_code}!")

    res_json = res.json()

    poi_ids = res_json["poi_list"]

    if not poi_ids:
        print("Sigh... nothing interesting nearby.")

    # No signature, etc... for retrieving the info about the PoIs themselves.
    for poi_id in poi_ids:
        url = f"http://{host}/poi"
        params = {"poi_id": poi_id}
        res = session.get(url=url, params=params)
        if res.status_code != 200:
            raise ClientHTTPError(f"Invalid return code {res.status_code}!")

        poi = res.json()
        print(f'You are near "{poi["poi_name"]}".')


if __name__ == "__main__":
    main(sys.argv[1:])
