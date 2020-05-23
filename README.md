# poochybot
The messy code for 1-Up World's very own Poochy, the host of Poochy's Emote Rally on the Discord server 1-Up World.

Having started on Poochy Bot in mid-March 2020, it now serves as an emote game for the Discord server 1-Up World. Having been the first time working with discord.py, MySQL databases, and a large variety of features that Python provides, it is currently quite messy. Over time, I do hope to clean it up and actually look decently presentable, while also adding a variety of new features!

FILE BREAKDOWN
--------------
poochybot_main.py - "Main" ran program for Poochy, including all the front-end connection with Discord, and connections with every other file
nickname_manager.py - Manages everything relating to what Poochy calls the user in various scenarios
coins_manager.py - Manages everything relating to the addition, subtraction, and finding of how many coins each user has
emotes_manager.py - Manages everything relating to the showcase and storage of all the emotes available in Poochy's Emote Rally
pulls_manager.py - Manages everything relating to the determination and showcase of what users get from the gatcha pulls
userdata_manager.py - Managers everything related to the emotes each user has obtained (slightly misleading file name, yes)
banner_manager.py - Manages everything related to the creation and showcase of the bimonthly banners
channel_manager.py - Manages everything relating to the permissions Poochy has on a per-channel basis
help_manager.py - The awfully-coded application of the *p!help* command
database_manager.py - The backend program that connects Poochy to its MySQL server and all the interactions required there
