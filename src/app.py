from flask import Flask
from endpoints import register_endpoints
from flask_cors import CORS
import psycopg2
import config

app = Flask(__name__)
CORS(app)
register_endpoints(app)

# Database connection logic
def init_db():
    try:
        conn = psycopg2.connect(
            host=config.db_host,
            port=config.db_port,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = conn.cursor()
        cursor.execute("CREATE SCHEMA IF NOT EXISTS messages;")
        cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages.private_messages (
            id SERIAL PRIMARY KEY,
            webmaster_id INT,
            sender_id TEXT,
            sender_name TEXT,
            recipient_id TEXT,
            recipient_name TEXT,
            message TEXT,
            timestamp TIMESTAMP
        )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error initializing database: ", e)

# Run database setup before starting the server
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
