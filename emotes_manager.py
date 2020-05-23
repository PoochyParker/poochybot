#emotes_manager.py

import discord, math
import database_manager as dm, nickname_manager as nm, pulls_manager as pm

#RARITY GUIDE: 0 - Unique, 1 - Common, 2 - Super, 3 - Super (Animated), 4 - Ultra, 5 - Ultra (Animated), 6 - Spotlight

def get_emote_rar(num):
    if(num == 0):
        return 'Unique'
    if(num == 1):
        return 'Common'
    elif(num == 2):
        return 'Super'
    elif(num == 3):
        return 'Super (Animated)'
    elif(num == 4):
        return 'Ultra'
    elif(num == 5):
        return 'Ultra (Animated)'
    elif(num == 6):
        return 'Spotlight'
    else:
        return ('NO CORRECT RARITY FOUND: ' + str(num))
#-----------------COMMAND METHODS-----------------#
def add_emote(message, calling_name, client):
    ignore_part = 'add '
    emote_data = nm.crop_out_command(message, ignore_part).split('|')
    emote_data[0] = emote_to_id(emote_data[0])
    if(dm.search_emotes('emote_id',emote_data[0])[0] == ''):
        dm.add_emote_item(emote_data[0],emote_data[1],int(emote_data[2]))
        return('There you go,' + calling_name + '! I have added the badge **' + emote_data[1] + '** ' + id_to_emote(emote_data[0],client) + ' with the rarity **' + get_emote_rar(int(emote_data[2])) + '**!')
    else:
        return('I found another emote with the ID <' + emote_data[0] + '> in my database,' + calling_name + '! Try adding a new emote instead.')

def get_emote(message, calling_name):
    ignore_part = 'get '
    id = emote_to_id(nm.crop_out_command(message, ignore_part))
    emote_data = dm.search_emotes('emote_id',id)
    if(emote_data[0] == ''):
        return('Sorry,' + calling_name + '! I cannot find an emote with the ID: <' + id + '> anywhere...')
    else:
        return('Alright,' + calling_name + '! According to my records, I have an emote with the ID: <' + id + '>, the name: **' + emote_data[1] + '**, and the **' + get_emote_rar(emote_data[2]) + '** rarity!')

def delete_emote(message, calling_name):
    ignore_part = 'delete '
    id = emote_to_id(nm.crop_out_command(message, ignore_part))
    dm.delete_emote_item(id)
    return('There we go, ' + calling_name + '! I deleted the emote with the ID: <' + id + '> from my database.')

def change_emote(message, calling_name, client):
    ignore_part = 'update '
    emote_data = nm.crop_out_command(message, ignore_part).split('|')
    emote_data[0] = emote_to_id(emote_data[0])
    if(dm.search_emotes('emote_id',emote_data[0])[0] == ''):
        return('I found cannot find any emote with the ID <' + emote_data[0] + '> in my database,' + calling_name + '! Make sure the ID has been added first with p!emote showall.')
    else:
        dm.change_emote_item(emote_data[0],emote_data[1],int(emote_data[2]))
        return('There you go,' + calling_name + '! I have changed the badge **' + emote_data[1] + '** (ID: ' + emote_data[0] + ') with the rarity **' + get_emote_rar(int(emote_data[2])) + '**!')

def id_to_emote(id, client):
    for x in client.emojis:
        if(x.id == int(id)):
            return str(x)
    return '[NO EMOTE FOUND]'

def emote_to_id(emote_txt):
    thing = emote_txt.split(':')[2]
    print(thing)
    return thing[0:len(thing) - 1]

def return_all_emotes(client):
    embed = discord.Embed(title = 'All Possible Emotes',color = discord.Color.from_rgb(69,72,255), type = 'rich')
    for rar in range(1,7):      
        rar_emotes = dm.get_rare_emotes(rar)
        if(len(rar_emotes) != 0):
            embed.add_field(name = '**__' + get_emote_rar(rar).upper() + ' EMOTES__**',value = '_' + str(pm.get_rars()[rar-1]) + '% chance of pulling_',inline = False)
            column_size = int(math.ceil(len(rar_emotes) / 3.0))
            value_cont = ''
            for emote_num in range (1,len(rar_emotes)+1):
                emote = rar_emotes[emote_num - 1] 
                #print(emote)
                #print('Emote Num: ' + str(emote_num) + ' | Col Size: ' + str(column_size))
                value_cont += id_to_emote(emote[1],client) + ' **' + dm.search_emotes('emote_id',emote[1])[1] + '**\n'
                if (emote_num % column_size == 0 and emote_num != 0) or emote_num == len(rar_emotes) or column_size == 1:
                    embed.add_field(name = '\u200b',value = value_cont,inline = True)
                    value_cont = ''
    return(embed)
