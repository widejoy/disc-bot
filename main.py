from discord import app_commands
import discord
import aiohttp
from discord import Embed
from dotenv import load_dotenv
import os

load_dotenv()

TEST_GUILD = discord.Object(932674444583911474)

TOKEN = os.environ.get("DISCORD_TOKEN")

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.tree.command()
async def hello(interaction: discord.Interaction):
    "test"
    await interaction.response.send_message('Hello')

@client.tree.command()
async def poll(interaction:discord.Interaction, date:str):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.waqi.info/feed/here/?token=a9c77eb13c293e975b9afd7fddd043417629ad24") as resp:
            data = await resp.json()
            date_var="2022-11-"
            date_act=date_var + date
                
            dict1={}
            for i in data["data"]["forecast"]["daily"]["pm10"]:
                if i["day"]==date_act:
                    for j in i.keys():
                       
                        dict1[j]=i[j]
                        # print(dict1)
                        

            dict2={}
            for i in data["data"]["forecast"]["daily"]["pm25"]:
                if i["day"]==date_act:
                    for j in i.keys():
                        
                        dict2[j]=i[j]
                        # print(dict2)

        embed = Embed(title="POLLUTION LEVELS OF DELHI p10")
        for i in dict1.keys():
            embed.add_field(name=i,value=dict1[i])

        embed2 = Embed(title="POLLUTION LEVELS OF DELHI p25")
        for i in dict2.keys():
            embed2.add_field(name=i,value=dict2[i])


        await interaction.response.send_message(embeds=[embed, embed2])




client.run(TOKEN)