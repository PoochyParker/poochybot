#banner_manager.py

import discord, datetime
import database_manager as dm, emotes_manager as em

def add_banner(cont):
    banner_data = cont.split('|')
    print(banner_data[0])
    end_date = datetime.datetime.strptime(banner_data[2], "%m%d%Y").date()
    dm.add_banner(banner_data[0],banner_data[1],end_date)
    return('Alrighty! I have created the **' + banner_data[1] + '** banner, ending on ' + str(end_date))

def show_banner(client): #creates an embed with the current banner data
    banner_data = dm.get_banner()
    print(banner_data[1])
    embed = discord.Embed(title = '*' + banner_data[2] + '* Banner',description = 'Active until: **' + banner_data[3].strftime("%a") + ', ' + banner_data[3].strftime("%B") + ' ' + banner_data[3].strftime("%d") + '**',color = discord.Color.from_rgb(255,20,20), type = 'rich')
    embed.set_image(url = str(banner_data[1]))
    spotlights = dm.get_rare_emotes(6)
    emb_cont = ''
    for emote in spotlights:
        emb_cont += em.id_to_emote(emote[1],client) + ' **' + dm.search_emotes('emote_id',emote[1])[1] + '**\n'
    embed.add_field(name = '**SPOTLIGHT EMOTES (6% CHANCE TO OBTAIN!)**',value = emb_cont,inline = True)
    return(embed)