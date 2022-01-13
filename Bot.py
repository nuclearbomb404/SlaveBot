import time
import discord
from discord.embeds import Embed, EmbedProxy
from discord.ext.commands import Bot
import random 
import datetime
import os, glob
import shutil
import subprocess
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pytube import YouTube
import atexit
import DeleteMP3
from threading import Condition
import audioread

g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)
vc = None
sussy = False
SAVE_PATH = "/home/yasser/Desktop/desktop/Python_Bot"
class MyClient(discord.Client):
    HP = 0 
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        #Return if the author of the message was the same bot
    async def on_message(self, message):

        print(f'Message from {message.author}: {message.content}')
        if message.author == client.user:
            return
        #Lists every message in MessageLog.txt
        file = open('MessageLog_'+ str(message.guild.name) + '.txt', 'a+')
        try:
            file.write("(Channel:"+message.channel.name+") ")
            file.write(message.author.name + " said: ")
            file.write(message.content+"\n")
        finally:
            #Close the file after editing it
            file.close()
        #Checks if the message starts with the prefix ('=')
        if message.content.startswith("*") and message.author != discord.Member.bot:
            if message.content == "*ping":
                await message.channel.send("Pong!")
                await message.channel.send(f"{message.author.mention} is the best")
            elif message.content == "*bee":
                await message.channel.send(":bee:")
            elif message.content == "*help":
                HelpAscii = """
                ░█████╗░░██████╗░█████╗░██╗██╗
                ██╔══██╗██╔════╝██╔══██╗██║██║
                ███████║╚█████╗░██║░░╚═╝██║██║
                ██╔══██║░╚═══██╗██║░░██╗██║██║
                ██║░░██║██████╔╝╚█████╔╝██║██║
                ╚═╝░░╚═╝╚═════╝░░╚════╝░╚═╝╚═╝"""
                HelpEmbed = discord.Embed(color=0x00ffce)
                HelpEmbed.title = "Slave Bot Help " 
                HelpEmbed.description = 'ping: Basic ping command \n\n bee: :bee: \n\n help: Sends help about the bot \n\n roulette: Test your luck \n\n time: Officially voted the #1 WORST way to check the time!\n\n ascii + <insert text>:'+HelpAscii + "\n\nsay + <thing to say>: I hope you don't type anything ***sussy***\n\n purge + <number of messages to delete>: Thanos snap :ok_hand:\n\n*dl + <link of youtube video>: Download youtube videos (NO LIMIT!) ((FUCK YOU DISCORD FOR YOUR DUMBASS FILE SHARING LIMIT))\n\n*problem: Pings my dumbass creator to come fix me"
                await message.channel.send(embed=HelpEmbed)
            elif message.content == "*roulette":
                bullet = random.randrange(1,7)
                if bullet == 6:
                    DeadEmbed = discord.Embed(color=0xba0000)
                    DeadEmbed.title = "Get Tabarnaqued " 
                    DeadEmbed.description = 'No one came to your funeral and you died a virgin LMAO'
                    await message.channel.send(embed=DeadEmbed)
                    await message.channel.send(file=discord.File(r'/home/yasser/Desktop/desktop/Python_Bot/Images/Fart.mp4'))
                    print(bullet)
                else:
                    AliveEmbed = discord.Embed(color=0x08ff00)
                    AliveEmbed.title = "You're alive, I guess"
                    AliveEmbed.description = "Bruh just die already"
                    await message.channel.send(embed=AliveEmbed)          
            elif message.content == "*history":
                await message.channel.send("Sending you this server's logs in DMs")
                await message.author.send(file=discord.File(r'/home/yasser/Desktop/desktop/Python_Bot/' + 'MessageLog_'+ str(message.guild.name) + '.txt'))
            elif message.content == "*time":
                now = datetime.datetime.now()
                Year = str(now.year)
                Month = now.strftime('%B')
                Day = str(now.day)
                Hour = str(now.hour)
                if now.minute < 10:
                    Minute = "0" + str(now.minute)
                else:
                    Minute = str(now.minute)
                CurrentDate =  "Today is " + Month + " " + Day + ", " + Year + "\nHour = " +  Hour + ":" +  Minute
                await message.channel.send(CurrentDate)
            elif "say" in message.content and "cowsay" not in message.content:
                await message.delete()
                await message.channel.send(message.content.replace("*say", ""))
            elif "purge" in message.content:
                if message.author.guild_permissions.administrator: 
                    Ammount = int(message.content.replace("*purge" , ""))
                    async for x in message.channel.history(limit=Ammount + 1):
                        await x.delete()
                elif message.author.name == "Nuclear Bomb":
                    Ammount = int(message.content.replace("*purge" , ""))
                    async for x in message.channel.history(limit=Ammount + 1):
                        await x.delete()
                elif message.author.name == "darkish":
                    Ammount = int(message.content.replace("*purge" , ""))
                    async for x in message.channel.history(limit=Ammount + 1):
                        await x.delete()
                else:
                    await message.channel.send("You don't have admin, that's a bit ***sussy***")
            elif "dl" in message.content:
                Link=message.content.replace("*dl", "")
                try: 
                    yt = YouTube(Link) 
                    await message.channel.send("Starting to download...\nVideo: " + yt.title )
                except: 
                    await message.channel.send("Connection Error")
                video = yt.streams.get_highest_resolution().download(SAVE_PATH)
                os.rename(yt.streams.get_highest_resolution().default_filename, yt.title + ".mp4")
                file = open(SAVE_PATH + "/" + yt.title + ".mp4","r")                      
                file_drive = drive.CreateFile({'title':os.path.basename(file.name)})  
                file_drive.SetContentFile(os.path.join(SAVE_PATH + '/',os.path.basename(file.name))) 
                file_drive.Upload()
                file.close()
                permission = file_drive.InsertPermission({
                            'type': 'anyone',
                            'value': 'anyone',
                            'role': 'reader'})
                DriveLink=file_drive['alternateLink']
                await message.channel.send(DriveLink)
                os.chdir(r'/home/yasser/Desktop/desktop/Python_Bot/')
                for x in glob.glob("*.mp4"):
                    os.remove(x)
                file_drive = None
            elif  message.content == "*problem":
                await message.channel.send("<@!550482788550180875> your bot is being dumb come fix it")
            elif "play" in message.content:
                VidLink = message.content.replace("*play ", "")
                try: 
                    yt = YouTube(VidLink) 
                except: 
                    await message.channel.send("Connection Error")
                yt.streams.get_audio_only().download(SAVE_PATH)
                os.rename(yt.streams.get_audio_only().default_filename, yt.title + ".mp3")
                voice_channel = message.author.voice.channel
                def SussyTrue():
                    sussy = True
                async def PlayCheck():
                    if vc.is_playing == False:
                        for x in client.voice_clients:
                            if(x.guild == message.guild):
                                return await x.disconnect()
                        os.remove(SAVE_PATH + "/" + yt.title + ".mp3")
                vc = await voice_channel.connect()
                message = await message.channel.send("Now playing: " + yt.title)
                vc.play(discord.FFmpegPCMAudio(SAVE_PATH + "/" + yt.title + ".mp3"), after=lambda e: SussyTrue())
                audiofile = audioread.audio_open(SAVE_PATH + "/" + yt.title + ".mp3")
                length = audiofile.duration
                print(length)
                time.sleep(length)
                for x in client.voice_clients:
                        if(x.guild == message.guild):
                            return await x.disconnect()
                os.remove(SAVE_PATH + "/" + yt.title + ".mp3")
                def stopcheck(m):
                            return m.content == 'stop' and m.channel == message.channel
                stopmsg = await client.wait_for('message', check=stopcheck)
                if stopmsg:
                    for x in client.voice_clients:
                        if(x.guild == message.guild):
                            return await x.disconnect()
                    os.remove(SAVE_PATH + "/" + yt.title + ".mp3")
            elif message.content.startswith("*ascii"):
                MessageToPrint = message.content.replace("*ascii ", "")
                if len(MessageToPrint) > 30:
                    await message.channel.send("Too long, didn't read")
                ascii = ""
                for x in MessageToPrint:
                    match x:
                        case "a":
                                ascii += """   
░█████╗░
██╔══██╗
███████║
██╔══██║
██║░░██║
╚═╝░░╚═╝ """
                        case "b":
                            ascii += """
██████╗░
██╔══██╗
██████╦╝
██╔══██╗
██████╦╝
╚═════╝░"""
                        case "c":
                            ascii += """
░█████╗░
██╔══██╗
██║░░╚═╝
██║░░██╗
╚█████╔╝
░╚════╝░"""
                        case "d":
                            ascii += """
██████╗░
██╔══██╗
██║░░██║
██║░░██║
██████╔╝
╚═════╝░"""
                        case "e":
                            ascii += """
███████╗
██╔════╝
█████╗░░
██╔══╝░░
███████╗
╚══════╝"""
                        case "f":
                            ascii += """
███████╗
██╔════╝
█████╗░░
██╔══╝░░
██║░░░░░
╚═╝░░░░░"""
                        case "g":
                            ascii += """
░██████╗░
██╔════╝░
██║░░██╗░
██║░░╚██╗
╚██████╔╝
░╚═════╝░"""
                        case "h":
                            ascii += """
██╗░░██╗
██║░░██║
███████║
██╔══██║
██║░░██║
╚═╝░░╚═╝"""
                        case "i":
                            ascii += """
░░██╗░░
░░██║░░
░░██║░░
░░██║░░
░░██║░░
░░╚═╝░░"""
                        case "j":
                            ascii += """
░░░░░██╗
░░░░░██║
░░░░░██║
██╗░░██║
╚█████╔╝
░╚════╝░"""
                        case "k":
                            ascii += """
██╗░░██╗
██║░██╔╝
█████═╝░
██╔═██╗░
██║░╚██╗
╚═╝░░╚═╝"""
                        case "l":
                            ascii += """
██╗░░░░░
██║░░░░░
██║░░░░░
██║░░░░░
███████╗
╚══════╝"""
                        case "m" :
                            ascii += """
███╗░░░███╗
████╗░████║
██╔████╔██║
██║╚██╔╝██║
██║░╚═╝░██║
╚═╝░░░░░╚═╝"""
                        case "n":
                            ascii += """
███╗░░██╗
████╗░██║
██╔██╗██║
██║╚████║
██║░╚███║
╚═╝░░╚══╝"""
                        case "o":
                            ascii += """
░█████╗░
██╔══██╗
██║░░██║
██║░░██║
╚█████╔╝
░╚════╝░"""
                        case "p":
                            ascii += """
██████╗░
██╔══██╗
██████╔╝
██╔═══╝░
██║░░░░░
╚═╝░░░░░"""
                        case "q":
                            ascii += """
░██████╗░
██╔═══██╗
██║██╗██║
╚██████╔╝
░╚═██╔═╝░
░░░╚═╝░░░"""
                        case "r":
                            ascii += """
██████╗░
██╔══██╗
██████╔╝
██╔══██╗
██║░░██║
╚═╝░░╚═╝"""
                        case "s":
                            ascii += """
░██████╗
██╔════╝
╚█████╗░
░╚═══██╗
██████╔╝
╚═════╝░"""
                        case "t":
                            ascii += """
████████╗
╚══██╔══╝
░░░██║░░░
░░░██║░░░
░░░██║░░░
░░░╚═╝░░░"""
                        case "u":
                            ascii += """
██╗░░░██╗
██║░░░██║
██║░░░██║
██║░░░██║
╚██████╔╝
░╚═════╝░"""
                        case "v":
                            ascii += """
██╗░░░██╗
██║░░░██║
╚██╗░██╔╝
░╚████╔╝░
░░╚██╔╝░░
░░░╚═╝░░░"""
                        case "w":
                            ascii += """
░██╗░░░░░░░██╗
░██║░░██╗░░██║
░╚██╗████╗██╔╝
░░████╔═████║░
░░╚██╔╝░╚██╔╝░
░░░╚═╝░░░╚═╝░░"""
                        case "x":
                            ascii += """
██╗░░██╗
╚██╗██╔╝
░╚███╔╝░
░██╔██╗░
██╔╝╚██╗
╚═╝░░╚═╝"""
                        case "y":
                            ascii += """
██╗░░░██╗
╚██╗░██╔╝
░╚████╔╝░
░░╚██╔╝░░
░░░██║░░░
░░░╚═╝░░░"""
                        case "z":
                            ascii += """
███████╗
╚════██║
░░███╔═╝
██╔══╝░░
███████╗
╚══════╝"""
                        case "A":
                                ascii += """   
░█████╗░
██╔══██╗
███████║
██╔══██║
██║░░██║
╚═╝░░╚═╝ """
                        case "B":
                            ascii += """
██████╗░
██╔══██╗
██████╦╝
██╔══██╗
██████╦╝
╚═════╝░"""
                        case "C":
                            ascii += """
░█████╗░
██╔══██╗
██║░░╚═╝
██║░░██╗
╚█████╔╝
░╚════╝░"""
                        case "D":
                            ascii += """
██████╗░
██╔══██╗
██║░░██║
██║░░██║
██████╔╝
╚═════╝░"""
                        case "E":
                            ascii += """
███████╗
██╔════╝
█████╗░░
██╔══╝░░
███████╗
╚══════╝"""
                        case "F":
                            ascii += """
███████╗
██╔════╝
█████╗░░
██╔══╝░░
██║░░░░░
╚═╝░░░░░"""
                        case "G":
                            ascii += """
░██████╗░
██╔════╝░
██║░░██╗░
██║░░╚██╗
╚██████╔╝
░╚═════╝░"""
                        case "H":
                            ascii += """
██╗░░██╗
██║░░██║
███████║
██╔══██║
██║░░██║
╚═╝░░╚═╝"""
                        case "I":
                            ascii += """
░░██╗░░
░░██║░░
░░██║░░
░░██║░░
░░██║░░
░░╚═╝░░"""
                        case "J":
                            ascii += """
░░░░░██╗
░░░░░██║
░░░░░██║
██╗░░██║
╚█████╔╝
░╚════╝░"""
                        case "K":
                            ascii += """
██╗░░██╗
██║░██╔╝
█████═╝░
██╔═██╗░
██║░╚██╗
╚═╝░░╚═╝"""
                        case "L":
                            ascii += """
██╗░░░░░
██║░░░░░
██║░░░░░
██║░░░░░
███████╗
╚══════╝"""
                        case "M" :
                            ascii += """
███╗░░░███╗
████╗░████║
██╔████╔██║
██║╚██╔╝██║
██║░╚═╝░██║
╚═╝░░░░░╚═╝"""
                        case "N":
                            ascii += """
███╗░░██╗
████╗░██║
██╔██╗██║
██║╚████║
██║░╚███║
╚═╝░░╚══╝"""
                        case "O":
                            ascii += """
░█████╗░
██╔══██╗
██║░░██║
██║░░██║
╚█████╔╝
░╚════╝░"""
                        case "P":
                            ascii += """
██████╗░
██╔══██╗
██████╔╝
██╔═══╝░
██║░░░░░
╚═╝░░░░░"""
                        case "Q":
                            ascii += """
░██████╗░
██╔═══██╗
██║██╗██║
╚██████╔╝
░╚═██╔═╝░
░░░╚═╝░░░"""
                        case "R":
                            ascii += """
██████╗░
██╔══██╗
██████╔╝
██╔══██╗
██║░░██║
╚═╝░░╚═╝"""
                        case "S":
                            ascii += """
░██████╗
██╔════╝
╚█████╗░
░╚═══██╗
██████╔╝
╚═════╝░"""
                        case "T":
                            ascii += """
████████╗
╚══██╔══╝
░░░██║░░░
░░░██║░░░
░░░██║░░░
░░░╚═╝░░░"""
                        case "U":
                            ascii += """
██╗░░░██╗
██║░░░██║
██║░░░██║
██║░░░██║
╚██████╔╝
░╚═════╝░"""
                        case "V":
                            ascii += """
██╗░░░██╗
██║░░░██║
╚██╗░██╔╝
░╚████╔╝░
░░╚██╔╝░░
░░░╚═╝░░░"""
                        case "W":
                            ascii += """
░██╗░░░░░░░██╗
░██║░░██╗░░██║
░╚██╗████╗██╔╝
░░████╔═████║░
░░╚██╔╝░╚██╔╝░
░░░╚═╝░░░╚═╝░░"""
                        case "X":
                            ascii += """
██╗░░██╗
╚██╗██╔╝
░╚███╔╝░
░██╔██╗░
██╔╝╚██╗
╚═╝░░╚═╝"""
                        case "Y":
                            ascii += """
██╗░░░██╗
╚██╗░██╔╝
░╚████╔╝░
░░╚██╔╝░░
░░░██║░░░
░░░╚═╝░░░"""
                        case "Z":
                            ascii += """
███████╗
╚════██║
░░███╔═╝
██╔══╝░░
███████╗
╚══════╝"""

                        case " ":
                            ascii += """


"""
                        case ".":
                            ascii += """
░░░
░░░
░░░
░░░
██╗
╚═╝"""
                        case ",":
                            ascii += """
░░░
░░░
░░░
██╗
╚█║
░╚╝"""
                        case ";":
                            ascii += """
██╗
╚═╝
░░░
██╗
╚█║
░╚╝"""
                        case ":":
                            ascii += """
██╗
╚═╝
░░░
░░░
██╗
╚═╝"""
                        case "<":
                            ascii += """
░░██╗
░██╔╝
██╔╝░
╚██╗░
░╚██╗
░░╚═╝"""
                        case ">":
                            ascii += """
██╗░░
╚██╗░
░╚██╗
░██╔╝
██╔╝░
╚═╝░░"""
                        case "=":
                            ascii += """
░░░░░░░
██████╗
╚═════╝
██████╗
╚═════╝
░░░░░░░"""
                        case "+":
                            ascii += """
░░░░░░░
░░██╗░░
██████╗
╚═██╔═╝
░░╚═╝░░
░░░░░░░"""
                        case "-":
                            ascii += """
░░░░░░
░░░░░░
█████╗
╚════╝
░░░░░░
░░░░░░"""
                        case "0":
                            ascii += """
░█████╗░
██╔══██╗
██║░░██║
██║░░██║
╚█████╔╝
░╚════╝░"""
                        case "1":
                            ascii += """
░░███╗░░
░████║░░
██╔██║░░
╚═╝██║░░
███████╗
╚══════╝"""
                        case "2":
                            ascii += """
██████╗░
╚════██╗
░░███╔═╝
██╔══╝░░
███████╗
╚══════╝"""
                        case "3":
                            ascii += """
██████╗░
╚════██╗
░█████╔╝
░╚═══██╗
██████╔╝
╚═════╝░"""
                        case "4":
                            ascii += """
░░██╗██╗
░██╔╝██║
██╔╝░██║
███████║
╚════██║
░░░░░╚═╝"""
                        case "5":
                            ascii += """
███████╗
██╔════╝
██████╗░
╚════██╗
██████╔╝
╚═════╝░"""
                        case "6":
                            ascii += """
░█████╗░
██╔═══╝░
██████╗░
██╔══██╗
╚█████╔╝
░╚════╝░"""
                        case "7":
                            ascii += """
███████╗
╚════██║
░░░░██╔╝
░░░██╔╝░
░░██╔╝░░
░░╚═╝░░░"""
                        case "8":
                            ascii += """
░█████╗░
██╔══██╗
╚█████╔╝
██╔══██╗
╚█████╔╝
░╚════╝░"""
                        case "9":
                            ascii += """
░█████╗░
██╔══██╗
╚██████║
░╚═══██║
░█████╔╝
░╚════╝░"""

                await message.channel.send(ascii)

        #Return if prefix isn't found
        else:
            return

async def Fight(self, message):
    MyClient.HP -= 1
    await message.channel.send(str(MyClient.HP) + " HP")
    if MyClient.HP == 0:
        await message.channel.send("Wow you killed him im so proud of you")

def on_exit():
    DeleteMP3.Start()

atexit.register(on_exit)
#Login
client = MyClient()
client.run('')
game = discord.Game("tabarnaque")