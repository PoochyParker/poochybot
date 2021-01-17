#LOCAL_DATA_STORAGE.PY

import database_manager
import emote as em, user as us

def fillDictionary(type):
    dict = {}
    data_list = database_manager.pull_database(type)

    #Translates database entry into a new object of appropriate type, then added to the dictionary
    if (type == 'users'):
        for user in data_list:
            dict[user[0]] = us.User(user[0], user[1], user[2], user[3], user[4]) 
    if (type == 'emotes'):
        for emote in data_list:
            dict[emote[0]] = em.Emote(emote[0], emote[1], emote[2], emote[3], emote[4]) 
    if (type == 'earned_emotes'):
        for emote in data_list:
            dict[emote[0]] = ea.Earned_Emote() #FLESH OUT
            #put in 4th one here too lol