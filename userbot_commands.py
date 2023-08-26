import os
import logging

import json
import datetime
from telethon import events
from userbot_services import UserbotServices

class UserbotCommands:
    def __init__(self, client):
        self.client = client
        self.services = UserbotServices(client)
        self.logger = logging.getLogger(__name__)

    async def handle_start(self, event):
        self.logger.info("Received !start command")
        await event.respond("Hello! I'm your Smart Telegram Userbot. How can I assist you today?")
        
        return

    async def handle_help(self, event):
        self.logger.info("Received !help command")
        user_input = event.raw_text.lower().split(" ", 1)
        if len(user_input) > 1:
            command_name = user_input[1]
            await self.show_command_help(event, command_name)
        else:
            await self.show_general_help(event)

    async def show_general_help(self, event):
        help_text = (
            "This is your Smart Telegram Userbot.\n"
            "Here are some available commands:\n\n"
            "!start - Start the userbot\n"
            "!help - Show this help message\n"
            "!remind - Set a reminder\n"
            "!weather - Get weather updates\n"
            "!translate - Translate text\n"
            "!schedule_message - Schedule a message\n"
            "!news_alerts - Get news alerts\n"
            "!note - Store and retrieve notes\n"
            "!auto_reply - Set up automated replies\n"
        )
        await event.respond(help_text)

    async def show_command_help(self, event, command_name):
        if command_name == "remind":
            help_text = (
                "Usage: !remind add \"DD-mm-yyyy\" \"3:30 PM\" \"reminder title\" \"reminder message\"\n"
                "       !remind show all\n"
                "       !remind show \"reminder title\"\n"
                "       !remind remove \"reminder title\"\n"
                "       !remind edit \"DD-mm-yyyy\" \"3:30 PM\" \"reminder title\" \"reminder message\"\n"
                "Example: !remind add \"20-08-2023\" \"3:30 PM\" \"Meeting\" \"Discuss project\"\n"
            )
            await event.respond(help_text)
        elif command_name == "weather":
            pass
            # Provide help text for the weather command
        elif command_name == "translate":
            pass
            # Provide help text for the translate command
        # Add more cases for other commands
    
    async def handle_commands(self, event):
        self.logger.info("Received command: %s", event.raw_text)
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
            pass
            #await event.respond("Command not recognized. Try using !start to get started.")

    # Add more functions for handling additional commands

# Create an instance of UserbotCommands
#userbot_commands = UserbotCommands(client)

# Event handler for incoming messages
#@client.on(events.NewMessage(pattern="^(?i)!.*"))
#async def commands_handler(event):
#    await userbot_commands.handle_command(event)

