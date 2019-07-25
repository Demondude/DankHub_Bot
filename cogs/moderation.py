import asyncio

import discord
import os
from discord.ext import commands
from functions.file_functions import get_config, get_image
from functions.json_functions import check_moderation


class moderation (commands.Cog):
    def __init__(self, client):
        self.client = client
        self._, self._, self.memeDir, self._, self.trashDir = get_config()

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def piccheck(self, ctx):
        if check_moderation(ctx.message.author):
            def check(reaction, user):
                if str(reaction.emoji) == "✅":
                    return user == ctx.message.author and str(reaction.emoji) == "✅"
                else:
                    return user == ctx.message.author and str(reaction.emoji) == "❎"

            if os.stat("trash_database").st_size <= 2:
                await ctx.send("Seems to me there are no reports. Great work.")
                return

            meme_selected, uploader = get_image("trash_database", self.memeDir)

            embed = discord.Embed(
                title='From ' + uploader + "'s Collection.",
                colour=discord.Color.blue()
                # TODO get a web server to use embeds
            )
            embed.set_footer(text='Should we delete this ?')
            await ctx.send(file=discord.File(meme_selected))
            await ctx.send("Debug: " + meme_selected)
            lastmsg = await ctx.send(embed=embed)
            await lastmsg.add_reaction(emoji="✅")
            await lastmsg.add_reaction(emoji="❎")

            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Meme is not removed.")
            else:
                if str(reaction.emoji) == "✅":
                    start = len(self.memeDir) + len(uploader) + 2
                    os.rename(meme_selected, self.trashDir + os.sep + meme_selected[start:])
                    await ctx.send("Ok meme removed.")

                else:
                    await ctx.send("meme is not removed.")
        else:
            await ctx.send("You don't have permission for that.")

    '''
    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def add_moderation_perm(self, ctx, user: discord.User, arg):
        if check_moderation(ctx.message.author):
            change_moderation(user, arg)
        else:
            await ctx.send("You don't have permission for that.")
    '''

def setup(client):
    client.add_cog(moderation(client))
