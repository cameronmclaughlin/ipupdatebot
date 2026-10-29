import discord
import time
from discord.ext import commands
from discord.ext import tasks
import requests

updateChannelID = 1565193431196635267

class ipUpdate(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()

        status = discord.Activity(type=discord.ActivityType.custom, name="yay ip")

        super().__init__(command_prefix="!", intents=intents, activity=status, status=discord.Status.online)

bot = ipUpdate()

@tasks.loop(hours=1.0)
async def hourlyUpdate():
    public_ip = requests.get('https://api.ipify.org').text
    print(f"update {public_ip}")
    channel = await bot.fetch_channel(updateChannelID)
    embed = discord.Embed(
        title="Hourly IP Update",
        description=f"IP is currently {public_ip}",
        color=discord.Color.green()
    )
    embed.set_footer(
        text="Use this to connect to the server. This is subject to change"
    )

    await channel.send(embed=embed)

token = ""
with open(".env", "r", encoding="utf-8") as file:
    token = file.read()

@bot.event
async def on_ready():
    hourlyUpdate.start()

bot.run(token)