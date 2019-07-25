import asyncio
import os
import random

import discord
from discord.ext import commands

from functions.file_functions import get_config, rebuild_database, get_image
from functions.json_functions import update_chromosomes


class Games (commands.Cog):
    def __init__(self, client):
        self.client = client
        self._, self.trapDir, self.memeDir, self._, self._ = get_config()

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def rtb(self, ctx):
        embed = discord.Embed(
            title='Rebuilding trap database...',
            colour=discord.Color.red()
        )
        embed.set_footer(text='This will take time.')
        await ctx.send(embed=embed)
        rebuild_database("trap_database", self.trapDir)
        await ctx.send("Done.")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def trapornot(self, ctx):

        def check(reaction, user):
            if str(reaction.emoji) == "✅":
                return user == ctx.message.author and str(reaction.emoji) == "✅"
            else:
                return user == ctx.message.author and str(reaction.emoji) == "❎"

        image_location, gender = get_image("trap_database", self.trapDir)

        if gender == "Trap":
            true_answer = "✅"
        else:
            true_answer = "❎"

        embed = discord.Embed(title="Is this a trap?", color=0xfb2fbd)
        embed.set_author(name="Trap or not?",
                         icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/twitter/180/female-sign_2640.png")
        embed.set_footer(text="Answer with reactions!!!")
        await ctx.send(file=discord.File(image_location))
        botmsg = await ctx.send(embed=embed)
        await botmsg.add_reaction(emoji="✅")
        await botmsg.add_reaction(emoji="❎")

        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("UR TOO SLOW!!!!!")
        else:
            if str(reaction.emoji) == true_answer:
                win_amount = random.uniform(0, 1)
                update_chromosomes(ctx.message.author, win_amount)
                await ctx.send("Ok you win. Adding " + str(win_amount) + " chromosomes™")
            else:
                win_amount = random.uniform(-1, 0)
                update_chromosomes(ctx.message.author, win_amount)
                await ctx.send("Lmao no. You are wrong. How did you not see it ? " + str(win_amount) + " chromosomes™")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def whosmemeisit(self, ctx):
        def check(m):
            if m.content == '1':
                return m.content == '1' and m.channel == ctx.channel
            if m.content == '2':
                return m.content == '2' and m.channel == ctx.channel
            if m.content == '3':
                return m.content == '3' and m.channel == ctx.channel

        embed = discord.Embed(title="Who's meme is it ?", color=0x3cffff)
        embed.set_thumbnail(
            url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/180/black-question-mark-ornament_2753.png")
        embed.set_footer(text="It's ez")
        answer = random.randint(1, 3)
        print(str(answer))
        answer_list = os.listdir(self.memeDir)
        answer_list_choice = random.choice(answer_list)
        img_list = os.listdir(self.memeDir + os.sep + answer_list_choice)
        img_list_choice = random.choice(img_list)
        while img_list_choice == "desktop.ini":
            answer_list_choice = random.choice(answer_list)
            img_list = os.listdir(self.memeDir + os.sep + answer_list_choice)
            img_list_choice = random.choice(img_list)
        image_location = self.memeDir + os.sep + answer_list_choice + os.sep + img_list_choice

        await ctx.send(file=discord.File(image_location))
        for x in range(1, 4):
            if x == answer:
                embed.add_field(name=answer_list_choice, value="Type " + str(x) + ".", inline=False)
            else:
                not_answer = random.choice(answer_list)
                if not_answer != answer_list_choice:
                    embed.add_field(name=not_answer, value="Type " + str(x) + ".", inline=False)
        await ctx.send(embed=embed)
        user_answer = await self.client.wait_for('message', check=check)

        if str(answer) == user_answer.content:
            win_amount = random.randint(1, 15)
            update_chromosomes(ctx.message.author, win_amount)
            await ctx.send("Ok you win. Adding " + str(win_amount) + " chromosomes™")
        else:
            win_amount = -random.randint(1, 5)
            update_chromosomes(ctx.message.author, win_amount)
            await ctx.send(
                "Lmao no. You are wrong. It was " + answer_list_choice + "'s meme " + str(win_amount) + " chromosomes™")







def setup(client):
    client.add_cog(Games(client))
