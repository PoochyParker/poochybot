#pulls_manager.py
#CONTROLS THE PULLING AND PRESENTATION OF EMOTES

import discord, random
import database_manager as dm, emotes_manager as em, coins_manager as cm, userdata_manager as um

coins_per = 5 #number of coins required to make a pull

cr = 60  #common rarity
sr = 15  #super rarity
sra = 15 #super (animated) rarity
ur = 2   #ultra rarity
ura = 2  #ultra (animated) rarity
spr = 6   #spotlight rarity

rar_table = [cr,sr,sra,ur,ura,spr]

#RARITY GUIDE: 1 - Common, 2 - Super, 3 - Super (Animated), 4 - Ultra, 5 - Ultra (Animated), 6 - Spotlight, 7 - Unique

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

def pull(user_id, bot, num):
    user = dm.search_user(user_id)
    req_coins = coins_per * num
    if(user[2] < req_coins):
        return('{{ping}} Terribly sorry, {{petname}}... You need **{{req}} Blue Coins <:bluecoin:711090808148721694>** in order to make a pull, while you only have **{have} Blue Coins <:bluecoin:711090808148721694>**. If you have not yet already, trying using `p!daily` for some coins!'.format(req = str(req_coins), have = str(user[2])))
    else:
        new_coins = user[2] - req_coins
        dm.update_value(user[0],'coins',new_coins)
        returnage = '{{ping}} Congratulations, {{petname}}! Here are the results of your {pull_num}-pull! \n'.format(pull_num = num)
        for x in range(num):
            pulled_emote = choose_emote()
            if (pulled_emote[3] == 6):
                dm.update_value(user_id,'num_spotlights',user[4] + 1)
            if(um.check_for_emote(user_id,pulled_emote[1])):
                um.lvl_up_emote(user_id,pulled_emote[1])
                returnage += '• **{emote_name}** {emote} [Rarity: **{rarity}**] [**Level {level}**]\n'.format(emote_name = pulled_emote[2], emote = str(em.id_to_emote(pulled_emote[1],bot)), rarity = em.get_emote_rar(pulled_emote[3]), level = str(dm.find_one_emote(user_id,pulled_emote[1])[1]))
            else:
                um.add_users_pull(user_id,pulled_emote[1])
                returnage += '• **{emote_name}** {emote} [Rarity: **{rarity}**] [**NEW**]\n'.format(emote_name = pulled_emote[2], emote = str(em.id_to_emote(pulled_emote[1],bot)), rarity = em.get_emote_rar(pulled_emote[3]))
        returnage += 'This pull cost {req} Blue Coins <:bluecoin:711090808148721694>, so now you have **{new} Blue Coins <:bluecoin:711090808148721694>**!'.format(req = str(req_coins),new = str(new_coins))
        return(returnage)

def choose_emote():
    rar = decide_rarity()
    all_rare_emotes = dm.get_rare_emotes(rar)
    num_rare_emotes = len(all_rare_emotes)
    return all_rare_emotes[int(random.random() * num_rare_emotes)]