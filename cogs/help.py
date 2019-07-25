import discord
from discord.ext import commands


class Help (commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def help(self, ctx):

        embed = discord.Embed(title="Help has been sent!", description="Check your private messages.", color=discord.Color.green())
        embed.set_thumbnail(url="https://discordapp.com/assets/c6b26ba81f44b0c43697852e1e1d1420.svg")
        embed.set_footer(text="Shazbot")
        await ctx.send(embed=embed)

        private_embed = discord.Embed(title="Meme category", description="Mostly meme stuff.", color=discord.Color.blue())
        private_embed.set_author(name="Commands of this bot", icon_url = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/180/black-question-mark-ornament_2753.png")
        private_embed.add_field(name=".meme", value='Posts a meme from the "drive".', inline=False)
        private_embed.add_field(name=".leaderboard", value="Best top 5 memers on .", inline=True)
        private_embed.add_field(name=".full_leaderboard", value="Full list of the leaderboard.", inline=True)
        private_embed.add_field(name='.search "user"',value="Posts a meme from specified memer. Has to be exact name from leaderboard.",inline=False)
        private_embed.add_field(name=".addme", value="Tells you a way of getting on the drive.", inline=True)
        private_embed.set_footer(text="ShazBot")
        await ctx.message.author.send(embed=private_embed)

        private_embed2 = discord.Embed(title="Homework category", description="Homework material stuff.(NSFW)", color=0xff69b4)
        private_embed2.set_author(name="Commands of this bot", icon_url = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/180/black-question-mark-ornament_2753.png")
        private_embed2.add_field(name=".homework", value='Your number one homework material provider.', inline=False)
        private_embed2.add_field(name=".homework_leaderboard", value="Ohh.... you know.", inline=True)
        private_embed2.add_field(name="search_homework", value="Searches for specified person's homework material", inline=True)
        private_embed2.set_footer(text="ShazBot")
        await ctx.message.author.send(embed=private_embed2)

        private_embed3 = discord.Embed(title='Game category", description="Best way to make some "CHROMOSOMES™"', color = discord.Color.blue())
        private_embed3.set_author(name="Commands of this bot", icon_url = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/180/black-question-mark-ornament_2753.png")
        private_embed3.add_field(name=".trapornot", value="In this stunning game you will have to guess the sex of the human in the picture.",inline=False)
        private_embed3.add_field(name=".whosmemeisit", value="Guess who's meme is it", inline=False)
        private_embed3.set_footer(text="ShazBot")
        await ctx.message.author.send(embed=private_embed3)

        private_embed4 = discord.Embed(title="Economy category", description='You can use our currency "CHROMOSOMES™". To make some "CHROMOSOMES™"', color = discord.Color.blue())
        private_embed4.set_author(name="Commands of this bot", icon_url = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/180/black-question-mark-ornament_2753.png")
        private_embed4.add_field(name=".balance", value='Prints the amount of "CHROMOSOMES™" you have', inline=False)
        private_embed4.add_field(name=".pay @user amount", value='Give some "CHROMOSOMES™" to some one (min: 1)', inline=False)
        private_embed4.add_field(name=".reset_chromosomes", value='DANGEROUS COMMAND DO NOT RUN unless you are getting errors in our awesome system "CHROMOSOMES™"', inline=False)
        private_embed4.set_footer(text="ShazBot")
        await ctx.message.author.send(embed=private_embed4)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def addme(self, ctx):
        embed = discord.Embed(title="Help has been sent!", description="Check your private messages.", color=discord.Color.green())
        embed.set_thumbnail(url="https://discordapp.com/assets/c6b26ba81f44b0c43697852e1e1d1420.svg")
        embed.set_footer(text="Shazbot")
        await ctx.send(embed=embed)
        await ctx.message.author.send("You will need to join this server to get validated. And added to the drive https://discord.gg/FjAMMxY")

def setup(client):
    client.add_cog(Help(client))
