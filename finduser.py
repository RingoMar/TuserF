import random
import re
import socket
import sys
import time
import webbrowser

import requests
import tqdm
from time import sleep as sleep
from colorama import Back, Fore, Style, init
from requests import Session

init()

print("-- Starting: Find User Script")
print(Fore.RED + "Version 2.0" + Style.RESET_ALL)

client_id = "zdllyq8tr3qg6piu3p3vzk2puvng5v"  # replace with your id
############################################################################

name = (sys.argv[1]).lower()
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

# finds all the followers the user has and adds the users to a list


def getfollows():
    print(Fore.BLUE + "> Finding the follows of the user." + Style.RESET_ALL)
    s = requests.Session()
    url = (
        f'https://api.twitch.tv/helix/users/follows?from_id={_id}&first=100')
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
            url = (
                f'https://api.twitch.tv/helix/users/follows?from_id={_id}&first=100&after={nextkey}')
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

# the main part of the program


def run():
    print(Fore.BLUE + "> Starting the program" + Style.RESET_ALL)
    getfollows()
    print(Fore.CYAN + "> Cheacking chats")
    s = requests.Session()
    for username in tqdm.tqdm(range(0, len(users))):
        # looks for them in the chat
        url = (
            "https://tmi.twitch.tv/group/user/{}/chatters").format(users[username].lower())
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
        # if they are found looks to see if the channel is live or not
        print(Fore.BLUE + "> Cheacking found channels for status" + Style.RESET_ALL)
        s = socket.socket()
        host = socket.getfqdn()
        port = 9082
        s.bind((host, port))

        print('Starting web server on http://%s:%d/' % (host, port))
        print('Opening Web page')
        webbrowser.open('http://%s:%d/' % (host, port))

        s.listen(5)

        while True:
            try:
                c, (client_host, client_port) = s.accept()
                print('Got connection from', client_host, client_port)
                c.recv(4280)
                c.send(bytes('HTTP/1.0 200 OK\n'.encode("utf-8")))
                c.send(bytes('Content-Type: text/html\n'.encode("utf-8")))
                c.send(bytes('\n'.encode("utf-8")))
                c.send(bytes('<html><body>'.encode("utf-8")))
                c.send(bytes("""
                <style>
                table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
                }

                .toprow {
                    cursor: pointer;
                }
                td,
                th {
                    border: 1px solid rgb(190, 190, 190);
                    padding: 10px;
                }

                td {
                    text-align: center;
                }

                tr:nth-child(even) {
                    background-color: #eee;
                }

                th[scope="col"] {
                    background-color: #696969;
                    color: #fff;
                }

                th[scope="row"] {
                    background-color: #d7d9f2;
                }

                caption {
                    padding: 10px;
                    caption-side: bottom;
                }

                table {
                    border-collapse: collapse;
                    border: 2px solid rgb(200, 200, 200);
                    letter-spacing: 1px;
                    font-family: sans-serif;
                    font-size: .8rem;
                }
                h1#toptext {
                    font-family: Helvetica;
                    text-align: center;
                }

                </style>
                <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>
                <meta http-equiv="Pragma" content="no-cache"/>
                <meta http-equiv="Expires" content="0"/>
                <meta charset="UTF-8">
                <meta http-equiv="refresh" content="120">
                <title>Found Users</title>
                </head>
                <body>""".encode("utf-8")))

                c.send(bytes(
                    f"""<h1 id="toptext"> CHANNELS {str(name).upper()} ARE IN </h1>""".encode("utf-8")))

                c.send(bytes("""<table id="myTable2">
                <tr class="toprow">
                    <th scope="col" onclick="sortTable(0)">NAME</th>
                    <th scope="col" onclick="sortTable(1)">TITLE</th>
                    <th scope="col" onclick="sortTable(2)">VIEWERS</th>
                    <th scope="col" onclick="sortTable(3)">STATUS</th>
                    <th>Thumbnail</th>
                </tr>""".encode("utf-8")))
                for foundusers in range(0, len(found)):
                    url = (
                        f"https://api.twitch.tv/helix/streams?user_login={str(found[foundusers]).lower()}")
                    headers = {'Client-ID': client_id}
                    r = requests.get(url, headers=headers).json()
                    try:
                        if str(r["data"][0]["type"]) == "live":
                            c.send(bytes(f"""
                                <tr>
                                    <td scope="row">{r["data"][0]["user_name"]}</td>
                                    <td scope="row">{r["data"][0]["title"]}</td>
                                    <td scope="row">{r["data"][0]["viewer_count"]}</td>
                                    <td scope="row">Live</td>
                                    <td align="center" valign="center" style="text-align: center;">
                                    <img src="{r["data"][0]["thumbnail_url"].replace("{width}", "160").replace("{height}", "90")}" alt="thumbnail_url" />
                                    </td>
                                </tr>""".encode("utf-8")))
                    except IndexError:
                        c.send(bytes(f"""
                            <tr>
                                <td scope="row">{found[foundusers]}</td>
                                <td scope="row">NONE</td>
                                <td scope="row">0</td>
                                <td scope="row">offline</td>
                                <td align="center" valign="center" style="text-align: center;">
                                <img src="https://static-cdn.jtvnw.net/previews-ttv/live_user_{name}-160x90.jpg" alt="thumbnail_url" />
                                </td>
                            </tr>""".encode("utf-8")))
                c.send(bytes(f"</table>".encode("utf-8")))
                c.send(bytes("""
                                <script>
                                function sortTable(n) {
                                var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
                                table = document.getElementById("myTable2");
                                switching = true;
                                dir = "asc"; 
                                while (switching) {
                                    switching = false;
                                    rows = table.rows;
                                    for (i = 1; i < (rows.length - 1); i++) {
                                    shouldSwitch = false;
                                    x = rows[i].getElementsByTagName("TD")[n];
                                    y = rows[i + 1].getElementsByTagName("TD")[n];
                                    if (dir == "asc") {
                                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                                        shouldSwitch = true;
                                        break;
                                        }
                                    } else if (dir == "desc") {
                                        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                                        shouldSwitch = true;
                                        break;
                                        }
                                    }
                                    }
                                    if (shouldSwitch) {
                                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                                    switching = true;
                                    switchcount ++; 
                                    } else {
                                    if (switchcount == 0 && dir == "asc") {
                                        dir = "desc";
                                        switching = true;
                                    }
                                    }
                                }
                                }
                                </script>
                """.encode("utf-8")))
                c.send(bytes("""</html>
                            </body>""".encode("utf-8")))
                c.close()
            except KeyboardInterrupt:
                break
                s.close()
                sys.exit()
            except ConnectionAbortedError:
                continue
            except requests.exceptions.ConnectionError:
                print("Error in request..... sleeping for 20 sec")
                for i in tqdm.tqdm(range(0, 20)):
                    sleep(1)
    else:
        print(Fore.RED + f"'{name}' not found." + Style.RESET_ALL)
    return


run()
