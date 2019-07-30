import re
import sys

import requests
import tqdm
from colorama import Back, Fore, Style, init
from requests import Session

init()

print("-- Starting: Find User Script" )
print(Fore.RED + "Version 2.0"+ Style.RESET_ALL)

client_id = "zdllyq8tr3qg6piu3p3vzk2puvng5v"  # replace with your id
############################################################################

name = sys.argv[1]
nextkey = ""
users = []
found = []

# turns the name into the user id for twitch to use

def get_id():
    s = requests.Session()
    url = ('https://api.twitch.tv/helix/users?login={}'.format(name.lower()))
    headers = {'Client-ID': client_id}
    r = s.get(url, headers=headers).json()
    id_ = (r['data'][0]['id'])
    return id_

_id = get_id()

def getfollows():
    print(Fore.BLUE + "> Finding the follows of the user." + Style.RESET_ALL)
    s = requests.Session()
    url = (f'https://api.twitch.tv/helix/users/follows?from_id={_id}&first=100')
    headers = {'Client-ID': client_id}
    r = s.get(url, headers=headers).json()
    nextkey = r['pagination']['cursor']
    try:
        for x in range(0, len(r['data']) + 1):
            users.append(r['data'][x]['to_name'])
    except IndexError:
        pass
    while nextkey:
        try:
            url = (f'https://api.twitch.tv/helix/users/follows?from_id={_id}&first=100&after={nextkey}')
            headers = {'Client-ID': client_id}
            r = s.get(url, headers=headers).json()
            nextkey = r['pagination']['cursor']
            try:
                for x in range(0, len(r['data']) + 1):
                    users.append(r['data'][x]['to_name'])
            except IndexError:
                pass
        except Exception as e:
            users.append(name)
            nextkey = ""
            print(Fore.BLUE + "> Found all channels..." + Style.RESET_ALL)

    return

def run():
    print(Fore.BLUE + "> Starting the program" + Style.RESET_ALL)
    getfollows()
    print(Fore.CYAN + "> Cheacking chats")
    s = requests.Session()
    for username in tqdm.tqdm(range(0, len(users) )):
        url = ("https://tmi.twitch.tv/group/user/{}/chatters").format(users[username].lower())
        rn = s.get(url).json()
        stream = str(rn)
        thename = str(f"{name}")
        UserName = (thename)
        try:
            for x in range(0, len(rn["chatters"]["viewers"])):
                if str(rn["chatters"]["viewers"][x]) == name:
                    found.append(users[username])
            for x in range(0, len(rn["chatters"]["moderators"])):
                if str(rn["chatters"]["moderators"][x]) == name:
                    found.append(users[username])
            for x in range(0, len(rn["chatters"]["vips"])):
                if str(rn["chatters"]["vips"][x]) == name:
                    found.append(users[username])
            for x in range(0, len(rn["chatters"]["broadcaster"])):
                if str(rn["chatters"]["broadcaster"][x]) == name:
                    found.append(users[username])
            for x in range(0, len(rn["chatters"]["staff"])):
                if str(rn["chatters"]["staff"][x]) == name:
                    found.append(users[username])
            for x in range(0, len(rn["chatters"]["admins"])):
                if str(rn["chatters"]["admins"][x]) == name:
                    found.append(users[username])
            for x in range(0, len(rn["chatters"]["global_mods"])):
                if str(rn["chatters"]["global_mods"][x]) == name:
                    found.append(users[username])
        except TypeError:
            pass
    if found:
        print(Fore.BLUE + "> Cheacking found channels for status" + Style.RESET_ALL)
        for foundusers in range(0, len(found)):
            url = (f"https://api.twitch.tv/helix/streams?user_login={str(found[foundusers]).lower()}")
            headers = {'Client-ID': client_id}
            r = s.get(url, headers=headers).json()
            try:
                if str(r["data"][0]["type"]) == "live":
                    print(Fore.WHITE + Back.GREEN + f"Found '{name}' in: {r['data'][0]['user_name']}, they are now live! [{r['data'][0]['title']}]" + Style.RESET_ALL )
            except IndexError:
                print(Fore.RED + f"Found '{name}' in: {found[foundusers]}, they a offline." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"'{name}' not found." + Style.RESET_ALL)
    return

run()
