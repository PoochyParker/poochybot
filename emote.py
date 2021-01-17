#EMOTE.PY

import discord, math
import database_manager as dm, nickname_manager as nm, pulls_manager as pm





class Emote:
    def __init__(self, id, name, rarity, is_spotlight, is_in_pool):
        self. id = id #Primary signifier  #int
        self.name = name                  #string
        self.rarity = rarity              #int
        self.is_spotlight = is_spotlight    #bool
        self.is_in_pool = is_in_pool          #bool

    def swap_id(self, new_id):
        self.id = new_id

    def change_emote_info(self, name, rarity):
        self.name = name
        self.rarity = rarity