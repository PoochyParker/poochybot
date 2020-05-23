#poochybot_manager.py
#THE MAIN RUNNER CLASS THAT DOESN'T DO MUCH ITSELF BUT IS WHAT THE COMMAND PROMPT RUNS

import discord, numpy as np, os, sys
import nickname_manager as nm, coins_manager as cm, emotes_manager as em, database_manager as dm, pulls_manager as pm, userdata_manager as um, channel_manager as chm, help_manager as hm, banner_manager as bm

poochys_id = '220390422441230346'
start_ping = ''

client = discord.Client()
#bot = commands.Bot(command_prefix='p!')
            

def crop_out_command(content, ignore_part): #removes a length of 'ignore_part' from str 'content'
    return content[len(ignore_part):len(content)]
def limit_cont(base_username,num): #limits str to 1 line of <= 30 chars
    new_username = base_username.split('\n')[0]
    return new_username[0:num]
def is_number(s): #credit to Daniel Goldberg on Stack Exchange
    try:
        int(s)
        return True
    except ValueError:
        return False

@client.event
async def on_message(message):
    if message.author == client.user: #assures poochybot cannot reply to itself
        return
    if(message.content.lower().startswith('p!') == False):
        return
    if (chm.look_for_channel(message.guild.id,message.channel.id) == True):
        return
    if(dm.search_user(message.author.id)[0] == ''):
        dm.add_user(message.author.id)
    calling_name = nm.set_calling_name(message.author.id,client = client)
    start_ping = '[' + nm.compile_name(message.author.id) + '] '
    mod_role = discord.utils.find(lambda r: r.name == 'Moderator', message.guild.roles)
    if message.content.lower().startswith('p!test'):
        ignore_part = 'p!test '
        com_mod = nm.crop_out_command(message.content,ignore_part)
        await message.channel.send(nm.decompile_name(com_mod))
#-----------------NICKNAME_MANAGER.PY-----------------#
    if message.content.lower().startswith('p!setpetname'):
        ignore_part = 'p!setpetname '
        com_mod = nm.crop_out_command(message.content,ignore_part)
        await message.channel.send(nm.nickname_set(com_mod, message.author))
    if message.content.lower().startswith('p!togglepetname'): #toggles whether the user is referred to by their petname 
        ignore_part = 'p!togglepetname '
        await message.channel.send(nm.nickname_toggle(message.author))
    if message.content.lower().startswith('p!wear'): #attaches an emote onto the user's petname
        ignore_part = 'p!wear '
        com_mod = nm.crop_out_command(message.content,ignore_part)
        await message.channel.send(um.attach_emote(com_mod, message.author, client))
    if message.content.lower().startswith('p!remove'): #removes an emote from the user's pername
        ignore_part = 'p!remove '
        await message.channel.send(um.detach_emote(message.author.id, client))
#-----------------COINS_MANAGER.PY-----------------#
    if message.content.lower().startswith('p!daily'): #allows the user to obtain their daily coins
        ignore_part = 'p!daily '
        await message.channel.send(start_ping + cm.daily_coins(message,calling_name))
    if message.content.lower().startswith('p!coins'): #allows the user to check how many coins they have
        ignore_part = 'p!coins '
        await message.channel.send(start_ping + cm.check_coins(message.author,calling_name))
#-----------------PULLS_MANAGER.PY-----------------#
    if message.content.lower().startswith('p!pull'):
        ignore_part = 'p!pull '
        com_mod = nm.crop_out_command(message.content,ignore_part)
        if com_mod is not None and is_number(com_mod) and int(com_mod) <= 10 and int(com_mod) > 0:
            await message.channel.send(start_ping + pm.pull(message,calling_name,client,int(com_mod)))
        elif com_mod.strip() == '':
            await message.channel.send(start_ping + pm.pull(message,calling_name,client,1))
        else:
            await message.channel.send(start_ping + 'You have to specify how many pulls you want, up to 10! Be sure you have the syntax correct: `p!pull [1-10]`!')
    if message.content.lower().startswith('p!myemotes') or message.content.lower().startswith('p!profile'):
        ignore_part = 'p!myemotes '     
        await message.channel.send(embed = um.return_all_emotes(message.author,client))
    if message.content.lower().startswith('p!allemotes'):
        ignore_part = 'p!allemotes '    
        await message.channel.send(embed = em.return_all_emotes(client))
    if message.content.lower().startswith('p!banner'):
        ignore_part = 'p!banner '   
        await message.channel.send(embed = bm.show_banner(client))
#-----------------HELP_MANAGER.PY-----------------#
    if message.content.lower().startswith('p!help'):
        ignore_part = 'p!help '     
        await message.channel.send(embed = hm.help_manager(nm.crop_out_command(message.content,ignore_part),client.user))
#-----------------MODERATOR ONLY COMMANDS-----------------#
    if mod_role in message.author.roles or str(message.author.id) == poochys_id:
        if message.content.lower().startswith('p!announce'): #quotes the forthcoming message in a preset channel
            ignore_part = 'p!announce '
            ann_ch = chm.get_channel(message.guild.id,1)
            if(ann_ch == ''):
                await message.channel.send(start_ping + 'You have yet to set an announcement channel,' + calling_name + '! Where am I supposed to go?')
            else:
                await client.get_channel(ann_ch).send(nm.crop_out_command(message.content,ignore_part))
        if message.content.lower().startswith('p!emote'):
            ignore_part = 'p!emote '
            com_mod = nm.crop_out_command(message.content,ignore_part)
            if com_mod.lower().startswith('add'): #adds a new emote with the format id|name|rarity
                await message.channel.send(start_ping + em.add_emote(com_mod,calling_name,client))
            if com_mod.lower().startswith('get'): #obtains an emote from the list
                await message.channel.send(start_ping + em.get_emote(com_mod,calling_name))
            if com_mod.lower().startswith('update'): #updates an emote with the format id|name|rarity
                await message.channel.send(start_ping + em.change_emote(com_mod,calling_name,client))
            if com_mod.lower().startswith('delete'): #deletes an emote from the list
                await message.channel.send(start_ping + em.delete_emote(com_mod,calling_name))
        if message.content.lower().startswith('p!give'): #gives a selected user something
            ignore_part = 'p!give '
            com_mod = nm.crop_out_command(message.content,ignore_part)
            if com_mod.lower().startswith('coins'):
                await client.get_channel(chm.get_channel(message.guild.id,2)).send(cm.coin_package(com_mod,client))
        if message.content.lower().startswith('p!remove'): #removes something from a selected user
            ignore_part = 'p!remove '
            com_mod = nm.crop_out_command(message.content,ignore_part)
            if com_mod.startswith('coins'):
                await message.channel.send(cm.taxation(com_mod,client))
        if message.content.lower().startswith('p!setchannel'):
            ignore_part = 'p!setchannel '   
            com_mod = nm.crop_out_command(message.content,ignore_part)
            await message.channel.send(chm.channel_creation(message.guild.id,com_mod,calling_name))
        if message.content.lower().startswith('p!unsetchannel'):
            ignore_part = 'p!unsetchannel ' 
            com_mod = nm.crop_out_command(message.content,ignore_part)
            await message.channel.send(chm.channel_deletion(message.guild.id,com_mod,calling_name))
        if message.content.lower().startswith('p!channels'):
            ignore_part = 'p!channels ' 
            await message.channel.send(chm.channel_log(message.guild.id))
#-----------------POOCHY ONLY COMMANDS-----------------#
    if str(message.author.id) == poochys_id:
        if message.content.startswith('p!goodnight'): #shuts off poochybot
            await message.channel.send('ZZZZZZZZZZZZZZZZZZZZZZZZzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz............')
            #exit()
        if message.content.startswith('p!powernap'): #restarts poochybot, credit goes to Justin G. on Stack Overflow
            await message.channel.send('Time for a powernap!')
            os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)
        if message.content.lower().startswith('p!status'):
            dm.user()  
            dm.get_all_emotes()
        if message.content.startswith('p!allpulls'):
            ignore_part = 'p!allpulls '
            um.return_all_emotes_from_all()
            await message.channel.send(start_ping + 'Obtained a list of **EVERY** emote!')
        if message.content.startswith('p!wipe'): #wipes a table with the following name
            ignore_part = 'p!wipe '
            com_mod = nm.crop_out_command(message.content,ignore_part)
            await message.channel.send(start_ping + dm.wipe_table(com_mod))
        if message.content.startswith('p!findallchannels'):
            ignore_part = 'p!findallchannels '
            chm.return_all_channels_test()
        if message.content.startswith('p!setplaying'):
            ignore_part = 'p!setplaying '
            com_mod = nm.crop_out_command(message.content,ignore_part)
            game = discord.Game(com_mod)
            await client.change_presence(status=discord.Status.idle, activity=game)
        if message.content.startswith('p!newbanner'):
            ignore_part = 'p!newbanner '
            com_mod = nm.crop_out_command(message.content,ignore_part)
            await message.channel.send(bm.add_banner(com_mod))
#@bot.check
#async def dont_reply_to_self(ctx):
#    return ctx.author is not client.user

#@bot.command
#async def daily(ctx):
#   await ctx.send(start_ping + cm.daily_coins(ctx.author,calling_name))

#@bot.command
#async def test(ctx, arg):
#    await ctx.send(arg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name + ' - ID:' + str(client.user.id))
    print('------')

with open('token.dat', 'r') as token:
    client.run(token.readline())