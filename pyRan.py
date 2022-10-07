import logging
import sqlite3
import time
from pprint import pprint
from datetime import timedelta
from telethon import errors
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.sync import TelegramClient, events
from telethon.tl.functions.channels import GetMessagesRequest
from dotenv import load_dotenv
import os


# Turn logging on (info level)
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

# Secrets
load_dotenv()
API_ID = os.get_env('API_ID')
API_HASH = os.get_env('API_HASH')
BOT_TOKEN = os.get_env('BOT_TOKEN')
OWNER = int(os.get_env('OWNER'))
ADMINS = [int(admin) for admin in os.get_env('ADMINS').split(' ')]

# Define client
bot = TelegramClient('client', API_ID, API_HASH).start(bot_token=BOT_TOKEN)




# Define an asynco check if user is admin
async def is_admin(peer_user, peer_channel):
    async for admin in bot.iter_participants(peer_channel, filter=ChannelParticipantsAdmins()):
        if admin.id == peer_user.user_id:
            return True
    return False


# Define check if bot alive
@bot.on(events.NewMessage(pattern='ping', func=lambda e: e.is_channel))
async def ping(e):
    await e.reply('**Pong!**')


# Define start command
@bot.on(events.NewMessage(pattern='/start'))
async def start(e):
    await e.reply('hi!')
    raise events.StopPropagation


# Define kick user option
@bot.on(events.NewMessage(pattern='kick', func=lambda e: e.is_channel))
async def kick(e):
    if await is_admin(e.from_id, e.peer_id):
        if e.message.reply_to:
            user = (await bot.get_messages(e.peer_id, ids=[e.reply_to.reply_to_msg_id]))[0].from_id.user_id
        elif len(e.text.split(' ')) == 2:
            user = int(e.text[5:]) if e.text[5:].isnumeric() else e.text[5:]
        try:
            await bot.edit_permissions(e.peer_id, user, view_messages=False)
            await bot.edit_permissions(e.peer_id, user)
            await e.reply('**✅ '+(f'[{user}](tg://user?id={user})' if user.isnumeric() else user)+' kicked!**')
        except errors.ChatAdminRequiredError:
            await e.reply('**Access Denied‼️\nAdmin me! 👮‍♂️**')
        except errors.UserAdminInvalidError:
            await e.reply('**Access Denied‼️\nHe/She is admin⁉️**')
        except ValueError as error:
            if 'Could not find the input entity for' in str(error):
                await e.reply('**ID is wrong‼️**')
            elif 'You cannot restrict yourself' == str(error):
                await e.reply('**I can\'t kick myself 😅**')
            elif 'You must pass a user entity' == str(error):
                await e.reply('**It\'s not a user‼️**')
            elif 'No user has "' in str(error):
                await e.reply('**Username is wrong‼️**')
            else:
                await e.reply(str(error))
    raise events.StopPropagation


# Define remove restrict user option
@bot.on(events.NewMessage(pattern='(unmute|unsilent)', func=lambda e: e.is_channel))
async def unmute(e):
    if await is_admin(e.from_id, e.peer_id):
        if e.message.reply_to:
            user = (await bot.get_messages(e.peer_id, ids=[e.reply_to.reply_to_msg_id]))[0].from_id.user_id
        elif len(e.text.split(' ')) == 2:
            user = int(e.text.split(' ')[1]) if e.text.split(' ')[1].isnumeric() else e.text.split(' ')[1]
        try:
            await bot.edit_permissions(e.peer_id, user)
            await e.reply('**✅ '+(f'[{user}](tg://user?id={user})' if user.isnumeric() else user)+' unmuted!**')
        except errors.ChatAdminRequiredError:
            await e.reply('**Access Denied‼️\nAdmin me! 👮‍♂️**')
        except errors.UserAdminInvalidError:
            await e.reply('**Access Denied‼️\nHe/She is admin⁉️**')
        except ValueError as error:
            if 'Could not find the input entity for' in str(error):
                await e.reply('**ID is wrong‼️**')
            elif 'You cannot restrict yourself' == str(error):
                await e.reply('**I can\'t unmute myself 😅**')
            elif 'You must pass a user entity' == str(error):
                await e.reply('**It\'s not a user‼️**')
            elif 'No user has "' in str(error):
                await e.reply('**Username is wrong‼️**')
            else:
                await e.reply(str(error))
    raise events.StopPropagation


# Define unban option
@bot.on(events.NewMessage(pattern='unban', func=lambda e: e.is_channel))
async def unban(e):
    if await is_admin(e.from_id, e.peer_id):
        if e.message.reply_to:
            user = (await bot.get_messages(e.peer_id, ids=[e.reply_to.reply_to_msg_id]))[0].from_id.user_id
        elif len(e.text.split(' ')) == 2:
            user = int(e.text[6:]) if e.text[6:].isnumeric() else e.text[6:]
        try:
            await bot.edit_permissions(e.peer_id, user)
            await e.reply('**✅ '+(f'[{user}](tg://user?id={user})' if user.isnumeric() else user)+' unbanned!**')
        except errors.ChatAdminRequiredError:
            await e.reply('**Access Denied‼️\nAdmin me! 👮‍♂️**')
        except errors.UserAdminInvalidError:
            await e.reply('**Access Denied‼️\nHe/She is admin⁉️**')
        except ValueError as error:
            if 'Could not find the input entity for' in str(error):
                await e.reply('**ID is wrong‼️**')
            elif 'You cannot restrict yourself' == str(error):
                await e.reply('**I can\'t unban myself 😅**')
            elif 'You must pass a user entity' == str(error):
                await e.reply('**It\'s not a user‼️**')
            elif 'No user has "' in str(error):
                await e.reply('**Username is wrong‼️**')
            else:
                await e.reply(str(error))
    raise events.StopPropagation


# Define ban user option
@bot.on(events.NewMessage(pattern='(ban|remove)', func=lambda e: e.is_channel))
async def ban(e):
    if await is_admin(e.from_id, e.peer_id):
        date = None
        if e.message.reply_to:
            user = (await bot.get_messages(e.peer_id, ids=[e.reply_to.reply_to_msg_id]))[0].from_id.user_id
            if len(e.text.split(' ')) == 2:
                if not e.text.split(' ')[1].isnumeric():
                    date = timedelta(hours=float(e.text.split(' ')[1]))
        elif len(e.text.split(' ')) > 1:
            user = int(e.text.split(' ')[1]) if e.text.split(' ')[1].isnumeric() else e.text.split(' ')[1]
            date = timedelta(hours=float(e.text.split(' ')[2])) if len(e.text.split(' ')) == 3 else None
        try:
            await bot.edit_permissions(e.peer_id, user, view_messages=False, until_date=date)
            await e.reply('**✅ '+(f'[{user}](tg://user?id={user})' if user.isnumeric() else user)+' '+\
                str(e.text.split(' ')[2]+' hours' if date else '')+' removed!**')
        except errors.ChatAdminRequiredError:
            await e.reply('**Access Denied‼️\nAdmin me! 👮‍♂️**')
        except errors.UserAdminInvalidError:
            await e.reply('**Access Denied‼️\nHe/She is admin⁉️**')
        except ValueError as error:
            if 'Could not find the input entity for' in str(error):
                await e.reply('**ID is wrong‼️**')
            elif 'You cannot restrict yourself' == str(error):
                await e.reply('**I can\'t remove myself 😅**')
            elif 'You must pass a user entity' == str(error):
                await e.reply('**It\'s not a user‼️**')
            elif 'No user has "' in str(error):
                await e.reply('**Username is wrong‼️**')
            else:
                await e.reply(str(error))
    raise events.StopPropagation


# Define restrict user option
@bot.on(events.NewMessage(pattern='(mute|silent)', func=lambda e: e.is_channel))
async def mute(e):
    if await is_admin(e.from_id, e.peer_id):
        date = None
        if e.message.reply_to:
            user = (await bot.get_messages(e.peer_id, ids=[e.reply_to.reply_to_msg_id]))[0].from_id.user_id
            if len(e.text.split(' ')) == 2:
                if not e.text.split(' ')[1].isnumeric():
                    date = timedelta(hours=float(e.text.split(' ')[1]))
        elif len(e.text.split(' ')) > 1:
            user = int(e.text.split(' ')[1]) if e.text.split(' ')[1].isnumeric() else e.text.split(' ')[1]
            date = timedelta(hours=float(e.text.split(' ')[2])) if len(e.text.split(' ')) == 3 else None
        try:
            await bot.edit_permissions(e.peer_id, user, send_messages=False, until_date=date)
            await e.reply('**✅ '+(f'[{user}](tg://user?id={user})' if user.isnumeric() else user)+' '+\
                str(e.text.split(' ')[2]+' hours' if date else '')+' muted!**')
        except errors.ChatAdminRequiredError:
            await e.reply('**Access Denied‼️\nAdmin me! 👮‍♂️**')
        except errors.UserAdminInvalidError:
            await e.reply('**Access Denied‼️\nHe/She is admin⁉️**')
        except ValueError as error:
            if 'Could not find the input entity for' in str(error):
                await e.reply('**ID is wrong‼️**')
            elif 'You cannot restrict yourself' == str(error):
                await e.reply('**I can\'t mute myself 😅**')
            elif 'You must pass a user entity' == str(error):
                await e.reply('**It\'s not a user‼️**')
            elif 'No user has "' in str(error):
                await e.reply('**Username is wrong‼️**')
            else:
                await e.reply(str(error))
    raise events.StopPropagation


# Define pin option
@bot.on(events.NewMessage(pattern='pin'))
async def pin(e):
    if await is_admin(e.from_id, e.peer_id):
        if e.message.reply_to:
            try:
                await bot.pin_message(e.peer_id, e.reply_to.reply_to_msg_id)
            except errors.ChatAdminRequiredError:
                await e.reply('**Access Denied‼️\nAdmin me! 👮‍♂️**')
    raise events.StopPropagation


# Define delete option
@bot.on(events.NewMessage(pattern='(del|delete)'))
async def test(e):
    if await is_admin(e.from_id, e.peer_id):
        if e.message.reply_to:
            try:
                await bot.delete_messages(e.peer_id, [e.reply_to.reply_to_msg_id])
            except errors.ChatAdminRequiredError:
                await e.reply('**Access Denied‼️\nAdmin me! 👮‍♂️**')
    raise events.StopPropagation


# Define an owner ultra access!
@bot.on(events.NewMessage(chats=OWNER))
async def me(e):
    if e.text[:4] == 'eval':
        try:
            await e.reply(str(eval(e.text.replace('eval ', ''))))
        except Exception as error:
            await e.reply('**Something wrong!\n\n**'+str(error))
    elif e.text[:4] == 'exec':
        try:
            exec(e.text.replace('exec ', ''))
            await e.reply('**Done!**')
        except Exception as error:
            await e.reply('**Something wrong!\n\n**'+str(error))
    raise events.StopPropagation


# Run the bot!
if __name__ == '__main__':
    bot.run_until_disconnected()
