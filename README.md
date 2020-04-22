# Repository moved!

Please see https://github.com/EU-OSHA/oira.statistics.deployment

# OSHA OiRA Statistics Deployment

This package contains configuration and scripts for deploying the OSHA OiRA statistics. The buildout configuration sets up a number of metabase instances to serve the statistics and generates scripts to prime them with a database dump and tweak their settings afterwards.

# Setup

Create a `buildout.cfg` like this:

    [buildout]
    extends =
        base.cfg
        secrets.cfg

    [metabase-instance]
    metabase-host = oira.local

Adapt `metabase-host` to the address you want to bind to or leave empty to use the default (`localhost`).

Create a `secrets.cfg` like this:

    [metabase-instance]
    metabase-password = ********

    [metabase-global]
    statistics-user-password = ********

    [metabase-eu]
    statistics-user-password = ********

    [metabase-fr]
    statistics-user-password = ********

# Usage

As usual, run:

    # bin/buildout

Then, to set up the metabase instances:

    # bin/init-metabase

After that you can log in to the metabase instances with the credentials you provided.

To make changes to the metabase content, use metabase-instance (not metabase_global or one of the country specific ones).

Check the database dump in the `dumps/` directory. Ideally you should use the same version of postgresql and pg_dump as specified at the top.

To dump the database, run:

    # bin/dump-metabase

Then inspect and, if satisfied, commit the changes to the database dump in the `dumps/` directory.

## init-metabase-instance

Apply settings to a single metabase instance. Sets database connection parameters and optionally creates an additional user. Run `init-metabase-instance --help` for arguments.
