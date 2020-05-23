#channel_manager.py

import database_manager as dm

def decompile_channel(ch): #turns a proper calling into a channel id
	return (ch[2:len(ch) - 1])
def compile_channel(id): #turns a channel id into a proper calling
	return '<#' + str(id) + '>'

def get_type(ty):
    if(ty == 'Announcement'):
        return 1
    elif(ty == 'Main'):
        return 2
    elif(ty == 'Side'):
        return 3
    else:
        return 0

def get_type_rev(ty):
    if(ty == 1):
        return 'Announcement'
    elif(ty == 2):
        return 'Main'
    elif(ty == 3):
        return 'Side'
    else:
        return ('CHANNEL TYPE NOT FOUND: ' + str(ty))

def look_for_channel(server_id,channel_id): #checks if channel log exists
    if(dm.check_for_existence(server_id) == False):
        return False
    else:
        return (dm.check_for_channel(server_id, channel_id) == False)

def channel_creation(server_id, content, calling_name): #creates channel log if none exists
    channel_data = content.split('|')
    channel_id = decompile_channel(channel_data[0])
    if (dm.check_for_channel(server_id,channel_id) == True):
        return('Wait a second,' + calling_name + '! That channel has already been assigned before!')
    else:
        type = get_type(channel_data[1])
        if (type == 0):
            return('Hold up,' + calling_name + '! Did you mess up your syntax? It should be like `p!setchannel [channel mention]|[Announcement/Main/Side]`.')
        else:
            if (type != 3):
                channels = dm.get_servers_channels(server_id,type)
                if(len(channels) > 0):
                    return('Sorry,' + calling_name + '! You already have a channel set as ' + channel_data[1] + ': ' + compile_channel(channels[0][1]) + '! To prevent confusion, only one channel can be set as the Main and Announcement channels.')
            dm.add_channel(server_id,channel_id,type)
            return('There we go,' + calling_name + '! I added ' + channel_data[0] + 'as a(n) ' + channel_data[1] + ' channel!')

def channel_deletion(server_id, content, calling_name): #removes a channel from the log
    channel_id = decompile_channel(content.strip())
    if (dm.check_for_channel(server_id,channel_id) == False):
        return('Wait a second,' + calling_name + '! That channel has yet to be assigned as anything!')
    else:
        dm.delete_channel(server_id,channel_id)
        return('There we go,' + calling_name + '! I can no longer talk in ' + content + '.')

def channel_log(server_id): #returns what servers are set as bot channels
    channels = dm.get_servers_channels(server_id,0)
    if(len(channels) == 0):
        return('Oh dear, it appears you have yet to mark any channels as bot channels! For now, I can go _anywhere..._ If you want to set a place for me to go, use the following command: `p!setchannel [channel mention]|[Announcement/Main/Side]`.')
    retext = 'Here is a list of all the servers that are marked as bot channels!'
    for channel in channels:
        retext += ('\n - ' + compile_channel(channel[1]) + ' -- Type: ' + get_type_rev(channel[2]))
    return(retext)

def return_all_channels_test(): #prints all of the test channels
    channels = dm.get_channels()
    for channel in channels:
        print(channel)

def get_channel(server_id,type): #returns the id of a specific channel
    try:
        return dm.get_servers_channels(server_id,type)[0][1]
    except:
        return ''
