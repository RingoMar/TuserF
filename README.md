# Twitch User Finder
This is simple script I made in my free time to use [Twitch](twitch.tv)'s public API. It's used to find Twitch users in channels, because who doesn't want to know what channels their friends who have the "OFFLINE" status are watching / lurking in..
also can be used to find sub gifters 😉
# How to get started
You would need [Python3](https://www.python.org/downloads/) or later.
# Libaries 
* [Requests](http://docs.python-requests.org/en/master/user/install/)
* [Progress](https://pypi.org/project/progress/)

## Client Id: 
* Go to [Twitch Dev Website](https://glass.twitch.tv/console/apps/create)
* Name your application!
* Set **OAuth Redirect** URL to `http://localhost`
* Set **Category** to **Analytics Tool**
* Now in the Developer Applications page, click **Manage** on the application you now made.
* Now copy the **Client ID** 
* Replace the **Client ID** on Line 9 with the new one

# How to Run
* Navigate to your folder where you have download the files with CMD... 
___
Now run the line `python tuserF.py username`
___
**Replace "username" above with the user you're loookig for**

# License
This project is licensed under GNU General Public License 
