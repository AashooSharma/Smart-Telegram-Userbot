# bot_All_features/function_1.py

import datetime
import json

class Function1:
    def __init__(self, client, db_path):
        self.client = client
        self.db_path = db_path

    async def handle_reminder(self, event):
        #args = event.pattern_match.group(1).split(" ", 1)
        args = event.raw_text.split(" ", 1)  # Split the entire text after the command trigger
        if len(args) == 1 and args[0].lower() == "help":
            await self.show_help(event)
        else:
            subcommand = args[0].lower()
            subcommand_args = args[1].split(" ", 1)

            subcommand_args_option= subcommand_args[0]
            if subcommand_args_option == "add":
                new_args= subcommand_args[1].split('"')
                subcommand_args = [item.strip() for item in new_args if item.strip()]
                await self.add_reminder(event, subcommand_args)
            elif subcommand_args_option == "show":
                new_args= subcommand_args[1].split('"')
                subcommand_args = [item.strip() for item in new_args if item.strip()]
                await self.show_reminders(event, subcommand_args)
            elif subcommand_args_option == "remove":
                new_args= subcommand_args[1].split('"')
                subcommand_args = [item.strip() for item in new_args if item.strip()]
                await self.remove_reminder(event, subcommand_args)
            elif subcommand_args_option == "edit":
                new_args= subcommand_args[1].split('"')
                subcommand_args = [item.strip() for item in new_args if item.strip()]
                await self.edit_reminder(event, subcommand_args)
            else:
                await event.reply(f"{subcommand_args}")
                await event.reply("Invalid subcommand. Use !remind help for usage details.")

    async def show_help(self, event):
        help_message = (
            "Usage examples:\n"
            "!remind add \"DD-mm-yyyy\" \"3:30 PM\" \"reminder title\" \"reminder message\"\n"
            "!remind show all\n"
            "!remind show \"reminder title\"\n"
            "!remind remove \"reminder title\"\n"
            "!remind edit \"reminder title\" \"DD-mm-yyyy\" \"3:30 PM\" \"updated reminder message\""
        )
        await event.reply(help_message)

    async def add_reminder(self, event, args):
        
        #await event.reply(f"{args[1]}")
        #new_args= args[1].split('"')
#        args = [item.strip() for item in new_args if item.strip()]
        #await event.reply(f"{args}")
        # Parse and validate input arguments
        try:
            date = datetime.datetime.strptime(args[0], "%d-%m-%Y")
            time = datetime.datetime.strptime(args[1], "%I:%M %p")
        except ValueError:
            await event.reply("Invalid date or time format. Use DD-mm-yyyy and h:mm AM/PM formats.")
            return

        reminder_title, reminder_message = "", ""
        if len(args) >= 3:
            reminder_title = args[2]
        if len(args) >= 4:
            reminder_message = args[3]

        # Calculate the timestamp and add the reminder to the database
        timestamp = (date + datetime.timedelta(hours=time.hour, minutes=time.minute)).timestamp()
        reminders = await self.load_reminders()
        reminders.append({"timestamp": timestamp, "title": reminder_title, "message": reminder_message})
        await self.save_reminders(reminders)

        await event.reply("Reminder added successfully!")

    async def show_reminders(self, event, args):
        reminders = await self.load_reminders()
        if not reminders:
            await event.reply("No reminders found.")
            return

        if args[0].lower() == "all":
            reminder_list = ""
            for idx, reminder in enumerate(reminders, start=1):
                timestamp = datetime.datetime.fromtimestamp(reminder["timestamp"]).strftime("%d-%m-%Y %I:%M %p")
                reminder_list += f"{idx}. {reminder['title']} - {timestamp}\n"

            await event.reply("Your reminders:\n" + reminder_list)
        else:
            await self.show_single_reminder(event, args[0])

    async def show_single_reminder(self, event, reminder_title):
        reminders = await self.load_reminders()
        matching_reminders = [reminder for reminder in reminders if reminder["title"].lower() == reminder_title.lower()]

        if not matching_reminders:
            await event.reply(f"No reminders found with title: {reminder_title}")
            return

        reminder_list = ""
        for idx, reminder in enumerate(matching_reminders, start=1):
            timestamp = datetime.datetime.fromtimestamp(reminder["timestamp"]).strftime("%d-%m-%Y %I:%M %p")
            reminder_list += f"{idx}. {timestamp} - {reminder['message']}\n"

        await event.reply(f"Reminders with title '{reminder_title}':\n" + reminder_list)

    async def remove_reminder(self, event, args):
        reminders = await self.load_reminders()
        if not reminders:
            await event.reply("No reminders found.")
            return

        reminder_title = args[0]
        matching_reminders = [reminder for reminder in reminders if reminder["title"].lower() == reminder_title.lower()]

        if not matching_reminders:
            await event.reply(f"No reminders found with title: {reminder_title}")
            return

        # Remove all matching reminders and save the updated list
        reminders = [reminder for reminder in reminders if reminder not in matching_reminders]
        await self.save_reminders(reminders)

        await event.reply(f"Removed {len(matching_reminders)} reminders with title '{reminder_title}'.")

    async def edit_reminder(self, event, args):
        reminders = await self.load_reminders()
        if not reminders:
            await event.reply("No reminders found.")
            return

        reminder_title = args[0]
        matching_reminders = [reminder for reminder in reminders if reminder["title"].lower() == reminder_title.lower()]

        if not matching_reminders:
            await event.reply(f"No reminders found with title: {reminder_title}")
            return

        new_date, new_time, new_message = "", "", ""
        if len(args) >= 2:
            new_date = args[1]
        if len(args) >= 3:
            new_time = args[2]
        if len(args) >= 4:
            new_message = args[3]

        # Update the matching reminders with new values and save the updated list
        for reminder in matching_reminders:
            if new_date:
                try:
                    date = datetime.datetime.strptime(new_date, "%d-%m-%Y")
                    reminder_date = datetime.datetime.fromtimestamp(reminder["timestamp"]).replace(hour=date.hour, minute=date.minute)
                    reminder["timestamp"] = reminder_date.timestamp()
                except ValueError:
                    pass
            if new_time:
                try:
                    time = datetime.datetime.strptime(new_time, "%I:%M %p")
                    reminder_time = datetime.datetime.fromtimestamp(reminder["timestamp"]).replace(hour=time.hour, minute=time.minute)
                    reminder["timestamp"] = reminder_time.timestamp()
                except ValueError:
                    pass
            if new_message:
                reminder["message"] = new_message

        await self.save_reminders(reminders)
        await event.reply(f"Updated {len(matching_reminders)} reminders with title '{reminder_title}'.")

    async def load_reminders(self):
        try:
            with open(self.db_path + "/reminders.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    async def save_reminders(self, reminders):
        with open(self.db_path + "/reminders.json", "w") as file:
            json.dump(reminders, file, indent=4)

