import sys

from PIL import Image
import io

from mysql import connector

mydb = connector.connect(
    host="localhost",
    user="username",
    passwd="user_pass",
    database="database_name"
)

mycursor = mydb.cursor()


def insert_first_data(data_, table):
    for data in data_:
        try:
            data_for_insert = tuple(data.values())
            sql_statement = f"INSERT INTO `{table}` VALUES (NULL, %s, %s, %s, %s, NULL, NULL, NULL, %s)"
            mycursor.execute(sql_statement, data_for_insert)
            mydb.commit()
        except Exception as err:
            if (err.__str__()[:4]) == '1062':
                print("Warning: trying to insert an existing book (was missed)")
            else:
                print(data.values())
                sys.exit('Error while inserting data')


def insert_second_data(data_, table, link_):
    try:
        data_for_insert = (*data_, link_)
        sql_statement = f"UPDATE {table} SET genre = %s, description = %s, preview = %s WHERE link = %s;"
        mycursor.execute(sql_statement, data_for_insert)
        mydb.commit()
    except Exception as err:
        print(err.__str__())
        sys.exit('Error while changing data')


def get_image():
    query = ("SELECT preview FROM info WHERE id = 78325")
    mycursor.execute(query)
    for preview in mycursor:
        stream = io.BytesIO(preview[0])
        img = Image.open(stream)
        img.show()

def get_link_where_is_null(table, site_name):
    query = f'SELECT link FROM {table} WHERE genre is NULL and site_name = "{site_name}" limit 1;'
    mycursor.execute(query)
    res = mycursor.fetchone()
    if res is None:
        return None
    else:
        return res[0]
# GRANT ALL PRIVILEGES ON books_db.* TO 'ivan'@'%' WITH GRANT OPTION;
