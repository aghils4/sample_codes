import mysql.connector

class MySQLConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Disconnected from MySQL database")

    def insert_data(self, table, data):
        try:
            cursor = self.connection.cursor()
            columns = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            cursor.execute(query, tuple(data.values()))
            self.connection.commit()
            print("Data inserted successfully")
        except mysql.connector.Error as err:
            self.connection.rollback()
            print(f"Error: {err}")
        finally:
            cursor.close()

    def update_data(self, table, update_values, condition):
        try:
            cursor = self.connection.cursor()
            set_clause = ', '.join([f"{key} = %s" for key in update_values.keys()])
            condition_clause = ' AND '.join([f"{key} = %s" for key in condition.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {condition_clause}"
            cursor.execute(query, tuple(update_values.values()) + tuple(condition.values()))
            self.connection.commit()
            print("Data updated successfully")
        except mysql.connector.Error as err:
            self.connection.rollback()
            print(f"Error: {err}")
        finally:
            cursor.close()

    def get_data(self, table, columns=None, condition=None):
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Build the SELECT query
            select_columns = '*'
            if columns:
                select_columns = ', '.join(columns)

            query = f"SELECT {select_columns} FROM {table}"

            if condition:
                condition_clause = ' AND '.join([f"{key} = %s" for key in condition.keys()])
                query += f" WHERE {condition_clause}"

            # Execute the query
            cursor.execute(query, tuple(condition.values()) if condition else None)

            # Fetch all the rows
            result = cursor.fetchall()

            return result

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()