#coins_manager.py
#CONTROLS THE GAINING AND REGULATION OF COINS

import discord
from datetime import datetime, timedelta, date
import nickname_manager as nm, database_manager as dm, pulls_manager as pm, userdata_manager as um

coins_added = 5
first_coins_added = 20

#-----------------COMMAND METHODS-----------------#
def daily_coins(ctx): #gives the author a certain amount of coins
    user_data = dm.search_user(ctx.author.id)
    if user_data[2] is None:
        coins, new_coins = add_coins(user_data,ctx,ctx.author,first_coins_added)
        return('{{ping}} Welcome to my Emote Rally, {{petname}}! As a starting bonus, you get **{coin_num} Blue Coins <:bluecoin:711090808148721694>**! Now use the command `p!pull 4` to obtain your first emotes!'.format(coin_num = coins))
    else:
        coins, new_coins = add_coins(user_data,ctx,ctx.author,coins_added)
        return("{{ping}} Here's your daily **{coin_num} Blue Coins <:bluecoin:711090808148721694>**, {{petname}}! You now have **{tot_coins} Blue Coins <:bluecoin:711090808148721694>**! Now you can get a pull with the command `p!pull`!".format(coin_num = coins,tot_coins = new_coins))

def coin_package(ctx,given_coins,users): #takes the list of users and deposits 'given_coins' coins into their account
    num_thru = 0
    for user in users:
        if dm.search_user(user.id)[0] == '':
            dm.add_user(user.id)
        user_data = dm.search_user(user.id)
        try:
            coins, new_coins = add_coins(user_data,ctx,user,given_coins)
            num_thru += 1
        except:
            return ('Welp! I was only about to get through the first {num} users on that list... Sorry about that... Make sure the formatting is all correct!'.format(num = num_thru))
    return ('Allllrightly! I added **{coin_num} Blue Coins <:bluecoin:711090808148721694>** to {num} account(s) (**{coin_num2}** to Superstars)!'.format(coin_num = given_coins, num = num_thru, coin_num2 = given_coins * 2))

def mega_coin_package(ctx,given_coins,bot): #deposits 'given_coins' coins into every user's account
    list_of_users = dm.get_all_users()
    member_obj = None
    for user in list_of_users:
        member_obj = um.get_member_obj(ctx,user)
        if member_obj:
            coins, new_coins = add_coins(user,ctx,member_obj,given_coins)
    return ("Wew! I added **{coin_num} Blue Coins <:bluecoin:711090808148721694>** to EVERYONE's account (**{coin_num2}** to Superstars)!".format(coin_num = given_coins, coin_num2 = given_coins * 2))

def taxation(ctx,given_coins,users): #takes the list of users and deposits 'coins' about of coins into their account
    num_thru = 0
    for user in users:
        if dm.search_user(user.id)[0] == '':
            dm.add_user(user.id)
        user_data = dm.search_user(user.id)
        try:
            coins, new_coins = add_coins(user_data,ctx,user,given_coins * -1)
            num_thru += 1
        except:
            return ('Welp! I was only about to get through the first {num} users on that list... Sorry about that... Make sure the formatting is all correct!'.format(num = num_thru))
    return ('Removed **{coin_num} Blue Coins <:bluecoin:711090808148721694>** from {num} account(s) (**{coin_num2}** to Superstars). Be more careful with your coin-adding next time!'.format(coin_num = given_coins, num = num_thru, coin_num2 = given_coins * 2))

def add_coins(user_data,ctx,member,amount):
    multi = 1
    role = discord.utils.find(lambda r: r.name == 'Superstar', ctx.guild.roles)
    if role in member.roles:
        multi = 2
    else:
        multi = 1
    added_coins = amount * multi
    new_coins = int(user_data[2]) + added_coins
    if new_coins < 0:
        new_coins = 0
    dm.update_value(str(user_data[0]),'coins',int(new_coins))
    return added_coins, new_coins

def check_coins(author): #tells the author how many coins they have
    user_data = dm.search_user(author.id)
    return('{{ping}} It looks like you have **{coin_num} Blue Coins <:bluecoin:711090808148721694>**, {{petname}}! You need 5 to make a single pull.'.format(coin_num = str(user_data[2])))