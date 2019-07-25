import asyncio
import os
import random

import discord
from discord.ext import commands

from functions.file_functions import get_image, get_config, rebuild_database, add_line


class MemeCommands (commands.Cog):
    def __init__(self, client):
        self.client = client
        self._, self._, self.memeDir, self._, self.trashDir = get_config()

    # Administrative command
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def rmb(self, ctx):
        embed = discord.Embed(
            title='Rebuilding meme database...',
            colour=discord.Color.red()
        )
        embed.set_footer(text='This will take time.')
        await ctx.send(embed=embed)
        rebuild_database("meme_database", self.memeDir)
        await ctx.send("Done.")

    # User commands

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def meme(self, ctx):
        if ctx.message.channel.name == "memes":

            def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) == "❗"

            meme_selected, uploader = get_image("meme_database", self.memeDir)

            embed = discord.Embed(
                title='From ' + uploader + "'s Collection.",
                colour=discord.Color.blue()
                # TODO get a web server to use embeds
            )
            embed.set_footer(text='You have 5 seconds to report shit memes by clicking the ! button.')
            await ctx.send(file=discord.File(meme_selected))
            lastmsg = await ctx.send(embed=embed)

            await lastmsg.add_reaction(emoji="❗")

            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=5.0, check=check)
            except asyncio.TimeoutError:
                return
            else:
                await ctx.send("Meme reported.")
                add_line(meme_selected, "trash_database")

        else:
            await ctx.send("Wrong channel. Go to memes")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def search(self, ctx, arg1):
        user_folder = self.memeDir + "/" + arg1
        if os.path.exists(user_folder):
            user_folder_list = os.listdir(user_folder)
            meme_selected = user_folder + "/" + random.choice(user_folder_list)

            embed = discord.Embed(
                title='From ' + arg1 + "'s Collection.",
                colour=discord.Color.blue()
            )
            embed.set_footer(text='Has about: ' + str(sum([len(files) for r, d, files in os.walk(user_folder)])))
            await ctx.send(file=discord.File(meme_selected))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='User ' + arg1 + " was not found",
                colour=discord.Color.dark_red()
            )
            embed.set_footer(text='Sorry.......')
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def leaderboard(self, ctx):
        if ctx.message.channel.name == "leaderboards":
            path_memes = self.memeDir
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
                title="These are the BEST memers in this server ",
                colour=discord.Color.red()
            )
            embed.set_author(name="Leaderboard",
                             icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/180/crossed-swords_2694.png")
            for i in range(0, 8):
                embed.add_field(name=meme_array[i], value=str(meme_array_size[i]), inline=False)
            cpt = sum([len(files) for r, d, files in os.walk(path_memes)])
            embed.set_footer(text='In total we have: ' + str(cpt) + ' memes.')
            await ctx.send(embed=embed)
        else:
            await ctx.send("Wrong channel. Go to leaderboards")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def full_leaderboard(self, ctx):
        if ctx.message.channel.name == "leaderboards":
            path_memes = self.memeDir
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

            for i in range(len(meme_array)):
                meme_array[i] = meme_array[i] + " (" + str(meme_array_size[i]) + ")\n"

            cpt = sum([len(files) for r, d, files in os.walk(path_memes)])
            await ctx.send("```" + ''.join(meme_array) + '\n\nIn total we have: ' + str(cpt) + "```")
        else:
            await ctx.send("Wrong channel. Go to leaderboards")


def setup(client):
    client.add_cog(MemeCommands(client))