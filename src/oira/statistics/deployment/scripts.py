# -*- coding: utf-8 -*-
from metabase_api import Metabase_API
import argparse
import logging
import subprocess
import sys

log = logging.getLogger(__name__)


def get_metabase_args():
    parser = argparse.ArgumentParser(
        description=(
            "Initialize a metabase instance by restoring a SQL dump and adapting "
            "settings to the given parameters."
        )
    )
    parser.add_argument(
        "--metabase-host",
        type=str,
        required=False,
        default="localhost",
        help=("Host that the metabase instance is running on"),
    )
    parser.add_argument(
        "--metabase-port",
        type=str,
        required=False,
        default=3000,
        help=("Port that the metabase instance is running on"),
    )
    parser.add_argument(
        "--metabase-user",
        type=str,
        required=True,
        help=("User name for connecting to the metabase instance"),
    )
    parser.add_argument(
        "--metabase-password",
        type=str,
        required=True,
        help=("Password for connecting to the metabase instance"),
    )
    parser.add_argument(
        "--database-name",
        type=str,
        required=True,
        help=("Name of the internal metabase database"),
    )
    parser.add_argument(
        "--database-host",
        type=str,
        required=False,
        default="localhost",
        help=("Host that the postgresql server is running on"),
    )
    parser.add_argument(
        "--database-port",
        type=str,
        required=False,
        default=5432,
        help=("Port that the postgresql server is running on"),
    )
    parser.add_argument(
        "--database-user",
        type=str,
        required=True,
        help=("User name for connecting to the postgresql server"),
    )
    parser.add_argument(
        "--database-password",
        type=str,
        required=True,
        help=("Password for connecting to the postgresql server"),
    )
    parser.add_argument(
        "--database-name-statistics",
        type=str,
        required=True,
        help=("Name of the postgresql statistics database"),
    )
    parser.add_argument(
        "--statistics-user-email",
        type=str,
        help=(
            "Email address for a non-superuser account to create for viewing the "
            "statistics"
        ),
    )
    parser.add_argument(
        "--statistics-user-password",
        type=str,
        help=("Password for the non-superuser statistics account"),
    )
    parser.add_argument(
        "--statistics-user-first-name",
        type=str,
        help=("First name of the non-superuser statistics account"),
    )
    parser.add_argument(
        "--statistics-user-last-name",
        type=str,
        help=("Last name of the non-superuser statistics account"),
    )
    return parser.parse_args()


def init_metabase_instance():
    logging.basicConfig(stream=sys.stderr, level=0)
    log.info("Cleaning and reinitializing metabase instance")
    args = get_metabase_args()

    postgres_url = (
        "postgresql://{args.database_user}:{args.database_password}@"
        "{args.database_host}:{args.database_port}/{args.database_name}"
    ).format(args=args)
    with open("sql/metabase-dump.sql") as metabase_dump:
        subprocess.check_output(["psql", postgres_url], stdin=metabase_dump)

    api_url = "http://{args.metabase_host}:{args.metabase_port}".format(args=args)
    mb = Metabase_API(api_url, args.metabase_user, args.metabase_password)

    result = mb.put(
        "/api/database/34",
        json={
            "name": args.database_name_statistics,
            "engine": "postgres",
            "details": {
                "dbname": args.database_name_statistics,
                "host": args.database_host,
                "port": args.database_port,
                "user": args.database_user,
                "password": args.database_password,
            },
        },
    )
    if result >= 400:
        log.error("Could not update database connection! ({})".format(result))

    if args.statistics_user_email:
        result = mb.post(
            "/api/user",
            json={
                "first_name": args.statistics_user_first_name,
                "last_name": args.statistics_user_last_name,
                "email": args.statistics_user_email,
                "password": args.statistics_user_password,
            },
        )
    if result >= 400:
        log.error("Could not create user! ({})".format(result))
