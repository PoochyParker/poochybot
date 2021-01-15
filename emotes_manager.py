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
    elif(num == 7):
        return 'Unique'
    elif(num == 8):
        return 'Scavenged'
    elif(num == 9):
        return 'Gold'
    else:
        return ('NO CORRECT RARITY FOUND: ' + str(num))
#-----------------COMMAND METHODS-----------------#
def add_emote(emote, rarity, name, bot):
    if(dm.search_emotes('emote_id',emote.id)[0] == ''):
        dm.add_emote_item(emote.id,name,rarity)
        return(('There you go! I have added the emote **{em_name}** {em} with the rarity **{rar}**!').format(em_name = name, em = str(emote), rar = get_emote_rar(rarity)))
    else:
        return('I found another emote with the ID <{id}> in my database! Try adding a new emote instead.'.format(id = emote.id))

def change_emote(emote, rarity, name, bot):
    if(dm.search_emotes('emote_id',emote.id)[0] != ''):
        dm.change_emote_item(emote.id,name,rarity)
        return(('There you go! I have changed the emote **{em_name}** {em} with the rarity **{rar}**!').format(em_name = name, em = str(emote), rar = get_emote_rar(rarity)))
    else:
        return('I found cannot find any emote with the ID <{id}> in my database! Make sure the ID has been added first.'.format(id = emote.id))

def add_gold_emote(normEmote, goldEmote, bot):
    og_emote_data = dm.search_emotes('emote_id',normEmote.id)
    if(og_emote_data[0] != ''):
        dm.add_emote_item(goldEmote.id,og_emote_data[1] + ' [G]',9)
        return('Alrighty! I have goldified **{em_name}** {em}!'.format(em_name = og_emote_data[1], em = str(goldEmote)))
    else:
        return('I found cannot find any emote with the ID <{id}> in my database! Make sure the ID has been added first.'.format(id = normEmote.id))

def id_to_emote(id, bot):
    emo = bot.get_emoji(int(id))
    if(emo is not None):
        return emo
    else:
        return '[N]'

def emote_to_id(emote_txt):
    thing = emote_txt.split(':')[2]
    return thing[0:len(thing) - 1]

def return_all_emotes(bot):
    embed = discord.Embed(title = 'All Possible Emotes',color = discord.Color.from_rgb(69,72,255), type = 'rich')
    for rar in range(1,7):      
        rar_emotes = dm.get_rare_emotes(rar)
        if(len(rar_emotes) != 0):
            embed.add_field(name = '**__' + get_emote_rar(rar).upper() + ' EMOTES__**',value = '_' + str(pm.get_rars()[rar-1]) + '% chance of pulling_',inline = False)
            column_size = int(math.ceil(len(rar_emotes) / 3.0))
            value_cont = ''
            for emote_num in range (1,len(rar_emotes)+1):
                emote = rar_emotes[emote_num - 1] 
                value_cont += str(id_to_emote(emote[1],bot)) + ' **' + dm.search_emotes('emote_id',emote[1])[1] + '**\n'
                if (emote_num % column_size == 0 and emote_num != 0) or emote_num == len(rar_emotes) or column_size == 1:
                    embed.add_field(name = '\u200b',value = value_cont,inline = True)
                    value_cont = ''
    return(embed)
