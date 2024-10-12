from databricks import sql
import datetime
import os

class DBConnector:
    def __init__(self):
        self.server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        self.http_path = os.getenv("DATABRICKS_HTTP_PATH")
        self.access_token = os.getenv("DATABRICKS_DB_TOKEN")
        self.connection = None

    def connect(self):
        try:
            self.connection = sql.connect(
                server_hostname=self.server_hostname,
                http_path=self.http_path,
                access_token=self.access_token
            )
            print("Connected to Databricks successfully.")
        except Exception as e:
            raise Exception(f"Failed to connect to Databricks: {e}")

    def insert_feedback(self, therapist_id, ai_case_notes, feedback):
        if self.connection is None:
            raise Exception("No database connection. Please connect first.")
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_query = """
        INSERT INTO feedback (therapist_id, ai_case_notes, feedback, feedback_submitted_at)
        VALUES (?, ?, ?, ?)
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(insert_query, (
                    therapist_id, ai_case_notes, feedback, timestamp))
                print("Data successfully submitted to Databricks.")
        except Exception as e:
            raise Exception(f"Failed to insert data: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")