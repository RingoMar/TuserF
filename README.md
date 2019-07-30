# Twitch User Finder
A simple script that makes use of [Twitch](twitch.tv) public API to find users.
# How to get started
You would need [Python3](https://www.python.org/downloads/) or later.
# External Libraries 
* [Colorama](https://pypi.org/project/colorama/)
* [tqdm](https://pypi.org/project/tqdm/)
___
`pip install [Library]`
___
**Replace "Library" above with the one you are installing**

## Client Id: 
* Go to [Twitch Dev Website](https://glass.twitch.tv/console/apps/create)
* Name your application!
* Set **OAuth Redirect** URL to `http://localhost`
* Set **Category** to **Analytics Tool**
* Now in the Developer Applications page, click **Manage** on the application you now made.
* Now copy the **Client ID** 
* Replace the **Client ID** on Line 9 with the new one

# How to Run
___
Now run the line `python tuserF.py username`
___
**Replace "username" above with the user you're looking for**

# License
This project is licensed under GNU General Public License 
