#database_manager.py
#THIS IS DEFINITELY GONNA BE THE MESSIEST FILE BECAUSE I HAVE NEVER USED DATABASES BEFORE AND I'M WORRIED
#IF I TOUCH ANY OF THIS STUFF ITS GONNA SHATTER INTO PIECES OR SOMETHING. IT WORKS THOUGH I THINK.

import mysql.connector

def create_connection():
    connection = mysql.connector.connect(user = 'poochy',passwd = 'Poochy1+1=2', database = 'poochybot')
    print("Connection to MySQL DB successful")
    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    print("Database created successfully")

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    print("Query executed successfully")
    
connection = create_connection()
cursor = connection.cursor()

#create_database_query = "CREATE DATABASE poochy"
#create_database(connection, create_database_query)

create_emotes_table = "CREATE TABLE IF NOT EXISTS emotes (num INT AUTO_INCREMENT PRIMARY KEY, emote_id TEXT NOT NULL, emote_name TEXT,rarity INT)"
create_useremotes_table = """
CREATE TABLE IF NOT EXISTS useremotes (
  user_id TEXT, 
  emote_id TEXT,
  lvl INT
)
"""
create_users_table = "CREATE TABLE IF NOT EXISTS users (user_id TEXT NOT NULL, petname TEXT, referby BOOL,coins INT, last_daily DATE,att_emote TEXT,num_spotlights INT NOT NULL)"
create_channels_table = """
CREATE TABLE IF NOT EXISTS channels (
  server_id TEXT, 
  channel_id TEXT,
  type INT
)
"""
create_bannerdata_table = """
CREATE TABLE IF NOT EXISTS bannerdata (
  id INT AUTO_INCREMENT PRIMARY KEY,
  banner_link TEXT, 
  name TEXT,
  end_date DATE
)
"""

#execute_query(connection, create_emotes_table)
#execute_query(connection, create_useremotes_table)
#execute_query(connection, create_users_table)
#execute_query(connection, create_channels_table)
#execute_query(connection, create_bannerdata_table)

#-----------------GENERAL FUNCTIONS-----------------#
def wipe_table(tbl_name):
    cursor.execute('TRUNCATE TABLE ' + tbl_name)
    connection.commit()
    return(tbl_name + ' has been wiped!')

#------------------USER FUNCTIONS-----------------#
#ARRAY: [user_id, petname, referby, coins, last_daily, att_emote, num_spotlights]
def search_user(user_id):
    sql = 'SELECT * FROM users WHERE user_id = %s'
    val = (str(user_id),)
    cursor.execute(sql, val)
    users_w_id = cursor.fetchall()
    if cursor.rowcount > 0:
        for data in users_w_id:
            return data
    else:
        return ['']
def user():
    sql = 'SELECT * FROM users'
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)
def add_user(user_id):
    sql = 'INSERT INTO users (user_id, coins, num_spotlights) VALUES (%s, %s, %s)'
    val = (str(user_id),0,0)
    cursor.execute(sql, val)
    connection.commit()

def update_value(user_id, param, value):
    sql = 'UPDATE users SET ' + str(param) + ' = %s WHERE user_id = %s'
    val = (value,user_id)
    cursor.execute(sql, val)
    connection.commit()

#-----------------EMOTE FUNCTIONS-----------------#
def search_emotes(param, value):
    sql = 'SELECT * FROM emotes WHERE ' + str(param) + ' = %s'
    val = (value,)
    cursor.execute(sql, val)
    emote_data = cursor.fetchall()
    if cursor.rowcount > 0:
        for data in emote_data:
            return [data[1], data[2], data[3]]
    else:
        return ['','',0]

def get_all_emotes():
    cursor.execute('SELECT * FROM emotes')
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

def get_rare_emotes(rarity):
    sql = 'SELECT * FROM emotes WHERE rarity = %s ORDER BY emote_name'
    val = (rarity,)
    cursor.execute(sql, val)
    emote_data = cursor.fetchall()

    return emote_data

def add_emote_item(emote_id, emote_name, rarity):
    sql = 'INSERT INTO emotes (emote_id, emote_name,rarity) VALUES (%s, %s, %s)'
    val = (emote_id, emote_name, rarity)
    cursor.execute(sql, val)
    connection.commit()

def change_emote_item(emote_id, emote_name, rarity):
    sql = 'UPDATE emotes SET emote_id = %s, emote_name = %s, rarity = %s WHERE emote_id = %s'
    val = (emote_id, emote_name, rarity, emote_id)
    cursor.execute(sql, val)
    connection.commit()
    
def delete_emote_item(emote_id):
    sql = 'DELETE FROM emotes WHERE emote_id = %s'
    val = (emote_id,)
    cursor.execute(sql, val)
    connection.commit()

#-----------------USEREMOTE FUNCTIONS-----------------#
def find_one_emote(user_id, emote_id):
    sql = 'SELECT * FROM useremotes WHERE user_id = %s AND emote_id = %s'
    val = (user_id, emote_id)
    cursor.execute(sql, val)
    users_emotes = cursor.fetchall()
    if cursor.rowcount > 0:
        for data in users_emotes:
            return [data[1],data[2]]
    else:
        return ['','']

def find_users_emotes(user_id):
    if(user_id == ''):
        sql = 'SELECT * FROM useremotes'
        cursor.execute(sql)
    else:
        sql = 'SELECT * FROM useremotes WHERE user_id = %s ORDER BY lvl DESC'
        val = (user_id,)
        cursor.execute(sql, val)
    users_emotes = cursor.fetchall()
    return users_emotes

def add_emote_get(user_id, emote_id):
    sql = 'INSERT INTO useremotes (user_id, emote_id, lvl) VALUES (%s, %s, %s)'
    val = (user_id, emote_id, 1)
    cursor.execute(sql, val)
    connection.commit()

def up_emote_lvl(user_id,emote_id):
    sql = 'UPDATE useremotes SET lvl = lvl + 1 WHERE user_id = %s AND emote_id = %s'
    val = (user_id, emote_id)
    cursor.execute(sql, val)

#-----------------CHANNEL FUNCTIONS-----------------#
#ARRAY [server_id, channel_id, type]
#Channel Types: 0 - None, 1 - Announcement Ch, 2 - Main Bot Ch,3 - Extra Bots Ch
def add_channel(server_id,channel_id,type):
    sql = 'INSERT INTO channels (server_id, channel_id, type) VALUES (%s, %s, %s)'
    val = (server_id,channel_id,type)
    cursor.execute(sql, val)
    connection.commit()

def delete_channel(server_id,channel_id):
    sql = 'DELETE FROM channels WHERE server_id = %s AND channel_id = %s'
    val = (server_id, channel_id)
    cursor.execute(sql, val)
    connection.commit()

def check_for_channel(server_id,channel_id):
    sql = 'SELECT * FROM channels WHERE server_id = %s AND channel_id = %s'
    val = (server_id,channel_id)
    cursor.execute(sql,val)
    channels = cursor.fetchall()
    return cursor.rowcount > 0

def check_for_existence(server_id):
    sql = 'SELECT * FROM channels WHERE server_id = %s'
    val = (server_id,)
    cursor.execute(sql,val)
    channels = cursor.fetchall()
    return(cursor.rowcount > 0)

def get_servers_channels(server_id,type):
    if(type == 0):
        sql = 'SELECT * FROM channels WHERE server_id = %s ORDER BY type'
        val = (server_id,)
        cursor.execute(sql,val)
    else:
        sql = 'SELECT * FROM channels WHERE server_id = %s AND type = %s'
        val = (server_id,type)
        cursor.execute(sql,val)
    channels = cursor.fetchall()
    return channels

def get_channels():
    sql = 'SELECT * FROM channels'
    cursor.execute(sql)
    channels = cursor.fetchall()
    return channels

#-----------------BANNERDATA FUNCTIONS-----------------#
#ARRAY [id, banner_link, name, end_date]

def get_banner():
    sql = 'SELECT * FROM bannerdata ORDER BY id DESC'
    cursor.execute(sql)
    return cursor.fetchall()[0]

def add_banner(img,name,end_date):
    sql = 'INSERT INTO bannerdata (banner_link, name, end_date) VALUES (%s, %s, %s)'
    val = (img, name, end_date)
    cursor.execute(sql,val)
    connection.commit()