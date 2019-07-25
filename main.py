import datetime
import os
from discord.ext import commands

from functions.file_functions import get_config

TOKEN, trapDir, memeDir, homeworkDir, trashDir = get_config()


print("NOTE: If the config has incorrect info please change it in config.json")
print("Token: " + TOKEN)
print("Trap folder's full directory: " + trapDir)
print("Meme folder's full directory: " + memeDir)
print("Homework(NSFW) folder's full directory: " + homeworkDir)
print("Trash directory for deleted files: " + trashDir)

client = commands.Bot(command_prefix='.')
client.remove_command('help')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    bot_arrival_time = datetime.datetime.now()
    print('Bot is Online\n' + str(bot_arrival_time))
    await client.wait_until_ready()


@client.command()
async def unload_cog(ctx, extension):
    if ctx.message.author.id == 135407256966660096:
        try:
            client.unload_extension("cogs." + extension)
            await ctx.send("Unloaded {}".format(extension))
        except Exception as error:
            await ctx.send("{} cannot be loaded. [{}]".format(extension, error))
    else:
        return


@client.command()
async def load_cog(ctx, extension):
    if ctx.message.author.id == 135407256966660096:
        try:
            client.load_extension("cogs." + extension)
            await ctx.send("Loaded {}".format(extension))
        except Exception as error:
            await ctx.send("{} cannot be loaded. [{}]".format(extension, error))
    else:
        return

extensions = os.listdir("cogs")

i = 0
for extension in extensions:
    extensions[i] = os.path.splitext(extension)[0]
    i = i+1


if __name__ == '__main__':
    for extension in extensions:
        try:
            if extension == "__init__" or extension == "__pycache__":
                print("Not loading " + extension)
            else:
                client.load_extension("cogs." + extension)
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(extension, error))

client.run(TOKEN)