#EMOTE_METHODS.PY

import discord
import emote as em, database_manager

emote_rarities = {
    1 : '★☆☆☆☆',
    2 : '★★☆☆☆',
    3 : '★★★☆☆',
    4 : '★★★★☆',
    5 : '★★★★★'
}

def id_to_emote(id, bot):
    emote = bot.get_emoji(id)
    if(emote is not None):
        return emo
    else:
        return '[N]'

def emote_to_id(emote_txt):
    thing = emote_txt.split(':')[2]
    return thing[0:len(thing) - 1]

def return_emote_list(emotes_dict, bot, rarity): #Returns list of emotes of a certain rarity
    embed = discord.Embed(title = 'AVAILABLE ' + emote_rarities[rarity] + ' EMOTES', description = '', color = discord.Color.from_rgb(69,72,255), type = 'rich')
    emotes_list = database_manager.get_rarity(rarity)
    column_size = int(math.ceil(len(rar_emotes) / 3.0))
    value_cont = ''

    for emote_num in range (0, len(emotes_list)):
        emote = emotes_list[emote_num]

        if (emotes_dict[emote[0]].is_spotlight == True):    #Spotlight emotes are bolded; unpullable emotes are italicized; standard emotes have no added emphasis
            emphasis = '**'
        elif (emotes_dict[emote[0]].is_in_pool == False):
            emphasis = '*'
        else:
            emphasis = ''

        value_cont += str(id_to_emote(emote[0],bot)) + ' ' + emphasis + emotes_dict[emote[0]].name + emphasis + '\n'
        if (emote_num % column_size == 0 and emote_num != 0) or emote_num == len(rar_emotes) or column_size == 1:
            embed.add_field(name = '\u200b',value = value_cont,inline = True)
            value_cont = ''

    return embed

def add_gold_emote(emotes_dict, old_emote, gold_emote_id, bot): #Adds a golden version of the emote into Poochybot's servers
    if (emotes_dict.get(old_emote.id) is None):
        return False
    emotes_dict[gold_emote_id] = em.Emote(gold_emote_id, old_emote.name + '~G', old_emote.rarity, False, False)
    return True


