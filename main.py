import discord
import time
from discord.ext import commands
from discord.ext import tasks
import requests
import mcstatus

lastIp = ""
updateChannelID = 1565193431196635267
lastOnline = False

class ipUpdate(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()

        status = discord.Activity(type=discord.ActivityType.custom, name="yay ip")

        super().__init__(command_prefix="!", intents=intents, activity=status, status=discord.Status.online)

    async def setup_hook(self):
        await self.tree.sync()
        print("Command tree synced")

bot = ipUpdate()

def getIp():
    return requests.get('https://api.ipify.org').text

@tasks.loop(minutes=1.0)
async def hourlyUpdate():
    ip = getIp()
    channel = await bot.fetch_channel(updateChannelID)
    if (ip != lastIp):
        embed = discord.Embed(
            title="New IP detected",
            description=f"IP is currently {ip}",
            color=discord.Color.green()
        )
        embed.set_footer(
            text="Use this to connect to the server. This is subject to change"
        )
        
        lastIp = ip
        await channel.send(embed=embed)
    # now, check if the server is online or offline
    online = False
    server = mcstatus.JavaServer(lastIp, 25565)
    try:
        status = server.status()
        online = True
    except Exception as e:
        online = False
    if(online != lastOnline):
        lastOnline = online
        statusEmbed = discord.Embed(
            title="Server has gone online",
            description="",
            color=discord.Color.green()
        )
        if (online == False):
            statusEmbed.title = "Server has gone offline"
            statusEmbed.color = discord.Color.red()
        await channel.send(embed=statusEmbed)
    

token = ""
with open(".env", "r", encoding="utf-8") as file:
    token = file.read()

@bot.tree.command(name="status", description="Get the status of the server")
async def getServerInfo(intr: discord.Interaction):
    await intr.response.defer(thinking=True)
    replyEmbed = discord.Embed(
        title = "Server Status",
        description = "",
        color = discord.Color.green()
    )
    server = mcstatus.JavaServer(getIp(), 25565)
    server.timeout = 1.5
    try:
        status = server.status()
        replyEmbed.add_field(name="IP", value=getIp(), inline=False)
        replyEmbed.add_field(name="MOTD", value=status.motd.raw, inline=False)
        replyEmbed.add_field(name="Latency", value=f"{int(status.latency)}ms", inline=False)
        replyEmbed.add_field(name="Online Count", value=f"{status.players.online}/{status.players.max}", inline=False)
        playerString = ""
        if status.players.sample:
            for player in status.players.sample:
                playerString+=f"{player.name}\n"
            replyEmbed.add_field(name="Players", value=playerString)
    except Exception as e:
        replyEmbed.description = "Server is probably offline"
        replyEmbed.add_field(name="RESPONSE", value=e, inline=False)
        replyEmbed.color = discord.Color.red()

    #await intr.response.send_message(embed=replyEmbed)
    await intr.followup.send(embed=replyEmbed)

@bot.event
async def on_ready():
    hourlyUpdate.start()

bot.run(token)