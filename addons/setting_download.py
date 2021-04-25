import settings
import mysql.connector
import json


def download_settings(gid, module_name):
    """
    :param gid: DISCORD GUILD ID
    :param module_name: MODULE NAME IN DATABASE
    :return: ARRAY WITH SETTINGS
    """
    # DATABASE CONFIG DONWLOAD
    mydb = mysql.connector.connect(
        host=settings.db_adres,
        user=settings.db_login,
        password=settings.db_password,
        database=settings.db_base
    )
    mycursor = mydb.cursor()
    sql = "SELECT data FROM bot_server_settings WHERE dc_guild_id = %s AND module_name = %s"
    mycursor.execute(sql, (gid, module_name,))
    myresult = mycursor.fetchone()

    # empty check
    if myresult is None:
        return None

    # data convert
    for a in myresult:
        data = json.loads(a)
        return data


def update_settings(gid, module_name, variable, value):
    """
    :param gid: Discord guild id
    :param module_name: Module name id database
    :param variable: Name of variable to be updated
    :param value: Value of this variable
    :return: True or False
    """
    # DATABASE CONFIG DONWLOAD
    mydb = mysql.connector.connect(
        host=settings.db_adres,
        user=settings.db_login,
        password=settings.db_password,
        database=settings.db_base
    )
    mycursor = mydb.cursor()
    sql = "SELECT data FROM bot_server_settings WHERE dc_guild_id = %s AND module_name = %s"
    mycursor.execute(sql, (gid, module_name,))
    myresult = mycursor.fetchone()
    if myresult == None:
        # create json and push to it
        value_data = {variable: value}
        encoded_json = json.dumps(value_data)
        print(encoded_json)

        # safe convert
        gid = str(gid)
        module_name = str(module_name)
        encoded_json = str(encoded_json)

        # add record to database
        sql = "INSERT INTO `bot_server_settings` (`id`, `dc_guild_id`, `module_name`, `data`) VALUES (NULL, %s, %s, %s)"
        mycursor.execute(sql, (gid, module_name, encoded_json))
        mydb.commit()
    else:
        # update detected record in database

        # update json
        encoded_json = json.loads(myresult[0])
        update_record = {variable: value}
        encoded_json.update(update_record)
        encoded_json = json.dumps(encoded_json)

        # safe convert
        gid = str(gid)
        module_name = str(module_name)
        encoded_json = str(encoded_json)

        print(encoded_json)
        # mysql update
        sql = "UPDATE `bot_server_settings` SET `data` = %s WHERE `bot_server_settings`.`dc_guild_id` = %s AND `bot_server_settings`.`module_name` = %s"
        mycursor.execute(sql, (encoded_json, gid, module_name))
        mydb.commit()


