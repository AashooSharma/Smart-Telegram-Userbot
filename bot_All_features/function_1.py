import datetime
import json

class ReminderManager:
    def __init__(self, reminders_file):
        self.reminders_file = reminders_file
        self.load_reminders()

    def load_reminders(self):
        try:
            with open(self.reminders_file, 'r') as f:
                self.reminders = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.reminders = []

    def save_reminders(self):
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f, indent=4)

    def add_reminder(self, user_id, task, date_time):
        reminder = {
            'user_id': user_id,
            'task': task,
            'date_time': date_time
        }
        self.reminders.append(reminder)
        self.save_reminders()

    def get_user_reminders(self, user_id):
        user_reminders = [reminder for reminder in self.reminders if reminder['user_id'] == user_id]
        return user_reminders

    def remove_reminder(self, user_id, index):
        user_reminders = self.get_user_reminders(user_id)
        if 0 <= index < len(user_reminders):
            del self.reminders[self.reminders.index(user_reminders[index])]
            self.save_reminders()

    def clear_expired_reminders(self):
        now = datetime.datetime.now()
        self.reminders = [reminder for reminder in self.reminders if datetime.datetime.strptime(reminder['date_time'], '%Y-%m-%d %H:%M:%S') > now]
        self.save_reminders()

# Initialize the ReminderManager
reminder_manager = ReminderManager('database/reminders.json')

