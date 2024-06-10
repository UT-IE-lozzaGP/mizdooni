from hashlib import sha256

import requests
import mysql.connector
import re

ENABLE = True


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def insert_to_table_using_api(url, table_name, c):
    is_user_table = table_name == 'user'
    response = requests.get(url)
    data = response.json()

    for i, row in enumerate(data):
        print("row #%d" % i)
        address = row.get('address')
        manager_username = row.get("managerUsername")
        if not is_user_table:
            client_username = row.get("username")
        else:
            client_username = None
        restaurant_name = row.get("restaurantName")
        if is_user_table:
            print(f"username is '{row.get('username')}'")
            print(f"password is '{row.get('password')}'")

        password: str = row.get("password")
        if password is not None:
            password = sha256(password.encode("utf-8")).hexdigest()

        address_id = None
        manager_id = None
        client_id = None
        restaurant_id = None

        if address is not None:
            columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in address.keys())
            values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in address.values())
            address_query = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('address', columns, values)

            print("address query is '%s'" % address_query)
            if ENABLE:
                c.execute(address_query)
                print("address query is executed")

                address_id = c.lastrowid
                print("The ID of the last inserted row is %s" % address_id)

        if manager_username is not None:
            client_query = "SELECT id FROM user WHERE username = '%s';" % manager_username

            print("manager query is '%s'" % client_query)
            if ENABLE:
                c.execute(client_query)
                print("manager query is executed")

                result = c.fetchone()
                if result is not None:
                    manager_id = result[0]
                    print("The ID of the manager is %s" % manager_id)
                else:
                    print("No manager found with the given username")

        if not is_user_table and client_username is not None:
            client_query = "SELECT id FROM user WHERE username = '%s';" % client_username

            print("client query is '%s'" % client_query)
            if ENABLE:
                c.execute(client_query)
                print("client query is executed")

                result = c.fetchone()
                if result is not None:
                    client_id = result[0]
                    print("The ID of the client is %s" % client_id)
                else:
                    print("No client found with the given username")

        if restaurant_name is not None:
            restaurant_query = "SELECT id FROM restaurant WHERE name = '%s';" % str(restaurant_name).replace('\'',
                                                                                                             '\\\'')

            print("restaurant query is '%s'" % restaurant_query)
            if ENABLE:
                c.execute(restaurant_query)
                print("restaurant query is executed")

                result = c.fetchone()
                if result is not None:
                    restaurant_id = result[0]
                    print("The ID of the restaurant is %s" % restaurant_id)
                else:
                    print("No restaurant found with the given name")

        keys = list(row.keys())
        values = list(row.values())

        if table_name.__contains__('table'):
            i = keys.index('managerUsername')
            keys.pop(i)
            values.pop(i)

        columns = ', '.join("`" + str(x) + "`"
                            for x in ['address_id' if y == 'address' else
                                      'manager_id' if y == 'managerUsername' else
                                      'client_id' if not is_user_table and y == 'username' else
                                      'restaurant_id' if y == 'restaurantName' else
                                      'ambience_rate' if y == 'ambianceRate' else
                                      camel_to_snake(y)

                                      for y in keys])
        values = ', '.join("'" + str(x).replace('\'', '\\\'') + "'"
                           for x in [address_id if keys[i] == 'address' else
                                     manager_id if keys[i] == 'managerUsername' else
                                     client_id if not is_user_table and keys[i] == 'username' else
                                     restaurant_id if keys[i] == 'restaurantName' else
                                     password if keys[i] == 'password' else
                                     y

                                     for i, y in enumerate(values)])
        query = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table_name, columns, values)

        print("query is '%s'" % query)
        if ENABLE:
            c.execute(query)
            print("query is executed")


if __name__ == "__main__":
    db = mysql.connector.connect(
        host='localhost',
        port='3333',
        user='mizdooni-admin',
        password='admin56@Mizdooni',
        database='mizdooni'
    )
    cursor = db.cursor()
    print("database is connected")
    try:
        insert_to_table_using_api("http://91.107.137.117:55/users", 'user', cursor)
        insert_to_table_using_api("http://91.107.137.117:55/restaurants", 'restaurant', cursor)
        insert_to_table_using_api("http://91.107.137.117:55/tables", '`table`', cursor)
        insert_to_table_using_api("http://91.107.137.117:55/reviews", '`review`', cursor)
        db.commit()
        print("changes were committed")
    except Exception as e:
        print(e)
        db.rollback()
        print("changes were rolled back")
    finally:
        cursor.close()
        db.close()
        print("database is closed")