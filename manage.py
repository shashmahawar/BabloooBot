from time import time
import utils
import discord
from discord.ext import commands
import asyncio
import csv, json, datetime, os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.bans = True

client = commands.Bot(command_prefix='!', intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name="Facchas"), case_insensitive = True)
client.remove_command('help')

VCS = []
discord_ids = {}
claimedkerberos = []
with open('discord_ids.json', 'r') as f:
    discord_ids = json.load(f)
branches = ["AM1","BB1","CE1","CH1","CH7","CS1","CS5","EE1","EE3","ES1","ME1","ME2","MS1","MT1","MT6","PH1","TT1"]

@client.event
async def on_ready():
    print('Bot is Online!')

# @client.event
# async def on_command_error(ctx, error):
#     return

@client.event
async def on_member_join(member):
    guild = client.get_guild(903690299442860052)
    stats = client.get_channel(934012213189034054)
    await stats.edit(name=f"Members: {guild.member_count}")
    channel = client.get_channel(932320002030325790)
    await channel.send(f"Hey {member.mention} Welcome to **Facche Mann Ke Sachhe**. Send your **KERBEROS ID** `(For eg. cs1210001)` here within next 10 minutes else you would be kicked.")
    await asyncio.sleep(600)
    fresher = discord.utils.get(guild.roles, id=903694577993670727)
    if fresher not in member.roles:
        await member.kick(reason = "Didn't Verify")

@client.event
async def on_member_remove(member):
    guild = client.get_guild(903690299442860052)
    stats = client.get_channel(934012213189034054)
    await stats.edit(name=f"Members: {guild.member_count}")
    try:
        discord_ids.pop(member.id)
        with open('discord_ids.json', 'w') as f:
            json.dump(discord_ids,f)
    except:
        pass

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id == 932320002030325790:
        kerberos = message.content
        kerberos = kerberos.lower()
        verify_logs = client.get_channel(934514103060426812)
        if kerberos in utils.kerberos_data:
            fresher = discord.utils.get(message.guild.roles, id=903694577993670727)
            branch = discord.utils.get(message.guild.roles, name=kerberos[:3].upper())
            for K,V in discord_ids.items():
                if V["Kerberos"] == kerberos and K != str(message.author.id):
                    user = await client.fetch_user(int(K))
                    goldenmember = await client.fetch_user(886907701672673291)
                    embed = discord.Embed(description=f"Kerberos is already registered with {user.mention}. Moderators take immediate action." ,color=discord.Color.yellow(), timestamp=datetime.datetime.now())
                    embed.set_author(name=f"Kerberos Clash", icon_url="https://icones.pro/wp-content/uploads/2021/05/symbole-d-avertissement-jaune.png")
                    embed.add_field(name="Name", value=utils.kerberos_data[kerberos])
                    embed.add_field(name="Kerberos", value=kerberos)
                    embed.add_field(name="User", value=message.author.mention)
                    embed.set_footer(text=message.author.id)
                    await verify_logs.send(embed=embed)
                    await message.reply(f"This Kerberos ID is already registed with {user.mention}. If you believe that this is your Kerberos, contact {goldenmember.mention} immediately.")
                    return
            await message.author.add_roles(fresher)
            await message.author.add_roles(branch)
            try:
                await message.author.edit(nick=utils.kerberos_data[kerberos])
            except:
                pass
            embed = discord.Embed(color=discord.Color.green(), timestamp=datetime.datetime.now())
            embed.set_author(name=f"Member Verified", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Eo_circle_green_white_checkmark.svg/2048px-Eo_circle_green_white_checkmark.svg.png")
            embed.add_field(name="Name", value=utils.kerberos_data[kerberos])
            embed.add_field(name="Kerberos", value=kerberos)
            embed.add_field(name="User", value=message.author.mention)
            embed.set_footer(text=message.author.id)
            await verify_logs.send(embed=embed)
            discord_ids[message.author.id] = {"Name":utils.kerberos_data[kerberos], "Kerberos":kerberos}
            with open('discord_ids.json', 'w') as f:
                json.dump(discord_ids,f)
        else:
            embed = discord.Embed(description=f"<:false:934519099382431765>  **|  *Kerberos not found in Database. Try Again.***", color=discord.Color.red())
            await message.reply(embed=embed)
            embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.now())
            embed.set_author(name=f"Failed Verification", icon_url="https://cdn3.iconfinder.com/data/icons/simple-web-navigation/165/cross-512.png")
            embed.add_field(name="Kerberos Entered", value=kerberos)
            embed.add_field(name="User", value=message.author.mention)
            embed.set_footer(text=message.author.id)
            await verify_logs.send(embed=embed)
    await client.process_commands(message)
        

@client.event
async def on_voice_state_update(user, before, after):
    role = discord.utils.get(user.guild.roles, id=932231323488231456)
    if after.channel is not None:
        await user.add_roles(role)
        if after.channel.id == 932237872495484938:
            newVC = await user.guild.create_voice_channel(name=f"[Study] {user.name}", category=after.channel.category)
            await user.move_to(newVC)
            await asyncio.sleep(7)
            VCS.append(newVC)
        elif after.channel.id == 932283208073109574:
            newVC = await user.guild.create_voice_channel(name=f"[Gaming] {user.name}", category=after.channel.category)
            await user.move_to(newVC)
            await asyncio.sleep(7)
            VCS.append(newVC)
        elif after.channel.id == 932283427514896394:
            newVC = await user.guild.create_voice_channel(name=f"[Music] {user.name}", category=after.channel.category)
            await user.move_to(newVC)
            await asyncio.sleep(7)
            VCS.append(newVC)
    else:
        await user.remove_roles(role)
    for VC in VCS:
        if len(VC.members) == 0:
            VCS.remove(VC)
            await VC.delete()

@client.command()
@commands.has_any_role(915286517071618141,903698939478421554)
async def update(ctx, user: discord.Member, kerberos):
    kerberos = kerberos.lower()
    if kerberos in utils.kerberos_data:
        for i in user.roles:
            if i.name in branches:
                await user.remove_roles(i)
        fresher = discord.utils.get(ctx.message.guild.roles, id=903694577993670727)
        branch = discord.utils.get(ctx.message.guild.roles, name=kerberos[:3].upper())
        verify_logs = client.get_channel(934514103060426812)
        prev_user = None
        for K,V in discord_ids.items():
            if V["Kerberos"] == kerberos:
                prev_user = ctx.guild.get_member(int(K))
                await prev_user.remove_roles(fresher)
                await prev_user.remove_roles(branch)
                await ctx.send(f"Kerberos was previously registered with {prev_user.mention}")
            if K == str(user.id):
                await ctx.send(f'User\'s previous Kerberos was `{V["Kerberos"]}`')

        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.now())
        embed.set_author(name=f"Kerberos Updated", icon_url="https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/refresh-circle-blue-512.png")
        if prev_user is not None:
            embed.add_field(name="Previous User", value=prev_user.mention)
            discord_ids.pop(prev_user.id)
        embed.add_field(name="New User", value=user.mention)
        embed.add_field(name="Moderator", value=ctx.message.author.mention)
        embed.add_field(name="Name", value=utils.kerberos_data[kerberos])
        embed.add_field(name="Kerberos", value=kerberos)
        embed.set_footer(text=ctx.message.author.id)
        await verify_logs.send(embed=embed)
        await user.add_roles(fresher)
        await user.add_roles(branch)
        try:
            await user.edit(nick=utils.kerberos_data[kerberos])
            await prev_user.edit(nick=None)
        except:
            pass
        discord_ids[user.id] = {"Name":utils.kerberos_data[kerberos], "Kerberos":kerberos}
        with open('discord_ids.json', 'w') as f:
            json.dump(discord_ids,f)
        await ctx.channel.send(f"{user.name}#{user.discriminator} Updated")

utils.reload()
load_dotenv()
client.run(os.getenv('BOT_TOKEN'))
