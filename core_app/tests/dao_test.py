from core_app.utils import database_utils

db = database_utils.MySQLCRUD(host='localhost', user='root', password='xxx', database='city_disaster_response', port='3306')
result = db.read(table='incident')
print("Data from the table:")
for row in result:
    print(row)


## use example:
# create_table_query = """
# CREATE TABLE IF NOT EXISTS example_table (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255),
#     age INT
# );
# """
# db.cursor.execute(create_table_query)
# db.connection.commit()
#
# data_to_insert = {'name': 'John Doe', 'age': 30}
# db.create(table='example_table', data=data_to_insert)
#
# result = db.read(table='example_table')
# print("Data from the table:")
# for row in result:
#     print(row)
#
# update_data = {'age': 31}
# db.update(table='example_table', data=update_data, condition='name="John Doe"')
#
#
# result_after_update = db.read(table='example_table')
# print("Data after update:")
# for row in result_after_update:
#     print(row)
#
# db.delete(table='example_table', condition='name="John Doe"')
#
# db.close()