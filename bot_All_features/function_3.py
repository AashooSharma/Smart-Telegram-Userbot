import requests

class Function3:
    async def handle_translation(self, event):
        args = event.pattern_match.group(1).split(" ", 1)
        if event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
            text = reply_message.text
        else:
            text = args[0]
        
        if len(args) >= 2:
            source_lang, target_lang = args[0].lower(), args[1].lower()
            translated_text = await self.translate_text(text, source_lang, target_lang)
            await event.reply(translated_text)
        else:
            await event.reply("Invalid usage. Use !translate <source_lang> <target_lang> <text>")

    async def translate_text(self, text, source_lang, target_lang):
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": source_lang,
            "tl": target_lang,
            "dt": "t",
            "q": text,
        }
        response = requests.get(url, params=params)
        translated_text = response.json()[0][0][0]
        return translated_text

# Create an instance of Function3 class
function_3 = Function3()
