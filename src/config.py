"""
App configuration taken from environment variables
"""

import os

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')

# For debugging purposes
# db_host = 'localhost'
# db_port = '5432'
# user='postgres'
# password='postgres'
# database='kapo'