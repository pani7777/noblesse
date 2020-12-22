

**THIS IS ONLY MADE FOR WINDOWS, MOST COMMANDS WORK FOR LINUX EXCEPT FOR THE NUKER (MODIFY IT YOURSELF)**



 ███▄    █  ▒█████   ▄▄▄▄    ██▓    ▓█████   ██████   ██████ ▓█████ 
 ██ ▀█   █ ▒██▒  ██▒▓█████▄ ▓██▒    ▓█   ▀ ▒██    ▒ ▒██    ▒ ▓█   ▀ 
▓██  ▀█ ██▒▒██░  ██▒▒██▒ ▄██▒██░    ▒███   ░ ▓██▄   ░ ▓██▄   ▒███   	@siph.er
▓██▒  ▐▌██▒▒██   ██░▒██░█▀  ▒██░    ▒▓█  ▄   ▒   ██▒  ▒   ██▒▒▓█  ▄ 
▒██░   ▓██░░ ████▓▒░░▓█  ▀█▓░██████▒░▒████▒▒██████▒▒▒██████▒▒░▒████▒	https://github.com/siph-er/noblesse
░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░▒▓███▀▒░ ▒░▓  ░░░ ▒░ ░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░░░ ▒░ ░
░ ░░   ░ ▒░  ░ ▒ ▒░ ▒░▒   ░ ░ ░ ▒  ░ ░ ░  ░░ ░▒  ░ ░░ ░▒  ░ ░ ░ ░  ░
   ░   ░ ░ ░ ░ ░ ▒   ░    ░   ░ ░      ░   ░  ░  ░  ░  ░  ░     ░   
         ░     ░ ░   ░          ░  ░   ░  ░      ░        ░     ░  ░
                          ░                                         
                                                      
**Steps to Run the Selfbot Correctly**:

1) Make sure you have python to PATH, https://www.python.org/downloads/ 
   (run the python installer, and turn on the PATH option), so you're able to 
   run pip in Command Prompt using 'python -m pip install <package>'
   or 'pip install <package>'.

2) Double-click the install.bat, this will install all modules in the 
   requirements.txt file.

3) After it has all installed, open assets/config.json and input your data.
 - If the 'StoreDMFiles' key in the config.json is set to'True', it will log 
   images and videos from DM Channels (Set it to False or anything else if 
   you don't wanna log).

 - If the 'StoreGCFiles' key in the config.json is set to'True', it will log 
   images and videos from Group Channels (Set it to False or anything else if 
   you don't wanna log).

 - If the 'StoreGuildFiles' key in the config.json is set to'True', it will log 
   images and videos from Servers and allocate it to different channels in the
   guild file. (Set it to 'False' or anything else if you don't wanna log).

 - if the 'NitroSniper' key in the config.json is 'True', it will snipe all nitro links 
   sent in any server or DM Channels (Set it to False or anything else if 
   you don't wanna snipe).

 - if the 'SlotbotSniper['snipe']' key in the config.json is 'True', it will snipe all slotbots 
   sent in any server (Set it to False or anything else if you don't wanna snipe).

 - if the 'PolluxSniper['snipe']' key in the config.json is 'True', it will snipe all Pollux's 
   sent in any server (Set it to False or anything else if you don't wanna snipe).

 - The 'attachment_webhook' key is a webhook link which sends every attachment sent to you,
   not including bots.

 - The 'nitro_webhook' key is also a webhook link which sends you the status of each nitro code
   you attempt to redeem.

4) The folder 'files' is where all the images and videos from each user 
   is stored, it stores via ID since ID doesn't change, however in the 
   ID Folder there is another folder, called the name of the user,
   making it easier to see who is who.

5) Once you have understood this, go to assets/nuke/config.json and open it.
   Inside should be a configuration for the genesis nuker, change it to what you want,
   it tells you which ones which.

6) In order to run the nuker, you must type [prefix]start-nuker <token> in any channel.
   This will open a whole new console already logged into the token.

7) I remade the bot cos why not, also if you dont have the new noblesse module re-run
   install.bat it should download latest one.
   