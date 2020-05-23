#coins_manager.py
#CONTROLS THE GAINING AND REGULATION OF COINS

import discord
from datetime import datetime, timedelta, date
import nickname_manager as nm, database_manager as dm, pulls_manager as pm

coins_added = 5
coins_added_w_nitro = 10
first_coins_added = 20
first_coins_added_w_nitro = 40

#-----------------COMMAND METHODS-----------------#
def daily_coins(message, calling_name): #gives the author a certain amount of coins
    user_data = dm.search_user(message.author.id)
    curr = (datetime.now() + timedelta(hours = 1)).date()
    if user_data[4] is None:
        role = discord.utils.find(lambda r: r.name == '1-Up Booster', message.guild.roles)
        if role in message.author.roles:
                coins = first_coins_added_w_nitro
        else:
            coins = first_coins_added
        new_coins = add_coins(user_data,coins)
        dm.update_value(user_data[0],'last_daily',curr)
        return("Welcome to my Emote Rally," + calling_name + '! As a starting bonus, you get **' + str(coins) + ' Blue Coins <:bluecoin:711090808148721694>**! Now use the command `p!pull 4` to obtain your first emotes!')
    else:
        if curr > user_data[4]:
            role = discord.utils.find(lambda r: r.name == '1-Up Booster', message.guild.roles)
            if role in message.author.roles:
                coins = coins_added_w_nitro
            else:
                coins = coins_added
            new_coins = add_coins(user_data,coins)
            dm.update_value(user_data[0],'last_daily',curr)
            return("Here's your daily " + str(coins) + " Blue Coins <:bluecoin:711090808148721694>," + calling_name + '! You now have **' + str(new_coins) + ' Blue Coins <:bluecoin:711090808148721694>**! Now you can get a pull with the command `p!pull`!')
        else:
            return('Hold up there,' + calling_name + '! Sadly, you have to wait until tomorrow for more Blue Coins <:bluecoin:711090808148721694>...')

def coin_package(message,client):
    ignore_part = 'coins '
    data = nm.crop_out_command(message, ignore_part).split('|')
    id = nm.decompile_name(data[0])
    if dm.search_user(id)[0] == '':
        dm.add_user(id)
    taker = dm.search_user(id)
    try:
        new_coins = add_coins(taker,int(data[1]))
        return('Wow,' + nm.set_calling_name(id,client)  + '! You got a prize of **' + data[1] + ' Blue Coins <:bluecoin:711090808148721694>**! Now you have a total of **' + str(new_coins) + ' Blue Coins <:bluecoin:711090808148721694>**!')
    except:
        return('Careful! You need to make sure that you are using the correct syntax. It should look like `p!give coins [user ping]|[# of coins]`.')

def taxation(message,client):
    ignore_part = 'coins '
    data = nm.crop_out_command(message, ignore_part).split('|')
    id = nm.decompile_name(data[0])
    if dm.search_user(id)[0] == '':
        dm.add_user(id)
    taker = dm.search_user(id)
    try:
        new_coins = add_coins(taker,int(data[1]) * -1)
        return('Removed ' + data[1] + ' Blue Coins <:bluecoin:711090808148721694> from' + nm.set_calling_name(id,client) + "'s account. They now have " + str(new_coins) + ' Blue Coins <:bluecoin:711090808148721694>. Be more careful with your coin-adding next time!')
    except:
        return('Careful,' + calling_name + '! You need to make sure that you are using the correct syntax. It should look like `p!remove coins [user ping]|[# of coins]`.')

def add_coins(user_data,amount):
    new_coins = int(user_data[3]) + amount
    if new_coins < 0:
        new_coins = 0
    dm.update_value(user_data[0],'coins',new_coins)
    return new_coins

def check_coins(author, calling_name): #tells the author how many coins they have
    user_data_for_coins = dm.search_user(author.id)
    return('It looks like you have **' + str(user_data_for_coins[3]) + ' Blue Coins <:bluecoin:711090808148721694>**,' + calling_name + '! You need 5 to make a single pull.')