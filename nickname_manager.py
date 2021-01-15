#nickname_manager.py
#CONTROLS THE WHOLE NICKNAME MANAGEMENT SYSTEM THAT IS ONE OF POOCHY BOT'S SIGNATURE FEATURES

import discord, re
import database_manager as dm, emotes_manager as em

calling_name = ''
petnames = 'nicknames.dat'

nickname_limit = 32

def crop_out_command(content, ignore_part): #removes a length of 'ignore_part' from str 'content'
    return content[len(ignore_part):len(content)]
def limit_cont(base_username,num): #limits str to 1 line of <= 30 chars
    new_username = base_username.split('\n')[0]
    return new_username[0:num]

def return_petnames():
    return petnames
def compile_name(id): #turns a user id into a proper ping
    return '<@' + str(id) + '>'
def decompile_name(ping): #turns a proper ping into a user id
    return (re.sub("[^0-9]", "", ping))

def check_badwords(name): #certain bad word filter
    return re.search("n[i1]g|f[a4]g|tranny|bitch|fuck|cum|pen[i1]s|c[o0]ck|sh[i1]t|p[i1]ss|a[s$][s$]|s[e3]x|p[o0][o0]p|t[a4]rd|xxx|:regional_indicator_.:|:.:|[\U00002600-\U000027BF]|[\U0001f170-\U0001f64F]|[\U0001f680-\U0001f6FF]", name)

def set_calling_name(author, bot): #checks whether or not the message.author should be called by a nickname
    global calling_name
    user_data = dm.search_user(author.id)
    name = ''
    if(user_data[1] is not None and user_data[1] != ''):
        name += user_data[1]
    else:
        name += author.name
    if(user_data[3] is not None and user_data[3] != ''):
        name += ' ' + str(em.id_to_emote(user_data[3],bot))
    return name

def set_embed_calling_name(author, bot): #checks whether or not the message.author should be called by a nickname
    user_data = dm.search_user(author.id)
    name = ' '
    if(user_data[1] is not None and user_data[1] != ''):
        name += user_data[1]
    else:
        name += author.name
    if(user_data[3] is not None and user_data[3] != ''):
        name += ' ' + str(em.id_to_emote(user_data[3],bot))
    return name
#-----------------COMMAND METHODS-----------------#
def nickname_set(message,author): #sets the author's nickname
    user_data = dm.search_user(author.id)
    nickname = limit_cont(message,nickname_limit)
    if nickname.strip() != '':
        if check_badwords(nickname.lower()):
            return('WHAT? I cannot call you that, {}!'.format(compile_name(author.id)))
        else:
            dm.update_value(user_data[0],'petname',nickname)
            return ('Alright! I got your nickname now, {}!'.format(nickname))
    else:
        dm.update_value(user_data[0],'petname','')
        return ("Alrighty, {}! I reset your petname.".format(compile_name(author.id)))

#def nickname_toggle(author): #toggles whether poochy bot will refer to the author by their nickname
#    user_data = user_data = dm.search_user(author.id)
#    if user_data[1] != '' or user_data[1] is None:
#        if user_data[2] == True:
#            dm.update_value(user_data[0],'referby',0)
#            return ('Alright, ' + compile_name(author.id) + ". I've turned your nickname off.")
#        else:
#            dm.update_value(user_data[0],'referby',1)
#            return ('Got it, ' + user_data[1] + '! Nickname back on!')
#    else:
#        return ('Wait, ' + calling_name + "! You don't even have a nickname!")