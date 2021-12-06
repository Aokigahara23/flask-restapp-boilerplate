# Forest23 Flask project boilerplate

## Quickstart

----------

After download, in the project root create a virtual environment and install `requirements.txt`:

    <python binary> -m venv venv && ./venv/bin/activate && pip install -r ./requirements.txt

You could run the app from PyCharm IDE from `./app.py` or directly from the command line using:

    flask run --with-threads

## Migrations

----------

Whenever a database migration needs to be made. Run the following commands:

    flask db migrate

This will generate a new migration script. Then run:

    flask db upgrade

To apply the migration.

For a full migration command reference, run ``flask db --help``.

## First Migration *

----------

Project was made as an example. So it has one migration file already created and stored in the repo. So if you want to play with kitties - just perform an upgrade after downloading the project. Otherwise delete the migration file `<Project root>/migrations/versions/*.py`