import mysql.connector

class SQLService:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.db = "crewinsights"
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db
        )
        if self.connection.is_connected():
            print("DB connected")

    def executeQuery(self, query, params):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(str(e))
        finally:
            if self.connection.is_connected():
                self.connection.commit()
                cursor.close()
                self.connection.close()
                print("DB disconnected")

