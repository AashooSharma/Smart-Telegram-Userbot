import os
import json
import datetime
from telethon import events
from userbot_services import UserbotServices

class UserbotCommands:
    def __init__(self, client):
        self.client = client
        self.services = UserbotServices(client)

    async def start(self, event):
        await event.respond("Hello! I'm your Smart Telegram Userbot. How can I assist you today?")

    async def handle_command(self, event):
        user_input = event.raw_text.lower()

        if user_input.startswith("!remind"):
            await self.services.handle_reminder(event)
        elif user_input.startswith("!weather"):
            await self.services.handle_weather(event)
        elif user_input.startswith("!translate"):
            await self.services.handle_translation(event)
        elif user_input.startswith("!schedule_message"):
            await self.services.handle_scheduled_message(event)
        elif user_input.startswith("!news_alerts"):
            await self.services.handle_news_alerts(event)
        elif user_input.startswith("!note"):
            await self.services.handle_note(event)
        elif user_input.startswith("!add_auto_reply"):
            await self.services.handle_add_auto_reply(event)
        elif user_input.startswith("!remove_auto_reply"):
            await self.services.handle_remove_auto_reply(event)
        else:
            await event.respond("Command not recognized. Try using !start to get started.")

    # Add more functions for handling additional commands

# Create an instance of UserbotCommands
userbot_commands = UserbotCommands(client)

# Event handler for incoming messages
@client.on(events.NewMessage(pattern="^(?i)!.*"))
async def commands_handler(event):
    await userbot_commands.handle_command(event)

