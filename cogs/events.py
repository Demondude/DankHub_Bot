from discord.ext import commands
from functions.json_functions import update_data


class Events (commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("```" + error.args[0] + "```")
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission for that.")
            return
        if isinstance(error, commands.CheckFailure):
            await ctx.send("This is NSFW material please got to that channel.")
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You are missing some arguments. Check .help for more information.")
            return
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error.args[0])
            return
        """if isinstance(error, commands.MissingRole):
            await ctx.send("You don't have role for that.")
            return
            
            I need a new version of discord.py
        """
        await ctx.send("UwU We made a fucky wucky!! A wittle fucko boingo! The code monkets at out headquarters are working VEWY HAWD to fix this! Also report this to Demondude#2261 ""\n```" + str(error) + "```")
        raise error

    @commands.Cog.listener()
    async def on_member_join(self, member):
        update_data(member)


def setup(client):
    client.add_cog(Events(client))
        

