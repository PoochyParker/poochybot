#userdata_manager.py
#STORES THE EMOTES THAT EACH USER HAS OBTAINED

import discord, math
import database_manager as dm, emotes_manager as em, nickname_manager as nm

def add_users_pull(user_id, emote_id):
    dm.add_emote_get(user_id,emote_id)

def check_for_emote(user_id, emote_id):
    emote_id = dm.find_one_emote(user_id, emote_id)[0]
    return (emote_id != '')

def return_all_emotes(author, client):
    emotes = dm.find_users_emotes(author.id)
    embed = discord.Embed(title = nm.set_embed_calling_name(author,client) + "'s Pulled Emotes [" + str(dm.search_user(author.id)[6]) + ']',description = "A list of your emotes, including the level of each in parentheses (how many times you have pulled it).",color = discord.Color.from_rgb(69,72,255), type = 'rich')
    embed.set_thumbnail(url = str(author.avatar_url_as(size = 64)))
    if(len(emotes) != 0):
        column_size = int(math.ceil(len(emotes) / 3.0))
        if column_size > 20:
            column_size = 20
        value_cont = ''
        for emote_num in range (1,len(emotes)+1):
            emote = emotes[emote_num - 1] 
            value_cont += em.id_to_emote(emote[1],client) + ' **' + dm.search_emotes('emote_id',emote[1])[1] + '** *(' + str(emote[2]) + ')*\n'
            if (emote_num % column_size == 0 and emote_num != 0) or emote_num == len(emotes) or column_size == 1:
                    embed.add_field(name = '\u200b',value = value_cont,inline = True)
                    value_cont = ''
        return(embed)


def attach_emote(name, author, client):
    emote_data = dm.search_emotes('emote_name',name)
    if(emote_data[0] == ''):
        return ('Oh dear... it appears that no such emote exists,' + nm.set_calling_name(author.id,client) + '... Be sure you got the correct emote name! You can find which you have using the p!myemotes command!')
    if(check_for_emote(author.id,emote_data[0])):
        dm.update_value(author.id,'att_emote',emote_data[0])
        return('Alright' + nm.set_calling_name(author.id,client) + '! You now are wearing the prestigious **' + name + '** ' + em.id_to_emote(emote_data[0],client) + '! Wear it with pride!')
    else:
        return ('Wait a second... seems like you have yet to pull that emote,' + nm.set_calling_name(author.id,client) + '... You can only attach emotes you have collected! You can find which you have using the p!myemotes command!')

def detach_emote(id, client):
    dm.update_value(id,'att_emote','')
    return('Alright,' + nm.set_calling_name(id,client) + '! I have removed the attached emote.')

def return_all_emotes_from_all():
    emotes = dm.find_users_emotes('')

def lvl_up_emote(user_id,emote_id):
    dm.up_emote_lvl(user_id,emote_id)
    return 