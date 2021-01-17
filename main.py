import os
import random
import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv
from lib import db
from link_preview import link_preview

# START

print("BOT STARTED !!!")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DB_PATH = os.getenv("DB_PATH") + "/" + os.getenv("DB_NAME")
CHANNEL_YT = os.getenv("CHANNEL_YT")
CHANNEL_SP = os.getenv("CHANNEL_SP")

print(DB_PATH)

DataUser = db.user(DB_PATH)
DataPost = db.vote(DB_PATH)

bot = commands.Bot(command_prefix="/")

client = discord.Client()
bot.remove_command("help")
# COMMAND
# help
@bot.command(name="help")
async def help(ctx):
    urlDict = link_preview.generate_dict("https://github.com/DarkOnion0/ADZTBot")
    embed = discord.Embed(
        title=urlDict["title"],
        description="Check the command section on the README\n\n"
        + urlDict["description"],
        url="https://github.com/DarkOnion0/ADZTBot#command-list",
        colour=discord.Color.gold(),
    )

    embed.set_author(
        name="HELP",
        icon_url="https://raw.githubusercontent.com/DarkOnion0/ADZTBot/master/logo.png",
        url="https://github.com/DarkOnion0/ADZTBot",
    )
    embed.set_thumbnail(url=urlDict["image"])

    await ctx.send(embed=embed)


# linux


@bot.command(name="linux", help="Linux Propagande", pass_context=True)
async def linux(ctx, *arg):
    arg = list(arg)
    print(len(arg), type(arg), arg)

    # info command, give a list of linux distro
    if arg[0] == "info":
        if len(arg) == 1:
            msg = "**Linux > ALL | YOU MUST CHECK ONE OF THESE LINUX DISTRO :** \n***Arch based distro:*** \n- archlinux \n- manjaro \n- endeavourOS \n\n***RPM distro*** \n- fedora \n- centos stream \n\n***Debian / Ubuntu based distro*** \n- debian \n- linux mint \n- PopOS \n- ubuntu flavour \n\nhttps://tenor.com/view/mst3k-join-us-come-gif-13947932"
            await ctx.send(msg)
        if len(arg) == 2:
            if arg[1] == "archlinux":
                msg = "**ArchLinux**\n***- WebSite |*** https://archlinux.org/ \n***- Wikipedia |*** https://en.wikipedia.org/wiki/Arch_Linux \n***- Level |*** Hard (it is not a distro for people who don't know or want to understand linux)\n***- Comment |*** I think it's one or the best linux distribution in the world :earth_africa:"
                await ctx.send(msg)


# dice
@bot.command(name="dice", help="Simulates rolling dice between 0 and 10")
async def roll(ctx):
    nb = random.randint(0, 10)
    response = ":game_die: | {}".format(nb)

    await ctx.send(response)


# pile ou face
@bot.command(name="pouf", help="simulate a coins launch (pile ou face game)")
async def pouf(ctx):
    nb = random.randint(1, 2)

    if nb == 1:
        await ctx.send(":full_moon_with_face: | pile")
    else:
        await ctx.send(":new_moon_with_face: | face")


# user info


@bot.command(
    name="profile",
    help="Main command for setup a Server Profile (en dev)",
    pass_context=True,
)
async def profile(ctx, *arg):
    # arg = str(arg)
    # arg = arg.split(" ")

    # print(arg) # debug
    if arg[0] == "init":
        # DataUser.add(ctx.message)
        # print(ctx.message.author, "Hello") # debug
        author = str(ctx.message.author)
        author = author.split("#")
        DataUser.add(author[0])
        await ctx.send(
            "Welcome {},\nYour profile has been setup successfully :+1:".format(
                author[0]
            )
        )
    else:
        msg = "**ERROR**\n veuillez mettre un des arguments suivant :\n`init | init your profile in the database`"
        await ctx.send(msg)


# post command


@bot.command(name="post", pass_context=True, add_reactions=True, embed_links=True)
async def post(ctx, *arg):
    arg = list(arg)
    author = str(ctx.message.author)
    authorId = int(ctx.message.author.id)
    authorTmp = discord.utils.get(
        ctx.guild.members, name=str(arg[0]), discriminator=str(arg[1])
    )
    print(authorId, authorTmp)

    author = author.split("#")

    if arg[0] == "m":  # music option
        embed = discord.Embed(colour=discord.Color.green())
        result = DataPost.post(author[0], "m", arg[1])
        print(result, type(result))
        muId, answer = result

        print(answer)
        if answer == 0.1:  # ERROR -> profile doesn't exist
            await ctx.send(
                "**:warning: ERROR 1 :** please create a profile by typing `/profile init`"
            )
        if answer == 0.2:  # ERROR -> already post
            await ctx.send(
                "**:warning: ERROR 2 :** please don't post a link that was already post"
            )
        if answer == 1:  # SUCCESS
            print("Hello")
            channelM = bot.get_channel(int(CHANNEL_SP))

            # target url
            url = arg[1]
            # making requests instance
            reqs = requests.get(url)
            urlDict = link_preview.generate_dict(url)
            # using the BeaitifulSoup module
            soup = BeautifulSoup(reqs.text, "html.parser")
            # displaying the title
            for title in soup.find_all("title"):
                url = title.get_text()

            msg = "[{}]({})".format(url, arg[1])
            # url + "\n" + arg[1]

            embed.set_author(
                name="Posted by {}".format(author[0]), icon_url=ctx.author.avatar_url
            )
            embed.add_field(name="Music #{}".format(muId), value=msg, inline=True)
            embed.set_image(url=urlDict["image"])

            await channelM.send(
                embed=embed
            )  # send message in the channel for music proposal
            await ctx.send(
                "**:star: SUCCESS : **Your post has been registred successfully"  # send message in the current channel
            )
    elif arg[0] == "v":  # video option
        embed = discord.Embed(colour=discord.Color.red())
        result = DataPost.post(author[0], "v", arg[1])
        print(result, type(result))
        muId, answer = result

        print(answer)
        if answer == 0.1:  # ERROR -> profile doesn't exist
            await ctx.send(
                "**:warning: ERROR 1 :** please create a profile by typing `/profile init`"
            )
        if answer == 0.2:  # ERROR -> already post
            await ctx.send(
                "**:warning: ERROR 2 :** please don't post a link that was already post"
            )
        if answer == 1:  # SUCCESS
            print("Hello")
            channelM = bot.get_channel(int(CHANNEL_YT))

            # target url
            url = arg[1]
            # making requests instance
            reqs = requests.get(url)
            urlDict = link_preview.generate_dict(url)
            # using the BeaitifulSoup module
            soup = BeautifulSoup(reqs.text, "html.parser")
            # displaying the title
            for title in soup.find_all("title"):
                url = title.get_text()

            msg = "[{}]({})".format(url, arg[1])

            embed.set_author(name="Posted by {}".format(author[0]))
            embed.add_field(name="Video #{}".format(muId), value=msg, inline=True)
            embed.set_image(url=urlDict["image"])

            await channelM.send(
                embed=embed
            )  # send message in the channel for music proposal
            await ctx.send(
                "**:star: SUCCESS : **Your post has been registred successfully {}".format(
                    author[0]
                )  # send message in the current channel
            )
    else:
        msg = "**:warning: ERROR :warning:** please specify *v or m* option"
        await ctx.send(msg)


# vote command


@bot.command(name="vote", pass_context=True)
async def vote(ctx, *arg):

    arg = list(arg)
    author = str(ctx.message.author)
    author = author.split("#")

    if len(arg) != 3:
        msg = "**:warning: ERROR :warning:** please specify *v or m* option, after the music id and finally the vote (+1 or -1)"
        await ctx.send(msg)

    result = DataPost.vote(author[0], arg[0], arg[1], arg[2])

    if result == 0.1:
        await ctx.send(
            "**:warning: ERROR 1 :** please create a profile by typing `/profile init`"
        )
    if result == 0.2:
        await ctx.send(
            "**:warning: ERROR 2 :** the post id `{}` doesn't exist in the `{}` categorie".format(
                arg[1], arg[0]
            )
        )
    if result == 0.3:
        await ctx.send("**:warning: ERROR 3 :** please don't revote on the same post")
    if result == 1:
        await ctx.send(
            "**:star: SUCCESS :** Your vote has been successfully registred {}".format(
                author[0]
            )
        )


bot.run(TOKEN)
