Python 3.8

Install dependencies
`pip install -r requirements.txt`

Create database
`POSTGRES_PORT=some_port POSTGRES_DB=some_db POSTGRES_USER=some_user POSTGRES_PASSWORD=some_password docker-compose -f docker/docker-compose.yaml up -d`

Environment variables
```sh
export DB_NAME=some_value
export DB_USER=some_value
export DB_PASSWORD=some_value
export DB_HOST=some_value
export DB_PORT=some_value
export SERVER_POLYGON_PORT=some_value
```

Run tests `pytest tests`

Run server `pytho3.8 main.py`