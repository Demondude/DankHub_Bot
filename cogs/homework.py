import asyncio
import os
import random

import discord
from discord.ext import commands

from functions.file_functions import get_config, rebuild_database, get_image, add_line


class Homework (commands.Cog):
    def __init__(self, client):
        self.client = client
        self._, self._, self._, self.homeworkDir, self._ = get_config()

    # Administrative command
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def rhb(self, ctx):
        embed = discord.Embed(
            title='Rebuilding homework database...',
            colour=discord.Color.red()
        )
        embed.set_footer(text='This will take time.')
        await ctx.send(embed=embed)
        rebuild_database("homework_database", self.homeworkDir)
        await ctx.send("Done.")
    # User commands

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.is_nsfw()
    async def homework(self, ctx):
        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == "❗"

        homework_selected, uploader = get_image("homework_database", self.homeworkDir)

        embed = discord.Embed(
            title='From ' + uploader + ' Collection.',
            colour=0xff69b4
        )
        embed.set_footer(text=".fbi_report please use it.")
        await ctx.send(file=discord.File(homework_selected))
        lastmsg = await ctx.send(embed=embed)
        await lastmsg.add_reaction(emoji="❗")

        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=10.0, check=check)
        except asyncio.TimeoutError:
            return
        else:
            await ctx.send("Homework reported.")
            add_line(homework_selected, "trash_database")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.is_nsfw()
    async def search_homework(self, ctx, arg1):
        if ctx.message.channel.name == "homework":
            user_folder = self.homeworkDir + os.sep + arg1
            if os.path.exists(user_folder):
                user_folder_list = os.listdir(user_folder)
                homework_selected = user_folder + os.sep + random.choice(user_folder_list)

                embed = discord.Embed(
                    title='From ' + arg1 + "'s Collection.",
                    colour=discord.Color.blue()
                )
                embed.set_footer(text='Has about: ' + str(sum([len(files) for r, d, files in os.walk(user_folder)])))
                await ctx.send(file=discord.File(homework_selected))
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='User ' + arg1 + " was not found",
                    colour=discord.Color.dark_red()
                )
                embed.set_footer(text='Sorry.......')
                await ctx.send(embed=embed)
        else:
            await ctx.send("Wrong channel. Go to homework")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def homework_leaderboard(self, ctx):
        if ctx.message.channel.name == "leaderboards":
            path_memes = self.homeworkDir
            meme_array = os.listdir(path_memes)
            meme_array_size = [0] * len(meme_array)

            for i in range(len(meme_array)):
                meme_array_size[i] = len(os.listdir(path_memes + os.sep + meme_array[i]))

            for passnum in range(len(meme_array_size) - 1, 0, -1):
                for i in range(passnum):
                    if meme_array_size[i] < meme_array_size[i + 1]:
                        temp = meme_array_size[i]
                        meme_array_size[i] = meme_array_size[i + 1]
                        meme_array_size[i + 1] = temp
                        temp_str = meme_array[i]
                        meme_array[i] = meme_array[i + 1]
                        meme_array[i + 1] = temp_str

            embed = discord.Embed(
                title="These are the BEST homework posters in this server ",
                colour=0xff69b4
            )
            embed.set_author(name="Leaderboard",
                             icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/180/heavy-black-heart_2764.png")
            for i in range(len(meme_array)):
                if meme_array_size[i] != 0:
                    embed.add_field(name=meme_array[i], value=str(meme_array_size[i]), inline=False)
            cpt = sum([len(files) for r, d, files in os.walk(path_memes)])
            embed.set_footer(text='In total we have: ' + str(cpt) + ' homework material.')
            await ctx.send(embed=embed)
        else:
            await ctx.send("Wrong channel. Go to leaderboards")


def setup(client):
    client.add_cog(Homework(client))
