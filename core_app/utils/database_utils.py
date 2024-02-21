import mysql.connector

class MySQLCRUD:
    def __init__(self, host, user, password, database, port):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        self.cursor = self.connection.cursor()

    def create(self, table, data):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.cursor.execute(query, tuple(data.values()))
        self.connection.commit()

    def read(self, table, condition=None):
        query = f"SELECT * FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update(self, table, data, condition):
        update_values = ', '.join([f"{key}=%s" for key in data.keys()])
        query = f"UPDATE {table} SET {update_values} WHERE {condition}"
        self.cursor.execute(query, tuple(data.values()))
        self.connection.commit()

    def delete(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.cursor.execute(query)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
