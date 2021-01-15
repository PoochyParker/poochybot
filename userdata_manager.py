#userdata_manager.py
#STORES THE EMOTES THAT EACH USER HAS OBTAINED

import discord, math
import database_manager as dm, emotes_manager as em, nickname_manager as nm

def get_member_obj(ctx, user): #returns a member object that has the same ID as the given user array
    for member in ctx.guild.members:
            if(str(member.id) == str(user[0])):
                return member

def add_users_pull(user_id, emote_id):
    dm.add_emote_get(user_id,emote_id)

def trade_for_gold(user_id, emote_name, bot):
    copies = 0
    og_emote_data = dm.search_emotes('emote_name', emote_name)
    if(og_emote_data[0] == ''):
        return ('{ping} Oh dear... it appears that no such emote exists, {petname}... Be sure you got the correct emote name! You can find which you have using the p!myemotes command!')
    if(og_emote_data[2] == 9):
        return("{ping} Quit being so cheeky, {petname}! That emote is already gold! What do you want, a Double Gold emote?")
    user_emote_data = dm.find_one_emote(user_id, og_emote_data[0])
    if(og_emote_data[2] == 1): #12 emotes for common, 6 for super, and 3 for ultra/spotlight
        copies = 12
    elif(og_emote_data[2] == 2 or og_emote_data[2] == 3):
        copies = 6
    else:
        copies = 3
    if(user_emote_data[1] < copies):
        return ('{{ping}} Welp... Sorry, {{petname}}, but you need at least {copies} copies of **{emote_name}** to goldify it!'.format(copies = copies, emote_name = emote_name))
    else:
        gold_data = dm.search_emotes('emote_name', emote_name + ' [G]') 
        if(gold_data[0] == ''):
            return ("{ping} Whoops, {petname}, that emote hasn't gotten a GOLD variation yet. Ask <@220390422441230346> to add one!")
        if(check_for_emote(user_id,gold_data[0])):
            lvl_up_emote(user_id,gold_data[0])
        else:
            add_users_pull(user_id,gold_data[0])
        dm.down_emote_lvl(user_id,og_emote_data[0],copies - 1) #Keep at least one copy ultimately
        return ('{{ping}} Allllllllllrighty, {{petname}}! I turned {copies} copies of your **{emote_name}** emote into one extra special GOLDEN **{emote_name}** {emote_itself}!!!'.format(copies = copies - 1, emote_name = emote_name, emote_itself = str(em.id_to_emote(gold_data[0],bot))))

def check_for_emote(user_id, emote_id):
    emote_id = dm.find_one_emote(user_id, emote_id)[0]
    return (emote_id != '')

def return_my_emotes(author, bot, page_num): #Returns an embed of 15 of the user's emotes they have pulled
    if (dm.num_emotes(author.id) < 15):
        page_num = 1
    emotes = dm.find_users_emotes(author.id,page_num)
    embed = discord.Embed(title = "{name}'s Pulled Emotes [Level {lvl}]".format(name = nm.set_embed_calling_name(author,bot),lvl = str(dm.search_user(author.id)[4])),description = "A list of your emotes, including the level of each in parentheses (how many times you have pulled it).\n**PAGE {num}** (Use `p!profile [page #]` to see more emotes)".format(num = page_num),color = discord.Color.from_rgb(69,72,255), type = 'rich')
    embed.set_thumbnail(url = str(author.avatar_url_as(size = 64)))
    if(len(emotes) != 0):
        column_size = int(math.ceil(len(emotes) / 3.0))
        if column_size > 5:
            column_size = 5
        value_cont = ''
        for emote_num in range (1,len(emotes)+1):
            emote = emotes[emote_num - 1] 
            value_cont += str(em.id_to_emote(emote[1],bot)) + ' **' + dm.search_emotes('emote_id',emote[1])[1] + '** *(' + str(emote[2]) + ')*\n'
            if (emote_num % column_size == 0 and emote_num != 0) or emote_num == len(emotes) or column_size == 1:
                    embed.add_field(name = '\u200b',value = value_cont,inline = True)
                    value_cont = ''
    else:
        embed.add_field(name = 'You have yet to pull any emotes.',value = 'Use `p!pull` to get your first!',inline = True)
    return(embed)

def attach_emote(name, author, bot): #Attaches the emote with the corresponding name to their profile
    emote_data = dm.search_emotes('emote_name',name)
    if(emote_data[0] == ''):
        return ('{ping} Oh dear... it appears that no such emote exists, {petname}... Be sure you got the correct emote name! You can find which you have using the p!myemotes command!')
    if(check_for_emote(author.id,emote_data[0])):
        dm.update_value(author.id,'att_emote',emote_data[0])
        return('{{ping}} Alright {{petname}}! You now are wearing the prestigious **{em_name}** {em}! Wear it with pride!'.format(em_name = name, em = em.id_to_emote(emote_data[0],bot)))
    else:
        return ('{ping} Wait a second... seems like you have yet to pull that emote, {petname}... You can only attach emotes you have collected! You can find which you have using the p!myemotes command!')

def post_emote(name, author, start_ping, bot): #posts an emote with the corresponding name
    emote_data = dm.search_emotes('emote_name',name)
    embed = None
    if(emote_data[0] == ''):
        return "{ping} I can't find any emote of the sort, sorry...".format(ping = start_ping), True
    embed = discord.Embed(title = '{name} sent a...'.format(name = author.name),color = discord.Color.from_rgb(255,218,0), type = 'rich')
    if(check_for_emote(author.id,emote_data[0])):
        if(em.id_to_emote(emote_data[0], bot).animated):
            embed.set_image(url = 'https://cdn.discordapp.com/emojis/{id}.gif'.format(id = emote_data[0]))
        else:
            embed.set_image(url = 'https://cdn.discordapp.com/emojis/{id}.png'.format(id = emote_data[0]))
        return embed, False
    else:
        return "{ping} Hold up, you don't have that emote! Check which ones you have in #robotic-operating-buddy with `p!myemotes`.".format(ping = start_ping), True

def emote_package(ctx,given_emote,users): #takes the list of users and gives each of them the given_emote
    num_thru = 0
    em_data = dm.search_emotes('emote_id', str(given_emote.id))
    if(em_data[0] != ''):
        return ('{ping} Oh dear... it appears that no such emote exists, {petname}... Be sure you got the correct emote name! You can find which you have using the p!myemotes command!')
    else:
        for user in users:
            if dm.search_user(user.id)[0] == '':
                dm.add_user(user.id)
            user_data = dm.search_user(user.id)
            try:
                if(check_for_emote(user.id,given_emote.id)):
                    lvl_up_emote(user.id,given_emote.id)
                else:
                    add_users_pull(user.id,given_emote.id)
                num_thru += 1
            except:
                return ('Welp! I was only about to get through the first {num} users on that list... Sorry about that... Make sure the formatting is all correct!'.format(num = num_thru))
        return ('Allllrightly! I gave **{em_name}** {em} to {num} account(s))!'.format(em_name = em_data[1], em = str(given_emote), num = num_thru))
        

def mega_emote_package(ctx,given_emote,bot): #deposits 'given_coins' coins into every user's account
    em_data = dm.search_emotes('emote_id', str(given_emote.id))
    if(em_data[0] == ''):
        return ('{ping} Oh dear... it appears that no such emote exists, {petname}... Be sure you got the correct emote name! You can find which you have using the p!myemotes command!')
    else:
        list_of_users = dm.get_all_users()
        member_obj = None
        for user in list_of_users:
            member_obj = get_member_obj(ctx,user)
            if member_obj:
                user_data = dm.search_user(user[0])
                try:
                    if(check_for_emote(user[0],given_emote.id)):
                        lvl_up_emote(user[0],given_emote.id)
                    else:
                        add_users_pull(user[0],given_emote.id)
                except:
                    return ('Well *something* went wrong!')
        return ("Allllrightly! I gave **{em_name}** {em} to EVERYONE's account".format(em_name = em_data[1], em = str(given_emote)))

def detach_emote(author, bot):
    dm.update_value(author.id,'att_emote','')
    return('{ping} Alright, {petname}! I have removed the attached emote.')

def return_all_emotes_from_all():
    emotes = dm.find_users_emotes('')

def lvl_up_emote(user_id,emote_id):
    dm.up_emote_lvl(user_id,emote_id)
    return 