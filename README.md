# DRP 15 - Server

## Requirements

- Python 3.8 or above
- [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [MongoDB](https://docs.mongodb.com/manual/core/schema-validation/)
- [Docker](https://docs.docker.com/engine/install/)


## Running the app locally

You can run the server locally as followed:

```shell
# Create a new virtual environment
python3 -m venv env 
source env/bin/activate

# Install required packages
pip3 install -r requirements.txt 
```

**_IMPORTANT_**: Do not use production database when running locally! 

```shell
export DB_CONNECTION_STRING=<dev database connection string>
```

```shell
uvicorn --port $PORT --workers 8 niched.main:app```
```

## Testing locally

**_IMPORTANT_**: Again, use development database as before!

### Running unit tests
Unit tests should not connect to the database or communicate with the 'outside world'

```shell
# Create a new virtual environment
python3 -m venv env 
source env/bin/activate
pip3 install -r requirements.txt 
export PYTHONPATH=.

pytest --cov-report term-missing:skip-covered --cov=niched/ test/unit_tests/
```

When running integration tests, use **dev** database! You can also create your own database locally,
and then connect to this database in development stage. 

To create a local mongoDB, follow [this guide](https://docs.mongodb.com/manual/installation/)! 
```shell
# Create a new virtual environment
python3 -m venv env 
source env/bin/activate
pip3 install -r requirements.txt 
export PYTHONPATH=.
export DB_CONNECTION_STRING=<dev database connection>

pytest --cov-report term-missing:skip-covered --cov=niched/ test/integration_tests/
```

[Pytest](https://docs.pytest.org/en/6.2.x/index.html) has more options for reports, see the page for more information!