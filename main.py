import logging

import asyncio
from telethon.sync import TelegramClient, events
from dotenv import load_dotenv
import os
from userbot_commands import UserbotCommands
from userbot_services import UserbotServices

load_dotenv()

# Initialize the Telethon client
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_name = "userbot_session"  # You can change this as needed

client = TelegramClient(session_name, api_id, api_hash)

# Initialize UserbotCommands and UserbotServices instances
commands_handler = UserbotCommands(client)
services_handler = UserbotServices(client)

# Handle incoming messages
@client.on(events.NewMessage(pattern="^!start"))
async def start_command(event):
    await commands_handler.handle_start(event)
    return

@client.on(events.NewMessage(pattern="^!help"))
async def help_command(event):
    await commands_handler.handle_help(event)
    return

# Handle other commands and services
@client.on(events.NewMessage(pattern="^![a-zA-Z]+"))
async def handle_commands(event):
    await commands_handler.handle_commands(event)
    return

#@client.on(events.NewMessage())
#async def handle_services(event):
#    await services_handler.handle_services(event)

# Run the client
async def main():
    await client.start()
    print("bot is running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

