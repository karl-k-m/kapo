"""
Main service file for the application
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import config

# Connect to the database
conn = psycopg2.connect(
    host=config.db_host,
    port=config.db_port,
    user=config.user,
    password=config.password,
    database=config.database
)


def post_private_message(webmaster_id: int,
                 sender_id: str,
                 sender_name: str,
                 recipient_id: str,
                 recipient_name: str,
                 message: str,
                 timestamp: str):
    """
    Post a message to the database
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO messages.private_messages (webmaster_id, sender_id, sender_name, recipient_id, recipient_name, message, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (webmaster_id, sender_id, sender_name, recipient_id, recipient_name, message, timestamp)
    )
    conn.commit()
    cursor.close()


def get_dms(sender_id: str,
            recipient_id: str,
            last_message_id: int):
    """
    Get all direct messages for a given pair of users where the last message id is greater than the last message id
    """
    if last_message_id is None:
        last_message_id = -1
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        f"""
        SELECT id, webmaster_id, sender_id, sender_name, recipient_id, recipient_name, message, timestamp
        FROM messages.private_messages
        WHERE (sender_id = '{sender_id}' AND recipient_id = '{recipient_id}')
        OR (sender_id = '{recipient_id}' AND recipient_id = '{sender_id}')
        AND id > {last_message_id}
        ORDER BY timestamp ASC
        """
    )
    messages = cursor.fetchall()
    for message in messages:
        message['timestamp'] = message['timestamp'].strftime('%Y-%m-%d %H:%M:%S')  # Format as string
    cursor.close()
    return messages

def get_dm_user_pairs():
    """
    Get all user pairs that have had direct messages (user pairs where sender and recipient are the same are treated as the same pair)
    """

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """
        SELECT DISTINCT sender_id, sender_name, recipient_id, recipient_name
        FROM messages.private_messages
        """
    )
    # return in format such as:
    """
    [
    {
        "sender_id": "sender123",
        "recipient_id": "recipient456",
        "sender_name": "Sender Name",
        "recipient_name": "Recipient Name"
    },
    {
        "sender_id": "sender789",
        "recipient_id": "recipient101",
        "sender_name": "Another Sender",
        "recipient_name": "Another Recipient"
    }
    ]
    """
    user_pairs = cursor.fetchall()
    cursor.close()
    return user_pairs