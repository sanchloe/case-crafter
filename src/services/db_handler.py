import os
import datetime

from databricks import sql

class DBConnector:
    def __init__(self):
        self.server_hostname = os.getenv("DATABRICKS_HOST")
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
        
    def insert_case_notes(
            self, session_id, client_id, client_name, therapist_id, llm_case_notes):
        if self.connection is None:
            raise Exception("No database connection. Please connect first.")
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_query = """
        INSERT INTO case_notes (session_id, client_id, client_name, therapist_id, llm_case_notes, case_notes_submitted_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(insert_query, (
                    session_id, client_id, client_name, therapist_id, llm_case_notes, timestamp))
                print("Data successfully submitted to Databricks.")
        except Exception as e:
            raise Exception(f"Failed to insert data: {e}")

    def update_feedback(self, session_id, feedback):
        if self.connection is None:
            raise Exception("No database connection. Please connect first.")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        update_query = """
        UPDATE case_notes
        SET feedback = ?, feedback_submitted_at = ?
        WHERE session_id = ?
        """
        print('sesh id', session_id)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(update_query, (feedback, timestamp, session_id))
                print("Feedback successfully updated.")
        except Exception as e:
            raise Exception(f"Failed to update feedback: {e}")
        
    def insert_progress_notes(self, therapist_id, client_name, client_id, client_presentation, response_treatment, client_status, risk_assesment):
        if self.connection is None:
            raise Exception("No database connection. Please connect first.")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_query = """
        INSERT INTO progress_notes (therapist_id, client_name, client_id, client_presentation, response_treatment, client_status, risk_assesment, timestamp)
        VALUES (?, ?, ?, ?)
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(insert_query, (
                    therapist_id, client_name, client_id, client_presentation, response_treatment, client_status, risk_assesment, timestamp))
                print("Data successfully submitted to Databricks.")
        except Exception as e:
            raise Exception(f"Failed to insert data: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")