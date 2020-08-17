import os


DB_NAME = os.getenv('DB_NAME', 'polygon')
DB_USER = os.getenv('DB_USER', 'gis')
DB_PASSWORD = os.getenv('DB_PASSWORD', '12345')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5436')
SERVER_POLYGON_PORT = os.getenv('SERVER_POLYGON_PORT', 8800)

