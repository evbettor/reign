import discord
from discord import Intents
from discord.ext import commands
import os
import requests
import json
import urllib

## https://replit.com/@drewshields/EducatedTechnoSpellchecker
#client = discord.Client(intents=discord.Intents.all())

#intents = discord.Intents.all()
#intents.message_content = True
bot = commands.Bot(command_prefix="$",
                   intents=Intents.all(),
                   help_command=None)
embed = discord.Embed()


def get_dat(num_1, num_3):
    query = {'a': num_1, 'b': num_3}
    response = requests.get(
        'http://ec2-18-222-189-197.us-east-2.compute.amazonaws.com:8000/sum',
        params=query)
    return response.json()


@bot.event
async def on_read():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content

    if message.content.startswith('gm'):
        await message.channel.send(
            'GM'
        )
        #dat = get_dat(msg)
        #await message.channel.send(dat)
    await bot.process_commands(message)


@bot.command()
async def plot(ctx, player):
    await ctx.send(
        'http://ec2-18-222-189-197.us-east-2.compute.amazonaws.com:8000/plot_player?player_name='
        + urllib.parse.quote(player))


@bot.command()
async def floor(ctx, player):
    response = requests.get(
        'http://ec2-18-222-189-197.us-east-2.compute.amazonaws.com:8000/floor?player_name='
        + urllib.parse.quote(player)).json()
    str_response = json.dumps(response, indent=2)
    await ctx.send('```\n' + str_response + '\n```')


@bot.command()
async def xray(ctx, user):
    link = 'http://ec2-18-222-189-197.us-east-2.compute.amazonaws.com:8000/xray?user=' + urllib.parse.quote(
        user)
    embed.description = user + " [download](" + link + ")."
    await ctx.send(embed=embed)
    #  await ctx.send('http://ec2-18-222-189-197.us-east-2.compute.amazonaws.com:8000/xray?user='
    #     + urllib.parse.quote(user))

  
@bot.command()
async def value(ctx, user):
    statement = requests.get('http://ec2-18-222-189-197.us-east-2.compute.amazonaws.com:8000/portfolio?user='
        + urllib.parse.quote(user))
    statement = statement.json()[0]
    await ctx.send(
        statement)

@bot.command()
async def depth(ctx, player, rarity = "Elite", days = 7):
    player = urllib.parse.quote(player)
    await ctx.send(
        f"http://ec2-18-222-189-197.us-east-2.compute.amazonaws.com:8000/depth?play={player}&rarity={rarity}&days={days}")


@bot.command()
async def xray_tier(ctx, user, rarity = 'elite', gt = 'main'):
    statement = requests.get(f"http://ec2-18-222-189-197.us-east-2.compute.amazonaws.com:8000/xray_tier?user={user}&rarity={rarity}&gt={gt}").json()
    str_response = json.dumps(statement, indent=2)
    await ctx.send('```\n' + str_response + '\n```')

  
@bot.command()
async def floor_def(ctx, team, rarity_tier):
    response = requests.get(f"http://ec2-18-222-189-197.us-east-2.compute.amazonaws.com:8000/floor_def?tm={team}&rarity_tier={rarity_tier}").json()
    str_response = json.dumps(response, indent=2)
    await ctx.send('```\n' + str_response + '\n```')


my_secret = os.environ['TOKEN']
bot.run(my_secret)
#bot.run(os.environ.get('TOKEN'))
