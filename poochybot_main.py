#poochybot_manager.py
#THE MAIN RUNNER CLASS THAT DOESN'T DO MUCH ITSELF BUT IS WHAT THE COMMAND PROMPT RUNS

import discord, math, typing, os, sys
from discord.ext import commands
from discord.ext.commands import has_permissions
import nickname_manager as nm, coins_manager as cm, emotes_manager as em, database_manager as dm, pulls_manager as pm, userdata_manager as um, channel_manager as chm, help_manager as hm, banner_manager as bm

calling_name = ''
start_ping = ''
good_channels = [689175409883218027,689296251061272648,417918334621712384]
#CHANNEL IDS
#417918334621712384 - #bot-testing on 1UW
#355186664869724161 - #robotic-operating-buddy on 1UW
#689175409883218027 - #bot-testing on PGE
#710060989781114890 - #text on PB-E1
bad_megamote_chhanels = [355119082808541185,687843926937305236]
#355119082808541185 - #off-topic
#687843926937305236 - #serious-discussion

client = discord.Client()
bot = commands.Bot(command_prefix='d!')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name + ' - ID:' + str(bot.user.id))
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Poochy's Emote Rally | Prefix: p!"))
            
#GENERIC COMMANDS##############################
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
#CHECKS########################################
def channel_check():
    async def good_channel(ctx):
        for channel in good_channels:
            if channel == ctx.channel.id:
                return True
        return False
    return commands.check(good_channel)

def megamote_check():
    async def good_channel(ctx):
        for channel in bad_megamote_chhanels:
            if channel == ctx.channel.id:
                return False
        return True
    return commands.check(good_channel)

#COINS#########################################
@bot.command(aliases = ['d'])
@commands.cooldown(1, 60*60*20, commands.BucketType.user) #can only be used every 10 hours
@channel_check()
async def daily(ctx):
    await ctx.send(cm.daily_coins(ctx).format(petname = calling_name, ping = start_ping))
@daily.error
async def toosoon(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('{ping} Hold up there, {petname}! You still have about **{hour} hour(s)** and **{minute} minute(s)** until you can get more Blue Coins <:bluecoin:711090808148721694>!'.format(ping = start_ping, petname = calling_name, hour = int(error.retry_after / 3600), minute = int(error.retry_after / 60) % 60))

@bot.command(aliases = ['c', '$'])
@channel_check()
async def coins(ctx):
    await ctx.send(cm.check_coins(ctx.author).format(petname = calling_name, ping = start_ping))

#BADGE PULLING#################################
@bot.command(aliases = ['p'])
@channel_check()
async def pull(ctx, num = 1):
    if num > 0 and num <= 10:
        await ctx.send(pm.pull(ctx.author.id,bot,num).format(petname = calling_name, ping = start_ping))
    else:
        await ctx.send('{ping} You have to specify how many pulls you want, up to 10! Be sure you have the syntax correct: `p!pull [1-10]`!'.format(ping = start_ping))
@pull.error
async def cantpull(ctx, blank):
    await ctx.send('{ping} You have to specify how many pulls you want, up to 10! Be sure you have the syntax correct: `p!pull [1-10]`!'.format(ping = start_ping))

@bot.command()
@channel_check()
async def goldify(ctx, *, emote_name):
    await ctx.send(um.trade_for_gold(ctx.author.id,emote_name,bot).format(petname = calling_name, ping = start_ping))

#BADGE SHOWCASE################################
@bot.command(aliases = ['myemotes']) #shows an embeded list of the users emotes, 15 at a time; put # after command to show different page
@channel_check()
async def profile(ctx, page: int = 1):
    await ctx.send(embed = um.return_my_emotes(ctx.author,bot,page))

@bot.command(aliases = ['allemotes', 'rarities', 'emotelist'])
@channel_check()
async def emotes(ctx):
    await ctx.send(embed = em.return_all_emotes(bot))

@bot.command(aliases = ['bigemote', 'postemote', 'megaemote'])
@commands.cooldown(1, 60*15, commands.BucketType.user) #can only be used every 15 minutes
@megamote_check()
async def megamote(ctx, *, emote_name):
    await ctx.message.delete()
    post, should_delete = um.post_emote(emote_name, ctx.author, start_ping, bot)
    if should_delete:
        await ctx.send(post, delete_after = 5)
    else:
        await ctx.send(embed = post)
@megamote.error
async def toosoon(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        await ctx.send('{ping} Hold up there! You can post a megamote in about **{minute} minute(s)** and **{second} second(s)**.'.format(ping = start_ping, minute = int(error.retry_after / 60) % 60, second = int(error.retry_after) % 60), delete_after = 5)
    else: 
        await ctx.message.delete()
#PETNAMES / BADGE WEARING######################
@bot.command(aliases = ['setpetname'])
@channel_check()
async def petname(ctx, *, petname):
    await ctx.send(nm.nickname_set(petname, ctx.author))

@bot.command(aliases = ['attachemote','wearemote'])
@channel_check()
async def wear(ctx, *, emote_name):
    await ctx.send(um.attach_emote(emote_name, ctx.author, bot).format(petname = calling_name, ping = start_ping))
@wear.error
async def unwear(ctx, blank):
    await ctx.send(um.detach_emote(ctx.author, bot).format(petname = calling_name, ping = start_ping))

#OTHER########################################
@bot.command()
@channel_check()
async def banner(ctx):
    await ctx.send(embed = bm.show_banner(bot))

@bot.command()
@channel_check()
async def help(ctx, command: str = ''):
    await ctx.send(embed = hm.help_manager(command, bot.user.avatar_url_as(size = 128)))

#MODERATOR-COMMANDS###########################
@bot.command() #Gives a selected list of users the selected amount of coins
@has_permissions(view_audit_log = True)  
async def givecoins(ctx, num_coins: int, members: commands.Greedy[discord.Member]):
    await ctx.send(cm.coin_package(ctx,num_coins,members).format(petname = calling_name, ping = start_ping))

@bot.command() #Removes a selected amount of coins from a list of selected users
@has_permissions(view_audit_log = True)  
async def takecoins(ctx, num_coins: int, members: commands.Greedy[discord.Member]):
    await ctx.send(cm.taxation(ctx,num_coins,members).format(petname = calling_name, ping = start_ping))

@bot.command() #Gives a selected list of users the selected amount of coins
@has_permissions(view_audit_log = True)  
async def giveemote(ctx, emote: discord.Emoji, members: commands.Greedy[discord.Member]):
    await ctx.send(um.emote_package(ctx,emote,members).format(petname = calling_name, ping = start_ping))

@bot.command() #Adds an emote with the rarity and name
@has_permissions(view_audit_log = True)  
async def addemote(ctx, emote: discord.Emoji, rarity: int, *, name):
    await ctx.send(em.add_emote(emote,rarity,name,bot))

@bot.command() #Changes the name or rarity of an already-existing emote in the database; same format as adding one
@has_permissions(view_audit_log = True)  
async def changeemote(ctx, emote: discord.Emoji, rarity: int, *, name):
    await ctx.send(em.change_emote(emote,rarity,name,bot))

@bot.command()
@has_permissions(view_audit_log = True)  
async def addgoldemote(ctx, normEmote: discord.Emoji, goldEmote: discord.Emoji):
    await ctx.send(em.add_gold_emote(normEmote,goldEmote,bot))

@bot.command()
@has_permissions(view_audit_log = True)  
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

#POOCHY COMMANDS#############################
def is_owner(): #Checks if the user of the command is me (Poochybot's owner), via checking ID
    async def owner(ctx):
        return ctx.author.id == 220390422441230346
    return commands.check(owner)

@bot.command() #Gives EVERY user the selected amount of coins (USE WITH CAUTION)
@is_owner()
async def giveeveryonecoins(ctx, num_coins: int):
    await ctx.send(cm.mega_coin_package(ctx,num_coins,bot).format(petname = calling_name, ping = start_ping))

@bot.command() #Gives EVERY user the selected emote (USE WITH CAUTION)
@is_owner()
async def giveeveryoneemote(ctx, emote: discord.Emoji):
    await ctx.send(um.mega_emote_package(ctx,emote,bot).format(petname = calling_name, ping = start_ping))

@bot.command() #Resets Poochybot
@is_owner()
async def powernap(ctx):
    await ctx.send('Time for a powernap!')
    os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)

@bot.command() #Wipes a selected table
@is_owner()
async def wipe(ctx, table):
    await ctx.send(dm.wipe_table(table))

@bot.command() #Sets Poochybot's playing status to [message]
@is_owner()
async def setplaying(ctx, *, message):
    await bot.change_presence(activity = discord.Game(message))

@bot.command() #Creates a new banner with an image, date, and name
@is_owner()
async def newbanner(ctx, link, date, *, name):
    await ctx.send(bm.add_banner(name,date,link))

@bot.command() #Prints out a database
@is_owner()
async def printdatabase(ctx, database):
    dm.print_database(database)

#CHECK#####################################
@bot.check #Various mechanisms Poochybot does upon each command to make sure it can handle every command universally; also checks to not reply to itself
async def base_setup(ctx):
    if(dm.search_user(ctx.author.id)[0] == ''):
        dm.add_user(ctx.author.id)
    global calling_name, start_ping
    start_ping = '[' + nm.compile_name(ctx.author.id) + ']' #ping at the start of each message to alert users
    calling_name = nm.set_calling_name(ctx.author,bot)   #customizable name used 
    return (ctx.author != bot.user)

with open('token2.dat', 'r') as token:
    bot.run(token.readline())