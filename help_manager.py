#help_manager.py

import discord

def help_manager(cont,self):
    title = cont
    syntax = ''
    desc = ''
    if(cont == 'daily'):
        syntax = 'p!daily'
        desc = 'Allows you to obtain Blue Coins once per day, resetting at midnight Central Time. By default, you get 5 Blue Coins, but **Nitro Server Boosters** get 10 Blue Coins instead. Your first time doing so, you get a one-time bonus of 20 Blue Coins.'
    elif(cont == 'coins'):
        syntax = 'p!coins'
        desc = 'Allows you to see how many Blue Coins you have obtained.'
    elif(cont == 'pull'):
        syntax = 'p!pull [number between 1 & 10]'
        desc = 'Allows you to pull up to 10 emotes at once, each pull costing 5 Blue Coins. There is no benefit regarding which emotes you obtain for pulling for multiple at once, its simply for convenience.'
    elif(cont == 'myemotes'):
        syntax = 'p!myemotes'
        desc = 'Allows you to see a list of every emote you have obtained. The number next to them is the level of the emote, which increases each time you pull a duplicate emote.'
    elif(cont == 'allemotes'):
        syntax = 'p!allemotes'
        desc = 'Allows you to see a list of every emote available to pull using `p!pull`, sorted by rarity. Additionally, it shows the chance of obtaining each rarity level when you pull.'
    elif(cont == 'setpetname'):
        syntax = 'p!setpetname [petname]'
        desc = 'Allows you to set a string that Poochy will refer you to in every interaction. It can be up to 30 characters long on a single line. If you have set it so that Poochy will not refer to you by a petname, changing it will automatically make Poochy refer to you by it.'
    elif(cont == 'togglepetname'):
        syntax = 'p!togglepetname'
        desc = 'Allows you to toggle whether Poochy refers to you by the petname you have set.'
    elif(cont == 'wear'):
        syntax = 'p!wear [name of emote]'
        desc = 'Allows you to append an emote you have previously pulled using `p!pull` to the end of your petname. **You must use the name that the emote is referred to by when you pull it.** To find this name, use `p!myemotes`.'
    elif(cont == 'remove'):
        syntax = 'p!remove'
        desc = 'Takes the appended emote off the end of your petname if you previously had one.'
    elif(cont == 'banner'):
        syntax = 'p!banner'
        desc = 'Allows you see the details on the currently-running banner, including the Spotlight emotes and how long it runs until.'
    else:
        embed = discord.Embed(title = "Poochy's Available Commands",description = "The list of commands available for Poochy, a 1-Up World bot and the runner of **Poochy's Emote Rally**. For specific details on any command, use `p!help [command name]`.",color = discord.Color.from_rgb(87,212,58), type = 'rich')
        embed.set_thumbnail(url = str(self.avatar_url_as(size = 128)))
        embed.add_field(name = '**COIN COMMANDS**',value = '`p!daily`\n`p!coins`',inline = False)
        embed.add_field(name = '**PULL/EMOTE COMMANDS**',value = '`p!pull`\n`p!myemotes`\n`p!allemotes`',inline = False)
        embed.add_field(name = '**PETNAME COMMANDS**',value = '`p!setpetname`\n`p!togglepetname`\n`p!wear`\n`p!remove`',inline = False)
        embed.add_field(name = '**OTHER COMMANDS**',value = '`p!banner`',inline = False)
        return(embed)
    embed = discord.Embed(title = 'p!' + title + ' Information',description = '\u200b',color = discord.Color.from_rgb(255,128,248), type = 'rich')
    embed.set_thumbnail(url = str(self.avatar_url_as(size = 128)))
    embed.add_field(name = '**SYNTAX**',value = '`' + syntax + '`',inline = False)
    embed.add_field(name = '**DESCRIPTION**',value = desc,inline = False)
    return(embed)