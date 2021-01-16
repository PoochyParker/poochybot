#USER.PY

import nickname_methods

class User:
    def __init__(self, user_id): #Completely new user creation
        self.nickname = ""
        self.user_id = user_id
        self.num_coins = 0
        self.att_emote = 0
        self.user_level = 1
        self.new_user = True

    def __init__(self, nickname, user_id, num_coins, att_emote, user_level): #Grabbing user data from database on first startup
        self.nickname = nickname
        self.user_id = user_id
        self.num_coins = num_coins
        self.att_emote = att_emote
        self.user_level = user_level
        self.new_user = False

    def set_nickname(self, nickname):
        if (nickname_methods.check_badwords(nickname)):
            return False
        if (nickname.strip() == ''): #Resets nickname
            nickname = ''
            return True
        else:
            nickname = nickname_methods.limit_cont(nickname)
            return True
