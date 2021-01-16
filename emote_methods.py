#EMOTE_METHODS.PY

import discord

def id_to_emote(id, bot):
    emote = bot.get_emoji(id)
    if(emote is not None):
        return emo
    else:
        return '[N]'

def emote_to_id(emote_txt):
    thing = emote_txt.split(':')[2]
    return thing[0:len(thing) - 1]