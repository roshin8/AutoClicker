AutoClicker - An amazing bot which saves time
===========

AutoClicker is a bot for URL Shortening PTC webstites like *shorte.st*, *linkbucks*, *admy.link*, etc. that automatically skips Ads

Auto clickers can be as simple as a program that simulates mouse clicking. This type of auto-clicker is fairly generic and will often work alongside any other computer program running at the time and acting as though a physical mouse button is pressed.

More complex auto clickers can similarly be as general, but often are custom-made for use with one particular program and involve memory reading. Such auto clickers may allow the user to automate most or all mouse functions, as well as simulate a full set of keyboard inputs. Custom-made auto clickers may have a narrower scope than a generic auto clicker

----------


Requirements:
-------------

 - Python 2.7 
 - Selenium
	 - sudo pip install selenium
 - X virtual framebuffer (xvfb)
	 - sudo apt-get install xvfb
 - Google Spreadsheets Python API (gspread)
	 - sudo pip install gspread
 - oauth2client
	 - sudo pip install oauth2client
 - [Close Proxy Authentication](https://addons.mozilla.org/en-US/firefox/addon/close-proxy-authentication/) Firefox extension



> **Note:**

> - To use [gpread](https://github.com/burnash/gspread) you have to [obtain OAuth2 credentials from Google Developers Console](http://gspread.readthedocs.org/en/latest/oauth2.html)
> - **gpread** is used to keep track of the proxies used for a specific URL
> - **xvfb** is optional if you want to run in a VPS (Headless browser)
> - [Close Proxy Authentication](https://addons.mozilla.org/en-US/firefox/addon/close-proxy-authentication/) Firefox extension is used for proxies that needs authentication

----------

How to use:
-------------------

 1. [Create new Firefox Profile](https://support.mozilla.org/en-US/kb/profile-manager-create-and-remove-firefox-profiles) and install [Close Proxy Authentication](https://addons.mozilla.org/en-US/firefox/addon/close-proxy-authentication/) Firefox extension in it.
 2.  Copy **geckodriver** file to */usr/local/bin*
 3. Run the script
 - Without **xvfb**:
 `python autoclicker.py --website ADMYLINK --profile MUD --random` 
 
 - Using **xvfb**:
 `xvfb-run -a python autoclicker.py --website ADMYLINK --profile MUD --random`

    > **Note:**  `--link 2` can be used instead of `--random` if you want to use a specific link
