from telethon import TelegramClient, events, sync
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

def load_config(config_file):
	try:
		with open(config_file, 'r') as file:
			config_data = json.load(file)
			return config_data
	except FileNotFoundError:
		print(f'Error: File {config_file} not found.')
		return None
	except json.JSONDecodeError:
		print(f'Error: File {config_file} is not a valid JSON.')
		return None

config = load_config("config.json")

bot = TelegramClient('bot_session_2', config["api_id"], config["api_hash"]).start(bot_token=config["bot_token"])
client = TelegramClient('user_session_2', config["api_id"], config["api_hash"])

bot_settings = {
	"messages": [],
	"model": "openai/gpt-4o-mini",
}


def do_send_post_request(data, url, headers={'Content-Type': 'application/json; charset=UTF-8'}):
	try:
		print(data)

		response = requests.post(config["url"] + url, json=data, headers=headers, stream=True)

		rsp = response.content.decode('utf8').split("\n\n")

		response = ""

		for chunk in rsp:
			js = {}
			try:
				js = json.loads(chunk[6:])
			except Exception:
				continue
			if "choices" not in js:
				continue
			for msg in js["choices"]:
				if "delta" not in msg:
					continue
				response += msg["delta"]["content"]

		print(response)

		bot_settings["messages"].append({
			"role": "assistant",
			"content": response,
		})

		return response

	except requests.exceptions.RequestException as e:
		print('Error during the request:', str(e))

def send_post_request(message):
	token = config["token"]
	headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Origin": config["url"],
        "Connection": "keep-alive",
        "Cookie": f"token={token}",
        "Priority": "u=0",
	}

	print("messages")
	print(bot_settings["messages"])

	bot_settings["messages"].append({
		"role": "user",
		"content": message,
	})

	data = {
        "stream": True,
        "model": bot_settings["model"],
        "messages": bot_settings["messages"],
        "session_id": config["session_id"],
        "chat_id": config["chat_id"],
        "user_id": config["user_id"],
    }

	return do_send_post_request(data, "/api/chat/completions", headers)

async def start_client():
    # Логин клиента пользователя
    await client.start(config["phone"])
    print("Client logged in")


# Обработчик команды /set_settings
@bot.on(events.NewMessage(pattern='/set_settings'))
async def set_settings(event):
    try:
        # Пример команды: /set_settings {"message": "Your predefined message"}
        settings_str = event.message.text.split(' ', 1)[1]
        bot_settings.update(json.loads(settings_str))
        await event.respond('Settings updated: {}'.format(settings_str))
    except (json.JSONDecodeError, IndexError) as e:
        await event.respond('Invalid settings. Use /set_settings {"key": "value"}')

@bot.on(events.NewMessage(pattern='/set_model'))
async def set_settings(event):
    try:
        settings_str = event.message.text.split(' ', 1)[1]
        bot_settings["model"] = settings_str
        await event.respond('Model updated: {}'.format(settings_str))
    except (json.JSONDecodeError, IndexError) as e:
        await event.respond('Invalid settings. Use /set_settings {"key": "value"}')


# Обработчик команды /send_message
@bot.on(events.NewMessage(pattern='/send_message'))
async def send_message(event):
    try:
        # Пример команды: /send_message username_of_the_user
        command, username, message = event.message.text.split(' ', 3)
        # resp = do_send_post_request({"chat": {}}, "/api/v1/chats/new")
        # print("new chat request")
        # print(resp)
        # bot_settings["chat"] = resp

        user = await bot.get_entity(username)
        await client.send_message(user, message)
        await event.respond('Message sent to {}: {}'.format(username, message))
    except Exception as e:
        await event.respond('Failed to send message. Error: {}'.format(str(e)))

# Обработчик входящих сообщений от конкретных пользователей
@client.on(events.NewMessage())
async def message_handler(event):
    # Проверка, что сообщение не от самого бота
    if event.is_private and not event.message.out:
        sender = await event.get_sender()
        username = sender.username

        response = send_post_request(event.message.text)
        await event.respond(str(response))

# Запуск бота и клиента
with bot:
    bot.loop.run_until_complete(start_client())
    bot.run_until_disconnected()