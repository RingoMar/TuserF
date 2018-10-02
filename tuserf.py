import requests
import re
import sys
from progress.bar import Bar

print ("Welcome the Twitch User finder....")
print ("version 1.0.0")

client_id = "mkenjzkw63k3ld902tdfnmwpwjdn5v" #replace with your id
name = sys.argv[1]

# turns the name into the user id for twitch to use 

def get_id():
    url = ('https://api.twitch.tv/helix/users?login={}'.format(name.lower()))
    headers = {'Client-ID': client_id,
               'Accept': 'application/vnd.twitchtv.v5+json'}
    r = requests.get(url, headers=headers).json()
    id_ = (r['data'][0]['id'])
    return id_

idnum = get_id()

rawlinks = {
    1: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100".format(idnum),
    2: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=100".format(idnum),
    3: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=200".format(idnum),
    4: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=300".format(idnum),
    5: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=400".format(idnum),
    6: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=500".format(idnum),
    7: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=600".format(idnum),
    8: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=700".format(idnum),
    9: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=800".format(idnum),
    10: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=900".format(idnum),
    11: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=1000".format(idnum),
    12: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=1100".format(idnum),
    13: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=1200".format(idnum),
    14: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=1300".format(idnum),
    15: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=1400".format(idnum),
    16: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=1500".format(idnum),
    17: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=1600".format(idnum),
    18: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=1700".format(idnum),
    19: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=1800".format(idnum),
    20: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=1900".format(idnum),
    21: "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=100&offset=2000".format(idnum)
}

# checks the urls above for names of channels user follows
open("data/names.json", "w").close()
print("Getting the names of channels")
with open("data/names.json", "a+") as f:
    for i in range(1, 22):
        url = rawlinks[i]
        headers = {'Client-ID': client_id ,'Accept': 'application/vnd.twitchtv.v5+json'}
        n = requests.get(url, headers=headers).json()
        pages = n["_total"]
        for i in range(0, pages):
            try:
                idname = (n["follows"][i]["channel"]["display_name"])
                f.write(str("{}\n").format(idname))
                f.close
            except UnicodeEncodeError:
                pass
            except IndexError:
                pass
print("Done...")
print
print("Checking the chats!")

# starts to look for the user
with open ("data/names.json", "r") as namesfile:
    count = 0
    maxnu =(int(pages))
    bar = Bar('Checking Channels', max=maxnu, suffix='%(index)d/%(max)d - %(percent)d%% [ETA: %(eta_td)s || TIME: %(elapsed_td)s ]')
    for line in namesfile:
        for x in range(0, pages):
            try:
                if (' ' in line) == True:
                    continue
                else:
                    bar.next()
                    selname = line.rstrip('\n')
                    url = ("https://tmi.twitch.tv/group/user/{}/chatters").format(selname.lower())
                    rn = requests.get(url).json()

                    stream = str(rn)
                    name = sys.argv[1]
                    UserName = (r"{}").format(name)
                    if re.findall(UserName, stream):
                        print ("\nFound '{}' in {}".format(name, line))
                        count += 1
                    else:
                        pass 
            except IndexError:
                pass
            break 

print ("\nThe user '{}' was found in {} channels.".format(name, count))
open("data/names.json", "w").close()
