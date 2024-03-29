# Install BenBotAsync

import os
os.system('pip install BenBotAsync')

# -*- coding: utf-8 -*-

try:
    import asyncio
    import sys
    import os
    import time
    from datetime import datetime
    import json
    from functools import partial
    import random as rand

    from colorama import Fore, Back, Style, init

    import fortnitepy
    from fortnitepy.ext import commands
    import BenBotAsync
    import aiohttp
    import colorama
    import requests

except ModuleNotFoundError as e:
    print(e)
    print(Fore.RED + f'[FEHLER] ' + Fore.RESET + 'you forgot to install packages ! "INSTALL PACKAGES.bat')
    exit()

os.system('cls||clear')

intro = Fore.LIGHTBLUE_EX + """
 
   _____                      ______ _   _   _           _     _           
  / ____|                    |  ____| \ | | | |         | |   | |          
 | (___  _ __   __ _  ___ ___| |__  |  \| | | |     ___ | |__ | |__  _   _ 
  \___ \| '_ \ / _` |/ __/ _ \  __| | . ` | | |    / _ \| '_ \| '_ \| | | |
  ____) | |_) | (_| | (_|  __/ |    | |\  | | |___| (_) | |_) | |_) | |_| |
 |_____/| .__/ \__,_|\___\___|_|    |_| \_| |______\___/|_.__/|_.__/ \__, |
        | |                                                           __/ |
        |_|                                                          |___/ 
 https://discord.gg/peYSuY28S6 \n \n Get your auth code\n \n https://www.epicgames.com/id/login?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Fapi%2Fredirect%3FclientId%3D3446cd72694c4a4485d81b77adbb2141%26responseType%3Dcode
"""

print(intro)

response = requests.get("https://benbot.app/api/v1/status")
patch = response.json()["currentFortniteVersion"]

print(Fore.BLUE + f'[LOAD] ' + Fore.RESET + 'SpaceFN Bot is loading')

def lenPartyMembers():
    members = client.party.members
    return len(members)

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

def lenFriends():
    friends = client.friends
    return len(friends)

def getNewSkins():
    r = requests.get('https://benbot.app/api/v1/files/added')

    response = r.json()

    cids = []

    for cid in [item for item in response if item.split('/')[-1].upper().startswith('CID_')]:
        cids.append(cid.split('/')[-1].split('.')[0])
    
    return cids

def getNewEmotes():
    r = requests.get('https://benbot.app/api/v1/files/added')

    response = r.json()

    eids = []

    for cid in [item for item in response if item.split('/')[-1].upper().startswith('EID_')]:
        eids.append(cid.split('/')[-1].split('.')[0])
    
    return eids

def get_device_auth_details():
    if os.path.isfile("auths.json"):
        with open("auths.json", 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open("auths.json", 'w') as fp:
        json.dump(existing, fp)

with open('config.json') as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(Fore.RED + ' [FEHLER] ' + Fore.RESET + "An error occurred in one of the bot files! (config.json). If you are having trouble resolving the problem, please join the Discord support server for help - https://discord.gg/peYSuY28S6")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        exit(1)

with open('info.json') as f:
    try:
        info = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(Fore.RED + ' [FEHLER] ' + Fore.RESET + "An error occurred in one of the bot files! (info.json) If you are having trouble resolving the problem, please join the Discord support server for help - https://discord.gg/peYSuY28S6")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        exit(1)

def is_admin():
    async def predicate(ctx):
        return ctx.author.id in info['FullAccess']
    return commands.check(predicate)

device_auth_details = get_device_auth_details().get(data['email'], {})

prefix = '!'

client = commands.Bot(
    command_prefix=prefix,
    case_insensitive=True,
    auth=fortnitepy.AdvancedAuth(
        email=data['email'],
        password=data['password'],
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        **device_auth_details
    ),
    status=data['status'],
    platform=fortnitepy.Platform(data['platform']),
)
client.party_build_id = "1:3:"

@client.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)




@client.event
async def event_ready():
    os.system('cls||clear')
    print(intro)
    print(Fore.RED + ' [Success] ' + Fore.RESET + 'SpaceFN Bot Is successfully online enjoy! ' + Fore.LIGHTBLUE_EX + f'{client.user.display_name}')

    member = client.party.me

    await member.edit_and_keep(
        partial(
            fortnitepy.ClientPartyMember.set_outfit,
            asset=data['cid']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_backpack,
            asset=data['bid']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_pickaxe,
            asset=data['pid']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon=data['banner'],
            color=data['banner_color'],
            season_level=data['level']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level=data['bp_tier']
        )
    )

    client.set_avatar(fortnitepy.Avatar(asset=data['cid'], background_colors=['#ffffff', '#ee1064', '#ff0000']))
    

@client.event
async def event_party_invite(invite):
    if data['joinoninvite'].lower() == 'true':
        try:
            await invite.accept()
            print(Fore.BLUE + ' [Console] ' + Fore.RESET + f'Party invitation accepted by {invite.sender.display_name}')
        except Exception:
            pass
    elif data['joinoninvite'].lower() == 'false':
        if invite.sender.id in info['FullAccess']:
            await invite.accept()
            print(Fore.BLUE + ' [Console] ' + Fore.RESET + 'Party invitation accepted by' + Fore.LIGHTGREEN_EX + f'{invite.sender.display_name}')
        else:
            print(Fore.RED + ' [Console] ' + Fore.RESET + f'party invitation from never accepted from {invite.sender.display_name}')


@client.command()
async def pinkghoul(ctx):
    skin_variants = client.party.me.create_variants(
        material=3
    )

    await client.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=skin_variants
    )

    await ctx.send('Skin set to Pink Ghoul Trooper!')

@client.event
async def event_friend_request(request):
    if data['friendaccept'].lower() == 'true':
        try:
            await request.accept()
            print(f' [Console] Accepted friend request from {request.display_name}' + Fore.LIGHTGREEN_EX + f' ({lenFriends()})')
        except Exception:
            pass
    elif data['friendaccept'].lower() == 'false':
        if request.id in info['FullAccess']:
            try:
                await request.accept()
                print(Fore.BLUE + ' [Console] ' + Fore.RESET + 'Accepted friend request from' + Fore.LIGHTGREEN_EX + f'{request.display_name}' + Fore.LIGHTBLUE_EX + f' ({lenFriends()})')
            except Exception:
                pass
        else:
            print(f' [Console] Never accepted friend request from {request.display_name}')


@client.event
async def event_party_member_join(member):
    if client.user.display_name != member.display_name:
        try:
            if client.user.id in info['FullAccess']:
                print(Fore.LIGHTBLUE_EX + f' [Lobby] {member.display_name}' + Fore.RESET + 'has joined the lobby.')
            else:
                print(f' [Lobby] {member.display_name} ist der Lobby beigetreten.' + Fore.LIGHTGREEN_EX + f' ({lenPartyMembers()})')
        except fortnitepy.HTTPException:
            pass
        await client.party.send(f' Welcome {member.display_name}! Thank you for using SpaceFN')


@client.event
async def event_party_member_leave(member):
    if client.user.display_name != member.display_name:
        try:
            if client.user.id in info['FullAccess']:
                print(Fore.LIGHTBLUE_EX + f' [Lobby] {member.display_name}' + Fore.RESET + 'left the lobby.')
            else:
                print(f' [Lobby] {member.display_name} left the lobby.' + Fore.LIGHTGREEN_EX + f' ({lenPartyMembers()})')
        except fortnitepy.HTTPException:
            pass


@client.event
async def event_party_message(message):
    if message.author.id in info['FullAccess']:
        name = Fore.LIGHTGREEN_EX + f'{message.author.display_name}'
    else:
        name = Fore.RESET + f'{message.author.display_name}'
    print(Fore.LIGHTGREEN_EX + ' [Chat] ' + f'{name}' + Fore.RESET + f': {message.content}')


@client.event
async def event_friend_message(message):
    if message.author.id in info['FullAccess']:
        name = Fore.LIGHTMAGENTA_EX + f'{message.author.display_name}'
    else:
        name = Fore.RESET + f'{message.author.display_name}'
    print(Fore.LIGHTMAGENTA_EX + ' [Flüstern] ' + f'{name}' + Fore.RESET + f': {message.content}')

    if message.content.upper().startswith('CID_'):
        await client.party.me.set_outfit(asset=message.content.upper())
        await message.reply(f'Skin set to: {message.content}')
    elif message.content.upper().startswith('BID_'):
        await client.party.me.set_backpack(asset=message.content.upper())
        await message.reply(f'Backpack set to: {message.content}')
    elif message.content.upper().startswith('EID_'):
        await client.party.me.set_emote(asset=message.content.upper())
        await message.reply(f'Emote set to: {message.content}')
    elif message.content.upper().startswith('PID_'):
        await client.party.me.set_pickaxe(asset=message.content.upper())
        await message.reply(f'Pickaxe set to: {message.content}')
    elif message.content.startswith('Playlist_'):
        try:
            await client.party.set_playlist(playlist=message.content)
            await message.reply(f'Playlist set to: {message.content}')
        except fortnitepy.Forbidden:
            await message.reply(f"I can not set gamemode because I am not party leader.")
    elif message.content.lower().startswith('prefix'):
        await message.reply(f'Current prefix: {prefix}')


@client.event
async def event_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'That is not a command. Try {prefix}help')
    elif isinstance(error, IndexError):
        pass
    elif isinstance(error, fortnitepy.HTTPException):
        pass
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have access to that command.")
    elif isinstance(error, TimeoutError):
        await ctx.send("You took too long to respond!")
    else:
        print(error)                  


@client.command()

async def skin(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No skin was given, try: {prefix}skin (skin name)')
    elif content.upper().startswith('CID_'):
        await client.party.me.set_outfit(asset=content.upper())
        await ctx.send(f'Skin set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await client.party.me.set_outfit(asset=cosmetic.id)
            await ctx.send(f'Skin set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {content}')


@client.command()

async def backpack(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No backpack was given, try: {prefix}backpack (backpack name)')
    elif content.lower() == 'none':
        await client.party.me.clear_backpack()
        await ctx.send('Backpack set to: None')
    elif content.upper().startswith('BID_'):
        await client.party.me.set_backpack(asset=content.upper())
        await ctx.send(f'Backpack set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await client.party.me.set_backpack(asset=cosmetic.id)
            await ctx.send(f'Backpack set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a backpack named: {content}')


@client.command()
async def emote(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No emote was given, try: {prefix}emote (emote name)')
    elif content.lower() == 'floss':
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_Floss')
        await ctx.send(f'Emote set to: Floss')
    elif content.lower() == 'scenario':
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_KPopDance03')
        await ctx.send(f'Emote set to: Scenario')
    elif content.lower() == 'none':
        await client.party.me.clear_emote()
        await ctx.send(f'Emote set to: None')
    elif content.upper().startswith('EID_'):
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset=content.upper())
        await ctx.send(f'Emote set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset=cosmetic.id)
            await ctx.send(f'Emote set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find an emote named: {content}')


@client.command()
async def pickaxe(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No pickaxe was given, try: {prefix}pickaxe (pickaxe name)')
    elif content.upper().startswith('Pickaxe_'):
        await client.party.me.set_pickaxe(asset=content.upper())
        await ctx.send(f'Pickaxe set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await client.party.me.set_pickaxe(asset=cosmetic.id)
            await ctx.send(f'Pickaxe set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pickaxe named: {content}')


@client.command()
async def pet(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No pet was given, try: {prefix}pet (pet name)')
    elif content.lower() == 'none':
        await client.party.me.clear_pet()
        await ctx.send('Pet set to: None')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPet"
            )
            await client.party.me.set_pet(asset=cosmetic.id)
            await ctx.send(f'Pet set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pet named: {content}')


@client.command()
async def emoji(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No emoji was given, try: {prefix}emoji (emoji name)')
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaEmoji"
        )
        await client.party.me.clear_emoji()
        await client.party.me.set_emoji(asset=cosmetic.id)
        await ctx.send(f'Emoji set to: {cosmetic.name}')
    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f'Could not find an emoji named: {content}')

    

@client.command()
async def current(ctx, setting = None):
    if setting is None:
        await ctx.send(f"Missing argument. Try: {prefix}current (skin, backpack, emote, pickaxe, banner)")
    elif setting.lower() == 'banner':
        await ctx.send(f'Banner ID: {client.party.me.banner[0]}  -  Banner Color ID: {client.party.me.banner[1]}')
    else:
        try:
            if setting.lower() == 'skin':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.outfit
                    )

            elif setting.lower() == 'backpack':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.backpack
                    )

            elif setting.lower() == 'emote':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.emote
                    )

            elif setting.lower() == 'pickaxe':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.pickaxe
                    )

            await ctx.send(f"My current {setting} is: {cosmetic.name}")
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f"I couldn't find a {setting} name for that.")



@client.command()
async def name(ctx, *, content=None):
    if content is None:
        await ctx.send(f'No ID was given, try: {prefix}name (cosmetic ID)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic_from_id(
                cosmetic_id=content
            )
            await ctx.send(f'The name for that ID is: {cosmetic.name}')
            print(f' [+] The name for {cosmetic.id} is: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a cosmetic name for ID: {content}')



@client.command()
async def cid(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No skin was given, try: {prefix}cid (skin name)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaCharacter"
            )
            await ctx.send(f'The CID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The CID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {content}')
        


@client.command()
async def bid(ctx, *, content):
    if content is None:
        await ctx.send(f'No backpack was given, try: {prefix}bid (backpack name)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await ctx.send(f'The BID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The BID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a backpack named: {content}')



@client.command()
async def eid(ctx, *, content):
    if content is None:
        await ctx.send(f'No emote was given, try: {prefix}eid (emote name)')
    elif content.lower() == 'floss':
        await ctx.send(f'The EID for Floss is: EID_Floss')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await ctx.send(f'The EID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The EID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find an emote named: {content}')



@client.command()
async def pid(ctx, *, content):
    if content is None:
        await ctx.send(f'No pickaxe was given, try: {prefix}pid (pickaxe name)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await ctx.send(f'The PID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The PID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pickaxe named: {content}')



@client.command()
async def random(ctx, content = None):

    skins = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaCharacter"
    )

    skin = rand.choice(skins)

    backpacks = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaBackpack"
    )

    backpack = rand.choice(backpacks)

    emotes = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaDance"
    )

    emote = rand.choice(emotes)

    pickaxes = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaPickaxe"
    )

    pickaxe = rand.choice(pickaxes)

    
    if content is None:
        me = client.party.me
        await me.set_outfit(asset=skin.id)
        await me.set_backpack(asset=backpack.id)
        await me.set_pickaxe(asset=pickaxe.id)

        await ctx.send(f'Loadout randomly set to: {skin.name}, {backpack.name}, {pickaxe.name}')
    else:
        if content.lower() == 'skin':
            await client.party.me.set_outfit(asset=skin.id)
            await ctx.send(f'Skin randomly set to: {skin.name}')

        elif content.lower() == 'backpack':
            await client.party.me.set_backpack(asset=backpack.id)
            await ctx.send(f'Backpack randomly set to: {backpack.name}')

        elif content.lower() == 'emote':
            await client.party.me.set_emote(asset=emote.id)
            await ctx.send(f'Emote randomly set to: {emote.name}')

        elif content.lower() == 'pickaxe':
            await client.party.me.set_pickaxe(asset=pickaxe.id)
            await ctx.send(f'Pickaxe randomly set to: {pickaxe.name}')

        else:
            await ctx.send(f"I don't know that, try: {prefix}random (skin, backpack, emote, pickaxe - og, exclusive, unreleased")



@client.command()
async def point(ctx, *, content = None):
    if content is None:
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_IceKing')
        await ctx.send(f'Pointing with: {client.party.me.pickaxe}')
    
    else:
        if content.upper().startswith('Pickaxe_'):
            await client.party.me.set_pickaxe(asset=content.upper())
            await client.party.me.clear_emote()
            asyncio.sleep(0.25)
            await client.party.me.set_emote(asset='EID_IceKing')
            await ctx.send(f'Pointing with: {content}')
        else:
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=content,
                    backendType="AthenaPickaxe"
                )
                await client.party.me.set_pickaxe(asset=cosmetic.id)
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset='EID_IceKing')
                await ctx.send(f'Pointing with: {cosmetic.name}')
            except BenBotAsync.exceptions.NotFound:
                await ctx.send(f'Could not find a pickaxe named: {content}')



@client.command()
async def checkeredrenegade(ctx):
    variants = client.party.me.create_variants(material=2)

    await client.party.me.set_outfit(
        asset='CID_028_Athena_Commando_F',
        variants=variants
    )

    await ctx.send('Skin set to: Checkered Renegade')



@client.command()
async def purpleportal(ctx):
    variants = client.party.me.create_variants(
        item='AthenaBackpack',
        particle_config='Particle',
        particle=1
    )

    await client.party.me.set_backpack(
        asset='BID_105_GhostPortal',
        variants=variants
    )

    await ctx.send('Backpack set to: Purple Ghost Portal')


@client.command()
async def purpleskull(ctx):
    variants = client.party.me.create_variants(
        clothing_color=1
    )

    await client.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants=variants
    )

    await ctx.send('Skin set to Purple Skull Trooper!')


@client.command()
async def goldpeely(ctx):
    variants = client.party.me.create_variants(progressive=4)

    await client.party.me.set_outfit(
        asset='CID_701_Athena_Commando_M_BananaAgent',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('Skin set to: Golden Peely')


@client.command()
async def hatlessrecon(ctx):
    variants = client.party.me.create_variants(parts=2)

    await client.party.me.set_outfit(
        asset='CID_022_Athena_Commando_F',
        variants=variants
    )

    await ctx.send('Skin set to: Hatless Recon Expert')



@client.command()
async def hologram(ctx):
    await client.party.me.set_outfit(
        asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
    )
    
    await ctx.send("Skin set to: Hologram")



@client.command()
async def itemshop(ctx):
    previous_skin = client.party.me.outfit

    store = await client.fetch_item_shop()

    await ctx.send("Equipping all item shop skins + emotes")

    for cosmetic in store.featured_items + store.daily_items:
        for grant in cosmetic.grants:
            if grant['type'] == 'AthenaCharacter':
                await client.party.me.set_outfit(asset=grant['asset'])
                await asyncio.sleep(5)
            elif grant['type'] == 'AthenaDance':
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset=grant['asset'])
                await asyncio.sleep(5)

    await client.party.me.clear_emote()
    
    await ctx.send("Done!")

    await asyncio.sleep(1.5)

    await client.party.me.set_outfit(asset=previous_skin)



@client.command()
async def new(ctx, content = None):
    newSkins = getNewSkins()
    newEmotes = getNewEmotes()

    previous_skin = client.party.me.outfit

    if content is None:
        await ctx.send(f'There are {len(newSkins) + len(newEmotes)} new skins + emotes')

        for cosmetic in newSkins + newEmotes:
            if cosmetic.startswith('CID_'):
                await client.party.me.set_outfit(asset=cosmetic)
                await asyncio.sleep(4)
            elif cosmetic.startswith('EID_'):
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset=cosmetic)
                await asyncio.sleep(4)

    elif 'skin' in content.lower():
        await ctx.send(f'There are {len(newSkins)} new skins')

        for skin in newSkins:
            await client.party.me.set_outfit(asset=skin)
            await asyncio.sleep(4)

    elif 'emote' in content.lower():
        await ctx.send(f'There are {len(newEmotes)} new emotes')

        for emote in newEmotes:
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset=emote)
            await asyncio.sleep(4)

    await client.party.me.clear_emote()
    
    await ctx.send('Done!')

    await asyncio.sleep(1.5)

    await client.party.me.set_outfit(asset=previous_skin)

    if (content is not None) and ('skin' or 'emote' not in content.lower()):
        ctx.send(f"Not a valid option. Try: {prefix}new (skins, emotes)")



@client.command()
async def ready(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.READY)
    await ctx.send('Ready!')



@client.command()
async def unready(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Unready!')



@client.command()
async def sitin(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Sitting in')


@client.command()
async def sitout(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    await ctx.send('Sitting out')



@client.command()
async def tier(ctx, tier = None):
    if tier is None:
        await ctx.send(f'No tier was given. Try: {prefix}tier (tier number)') 
    else:
        await client.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )

        await ctx.send(f'Battle Pass tier set to: {tier}')



@client.command()
async def level(ctx, level = None):
    if level is None:
        await ctx.send(f'No level was given. Try: {prefix}level (number)')
    else:
        await client.party.me.set_banner(season_level=level)
        await ctx.send(f'Level set to: {level}')



@client.command()
async def banner(ctx, args1 = None, args2 = None):
    if (args1 is not None) and (args2 is None):
        if args1.startswith('defaultcolor'):
            await client.party.me.set_banner(
                color = args1
            )
            
            await ctx.send(f'Banner color set to: {args1}')

        elif args1.isnumeric() == True:
            await client.party.me.set_banner(
                color = 'defaultcolor' + args1
            )

            await ctx.send(f'Banner color set to: defaultcolor{args1}')

        else:
            await client.party.me.set_banner(
                icon = args1
            )

            await ctx.send(f'Banner Icon set to: {args1}')

    elif (args1 is not None) and (args2 is not None):
        if args2.startswith('defaultcolor'):
            await client.party.me.set_banner(
                icon = args1,
                color = args2
            )

            await ctx.send(f'Banner icon set to: {args1} -- Banner color set to: {args2}')
        
        elif args2.isnumeric() == True:
            await client.party.me.set_banner(
                icon = args1,
                color = 'defaultcolor' + args2
            )

            await ctx.send(f'Banner icon set to: {args1} -- Banner color set to: defaultcolor{args2}')

        else:
            await ctx.send(f'Not proper format. Try: {prefix}banner (Banner ID) (Banner Color ID)')


copied_player = ""



@client.command()
async def stop(ctx):
    global copied_player
    if copied_player != "":
        copied_player = ""
        await ctx.send(f'Stopped copying all users.')
        return
    else:
        try:
            await client.party.me.clear_emote()
        except RuntimeWarning:
            pass



@client.command()
async def copy(ctx, *, username = None):
    global copied_player

    if username is None:
        member = [m for m in client.party.members if m.id == ctx.author.id][0]

    else:
        user = await client.fetch_user(username)
        member = [m for m in client.party.members if m.id == user.id][0]

    await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_outfit,
                asset=member.outfit,
                variants=member.outfit_variants
            ),
            partial(
                fortnitepy.ClientPartyMember.set_backpack,
                asset=member.backpack,
                variants=member.backpack_variants
            ),
            partial(
                fortnitepy.ClientPartyMember.set_pickaxe,
                asset=member.pickaxe,
                variants=member.pickaxe_variants
            ),
            partial(
                fortnitepy.ClientPartyMember.set_banner,
                icon=member.banner[0],
                color=member.banner[1],
                season_level=member.banner[2]
            ),
            partial(
                fortnitepy.ClientPartyMember.set_battlepass_info,
                has_purchased=member.battlepass_info[0],
                level=member.battlepass_info[1]
            ),
            partial(
                fortnitepy.ClientPartyMember.set_emote,
                asset=member.emote
            )
        )

    await ctx.send(f"Now copying: {member.display_name}")

@client.event()
async def event_party_member_backpack_change(member, before, after):
    if member == copied_player:
        if after is None:
            await client.party.me.clear_backpack()
        else:
            await client.party.me.edit_and_keep(
                partial(
                    fortnitepy.ClientPartyMember.set_backpack,
                    asset=after,
                    variants=member.backpack_variants
                )
            )

@client.event()
async def event_party_member_backpack_variants_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_backpack,
                variants=member.backpack_variants
            )
        )

@client.event()
async def event_party_member_emote_change(member, before, after):
    if member == copied_player:
        if after is None:
            await client.party.me.clear_emote()
        else:
            await client.party.me.edit_and_keep(
                partial(
                    fortnitepy.ClientPartyMember.set_emote,
                    asset=after
                )
            )

@client.event()
async def event_party_member_pickaxe_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_pickaxe,
                asset=after,
                variants=member.pickaxe_variants
            )
        )

@client.event()
async def event_party_member_pickaxe_variants_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_pickaxe,
                variants=member.pickaxe_variants
            )
        )

@client.event()
async def event_party_member_banner_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_banner,
                icon=member.banner[0],
                color=member.banner[1],
                season_level=member.banner[2]
            )
        )

@client.event()
async def event_party_member_battlepass_info_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_battlepass_info,
                has_purchased=member.battlepass_info[0],
                level=member.battlepass_info[1]
            )
        )

async def set_and_update_party_prop(schema_key: str, new_value: str):
    prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}
    await client.party.patch(updated=prop)


@client.command()
@is_admin()
async def hide(ctx, *, user = None):
    if client.party.me.leader:
        if user != "all":
            try:
                if user is None:
                    user = await client.fetch_profile(ctx.message.author.id)
                    member = client.party.members.get(user.id)
                else:
                    user = await client.fetch_profile(user)
                    member = client.party.members.get(user.id)

                raw_squad_assignments = client.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]

                for m in raw_squad_assignments:
                    if m['memberId'] == member.id:
                        raw_squad_assignments.remove(m)

                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': raw_squad_assignments
                    }
                )

                await ctx.send(f"Hid {member.display_name}")
            except AttributeError:
                await ctx.send("I could not find that user.")
            except fortnitepy.HTTPException:
                await ctx.send("I am not party leader.")
        else:
            try:
                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': [
                            {
                                'memberId': client.user.id,
                                'absoluteMemberIdx': 1
                            }
                        ]
                    }
                )

                await ctx.send("Hid everyone in the party.")
            except fortnitepy.HTTPException:
                await ctx.send("I am not party leader.")
    else:
        await ctx.send("I need party leader to do this!")


@client.command()
@is_admin()
async def unhide(ctx: fortnitepy.ext.commands.Context, *, username = None):
    if client.party.me.leader:
        user = await client.fetch_user(ctx.author.display_name)
        member = client.party.get_member(user.id)

        await member.promote()

        await ctx.send("Unhid all players.")

    else:
        await ctx.send("I am not party leader.")



@client.command()
@is_admin()
async def avatar(ctx, *, skin = None):
    if skin is None:
        await ctx.send(f'No skin was given. Try: {prefix}avatar (skin name, cid)')
    elif skin.upper().startswith('CID_'):
        try:
            cosmetic = await BenBotAsync.get_cosmetic_from_id(
                cosmetic_id=skin.upper()
            )
            client.set_avatar(fortnitepy.Avatar(asset=cosmetic.id))
            await ctx.send(f'Avatar set to: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find the ID: {skin}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                name=skin,
                backendType="AthenaCharacter"
            )
            client.set_avatar(fortnitepy.Avatar(asset=cosmetic.id))
            await ctx.send(f'Avatar set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {skin}')



@client.command()
@is_admin()
async def say(ctx, *, message = None):
    if message is not None:
        await client.party.send(message)
        await ctx.send(f'Sent "{message}" to party chat')
    else:
        await ctx.send(f'No message was given. Try: {prefix}say (message)')



@client.command()
@is_admin()
async def whisper(ctx, member = None, *, message = None):
    if (member is not None) and (message is not None):
        try:
            user = await client.fetch_profile(member)
            friend = client.get_friend(user.id)

            if friend.is_online():
                await friend.send(message)
                await ctx.send("Message sent.")
            else:
                await ctx.send("That friend is offline.")
        except AttributeError:
            await ctx.send("I couldn't find that friend.")
        except fortnitepy.HTTPException:
            await ctx.send("Something went wrong sending the message.")
    else:
        await ctx.send(f"Command missing one or more arguments. Try: {prefix}whisper (friend) (message)")



@client.command()
@is_admin()
async def match(ctx, players = None):
    time = datetime.utcnow()
    if players is not None:
        if 'auto' in players.lower():
            if client.party.me.in_match():
                left = client.party.me.match_players_left
            else:
                left = 100
            await client.party.me.set_in_match(players_left=left, started_at=time)

            await asyncio.sleep(rand.randint(20, 30))

            while client.party.me.match_players_left > 5 and client.party.me.in_match():
                await client.party.me.set_in_match(players_left=client.party.me.match_players_left - rand.randint(3, 5), started_at=time),

                await asyncio.sleep(rand.randint(8, 18))

            while (client.party.me.match_players_left <= 5) and (client.party.me.match_players_left > 3):
                await client.party.me.set_in_match(players_left=client.party.me.match_players_left - rand.randint(1, 2), started_at=time)

                await asyncio.sleep(rand.randint(12, 20))

            while (client.party.me.match_players_left <= 3) and (client.party.me.match_players_left > 1):
                await client.party.me.set_in_match(players_left=client.party.me.match_players_left - 1, started_at=time)

                await asyncio.sleep(rand.randint(12, 20))

            await asyncio.sleep(6)
            await client.party.me.clear_in_match()

        elif 'leave' in players.lower():
            await client.party.me.clear_in_match()

        else:
            try:
                await client.party.me.set_in_match(players_left=int(players), started_at=time)
            except ValueError:
                await ctx.send(f"Invalid usage. Try: {prefix}match (0-255)")
                pass

    else:
        await ctx.send(f'Incorrect usage. Try: {prefix}match (auto, #, leave)')



@client.command()
@is_admin()
async def status(ctx, *, status = None):
    await client.set_presence(status) 
    await ctx.send(f'Status set to {status}')
    await ctx.send(f'No status was given. Try: {prefix}status (status message)')



@client.command()
@is_admin()
async def leave(ctx):
    await client.party.me.set_emote(asset='EID_Wave')
    await ctx.send('Bye!')
    await asyncio.sleep(0.3)
    await client.party.me.leave()



@client.command()
@is_admin()
async def kick(ctx: fortnitepy.ext.commands.Context, *, member = None):
    try:
        user = await client.fetch_user(member)
        member = client.party.get_member(user.id)
        if member is None:
            await ctx.send("Couldn't find that user. Are you sure they're in the party?")

        await member.kick()
        await ctx.send(f'Kicked: {member.display_name}')
    except fortnitepy.Forbidden:
        await ctx.send("I can't kick that user because I am not party leader")
    except AttributeError:
        await ctx.send("Couldn't find that user.")



@client.command()
@is_admin()
async def promote(ctx, *, username = None):
    if username is None:
        user = await client.fetch_user(ctx.author.display_name)
        member = client.party.get_member(user.id)
    else:
        user = await client.fetch_user(username)
        member = client.party.get_member(user.id)
    try:
        await member.promote()
        await ctx.send(f"Promoted: {member.display_name}")
    except fortnitepy.Forbidden:
        await ctx.send("Client is not party leader")
    except fortnitepy.PartyError:
        await ctx.send("That person is already party leader")
    except fortnitepy.HTTPException:
        await ctx.send("Something went wrong trying to promote that member")
    except AttributeError:
        await ctx.send("I could not find that user")



@client.command()
@is_admin()
async def privacy(ctx, setting = None):
    if setting is not None:
        try:
            if setting.lower() == 'public':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                await ctx.send(f"Party Privacy set to: Public")
            elif setting.lower() == 'friends':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS)
                await ctx.send(f"Party Privacy set to: Friends Only")
            elif setting.lower() == 'private':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE)
                await ctx.send(f"Party Privacy set to: Private")
            else:
                await ctx.send("That is not a valid privacy setting. Try: Public, Friends, or Private")
        except fortnitepy.Forbidden:
            await ctx.send("I can not set the party privacy because I am not party leader.")
    else:
        await ctx.send(f"No privacy setting was given. Try: {prefix}privacy (Public, Friends, Private)")



@client.command()
@is_admin()
async def join(ctx, *, member = None):
    try:
        if member is None:
            user = await client.fetch_profile(ctx.message.author.id)
            friend = client.get_friend(user.id)
        elif member is not None:
            user = await client.fetch_profile(member)
            friend = client.get_friend(user.id)

        await friend.join_party()
        await ctx.send(f"Joined {friend.display_name}'s party.")
    except fortnitepy.Forbidden:
        await ctx.send("I can not join that party because it is private.")
    except fortnitepy.PartyError:
        await ctx.send("That user is already in the party.")
    except fortnitepy.HTTPException:
        await ctx.send("Something went wrong joining the party")
    except AttributeError:
        await ctx.send("I can not join that party. Are you sure I have them friended?")
        


@client.command()
@is_admin()
async def invite(ctx, *, member = None):
    if member == 'all':
        friends = client.friends
        invited = []

        try:
            for f in friends:
                friend = client.get_friend(f)

                if friend.is_online():
                    invited.append(friend.display_name)
                    await friend.invite()
            
            await ctx.send(f"Invited {len(invited)} friends to the party.")

        except Exception:
            pass

    else:
        try:
            if member is None:
                user = await client.fetch_profile(ctx.message.author.id)
                friend = client.get_friend(user.id)
            if member is not None:
                user = await client.fetch_profile(member)
                friend = client.get_friend(user.id)

            await friend.invite()
            await ctx.send(f"Invited {friend.display_name} to the party.")
        except fortnitepy.PartyError:
            await ctx.send("That user is already in the party.")
        except fortnitepy.HTTPException:
            await ctx.send("Something went wrong inviting that user.")
        except AttributeError:
            await ctx.send("I can not invite that user. Are you sure I have them friended?")
        except Exception:
            pass



@client.command()
@is_admin()
async def add(ctx, *, member = None):
    if member is not None:
        try:
            user = await client.fetch_profile(member)
            friends = client.friends

            if user.id in friends:
                await ctx.send(f"I already have {user.display_name} as a friend")
            else:
                await client.add_friend(user.id)
                await ctx.send(f'Sent a friend request to {user.display_name}')
                print(Fore.GREEN + ' [+] ' + Fore.RESET + 'Sent a friend request to: ' + Fore.LIGHTBLACK_EX + f'{user.display_name}')

        except fortnitepy.HTTPException:
            await ctx.send("There was a problem trying to add this friend.")
        except AttributeError:
            await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f"No user was given. Try: {prefix}add (user)")



@client.command()
@is_admin()
async def block(ctx, *, user = None):
    if user is not None:
        try:
            user = await client.fetch_profile(user)
            friends = client.friends

            if user.id in friends:
                try:
                    await user.block()
                    await ctx.send(f"Blocked {user.display_name}")
                except fortnitepy.HTTPException:
                    await ctx.send("Something went wrong trying to block that user.")

            elif user.id in client.blocked_users:
                await ctx.send(f"I already have {user.display_name} blocked.")
        except AttributeError:
            await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f"No user was given. Try: {prefix}block (friend)")



@client.command()
@is_admin()
async def blocked(ctx):

    blockedusers = []

    for b in client.blocked_users:
        user = client.get_blocked_user(b)
        blockedusers.append(user.display_name)
    
    await ctx.send(f'Client has {len(blockedusers)} users blocked:')
    for x in blockedusers:
        if x is not None:
            await ctx.send(x)



@client.command()
@is_admin()
async def unblock(ctx, *, user = None):
    if user is not None:
        try:
            member = await client.fetch_profile(user)
            blocked = client.blocked_users
            if member.id in blocked:
                try:
                    await client.unblock_user(member.id)
                    await ctx.send(f'Successfully unblocked {member.display_name}')
                except fortnitepy.HTTPException:
                    await ctx.send('Something went wrong trying to unblock that user.')
            else:
                await ctx.send('That user is not blocked')
        except AttributeError:
            await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f'No user was given. Try: {prefix}unblock (blocked user)')
    


@client.command()
@is_admin()
async def friends(ctx):
    cfriends = client.friends
    onlineFriends = []
    offlineFriends = []

    try:
        for f in cfriends:
            friend = client.get_friend(f)
            if friend.is_online():
                onlineFriends.append(friend.display_name)
            else:
                offlineFriends.append(friend.display_name)
        
        await ctx.send(f"Client has: {len(onlineFriends)} friends online and {len(offlineFriends)} friends offline")
        await ctx.send("(Check cmd for full list of friends)")

        print(" [+] Friends List: " + Fore.GREEN + f'{len(onlineFriends)} Online ' + Fore.RESET + "/" + Fore.LIGHTBLACK_EX + f' {len(offlineFriends)} Offline ' + Fore.RESET + "/" + Fore.LIGHTWHITE_EX + f' {len(onlineFriends) + len(offlineFriends)} Total')
        
        for x in onlineFriends:
            if x is not None:
                print(Fore.GREEN + " " + x)
        for x in offlineFriends:
            if x is not None:
                print(Fore.LIGHTBLACK_EX + " " + x)
    except Exception:
        pass



@client.command()
@is_admin()
async def members(ctx: fortnitepy.ext.commands.Context):
    pmembers = client.party.members
    partyMembers = []
    
    for m in pmembers:
        member = client.get_user(m)
        partyMembers.append(member.display_name)
    
    await ctx.send(f"There are {len(partyMembers)} members in {client.user.display_name}'s party:")
    for x in partyMembers:
        if x is not None:
            await ctx.send(x)


@client.command()
async def invisible(ctx: fortnitepy.ext.commands.Context):
    await client.party.me.set_outfit("CID_Invisible")
    await ctx.send("I am now invisible.")



@client.command()
@is_admin()
async def id(ctx, *, user = None):
    if user is not None:
        user = await client.fetch_profile(user)
    
    elif user is None:
        user = await client.fetch_profile(ctx.message.author.id)

    try:
        await ctx.send(f"{user}'s Epic ID is: {user.id}")
        print(Fore.GREEN + ' [+] ' + Fore.RESET + f"{user}'s Epic ID is: " + Fore.LIGHTBLACK_EX + f'{user.id}')
    except AttributeError:
        await ctx.send("I couldn't find an Epic account with that name.")


#More Commands By SpaceFN ;)



@client.command()
@is_admin()
async def user(ctx, *, user = None):
    if user is not None:
        user = await client.fetch_profile(user)

        try:
            await ctx.send(f"The ID: {user.id} belongs to: {user.display_name}")
            print(Fore.GREEN + ' [+] ' + Fore.RESET + f'The ID: {user.id} belongs to: ' + Fore.LIGHTBLACK_EX + f'{user.display_name}')
        except AttributeError:
            await ctx.send(f"I couldn't find a user that matches that ID")
    else:
        await ctx.send(f'No ID was given. Try: {prefix}user (ID)')@client.command()

@client.command()
async def reset(ctx):
    member = client.party.me

    await member.edit_and_keep(
        partial(
            fortnitepy.ClientPartyMember.set_outfit,
            asset=data['cid']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_backpack,
            asset=data['bid']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_pickaxe,
            asset=data['pid']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon=data['banner'],
            color=data['banner_color'],
            season_level=data['level']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level=data['bp_tier']
        )
    )
    await ctx.send(f'Reset loadout to Config!')


@client.command()
async def Test(ctx, *, content = None):
    await client.party.me.set_outfit(asset='CID_636_Athena_Commando_M_GalileoGondola_78MFZ')
    await asyncio.sleep(0.2)
    await client.party.me.set_emote(asset='EID_Accolades')
    await ctx.send(f'I am Working :=)')


@client.command()
async def Tbd(ctx, *, content = None):
    await client.party.me.set_outfit(asset='CID_568_Athena_Commando_M_RebirthSoldier')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_636_Athena_Commando_M_GalileoGondola_78MFZ')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_637_Athena_Commando_M_GalileoOutrigger_7Q0YU')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_789_Athena_Commando_M_HenchmanGoodShorts_B')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_790_Athena_Commando_M_HenchmanGoodShorts_C')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_791_Athena_Commando_M_HenchmanGoodShorts_D')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_792_Athena_Commando_M_HenchmanBadShorts_B')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_793_Athena_Commando_M_HenchmanBadShorts_C')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_794_Athena_Commando_M_HenchmanBadShorts_D')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_F_CloakedAssassin')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_F_HenchmanSpyDark')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_F_HenchmanSpyGood')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_F_TowerSentinel')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_M_AlienRobot')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_M_Broccoli')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_M_CavernArmored')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_M_EmperorSuit')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_M_Fallback')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_M_HeistSummerIsland')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_M_PaddedArmorArctic')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_M_Scrapyard')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_M_SpaceWanderer')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_M_TacticalFishermanOil')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_HenchmanBadShorts')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_HenchmanGoodShorts')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_MadCommander')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_PaddedArmor')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_NPC_Athena_RebirthSoldier')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_TBD_Athena_Commando_F_BuffetCine')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_TBD_Athena_Commando_F_ConstructorTest')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_TBD_Athena_Commando_M_ConstructorTest')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_TBD_Athena_Commando_M_Nutcracker_CINE')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_TBD_Athena_Commando_M_Turtleneck_EVENT_NOTFORSTORE')
    await ctx.send(f'those were all tbd skins')



@client.command()
async def Og(ctx, *, content = None):
    await client.party.me.set_outfit(asset='CID_028_Athena_Commando_F')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_032_Athena_Commando_M_Medieval')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_033_Athena_Commando_F_Medieval')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_035_Athena_Commando_M_Medieval')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_052_Athena_Commando_F_PSBlue')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_080_Athena_Commando_M_Space')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_081_Athena_Commando_F_Space')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_082_Athena_Commando_M_Scavenger')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_083_Athena_Commando_F_Tactical')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_084_Athena_Commando_M_Assassin')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_039_Athena_Commando_F_Disco')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_017_Athena_Commando_M')
    await ctx.send(f'those were all Og skins')




@client.command()
async def exclusive(ctx, *, content = None):
    await client.party.me.set_outfit(asset='CID_175_Athena_Commando_M_Celestial')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_313_Athena_Commando_M_KpopFashion')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_085_Athena_Commando_M_Twitch')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_342_Athena_Commando_M_StreetRacerMetallic')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_434_Athena_Commando_F_StealthHonor')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_479_Athena_Commando_F_Davinci')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_261_Athena_Commando_M_RaptorArcticCamo')
    await asyncio.sleep(4.0)
    await client.party.me.set_outfit(asset='CID_783_Athena_Commando_M_AquaJacket')
    await ctx.send(f'those were all exclusive skins')



@client.command()

async def SpaceFN(ctx, *, content = None):
    if content is None:
        await ctx.send(f'Info: Bot Made By SpaceFN Team, Follow TheRealSxlar on tiktok!')
        await client.party.me.set_outfit(asset='CID_083_Athena_Commando_F_Tactical')
        await asyncio.sleep(1.0)
        await client.party.me.set_backpack(asset='BID_004_BlackKnight')
        await asyncio.sleep(1.0)
        await client.party.me.set_emote(asset='EID_Robot')
        await asyncio.sleep(5.0)
        await client.party.me.set_emote(asset='EID_Robot')

@client.command()

async def SpaceFNSetup(ctx, *, content = None):
    if content is None:
        await ctx.send(f'INFO: This Setup Matches With SpaceFN')
        await client.party.me.set_outfit(asset='CID_088_Athena_Commando_M_SpaceBlack')
        await asyncio.sleep(1.0)
        await client.party.me.set_backpack(asset='BID_004_BlackKnight')
        await asyncio.sleep(1.0)
        await client.party.me.set_emote(asset='EID_RocketRodeo')
        await asyncio.sleep(5.0)
        await client.party.me.set_emote(asset='EID_RocketRodeo')

@client.command()

async def Randomize(ctx, *, content = None):
    if content is None:
        await ctx.send(f'Randomized Skins')
        await client.party.me.set_outfit(asset='CID_042_Athena_Commando_M_Cyberpunk')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_043_Athena_Commando_F_Stealth')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_044_Athena_Commando_F_SciPop')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_045_Athena_Commando_M_HolidaySweater')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_046_Athena_Commando_F_HolidaySweater')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_047_Athena_Commando_F_HolidayReindeer')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_048_Athena_Commando_F_HolidayGingerbread')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_049_Athena_Commando_M_HolidayGingerbread')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_050_Athena_Commando_M_HolidayNutcracker')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_051_Athena_Commando_M_HolidayElf')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_052_Athena_Commando_F_PSBlue')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_053_Athena_Commando_M_SkiDude')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_054_Athena_Commando_M_SkiDude_USA')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_070_Athena_Commando_M_Cupid')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_071_Athena_Commando_M_Wukong')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_072_Athena_Commando_M_Scout')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_073_Athena_Commando_F_Scuba')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_074_Athena_Commando_F_Stripe')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_075_Athena_Commando_F_Stripe')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_076_Athena_Commando_F_Sup')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_077_Athena_Commando_M_Sup')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_080_Athena_Commando_M_Space')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_081_Athena_Commando_F_Space')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_082_Athena_Commando_M_Scavenger')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_083_Athena_Commando_F_Tactical')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_084_Athena_Commando_M_Assassin')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_085_Athena_Commando_M_Twitch')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_086_Athena_Commando_M_RedSilk')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_089_Athena_Commando_M_RetroGrey')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_096_Athena_Commando_F_Founder')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_097_Athena_Commando_F_RockerPunk')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_098_Athena_Commando_F_StPatty')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_099_Athena_Commando_F_Scathach')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_100_Athena_Commando_M_CuChulainn')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_101_Athena_Commando_M_Stealth')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_102_Athena_Commando_M_Raven')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_103_Athena_Commando_M_Bunny')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_104_Athena_Commando_F_Bunny')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_105_Athena_Commando_F_SpaceBlack')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_106_Athena_Commando_F_Taxi')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_107_Athena_Commando_F_PajamaParty')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_108_Athena_Commando_M_Fishhead')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_109_Athena_Commando_M_Pizza')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_043_Athena_Commando_F_Stealth')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_044_Athena_Commando_F_SciPop')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_045_Athena_Commando_M_HolidaySweater')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_046_Athena_Commando_F_HolidaySweater')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_047_Athena_Commando_F_HolidayReindeer')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_048_Athena_Commando_F_HolidayGingerbread')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_049_Athena_Commando_M_HolidayGingerbread')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_050_Athena_Commando_M_HolidayNutcracker')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_051_Athena_Commando_M_HolidayElf')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_052_Athena_Commando_F_PSBlue')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_053_Athena_Commando_M_SkiDude')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_054_Athena_Commando_M_SkiDude_USA')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_070_Athena_Commando_M_Cupid')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_071_Athena_Commando_M_Wukong')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_072_Athena_Commando_M_Scout')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_073_Athena_Commando_F_Scuba')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_074_Athena_Commando_F_Stripe')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_075_Athena_Commando_F_Stripe')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_076_Athena_Commando_F_Sup')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_077_Athena_Commando_M_Sup')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_080_Athena_Commando_M_Space')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_081_Athena_Commando_F_Space')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_082_Athena_Commando_M_Scavenger')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_083_Athena_Commando_F_Tactical')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_084_Athena_Commando_M_Assassin')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_085_Athena_Commando_M_Twitch')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_086_Athena_Commando_M_RedSilk')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_089_Athena_Commando_M_RetroGrey')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_096_Athena_Commando_F_Founder')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_097_Athena_Commando_F_RockerPunk')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_098_Athena_Commando_F_StPatty')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_099_Athena_Commando_F_Scathach')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_100_Athena_Commando_M_CuChulainn')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_101_Athena_Commando_M_Stealth')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_102_Athena_Commando_M_Raven')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_103_Athena_Commando_M_Bunny')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_104_Athena_Commando_F_Bunny')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_105_Athena_Commando_F_SpaceBlack')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_106_Athena_Commando_F_Taxi')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_107_Athena_Commando_F_PajamaParty')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_108_Athena_Commando_M_Fishhead')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_109_Athena_Commando_M_Pizza')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_043_Athena_Commando_F_Stealth')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_044_Athena_Commando_F_SciPop')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_045_Athena_Commando_M_HolidaySweater')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_046_Athena_Commando_F_HolidaySweater')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_047_Athena_Commando_F_HolidayReindeer')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_048_Athena_Commando_F_HolidayGingerbread')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_049_Athena_Commando_M_HolidayGingerbread')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_050_Athena_Commando_M_HolidayNutcracker')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_051_Athena_Commando_M_HolidayElf')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_052_Athena_Commando_F_PSBlue')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_053_Athena_Commando_M_SkiDude')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_054_Athena_Commando_M_SkiDude_USA')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_070_Athena_Commando_M_Cupid')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_071_Athena_Commando_M_Wukong')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_072_Athena_Commando_M_Scout')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_073_Athena_Commando_F_Scuba')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_074_Athena_Commando_F_Stripe')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_075_Athena_Commando_F_Stripe')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_076_Athena_Commando_F_Sup')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_077_Athena_Commando_M_Sup')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_080_Athena_Commando_M_Space')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_081_Athena_Commando_F_Space')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_082_Athena_Commando_M_Scavenger')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_083_Athena_Commando_F_Tactical')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_084_Athena_Commando_M_Assassin')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_085_Athena_Commando_M_Twitch')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_086_Athena_Commando_M_RedSilk')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_089_Athena_Commando_M_RetroGrey')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_096_Athena_Commando_F_Founder')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_097_Athena_Commando_F_RockerPunk')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_098_Athena_Commando_F_StPatty')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_099_Athena_Commando_F_Scathach')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_100_Athena_Commando_M_CuChulainn')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_101_Athena_Commando_M_Stealth')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_102_Athena_Commando_M_Raven')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_103_Athena_Commando_M_Bunny')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_104_Athena_Commando_F_Bunny')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_105_Athena_Commando_F_SpaceBlack')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_106_Athena_Commando_F_Taxi')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_107_Athena_Commando_F_PajamaParty')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_108_Athena_Commando_M_Fishhead')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_109_Athena_Commando_M_Pizza')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_043_Athena_Commando_F_Stealth')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_044_Athena_Commando_F_SciPop')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_045_Athena_Commando_M_HolidaySweater')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_046_Athena_Commando_F_HolidaySweater')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_047_Athena_Commando_F_HolidayReindeer')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_048_Athena_Commando_F_HolidayGingerbread')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_049_Athena_Commando_M_HolidayGingerbread')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_050_Athena_Commando_M_HolidayNutcracker')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_051_Athena_Commando_M_HolidayElf')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_052_Athena_Commando_F_PSBlue')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_053_Athena_Commando_M_SkiDude')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_054_Athena_Commando_M_SkiDude_USA')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_070_Athena_Commando_M_Cupid')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_071_Athena_Commando_M_Wukong')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_072_Athena_Commando_M_Scout')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_073_Athena_Commando_F_Scuba')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_074_Athena_Commando_F_Stripe')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_075_Athena_Commando_F_Stripe')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_076_Athena_Commando_F_Sup')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_077_Athena_Commando_M_Sup')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_080_Athena_Commando_M_Space')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_081_Athena_Commando_F_Space')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_082_Athena_Commando_M_Scavenger')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_083_Athena_Commando_F_Tactical')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_084_Athena_Commando_M_Assassin')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_085_Athena_Commando_M_Twitch')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_086_Athena_Commando_M_RedSilk')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_089_Athena_Commando_M_RetroGrey')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_096_Athena_Commando_F_Founder')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_097_Athena_Commando_F_RockerPunk')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_098_Athena_Commando_F_StPatty')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_099_Athena_Commando_F_Scathach')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_100_Athena_Commando_M_CuChulainn')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_101_Athena_Commando_M_Stealth')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_102_Athena_Commando_M_Raven')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_103_Athena_Commando_M_Bunny')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_104_Athena_Commando_F_Bunny')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_105_Athena_Commando_F_SpaceBlack')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_106_Athena_Commando_F_Taxi')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_107_Athena_Commando_F_PajamaParty')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_108_Athena_Commando_M_Fishhead')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_109_Athena_Commando_M_Pizza')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_043_Athena_Commando_F_Stealth')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_044_Athena_Commando_F_SciPop')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_045_Athena_Commando_M_HolidaySweater')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_046_Athena_Commando_F_HolidaySweater')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_047_Athena_Commando_F_HolidayReindeer')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_048_Athena_Commando_F_HolidayGingerbread')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_049_Athena_Commando_M_HolidayGingerbread')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_050_Athena_Commando_M_HolidayNutcracker')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_051_Athena_Commando_M_HolidayElf')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_052_Athena_Commando_F_PSBlue')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_053_Athena_Commando_M_SkiDude')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_054_Athena_Commando_M_SkiDude_USA')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_070_Athena_Commando_M_Cupid')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_071_Athena_Commando_M_Wukong')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_072_Athena_Commando_M_Scout')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_073_Athena_Commando_F_Scuba')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_074_Athena_Commando_F_Stripe')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_075_Athena_Commando_F_Stripe')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_076_Athena_Commando_F_Sup')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_077_Athena_Commando_M_Sup')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_080_Athena_Commando_M_Space')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_081_Athena_Commando_F_Space')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_082_Athena_Commando_M_Scavenger')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_083_Athena_Commando_F_Tactical')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_084_Athena_Commando_M_Assassin')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_085_Athena_Commando_M_Twitch')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_086_Athena_Commando_M_RedSilk')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_089_Athena_Commando_M_RetroGrey')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_096_Athena_Commando_F_Founder')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_097_Athena_Commando_F_RockerPunk')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_098_Athena_Commando_F_StPatty')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_099_Athena_Commando_F_Scathach')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_100_Athena_Commando_M_CuChulainn')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_101_Athena_Commando_M_Stealth')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_102_Athena_Commando_M_Raven')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_103_Athena_Commando_M_Bunny')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_104_Athena_Commando_F_Bunny')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_105_Athena_Commando_F_SpaceBlack')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_106_Athena_Commando_F_Taxi')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_107_Athena_Commando_F_PajamaParty')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_108_Athena_Commando_M_Fishhead')
        await asyncio.sleep(0.001)
        await client.party.me.set_outfit(asset='CID_109_Athena_Commando_M_Pizza')
        await ctx.send(f'Done!')



@client.command()

async def Spam(ctx, *, content = None):
    if content is None:
        await ctx.send(f'q')
        await asyncio.sleep(0.001)
        await ctx.send(f'w')
        await asyncio.sleep(0.001)
        await ctx.send(f'd')
        await asyncio.sleep(0.001)
        await ctx.send(f'r')
        await asyncio.sleep(0.001)
        await ctx.send(f't')
        await asyncio.sleep(0.001)
        await ctx.send(f'h')
        await asyncio.sleep(0.001)
        await ctx.send(f'z')
        await asyncio.sleep(0.001)
        await ctx.send(f'v')
        await asyncio.sleep(0.001)
        await ctx.send(f'p')
        await asyncio.sleep(0.001)
        await ctx.send(f'o')
        await asyncio.sleep(0.001)
        await ctx.send(f'y')
        await asyncio.sleep(0.001)
        await ctx.send(f'a')
        await asyncio.sleep(0.001)
        await ctx.send(f'1')
        await asyncio.sleep(0.001)
        await ctx.send(f'u')
        await asyncio.sleep(0.001)
        await ctx.send(f'n')
        await asyncio.sleep(0.001)
        await ctx.send(f'o')
        await asyncio.sleep(0.001)
        await ctx.send(f'p')
        await asyncio.sleep(0.001)
        await ctx.send(f'm')
        await asyncio.sleep(0.001)
        await ctx.send(f'u')
        await asyncio.sleep(0.001)
        await ctx.send(f'y')
        await asyncio.sleep(0.001)
        await ctx.send(f'c')
        await asyncio.sleep(0.001)
        await ctx.send(f'i')
        await asyncio.sleep(0.001)
        await ctx.send(f'o')
        await asyncio.sleep(0.001)
        await ctx.send(f'z')
        await asyncio.sleep(0.001)
        await ctx.send(f'c')
        await asyncio.sleep(0.001)
        await ctx.send(f'ü')
        await asyncio.sleep(0.001)
        await ctx.send(f'a')
        await asyncio.sleep(0.001)
        await ctx.send(f'u')
        await asyncio.sleep(0.001)
        await ctx.send(f'i')
        await asyncio.sleep(0.001)
        await ctx.send(f'g')
        await asyncio.sleep(0.001)
        await ctx.send(f'z')
        await asyncio.sleep(0.001)
        await ctx.send(f'x')
        await asyncio.sleep(0.001)
        await ctx.send(f'q')
        await asyncio.sleep(0.001)
        await ctx.send(f'h')
        await asyncio.sleep(0.001)
        await ctx.send(f'g')
        await asyncio.sleep(0.001)
        await ctx.send(f'h')
        await asyncio.sleep(0.001)
        await ctx.send(f'x')
        await asyncio.sleep(0.001)
        await ctx.send(f'c')
        await asyncio.sleep(0.001)
        await ctx.send(f'h')
        await asyncio.sleep(0.001)
        await ctx.send(f'o')
        await asyncio.sleep(0.001)
        await ctx.send(f'h')
        await asyncio.sleep(0.001)
        await ctx.send(f'a')
        await asyncio.sleep(0.001)
        await ctx.send(f'x')
        await asyncio.sleep(0.001)
        await ctx.send(f'j')
        await asyncio.sleep(0.001)
        await ctx.send(f'z')
        await asyncio.sleep(0.001)
        await ctx.send(f'p')
        await asyncio.sleep(0.001)
        await ctx.send(f'n')
        await asyncio.sleep(0.001)
        await ctx.send(f'p')
        await asyncio.sleep(0.001)
        await ctx.send(f'x')
        await asyncio.sleep(0.001)
        await ctx.send(f'a')
        await asyncio.sleep(0.001)
        await ctx.send(f'q')
        await asyncio.sleep(0.001)
        await ctx.send(f'e')
        await asyncio.sleep(0.001)
        await ctx.send(f'c')
        await asyncio.sleep(0.001)
        await ctx.send(f'o')
        await asyncio.sleep(0.001)
        await ctx.send(f'p')
        await asyncio.sleep(0.001)
        await ctx.send(f'f')
        await asyncio.sleep(0.001)
        await ctx.send(f'ü')
        await asyncio.sleep(0.001)
        await ctx.send(f'ä')
        await asyncio.sleep(0.001)
        await ctx.send(f'r')
        await asyncio.sleep(0.001)
        await ctx.send(f'h')
        await asyncio.sleep(0.001)
        await ctx.send(f's')





@client.command()

async def Hack(ctx, *, member = None):
    if member is None:
        member = [m for m in client.party.members if m.id == ctx.author.id][0]
        await ctx.send(f'Hacking Hacking Fortnite User {member.display_name}...')
        await asyncio.sleep(1.0)
        await ctx.send(f'please wait...')
        await asyncio.sleep(2.0)
        await ctx.send(f'Hacking ip...')
        await asyncio.sleep(3.0)
        await ctx.send(f'Success')
        await ctx.send(f'Hacking Fortnite account...')
        await asyncio.sleep(4.0)
        await ctx.send(f'Hacking E-mail....')
        await asyncio.sleep(3.0)
        await ctx.send(f'Success')
        await ctx.send(f'Hacking Passwort...')
        await asyncio.sleep(5.0)
        await ctx.send(f'Success')
        await ctx.send(f'ip addres: 99.193.184.146')
        await ctx.send(f'Fortnite E-mail {member.display_name}723@gmail.com ')
        await ctx.send(f'Fortnite Password: Fortnitelover2743')


@client.command()

async def SpecialCommand(ctx, *, content = None):
    if content is None:
        await ctx.send(f'{prefix}SpaceFN , {prefix}Randomize, {prefix}Spam, {prefix}Hack, {prefix}og, {prefix}Exclusive, {prefix}RE, {prefix}Toxic, {prefix}Rdw, {prefix}Johnnysins, {prefix}Info, {prefix}battlepassemotes ')



@client.command()

async def RE(ctx, *, content = None):
    if content is None:
        await client.party.me.set_emote(asset='EID_Accolades')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AcrobaticSuperhero')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Aerobics')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AfroHouse')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirGuitar')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirHorn')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alchemy_BZWS8')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alien')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AlienSupport')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AmazingForever_Q68W0')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AncientGladiator')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonBoardwalk')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonSaltLake')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinSalute')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinVest')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AutumnTea')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backflip')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backspin_R3NAI')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BadMood')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Balance')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletJumps')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletSpin')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Banana')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BangThePan')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BannerFlagWave')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Believer')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BestMates')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Bicycle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BicycleStyle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BigfootWalk')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AcrobaticSuperhero')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Aerobics')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AfroHouse')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirGuitar')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirHorn')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alchemy_BZWS8')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alien')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AlienSupport')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AmazingForever_Q68W0')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AncientGladiator')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonBoardwalk')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonSaltLake')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinSalute')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinVest')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AutumnTea')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backflip')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backspin_R3NAI')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BadMood')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Balance')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletJumps')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletSpin')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Banana')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BangThePan')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BannerFlagWave')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Believer')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BestMates')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Bicycle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BicycleStyle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BigfootWalk')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AcrobaticSuperhero')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Aerobics')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AfroHouse')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirGuitar')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirHorn')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alchemy_BZWS8')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alien')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AlienSupport')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AmazingForever_Q68W0')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AncientGladiator')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonBoardwalk')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonSaltLake')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinSalute')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinVest')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AutumnTea')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backflip')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backspin_R3NAI')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BadMood')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Balance')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletJumps')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletSpin')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Banana')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BangThePan')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BannerFlagWave')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Believer')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BestMates')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Bicycle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BicycleStyle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BigfootWalk')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AcrobaticSuperhero')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Aerobics')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AfroHouse')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirGuitar')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirHorn')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alchemy_BZWS8')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alien')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AlienSupport')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AmazingForever_Q68W0')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AncientGladiator')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonBoardwalk')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonSaltLake')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinSalute')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinVest')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AutumnTea')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backflip')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backspin_R3NAI')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BadMood')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Balance')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletJumps')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletSpin')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Banana')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BangThePan')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BannerFlagWave')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Believer')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BestMates')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Bicycle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BicycleStyle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BigfootWalk')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AcrobaticSuperhero')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Aerobics')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AfroHouse')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirGuitar')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirHorn')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alchemy_BZWS8')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alien')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AlienSupport')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AmazingForever_Q68W0')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AncientGladiator')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonBoardwalk')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonSaltLake')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinSalute')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinVest')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AutumnTea')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backflip')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backspin_R3NAI')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BadMood')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Balance')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletJumps')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletSpin')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Banana')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BangThePan')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BannerFlagWave')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Believer')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BestMates')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Bicycle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BicycleStyle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BigfootWalk')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AcrobaticSuperhero')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Aerobics')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AfroHouse')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirGuitar')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirHorn')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alchemy_BZWS8')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alien')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AlienSupport')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AmazingForever_Q68W0')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AncientGladiator')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonBoardwalk')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonSaltLake')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinSalute')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinVest')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AutumnTea')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backflip')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backspin_R3NAI')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BadMood')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Balance')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletJumps')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletSpin')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Banana')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BangThePan')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BannerFlagWave')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Believer')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BestMates')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Bicycle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BicycleStyle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BigfootWalk')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AcrobaticSuperhero')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Aerobics')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AfroHouse')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirGuitar')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AirHorn')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alchemy_BZWS8')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Alien')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AlienSupport')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AmazingForever_Q68W0')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AncientGladiator')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonBoardwalk')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AshtonSaltLake')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinSalute')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AssassinVest')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_AutumnTea')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backflip')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Backspin_R3NAI')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BadMood')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Balance')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletJumps')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BalletSpin')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Banana')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BangThePan')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BannerFlagWave')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Believer')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BestMates')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_Bicycle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BicycleStyle')
        await asyncio.sleep(0.01)
        await client.party.me.set_emote(asset='EID_BigfootWalk')
        await ctx.send(f'Done!')






@client.command()

async def Rdw(ctx, *, content = None):
    if content is None:
        await client.party.me.set_outfit(asset='CID_NPC_Athena_Commando_M_Kyle')
        await asyncio.sleep(1.0)
        await client.party.me.set_emote(asset='EID_Flex')





@client.command()

async def JohnnySins(ctx, *, content = None):
    if content is None:
        await client.party.me.set_outfit(asset='CID_989_Athena_Commando_M_ProgressiveJonesy_Event')




@client.command()

async def Info(ctx, *, content = None):
    if content is None:
        await ctx.send(f'Info')
        await ctx.send(f'Bot Made By SpaceFN Team.')
        await ctx.send(f'Bot File SpaceFNBOT Bot')
        await ctx.send(f'Cmd Titel SpaceFN Bot')
        await ctx.send(f'Tiktok: Therealsxlar')





@client.command()

async def BattleEmotes(ctx, *, content = None):
    if content is None:
        await ctx.send(f'All Battle pass emotes')
        await asyncio.sleep(5)
        await client.party.me.set_emote(asset='EID_Saucer')
        await asyncio.sleep(5)
        await client.party.me.set_emote(asset='EID_Believer')
        await asyncio.sleep(5)
        await client.party.me.set_emote(asset='EID_Ruckus')
        await asyncio.sleep(5)
        await client.party.me.set_emote(asset='EID_HighActivity')
        await asyncio.sleep(5)
        await client.party.me.set_emote(asset='EID_Terminal')
        await ctx.send(f'Done!')




@client.command()

async def Toxic(ctx, *, content = None):
    if content is None:
        await client.party.me.set_outfit(asset='CID_784_Athena_Commando_F_RenegadeRaiderFire')
        await asyncio.sleep(2.0)
        await client.party.me.set_emote(asset='EID_TakeTheElf')
        await asyncio.sleep(2.0)
        await ctx.send(f'HAHAHA Come Face Me Face TO Face IN FORTNITE BHE')

#More Commands soon ;)






@client.command()
async def admin(ctx, setting = None, *, user = None):
    if (setting is None) and (user is None):
        await ctx.send(f"Missing one or more arguments. Try: {prefix}admin (add, remove, list) (user)")
    elif (setting is not None) and (user is None):

        user = await client.fetch_profile(ctx.message.author.id)

        if setting.lower() == 'add':
            if user.id in info['FullAccess']:
                await ctx.send("You are already an admin")

            else:
                await ctx.send("Password?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if content == data['AdminPassword']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("Incorrect Password.")

        elif setting.lower() == 'remove':
            if user.id not in info['FullAccess']:
                await ctx.send("You are not an admin.")
            else:
                await ctx.send("Are you sure you want to remove yourself as an admin?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if (content.lower() == 'yes') or (content.lower() == 'y'):
                    info['FullAccess'].remove(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send("You were removed as an admin.")
                        print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                elif (content.lower() == 'no') or (content.lower() == 'n'):
                    await ctx.send("You were kept as admin.")
                else:
                    await ctx.send("Not a correct reponse. Cancelling command.")
                
        elif setting == 'list':
            if user.id in info['FullAccess']:
                admins = []

                for admin in info['FullAccess']:
                    user = await client.fetch_profile(admin)
                    admins.append(user.display_name)

                await ctx.send(f"The bot has {len(admins)} admins:")

                for admin in admins:
                    await ctx.send(admin)

            else:
                await ctx.send("You don't have permission to this command.")

        else:
            await ctx.send(f"That is not a valid setting. Try: {prefix}admin (add, remove, list) (user)")
            
    elif (setting is not None) and (user is not None):
        user = await client.fetch_profile(user)

        if setting.lower() == 'add':
            if ctx.message.author.id in info['FullAccess']:
                if user.id not in info['FullAccess']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("That user is already an admin.")
            else:
                await ctx.send("You don't have access to add other people as admins. Try just: !admin add")
        elif setting.lower() == 'remove':
            if ctx.message.author.id in info['FullAccess']:
                if user.id in info['FullAccess']:
                    await ctx.send("Password?")
                    response = await client.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if content == data['AdminPassword']:
                        info['FullAccess'].remove(user.id)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"{user.display_name} was removed as an admin.")
                            print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                    else:
                        await ctx.send("Incorrect Password.")
                else:
                    await ctx.send("That person is not an admin.")
            else:
                await ctx.send("You don't have permission to remove players as an admin.")
        else:
            await ctx.send(f"Not a valid setting. Try: {prefix}admin (add, remove) (user)")


if (data['email'] and data['password']) and (data['email'] != "" and data['password'] != ""):
    try:
        client.run()
    except fortnitepy.errors.AuthException as e:
        print(Fore.RED + ' [FEHLER] ' + Fore.RESET + f'{e}')
    except ModuleNotFoundError:
        print(e)
        print(Fore.RED + f'[FEHLER] ' + Fore.RESET + 'Bitte Starte "INSTALL PACKAGES.bat')
        exit()
else:
    print(Fore.RED + ' [FEHLER] ' + Fore.RESET + 'Du hast bei config.jason nicht deine fortnite acc daten eingegeben.')

#Placehold