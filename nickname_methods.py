#NICKNAME_METHODS.PY

import re, discord
import emotes_manager

nickname_limit = 32 #char limit on nicknames

def compile_name(id): #turns a user id into a proper ping
    return '<@' + str(id) + '>'
def decompile_name(ping): #turns a proper ping into a user id
    return (re.sub("[^0-9]", "", ping))

def limit_cont(base_username,num): #limits str to 1 line of <= 32 chars
    new_username = base_username.split('\n')[0]
    return new_username[0:num]

def check_badwords(name): #bad word filter
    return re.search("n[i1]g|f[a4]g|tranny|bitch|fuck|cum|pen[i1]s|c[o0]ck|sh[i1]t|p[i1]ss|a[s$][s$]|s[e3]x|p[o0][o0]p|t[a4]rd|xxx|:regional_indicator_.:|:.:|[\U00002600-\U000027BF]|[\U0001f170-\U0001f64F]|[\U0001f680-\U0001f6FF]", name)

def get_calling_name(user, name, bot):
    if (user.nickname == ''):
        calling_name = name #if no nickname set, defaults to Discord username
    else:
        calling_name = user.nickname
    if (user.att_emote != 0):
        calling_name += ' ' + str(emotes_manager.id_to_emote(user_data[3],bot))
    return calling_name