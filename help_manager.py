#help_manager.py

import discord

def help_manager(command, icon): #The laziest command : )
    title = command
    syntax = ''
    aliases = ''
    desc = ''
    if(command == 'petname'):
        syntax = 'p!petname [name]'
        aliases = '`p!setpetname`'
        desc = 'Sets a string that PoochyBot will refer you by. It can be up to 30 characters long on a single line. To remove your petname, simply leave the [name] space blank.'
    elif(command == 'wear'):
        syntax = 'p!wear [emote name]'
        desc = 'Appends an emote you have previously pulled using `p!pull` to the end of your petname. **You must use the name that the emote is referred to by in `p!profile`.** To detach your emote, simply leave the [emote name] space blank.'
    elif(command == 'coins'):
        syntax = 'p!coins'
        aliases = '`p!c`, `p!$`'
        desc = 'Shows how many Blue Coins you currently have.'
    elif(command == 'pull'):
        syntax = 'p!pull [number between 1 & 10]'
        aliases = '`p!p`'
        desc = 'You can pull up to 10 emotes at once, each pull costing 5 Blue Coins.'
    elif(command == 'goldify'):
        syntax = 'p!goldify [emote name]'
        desc = 'Turns a number of copies of 1 emote into a Golden version of said emote. Common emotes require 12 copies, Super require 6, and Ultra/Spotlight require 3. **You must use the name that the emote is referred to by in `p!profile`.**'
    elif(command == 'profile'):
        syntax = 'p!profile [page number]'
        aliases = '`p!myemotes`'
        desc = 'Shows a list of up to 15 emotes you have obtained, sorted by the number of copies you have. If you have pulled more than 15 emotes, you can see more emotes by changing the [page number]. The number next to the emote name is how many copies of that emote you have.'
    elif(command == 'emotes'):
        syntax = 'p!emotes'
        aliases = '`p!allemotes`, `p!rarities`, `p!emotelist`'
        desc = 'Posts a list of every emote available to pull, sorted by rarity.'
    elif(command == 'megamote'):
        syntax = 'p!megamote [emote name]'
        aliases = '`p!bigemote`, `p!postemote`, `p!megaemote`'
        desc = 'Posts a larger version of the emote with [emote name]. **You must use the name that the emote is referred to by in `p!profile`.** You may only use this command every 15 minutes, even if you misspell the emote name. This command can be used in every channel except #off-topic and #serious-discussion, but please use it in moderation!'
    elif(command == 'daily'):
        syntax = 'p!daily'
        aliases = '`p!d`'
        desc = 'Gives you 5 Blue Coins once every 20 hours. If you are a Superstar booster on 1-Up World, you get 10 Blue Coins instead!'
    elif(command == 'banner'):
        syntax = 'p!banner'
        desc = 'Gives details on the currently-running banner, including the Spotlight emotes and how long it runs.'
    else:
        embed = discord.Embed(title = "Poochy's Available Commands",description = "The list of commands available for PoochyBot, the runner of **Poochy's Emote Rally**. For specific details on any command, use `p!help [command name]`!.",color = discord.Color.from_rgb(87,212,58), type = 'rich')
        embed.set_thumbnail(url = str(icon))
        embed.add_field(name = '**USER COMMANDS**',value = '`p!petname`\n`p!wear`\n`p!coins`',inline = False)
        embed.add_field(name = '**EMOTE COMMANDS**',value = '`p!pull`\n`p!goldify`\n`p!profile`\n`p!emotes`\n`p!megamote`',inline = False)
        embed.add_field(name = '**OTHER COMMANDS**',value = '`p!daily`\n`p!banner`',inline = False)
        return(embed)
    embed = discord.Embed(title = 'p!' + title + ' Information',description = '\u200b',color = discord.Color.from_rgb(255,128,248), type = 'rich')
    embed.set_thumbnail(url = str(icon))
    embed.add_field(name = '**SYNTAX**',value = '`' + syntax + '`',inline = False)
    if(aliases != ''):
        embed.add_field(name = '**ALIASES**',value = aliases,inline = False)
    embed.add_field(name = '**DESCRIPTION**',value = desc,inline = False)
    return(embed)