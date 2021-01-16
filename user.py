#USER.PY

import nickname_methods

class User:
    def __init__(self, id): #Completely new user creation
        self.id = id #Primary signifier  #int
        self.nickname = ""               #string
        self.num_coins = 0               #int
        self.att_emote = ""              #string
        self.level = 1                   #int
        self.new_user = True             #bool

    def __init__(self, id, nickname, num_coins, att_emote, level): #Grabbing user data from database on first startup
        self.id = id
        self.nickname = nickname
        self.num_coins = num_coins
        self.att_emote = att_emote
        self.level = level
        self.new_user = False

    def set_nickname(self, nickname):
        if (nickname_methods.check_badwords(nickname)):
            return False
        if (nickname.strip() == ''): 
            nickname = '' #Resets nickname
            return True
        else:
            nickname = nickname_methods.limit_cont(nickname)
            return True
