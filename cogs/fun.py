import discord
from discord.ext import commands
from discord.utils import get
import datetime

class fun (commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        spamFile = open("spam_sites")
        content = spamFile.readlines()
        content = [x.strip() for x in content]

        for test in content:
            if test in message.content:

                # Moderation information

                embed = discord.Embed(title="Ladies and gentlemen we got him.", description="Sending him to the ranch",
                                      color=discord.Color.red())
                embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                channel = self.client.get_channel(552131493988663298)
                embed.add_field(name="Reason", value="Posted a scam link", inline=True)
                embed.add_field(name="Message", value=message.content, inline=True)
                embed.set_footer(text="ShazBot_AntiSpam " + str(datetime.datetime.now()))
                await channel.send(embed=embed)

                # Role manager

                for role in message.author.roles:
                    if role.name == "@everyone":
                        continue
                    await message.author.remove_roles(role)
                role = get(message.guild.roles, name="Indian")
                await message.author.add_roles(role)

                # Information for user.

                embed2 = discord.Embed(title="It seems that our bot has detected that you are a spam bot",
                                      description="Well no worries, you can ask any admins to put you back.",
                                      color=discord.Color.red())
                embed2.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                embed2.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/180/black-question-mark-ornament_2753.png")
                embed2.set_footer(text="ShazBot_AntiSpam " + str(datetime.datetime.now()))
                await message.author.send(embed=embed2)
                await message.delete()

                #Data collection

                dataFile = open("spam_data", "a")
                dataFile.write(message.author.name + " " + str(datetime.datetime.now()) + "\n")
                dataFile.close()


def setup(client):
    client.add_cog(fun(client))