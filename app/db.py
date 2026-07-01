import os
from typing import Optional, Dict, Any

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    """
    Creates a MySQL connection using environment variables.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3307")),
        database=os.getenv("DB_NAME", "isp_support_db"),
        user=os.getenv("DB_USER", "isp_user"),
        password=os.getenv("DB_PASSWORD", "isp_password"),
    )


def get_client_by_id(client_id: int) -> Optional[Dict[str, Any]]:
    """
    Returns one client by ID.
    If the client does not exist, returns None.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                id,
                full_name,
                service_plan,
                service_status,
                assigned_ip,
                gateway_ip,
                router_brand,
                connection_type,
                radius_status,
                tr069_status,
                last_seen,
                has_open_ticket
            FROM clients
            WHERE id = %s
            """,
            (client_id,),
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()