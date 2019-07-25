import discord
from discord.ext import commands

from functions.json_functions import *


class Economy (commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def reset_chromosomes(self, ctx):
        update_data(ctx.message.author)
        await ctx.send("Balance is now : 0")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def balance(self, ctx):
        await ctx.send(
            str(ctx.message.author.name) + " has about: " + str(
                check_chromosomes(ctx.message.author)) + " chromosomes™")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pay(self, ctx, user: discord.User, arg):
        if int(arg) < 1:
            await ctx.send("You can only send one full chromosome™")
            return

        if check_chromosomes(ctx.message.author) < 0:
            await ctx.send("You need to pay the chromosome™ tax first")
            return

        if check_chromosomes(ctx.message.author) < int(arg):
            await ctx.send("You don't even have that many chromosomes™")
            return
        transfer_chromosomes(ctx.message.author, user, int(arg))
        await ctx.send(str(ctx.message.author.name) + " has paid " + str(user.name) + " " + arg + " chromosomes™")


def setup(client):
    client.add_cog(Economy(client))
