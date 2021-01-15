#banner_manager.py

import discord, datetime
import database_manager as dm, emotes_manager as em

def add_banner(name, date, link): #creates a banner with the corresponding name, date, and link
    end_date = datetime.datetime.strptime(date, "%m%d%Y").date()
    dm.add_banner(link,name,end_date)
    return('Alrighty! I have created the **{banner_name}** banner, ending on {endate}'.format(banner_name = name, endate = end_date))

def show_banner(client): #creates an embed with the current banner data
    banner_data = dm.get_banner()
    embed = discord.Embed(title = '*' + banner_data[2] + '* Banner',description = 'Active until: **' + banner_data[3].strftime("%a") + ', ' + banner_data[3].strftime("%B") + ' ' + banner_data[3].strftime("%d") + '**',color = discord.Color.from_rgb(255,20,20), type = 'rich')
    embed.set_image(url = str(banner_data[1]))
    spotlights = dm.get_rare_emotes(6)
    emb_cont = ''
    for emote in spotlights:
        emb_cont += em.id_to_emote(emote[1],client) + ' **' + dm.search_emotes('emote_id',emote[1])[1] + '**\n'
    embed.add_field(name = '**SPOTLIGHT EMOTES (6% CHANCE TO OBTAIN!)**',value = emb_cont,inline = True)
    return(embed)