#pulls_manager.py
#CONTROLS THE PULLING AND PRESENTATION OF EMOTES

import discord, random
import database_manager as dm, emotes_manager as em, coins_manager as cm, userdata_manager as um

req_coins_one_thru_four = 5 #number of coins required to make a pull
req_coins_five_plus = 4 #number of coins required to make a six-pull

cr = 60  #common rarity
sr = 15  #super rarity
sra = 15 #super (animated) rarity
ur = 2   #ultra rarity
ura = 2  #ultra (animated) rarity
spr = 6   #spotlight rarity

rar_table = [cr,sr,sra,ur,ura,spr]

#RARITY GUIDE: 1 - Common, 2 - Super, 3 - Super (Animated), 4 - Ultra, 5 - Ultra (Animated), 6 - Spotlight

def get_rars():
    return rar_table
def decide_rarity():
    random.seed()
    ran = random.randint(1,100)
    if(ran <= cr):
        return(1)
    elif(ran <= cr + sr):
        return(2)
    elif(ran <= cr + sr + sra):
        return(3)
    elif(ran <= cr + sr + sra + ur):
        return(4)
    elif(ran <= cr + sr + sra + ur + ura):
        return(5)
    else:
        return(6)

def pull(message, calling_name, client, num):
    user_data = dm.search_user(message.author.id)
    multi = 1.0
    
    #if(num >= 5):
    #    req_coins = int(req_coins_five_plus * num * multi)
    #else:
    req_coins = req_coins_one_thru_four * num
    if(user_data[3] < req_coins):
        return('Terribly sorry,' + calling_name + '... You need **' + str(req_coins) + ' Blue Coins <:bluecoin:711090808148721694>** in order to make a pull, while you only have **' + str(user_data[3]) + ' Blue Coins <:bluecoin:711090808148721694>**. If you have not yet already, trying using `p!daily` for some coins!')
    else:
        new_coins = user_data[3] - req_coins
        dm.update_value(user_data[0],'coins',new_coins)
        returnage = ('Congratulations,' + calling_name + '! Here are the results of your ' + str(num) + '-pull! \n')
        for x in range(num):
            pulled_emote = choose_emote()
            if (pulled_emote[3] == 6):
                dm.update_value(message.author.id,'num_spotlights',dm.search_user(message.author.id)[6] + 1)
            if(um.check_for_emote(message.author.id,pulled_emote[1])):
                um.lvl_up_emote(message.author.id,pulled_emote[1])
                returnage += ('**' + pulled_emote[2] + '** ' +  em.id_to_emote(pulled_emote[1],client) + ' [Rarity: **' + em.get_emote_rar(pulled_emote[3]) + '**] [**Level ' + str(dm.find_one_emote(message.author.id,pulled_emote[1])[1]) + '**]\n')
            else:
                um.add_users_pull(message.author.id,pulled_emote[1])
                returnage += ('**' + pulled_emote[2] + '** ' +  em.id_to_emote(pulled_emote[1],client) + ' [Rarity: **' + em.get_emote_rar(pulled_emote[3]) + '**] [**NEW**]\n')
        returnage += ('This pull cost ' + str(req_coins) + ' Blue Coins <:bluecoin:711090808148721694>, so now you have **' + str(new_coins) + ' Blue Coins <:bluecoin:711090808148721694>**!')
        return(returnage)

def choose_emote():
    rar = decide_rarity()
    all_rare_emotes = dm.get_rare_emotes(rar)
    num_rare_emotes = len(all_rare_emotes)
    return all_rare_emotes[int(random.random() * num_rare_emotes)]