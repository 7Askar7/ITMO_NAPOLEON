# ITMO_NAPOLEON


## Запуск

Нуобоходимо запустить сервер сообщений, а также tg бота в соответствующйе последовательности

### Backend

```
cd agent-sales
source .venv/bin/activate
bash start.sh

cd ../agent_module

python db/api_chormadb.py
python db/agent_module.py
```

### TG Bot

```
cd tg_bot
```

```
mv exampleconfig.json config.json
```

Затем необходимо указать `api_hash`, `api_id` пользователя, от имени которого будут отправляться сообщения
А также токен бота

```
python bot.py
```


